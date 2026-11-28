"""Bind ongoing scene tests to a metadata lap by complete-tree identity."""
import json
from pathlib import Path

from vegetation_exact_note_folds import verify_folds
from vegetation_roughness_channel_fix_lap_proof import qualify as qualify_lap
from vegetation_dev_31a_render_input_equivalence import qualify as qualify_previous

W = Path('/workspace/work')
UPSTREAM = '5d1d9d2bd06dce649969770c1f6053a989dadb42'
MANUAL_PREFIX = 'vegetation-dev-31a'


def manual_source_equivalence(proof):
    old = json.loads((W/(MANUAL_PREFIX+'-final-integration-proof.json')).read_text())
    push = json.loads((W/(MANUAL_PREFIX+'-push-dispatch.json')).read_text())
    assert proof['actual_dev'] == UPSTREAM
    assert proof['previous_review_head'] == old['final_head'] == push['head']
    assert proof['source_sha256'] == old['source_sha256']
    assert proof['feature_code_sha256'] == old['feature_code_sha256']
    fold = verify_folds(Path(proof['repo']), old['final_tree'], proof['final_tree'])
    assert fold['complete'] and len(fold['folds']) == 4
    declared = proof['manual_source_equivalence']
    assert declared['complete'] and declared['tested_head'] == old['final_head']
    assert declared['tested_tree'] == old['final_tree']
    assert declared['current_tree'] == proof['final_tree']
    assert declared['only_exact_official_folds'] == fold
    return {
        'complete': True,
        'manual_source_prefix': MANUAL_PREFIX,
        'manual_tested_head': old['final_head'],
        'manual_tested_tree': old['final_tree'],
        'current_head': proof['final_head'],
        'current_tree': proof['final_tree'],
        'all47_feature_and_canonical_output_hashes_identical': True,
        'entire_repository_tree_identical_except_exact_official_release_fold': fold,
        'scope': 'The complete repository tree, including every renderer, asset, '
                 'dated record, test and canonical output, differs only by four '
                 'exact official release-note folds. Running browser/stock jobs '
                 'keep their actualac69 head; no result is relabelled. Fresh '
                 'actual-head Native and automatic regressions remain required.',
    }


def qualify(proof):
    binding = manual_source_equivalence(proof)
    old = json.loads((W/(MANUAL_PREFIX+'-final-integration-proof.json')).read_text())
    prior = qualify_previous(old)
    assert prior['complete'] and qualify_lap(proof)['complete']
    return {
        'complete': True,
        'measured_source_tree': proof['native_candidate_tree'],
        'current_integrated_tree': proof['final_tree'],
        'new_source_timing_execution_claimed': False,
        'manual_source_equivalence': binding,
        'previous_input_inspection': prior,
        'scope': 'The original complete6b Native and eligible actual EPYC7763/4 '
                 'readings retain their original identity. Actualac69 browser '
                 'and stock jobs continue on the exact scene source now present '
                 'in this metadata lap, with only the verified official release '
                 'fold differing. Current Native still runs on the actual merged '
                 'PR checkout; no current-head or timing claim is fabricated.',
    }
