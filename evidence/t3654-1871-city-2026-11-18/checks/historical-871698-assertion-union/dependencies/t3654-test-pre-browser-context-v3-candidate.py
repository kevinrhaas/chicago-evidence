#!/usr/bin/env python3
"""Synthetic refusal tests using copies/read-only inputs; no check or CI verdict is created."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('coverage_auditor', '/tmp/t3654-pre-browser-source-coverage-context-v3-candidate.py')
v = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(v)
BINDING = Path('/tmp/t3654-pre-browser-bindings-871698.json')


class CoverageProofTests(unittest.TestCase):
    def setUp(self):
        v.configure(BINDING)
        self.tmp = tempfile.TemporaryDirectory(prefix='t3654-source-proof-refusal-')
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.rows = v.declarations((v.APP / 'tools/check.sh').read_text())
        self.harness = dict(v.BINDINGS['harness_sha256'])
        self.local_path = Path('/tmp/t3654-source-fallback-14of16-attempt1.receipt.json')
        self.local = v.read_json(self.local_path)
        self.host_path = Path('/tmp/t3654-support-44407494538-part4-complete-meta.json')
        self.index = {x['job_id']: x for x in v.read_json(v.BINDINGS['hosted_evidence_index']['path'])['parts']}

    def write(self, name, value):
        p = self.dir / name
        p.write_text(json.dumps(value) if isinstance(value, (dict, list)) else value)
        return p

    def git(self, *args):
        responses = {
            ('rev-parse','HEAD'):v.HEAD, ('rev-parse','HEAD^{tree}'):v.TREE,
            ('status','--porcelain'):'', ('rev-parse','origin/dev'):v.BASE,
            ('merge-base','origin/dev','HEAD'):v.BASE,
            ('rev-parse',f'{v.CI_COMMIT}^{{tree}}'):v.TREE,
            ('show','-s','--format=%P',v.CI_COMMIT):f'{v.BASE} {v.HEAD}',
            ('ls-remote','origin',f'refs/heads/{v.BRANCH}','refs/heads/dev'):
                f'{v.HEAD}\trefs/heads/{v.BRANCH}\n{v.BASE}\trefs/heads/dev'}
        return responses[args]

    def audit(self, git=None):
        with patch.object(v, 'git', git or self.git):
            return v.audit()

    def reject_local(self, d):
        with self.assertRaises(v.Refusal):
            v.verify_local(self.write('receipt.json',d),self.rows,self.harness)

    def test_actual_native_local_positive(self):
        item, why = v.verify_local(self.local_path,self.rows,self.harness)
        self.assertIsNone(why); self.assertEqual(item['ordinals'],self.local['selected_ordinals'])

    def test_actual_qualified_kernel_exit_positive(self):
        p = Path('/tmp/t3654-source-fallback-6of16-attempt2.receipt.json')
        item, why = v.verify_local(p,self.rows,self.harness)
        self.assertIsNone(why); self.assertEqual(item['exit_proof']['kind'],'kernel_exit_0_with_original_transcript_identity')

    def test_old_head_has_zero_credit(self):
        d=copy.deepcopy(self.local);d['start_snapshot']['head']='a'*40
        item, why=v.verify_local(self.write('old.json',d),self.rows,self.harness)
        self.assertIsNone(item);self.assertEqual(why,'other_head')

    def test_changed_end_head_and_tree_and_dirty_source_refused(self):
        for key,value in [('head','a'*40),('tree','b'*40),('status_porcelain',' M changed')]:
            with self.subTest(key=key):
                d=copy.deepcopy(self.local);d['end_snapshot'][key]=value;self.reject_local(d)

    def test_changed_harness_and_declaration_refused(self):
        d=copy.deepcopy(self.local);d['end_snapshot']['harness_sha256']['tools/check_harness.sh']='0'*64;self.reject_local(d)
        d=copy.deepcopy(self.local);d['declaration_snapshot']='0'*64;self.reject_local(d)

    def test_in_progress_and_timeout_have_zero_credit(self):
        for status in ['running','timeout','pass_from_terminal_log']:
            d=copy.deepcopy(self.local);d['status']=status;d['exit_code']=124
            item,why=v.verify_local(self.write('incomplete.json',d),self.rows,self.harness)
            self.assertIsNone(item);self.assertEqual(why,'no_complete_successful_process')

    def test_current_assertion_failure_refused(self):
        d=copy.deepcopy(self.local);d['status']='fail';d['exit_code']=1;self.reject_local(d)

    def test_altered_log_and_process_hash_refused(self):
        d=copy.deepcopy(self.local);d['log_sha256']='0'*64;self.reject_local(d)
        d=copy.deepcopy(self.local);d['process_receipt_sha256']='0'*64;self.reject_local(d)

    def test_forged_exit_zero_claim_cannot_override_actual_exit(self):
        d=copy.deepcopy(self.local);p=v.read_json(d['process_receipt']);p['exit_code']=124
        pp=self.write('process.json',p);d.update(process_receipt=str(pp),process_receipt_sha256=v.digest(pp));self.reject_local(d)

    def test_real_old_attempt_exit_cannot_prove_current_attempt(self):
        d=v.read_json('/tmp/t3654-source-fallback-8of16-attempt2.receipt.json')
        old='/tmp/t3654-source-fallback-8of16-attempt1.process.json'
        d['process_receipt']=old;d['process_receipt_sha256']=v.digest(old)
        self.assertEqual(v.read_json(old)['part'],d['part'])
        self.assertEqual(v.read_json(old)['exit_code'],0)
        self.reject_local(d)

    def test_process_timing_must_match_the_bound_attempt_receipt(self):
        for key,value in [('end_epoch_s',self.local['end_epoch_s']+1),
                          ('duration_s',self.local['duration_s']+1),
                          ('start_epoch_s',self.local['end_epoch_s'])]:
            d=copy.deepcopy(self.local);d[key]=value
            with self.subTest(key=key):self.reject_local(d)

    def test_missing_exit_provenance_refused(self):
        d=copy.deepcopy(self.local);d.pop('process_receipt');self.reject_local(d)

    def test_claimed_ordinal_mutation_refused(self):
        d=copy.deepcopy(self.local);d['selected_ordinals']=d['selected_ordinals'][:-1];self.reject_local(d)

    def test_terminal_pass_and_headings_and_selftest_counts_refused(self):
        text=v.plain_log(self.local['log'])
        mutations=[text.replace('CHECK PASS — part 14/16: 89','CHECK PASS — part 14/16: 88'),
                   text+'\nCHECK FAIL — forced assertion failure\n',
                   text.replace('== '+v.selected(self.rows,'14/16')[0]['label'],'== missing heading',1),
                   text.replace('  27 of them are self-tests','  26 of them are self-tests'),
                   text+'\nCHECK PASS — part 14/16: 89 steps, none red.\n']
        for i,mutated in enumerate(mutations):
            with self.subTest(mutation=i),self.assertRaises(v.Refusal):v.verify_transcript(mutated,'14/16',self.rows)

    def test_actual_hosted_success_positive(self):
        item=v.verify_hosted(self.host_path,self.rows,self.index)
        self.assertEqual(len(item['ordinals']),175);self.assertTrue(item['pr_only_changelog_pass'])

    def test_hosted_wrong_head_and_failed_pr_only_step_refused(self):
        for mutation in ['head','prcheck','status']:
            d=v.read_json(self.host_path)
            if mutation=='head':d['headSha']='a'*40
            else:
                job=next(x for x in d['jobs'] if x['name']=='gate part 4/8')
                if mutation=='status':job['conclusion']='failure'
                else:next(x for x in job['steps'] if x['name']=='Does this change carry a changelog entry?')['conclusion']='failure'
            p=self.write(self.host_path.name,d)
            with self.subTest(mutation=mutation),self.assertRaises(v.Refusal):v.verify_hosted(p,self.rows,self.index)

    def test_hosted_changed_log_binding_and_checkout_refused(self):
        idx=copy.deepcopy(self.index);idx[135167297533]['log_sha256']='0'*64
        with self.assertRaises(v.Refusal):v.verify_hosted(self.host_path,self.rows,idx)
        with self.assertRaises(v.Refusal):v.verify_checkout('[command]/usr/bin/git log -1 --format=%H\n'+'a'*40)

    def test_sandbox_warning_success_cannot_credit_required_source_context(self):
        cases=[('/tmp/t3654-source-fallback-6of16-attempt2.log','6/16',"   ok    every raster reader the gate's steps need is installed: PIL (Pillow), numpy (numpy), scipy (scipy)"),
               ('/tmp/t3654-support-44407494538-job135167297814.log','5/8','   ok    base origin/dev at '+v.BASE[:9]),
               ('/tmp/t3654-source-fallback-13of16-attempt1.log','13/16','held to origin/dev at '+v.BASE[:9])]
        for log,part,success in cases:
            text=v.plain_log(log)
            self.assertIn(success,text)
            with self.subTest(part=part,success=success),self.assertRaises(v.Refusal):
                v.verify_transcript(text.replace(success,'WARN sandbox skipped the required work'),part,self.rows)

    def test_timeout_after_native_assertion_failure_is_not_excludable(self):
        exception=v.BINDINGS['excluded_hosted_timeouts'][0]
        text=v.plain_log(exception['log']['path'])+'\n   ^ a native assertion failed\n'
        with patch.object(v,'plain_log',return_value=text),self.assertRaises(v.Refusal):
            v.verify_timeout_exclusion(exception)
        text=v.plain_log(self.local['log'])+'\n   ^ a native assertion failed\n'
        with self.assertRaises(v.Refusal):v.verify_transcript(text,'14/16',self.rows)

    def test_known_timeout_has_no_credit(self):
        timeout=v.verify_timeout_exclusion(v.BINDINGS['excluded_hosted_timeouts'][0]);self.assertIs(timeout['coverage_credit'],False)
        self.assertNotIn('ordinals',timeout)

    def test_altered_bound_receipt_and_kernel_bundle_refused(self):
        d=copy.deepcopy(v.BINDINGS);d['accepted_local_receipts'][0]['sha256']='0'*64
        with patch.object(v,'BINDINGS',d),self.assertRaises(v.Refusal):self.audit()
        d=copy.deepcopy(v.BINDINGS);d['qualified_local_exits'][0]['bundle']['sha256']='0'*64
        with patch.object(v,'BINDINGS',d),self.assertRaises(v.Refusal):v.verify_local(Path('/tmp/t3654-source-fallback-6of16-attempt2.receipt.json'),self.rows,self.harness)

    def test_kernel_wait_status_and_pid_are_independently_decoded(self):
        original_read=v.read_json
        receipt_path=Path('/tmp/t3654-source-fallback-6of16-attempt2.receipt.json')
        for mutation in ['wait_status','pid','stdout_inode']:
            def altered(path):
                data=original_read(path)
                if str(path).endswith('-kernel-exit.json'):
                    if mutation=='wait_status':
                        prefix,tail=data['raw_proc_stat'].split(') ',1);fields=tail.split();fields[49]='256';data['raw_proc_stat']=prefix+') '+' '.join(fields)
                    if mutation=='pid':data['process_pid']+=1
                if str(path).endswith('-wrapper-repair.json') and mutation=='stdout_inode':data['original_inode']+=1
                return data
            with self.subTest(mutation=mutation),patch.object(v,'read_json',altered),self.assertRaises(v.Refusal):
                v.verify_local(receipt_path,self.rows,self.harness)

    def test_hosted_required_environment_and_exact_pr_command_refused(self):
        log=v.plain_log('/tmp/t3654-support-44407494538-job135167297533.log')
        for needle in ['C4D_GATE_REQUIRE_READERS: 1','C4D_GATE_REQUIRE_BASE: 1',f'node chicago/4d/tools/check-changelog-entry.mjs "{v.BASE}" "{v.HEAD}"']:
            with self.subTest(needle=needle),patch.object(v,'plain_log',return_value=log.replace(needle,'REMOVED')),self.assertRaises(v.Refusal):
                v.verify_hosted(self.host_path,self.rows,self.index)

    def test_exhaustive_union_and_overlaps_credited_once(self):
        result=self.audit()
        self.assertEqual(result['covered_ordinals'],list(range(1,1380)))
        self.assertEqual(result['missing_ordinals'],[])
        self.assertEqual(result['ordinary_covered'],1376)
        self.assertTrue(result['overlap_ordinals'])
        self.assertTrue(result['ready_for_browser_queue']) # Synthetic matching live refs only.
        self.assertFalse(result['merge_authorized_by_this_proof'])
        self.assertTrue(result['hosted_gate_required_before_merge'])

    def test_missing_timeout_partition_cannot_be_inferred_from_other_parts(self):
        d=copy.deepcopy(v.BINDINGS);d['accepted_local_receipts']=[x for x in d['accepted_local_receipts'] if not any(f'-{k}of16-' in x['path'] for k in [6,14])]
        with patch.object(v,'BINDINGS',d):result=self.audit()
        expected={r['ordinal'] for r in v.selected(self.rows,'6/8') if not r['every_part']}
        self.assertEqual(set(result['missing_ordinals']),expected)
        self.assertFalse(result['source_check_coverage_complete']);self.assertFalse(result['ready_for_browser_queue'])

    def test_new_head_binding_has_no_implicit_old_head_credit(self):
        d=copy.deepcopy(v.BINDINGS);d.update(source_commit='a'*40,accepted_local_receipts=[],accepted_hosted_metadata=[],qualified_local_exits=[],excluded_hosted_timeouts=[])
        index={'source_commit':'a'*40,'included_dev_base':v.BASE,'repository':v.REPO,'pull_request':v.PR,'run_id':v.RUN,'parts':[]}
        ip=self.write('empty-index.json',index);d['hosted_evidence_index']=v.bound(ip)
        bp=self.write('new-bindings.json',d);v.configure(bp)
        result=self.audit();self.assertEqual(result['covered_ordinals'],[]);self.assertEqual(len(result['missing_ordinals']),1379)
        self.assertFalse(result['ready_for_browser_queue'])

    def test_live_head_or_base_mismatch_blocks_complete_evidence(self):
        for target,blocker in [('dev','live_dev_base_changed'),(v.BRANCH,'live_branch_head_changed')]:
            def changed(*args):
                value=self.git(*args)
                if args[0]=='ls-remote':
                    lines=value.splitlines();value='\n'.join(('a'*40+'\t'+x.split('\t')[1]) if x.endswith('/'+target) else x for x in lines)
                return value
            result=self.audit(changed)
            self.assertTrue(result['source_check_coverage_complete']);self.assertFalse(result['ready_for_browser_queue'])
            self.assertIn(blocker,result['live_identity_blockers'])

    def test_unknown_hosted_failure_and_cancel_refused(self):
        for conclusion in ['failure','cancelled']:
            d=copy.deepcopy(v.BINDINGS);idx=v.read_json(d['hosted_evidence_index']['path']);idx['parts'].append({'job_id':999999,'status':'completed','conclusion':conclusion})
            ip=self.write('bad-index.json',idx);d['hosted_evidence_index']=v.bound(ip)
            with patch.object(v,'BINDINGS',d),self.subTest(conclusion=conclusion),self.assertRaises(v.Refusal):self.audit()

    def test_changed_source_before_or_during_audit_refused(self):
        for after in [False,True]:
            count=0
            def changed(*args):
                nonlocal count
                if args==('rev-parse','HEAD'):
                    count+=1
                    if not after or count==2:return 'a'*40
                return self.git(*args)
            with self.subTest(after=after),self.assertRaises(v.Refusal):self.audit(changed)

    def test_refusal_overwrites_stale_ready_output_and_returns_two(self):
        out=self.write('output.json',{'ready_for_browser_queue':True})
        d=copy.deepcopy(v.BINDINGS);d['output']=str(out);d['artifact_directory']=str(self.dir)
        bp=self.write('bindings.json',d)
        with patch('sys.argv',['auditor','--bindings',str(bp),'--require-complete']),patch.object(v,'audit',side_effect=v.Refusal('test mutation')),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(v.main(),2)
        self.assertFalse(v.read_json(out)['ready_for_browser_queue'])


if __name__=='__main__':
    unittest.main(verbosity=2)
