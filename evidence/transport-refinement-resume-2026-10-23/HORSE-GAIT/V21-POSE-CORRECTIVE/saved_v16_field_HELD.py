"""Load frozen V16 bytes only; no field builder, cast, optimizer or serialization."""
from pathlib import Path
import hashlib, json
import numpy as np

HERE=Path(__file__).resolve().parent

def load(parts):
    pins=json.loads((HERE/'INPUT-PINS.json').read_text())
    for row in pins.values():
        assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
    assert pins['v16_arrays']['sha256']=='04df599158ea091eb6d0036d3aeab9159ee96b8dfd43524a17ff874d72492e2d'
    receipt=json.loads(Path(pins['v16_field_receipt']['path']).read_text())
    assert receipt['original_protected_vectors_exact'] is True
    assert receipt['tail_vertices_bits_exact']==969
    assert receipt['original_lower_field_bits_exact'] is True
    assert receipt['V12_pastern_ledger_unchanged'] is True
    assert receipt['clipping_pruning_or_renormalization'] is False
    assert receipt['prior_V14_WALK_FAIL_preserved'] is True
    tail=json.loads((HERE/'PROVED-TAIL-COMPONENT.json').read_text())
    with np.load(pins['phase_a_arrays']['path'],allow_pickle=False) as saved:
        classes=[saved[f'vertex_classes_{i}'].copy() for i in range(3)]
        protected=saved['source_protected_class_ids'].copy()
        known_ids=saved['declared_known_class_ids'].copy()
        known_vectors=saved['declared_known_vectors'].copy()
        class_count=len(saved['points_m'])
    arrays=[]
    with np.load(pins['v16_arrays']['path'],allow_pickle=False) as saved:
        assert set(saved.files)=={f'mesh_{i}_{k}' for i in range(3) for k in ('joints','weights')}
        for i,part in enumerate(parts):
            j,w=saved[f'mesh_{i}_joints'].copy(),saved[f'mesh_{i}_weights'].copy()
            assert j.dtype==np.uint16 and w.dtype==np.float32
            assert j.shape==w.shape==(len(part[0]),4)
            assert (j<26).all() and np.isfinite(w).all() and (w>=0).all() and (w<=1).all()
            arrays.append((j,w))
    tail_vertices=np.asarray(tail['exact_source_vertex_ids'],dtype=int)
    tail_classes=np.unique(classes[0][tail_vertices])
    assert len(tail_vertices)==969 and len(tail_classes)==901
    # The legacy declaration is converted for comparison only; candidate bytes
    # are never cast, normalized or reserialized.
    expected=np.zeros((class_count,26),dtype=np.float32)
    expected[known_ids]=known_vectors.astype(np.float32)
    assert np.isin(protected,known_ids).all()
    def validate(candidate):
        for i,(j,w) in enumerate(candidate):
            baseline_j,baseline_w=arrays[i]
            assert np.array_equal(j,baseline_j), 'Frozen V16 slots changed'
            assert np.array_equal(w.view(np.uint32),baseline_w.view(np.uint32)), 'Frozen V16 bits changed'
            rows=np.flatnonzero(np.isin(classes[i],protected)&~np.isin(classes[i],tail_classes))
            dense=np.zeros((len(rows),26),dtype=np.float32)
            np.add.at(dense,(np.arange(len(rows))[:,None],j[rows]),w[rows])
            assert np.array_equal(dense,expected[classes[i][rows]]), 'Original source-known vector changed'
        j,w=candidate[0]
        assert np.array_equal(j[tail_vertices],parts[0][2][tail_vertices])
        assert np.array_equal(w[tail_vertices],parts[0][3][tail_vertices]), 'Original tail bits changed'
    validate(arrays)
    corrupted=[(j.copy(),w.copy()) for j,w in arrays]
    corrupted[1][1][0,0]+=.001
    rejected=False
    try:validate(corrupted)
    except AssertionError:rejected=True
    assert rejected, 'Frozen-field corruption control was not rejected'
    return arrays,{'status':'EXACT_SAVED_V16_FIELD_ONLY_NO_NEW_FIELD',
        'source_sha256':pins['v16_arrays']['sha256'],'all_slots_float32_bits_exact':True,
        'original_protected_vectors_exact':True,'tail_vertices_bits_exact':969,
        'new_fields':0,'float32_candidate_casts':0,'clipping_pruning_renormalization':False,
        'field_corruption_negative_control_rejected':rejected,
        'standing_V16_qualification_unchanged':True,'prior_V16_WALK_FAIL_preserved':True}
