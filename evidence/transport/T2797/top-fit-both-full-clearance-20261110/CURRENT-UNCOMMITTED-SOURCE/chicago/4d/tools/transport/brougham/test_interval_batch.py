# SPDX-License-Identifier: GPL-3.0-or-later
"""Caller/DFS/numerical controls only; not an actual carriage interval proof."""
import ast
import hashlib
import json
import math
from pathlib import Path
import struct
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

import check_door_aperture as checker
import interval_batch as helper


def state_hash(states):
    digest = hashlib.sha256()
    for start, end, depth in states:
        digest.update(struct.pack('<ddi', start, end, depth))
    return digest.hexdigest()


def traced_original():
    source = Path(checker.__file__).read_text()
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'interval_clear')
    original = ast.dump(node, include_attributes=False)
    probe = ast.parse('visit(start, end, depth)').body[0]
    node.body.insert(0, probe)
    assert ast.dump(ast.FunctionDef(name=node.name, args=node.args, body=node.body[1:],
        decorator_list=node.decorator_list, returns=node.returns, type_comment=node.type_comment), include_attributes=False) == original
    states = []
    namespace = {'math':math, 'np':np, 'turn':checker.turn, 'separation':checker.separation,
                 'visit':lambda start,end,depth:states.append((start,end,depth))}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])), '<original interval with trace only>', 'exec'), namespace)
    return namespace, states


def expected_pairs(triangle, fixed, candidates, start, end, depth, tolerance):
    reference, states = traced_original()
    results, traces = [], []
    for k in candidates:
        states.clear()
        results.append((int(k), *reference['interval_clear'](triangle, fixed[k], start, end, depth, tolerance)))
        traces.append(state_hash(states))
    return results, traces


def verify():
    a = np.array([[1.,0.,0.],[0.,0.,1.],[0.,0.,0.]])
    count = 259
    fixed = np.tile(a + [0,5,0], (count,1,1))
    contact_ids = [0,5,128,130,258]
    fixed[contact_ids] = a
    candidates = np.roll(np.arange(count,dtype=np.intp),7)
    frozen = (a.tobytes(),fixed.tobytes(),candidates.tobytes())
    start,end,depth,tolerance = 0.,-math.radians(65),12,1e-8
    expected,traces = expected_pairs(a,fixed,candidates,start,end,depth,tolerance)
    observed_traces, calls, entered = [], [], []
    real = helper.interval_clear_batch

    def observed(moving, static, left, right, remaining, tol, **kwargs):
        assert len(moving)<=128 and kwargs['scalar'] is checker.separation and kwargs['turn'] is checker.turn
        assert (left,right,remaining,tol)==(start,end,depth,tolerance)
        results,info=real(moving,static,left,right,remaining,tol,**kwargs)
        calls.append(len(results));observed_traces.extend(info['DFS_state_sha256_by_pair'])
        return results,info

    totals=checker.interval_batch_counters()
    with patch.object(checker,'interval_clear_batch',observed):
        actual=list(checker.interval_pair_results(a,fixed,candidates,start,end,depth,tolerance,totals,entered.append))
    assert actual==expected and observed_traces==traces
    assert calls==[128,128,3] and [x['candidate_offset'] for x in entered]==[0,128,256]
    assert [k for k,clear,_ in actual if not clear]==[int(k) for k in candidates if k in contact_ids]
    assert totals['helper_pairs_evaluated']==count and totals['max_pairs_per_chunk']==128 and totals['scalar_fallback_pairs']==0
    assert totals['max_owned_helper_workspace_bound_bytes']<=4*1024*1024
    assert not list(checker.interval_pair_results(a,fixed,np.array([],dtype=np.intp),start,end,depth,tolerance,checker.interval_batch_counters()))
    assert frozen==(a.tobytes(),fixed.tobytes(),candidates.tobytes())

    # Genuine caller failure controls: incomplete returned arrays cannot silently
    # omit a pair. Independently compared real results detect a flipped contact
    # or swapped ordering rather than checking a canned expected implementation.
    def truncated(*args,**kwargs):
        results,info=real(*args,**kwargs)
        return results[:-1],info
    with patch.object(checker,'interval_clear_batch',truncated):
        try:
            list(checker.interval_pair_results(a,fixed,candidates,start,end,depth,tolerance,checker.interval_batch_counters()))
        except AssertionError as error:
            assert 'omitted or added' in str(error)
        else:
            raise AssertionError('Native caller accepted an omitted independent pair')

    mutation_controls=[]
    for mutation in ['contact_relabelled_clear','pair_results_reversed']:
        def altered(*args,**kwargs):
            results,info=real(*args,**kwargs);results=list(results)
            if mutation=='contact_relabelled_clear':
                for i,result in enumerate(results):
                    if not result[0]:
                        results[i]=(True,0);break
            else:
                results.reverse()
            return results,info
        with patch.object(checker,'interval_clear_batch',altered):
            got=list(checker.interval_pair_results(a,fixed,candidates,start,end,depth,tolerance,checker.interval_batch_counters()))
        assert got!=expected, 'Independent original scalar comparison missed '+mutation
        mutation_controls.append({'mutation':mutation,'detected_by_independent_scalar_comparison':True,
                                  'not_claimed_runtime_redundant_scalar_check':True})

    # Strict CLI settings unsupported by the accelerator remain accepted through
    # the original scalar function. No catch-and-relax or helper rejection path.
    fallbacks=[]; subset=np.array([258,1,0],dtype=np.intp)
    for lo_arg,hi_arg,remaining,tol in [
            (start,end,1,1e-8),(start,end,13,1e-8),(start,end,16,1e-8),
            (start,end,12,1e-9),(start,end,16,1e-12),
            (0.,math.pi+.1,12,1e-8),(np.int64(0),np.int64(-1),12,1e-8),
            (start,end,np.int64(12),1e-8),(start,end,True,1e-8),
            (np.float32(.17),np.float32(-1.07),12,1e-8),
            (np.float64(.17),np.float64(-1.07),12,1e-8),
            (np.longdouble('.17'),np.longdouble('-1.07'),12,1e-8),
            (False,True,12,1e-8)]:
        want,want_traces=expected_pairs(a,fixed,subset,lo_arg,hi_arg,remaining,tol)
        reference,states=traced_original();seen=[]
        def scalar(left,right,lo,hi,d,t):
            states.clear();result=reference['interval_clear'](left,right,lo,hi,d,t)
            seen.append(state_hash(states));assert (lo,hi,d,t)==(lo_arg,hi_arg,remaining,tol)
            return result
        tally=checker.interval_batch_counters()
        with patch.object(checker,'interval_clear',scalar),patch.object(checker,'interval_clear_batch',side_effect=AssertionError('Unsupported setting entered accelerator')) as forbidden:
            got=list(checker.interval_pair_results(a,fixed,subset,lo_arg,hi_arg,remaining,tol,tally))
            forbidden.assert_not_called()
        assert got==want and seen==want_traces and tally['scalar_fallback_pairs']==len(subset) and tally['accelerated_chunks']==0
        fallbacks.append({'start':float(lo_arg),'end':float(hi_arg),'depth':int(remaining),'depth_type':type(remaining).__name__,'endpoint_types':[type(lo_arg).__name__,type(hi_arg).__name__],'tolerance_m':tol,'pairs':len(subset),'scalar_results_and_DFS_exact':True})

    # Both original numerical decision boundaries still have actual SAT/scalar
    # fallback. The caller passes both unchanged, including upper equality.
    boundary_rows=[]
    upper=2*math.sin(1/4)+tolerance
    for gap in [tolerance,upper,np.nextafter(upper,math.inf)]:
        target=checker.turn(a,.5)+[0,gap,0]
        want,want_trace=expected_pairs(a,target[None],np.array([0]),0.,1.,12,tolerance)
        diagnostics=[]
        def record(*args,**kwargs):
            result,info=real(*args,**kwargs);diagnostics.append(info);return result,info
        with patch.object(checker,'interval_clear_batch',record):
            got=list(checker.interval_pair_results(a,target[None],np.array([0]),0.,1.,12,tolerance,checker.interval_batch_counters()))
        assert got==want and diagnostics[0]['DFS_state_sha256_by_pair']==want_trace
        assert diagnostics[0]['scalar_fallback_rows']>=1
        boundary_rows.append({'gap_m':gap,'results_and_DFS_exact':True,'actual_scalar_fallback_rows':diagnostics[0]['scalar_fallback_rows']})

    # Full-check orchestration fixtures mock ONLY the already separately tested
    # structural prefix. All15sampled poses and full-circle AABB run normally.
    # A false/unresolved interval result must block default proof PASS.
    orchestration=[]
    for mode in ['clear','forced_unresolved','sampled_contact']:
        static=a.copy() if mode=='sampled_contact' else np.array([[-.9,0.,-.9],[-.85,0.,-.9],[-.9,0.,-.85]])
        triangles=np.array([a,static]);moving=np.array([True,False])
        structure={'schema':'UNIT_ORCHESTRATION_FIXTURE_NOT_GEOMETRY_PROOF','result':'STRUCTURE_ONLY_PASS'}
        data=({'open_angle_deg':-65},{},b'',[],triangles,moving,['moving','fixed'],a[None],static[None])
        with tempfile.TemporaryDirectory(prefix='t2797-interval-unit-') as folder:
            directory=Path(folder);source=Path(__file__)
            args=SimpleNamespace(input=source,candidate=source,recipe=source,source_receipt=source,
                report=directory/'unit-only-proof.json',progress=None,max_depth=12,tolerance=tolerance,structure_only=False,sampled_only=False)
            def uncertain(*args,**kwargs):
                results,info=real(*args,**kwargs)
                return [(False,0) for _ in results],info
            oracle=uncertain if mode=='forced_unresolved' else real
            if mode=='sampled_contact':
                oracle=lambda *a,**k:(_ for _ in ()).throw(AssertionError('Sampled contacts must block interval proof'))
            with patch.object(checker,'verify_structure',return_value=(structure,data)),patch.object(checker,'interval_clear_batch',oracle):
                good=checker.check(args)
            result=json.loads(args.report.read_text());progress=json.loads(Path(str(args.report)+'.progress.json').read_text())
            assert len(result['sampled'])==15 and good is (mode=='clear') and result['PASS'] is (mode=='clear')
            if mode=='sampled_contact':
                assert result['unresolved_continuous_pairs'] is None and result['interval_counts']['pairs_completed']==0
            else:
                assert result['interval_counts']['broadphase_pairs']==result['interval_counts']['pairs_completed']==1
                assert result['interval_batch_totals']['helper_pairs_evaluated']==1
                assert result['interval_counts']['moving_triangles_completed']==1
                assert result['unresolved_continuous_pairs']==(0 if mode=='clear' else 1)
            assert progress['final_PASS'] is (mode=='clear')
            orchestration.append({'fixture':mode,'all15_samples_run':True,'default_full_proof_verdict_correct':True,
                                  'actual_carriage_or_fit_qualification':False})
    return {'schema':'chicago-brougham-native-interval-caller-controls-v1','result':'NUMERICAL_CALLER_CONTROLS_PASS',
            'ordered_pairs_and_DFS_exact':count,'chunk_sizes':calls,'independent_false_clear_and_order_controls':mutation_controls,
            'truncated_result_rejected':True,'unsupported_settings_scalar_fallback':fallbacks,
            'both_threshold_scalar_fallback':boundary_rows,'full_check_orchestration':orchestration,
            'actual_door_geometry_or_continuous_clearance_qualified':False}


if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
