"""Bounded rest-shape fairing of an existing stock rim; never a fit certificate."""
from __future__ import annotations

import math


def fair_stock_top_rim(tops, bottoms, protected_indices, maximum_lowering_m):
    """Fair only between caller-declared style anchors, below the old jaw limit.

    The caller supplies its existing jaw-limited rim. Three neighbour-average
    passes remove isolated sample kinks. A smooth, zero-at-anchor downward
    correction keeps the entire result at or below that rim; a single blend
    factor per arc bounds lowering without pointwise reclipping its shape.
    This changes a reconstructed garment's rest shape, not body anatomy, skin
    weights, measured jaw clearance, period evidence or posed acceptance.
    """
    n = len(tops)
    if not 12 <= n <= 128 or len(bottoms) != n:
        raise ValueError('finite matched stock rings required')
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in (*tops, *bottoms)):
        raise ValueError('finite stock heights required')
    if (type(maximum_lowering_m) not in (int, float)
            or not math.isfinite(maximum_lowering_m) or not 0 < maximum_lowering_m <= .01):
        raise ValueError('bounded existing jaw-clearance allowance required')
    anchors = sorted(set(protected_indices))
    if (len(anchors) < 2 or any(type(i) is not int or not 0 <= i < n for i in anchors)):
        raise ValueError('explicit distinct stock style anchors required')
    spans = [top - bottom for top, bottom in zip(tops, bottoms)]
    if min(spans) <= 0:
        raise ValueError('positive original stock height required')
    result = list(tops)
    arcs = []
    for left, right in zip(anchors, anchors[1:] + [anchors[0] + n]):
        ids = [i % n for i in range(left, right + 1)]
        if len(ids) <= 2:
            continue
        old = [tops[i] for i in ids]
        smooth = list(old)
        for _ in range(3):
            previous = smooth
            smooth = [old[0]] + [math.fsum((previous[j-1], 2*previous[j], previous[j+1])) / 4
                for j in range(1, len(ids)-1)] + [old[-1]]
        taper = [math.sin(math.pi*j/(len(ids)-1))**2 for j in range(len(ids))]
        downward_shift = max(0., *(max(0., smooth[j]-old[j])/taper[j]
            for j in range(1, len(ids)-1)))
        delta = [0.] + [min(0., smooth[j]-downward_shift*taper[j]-old[j])
            for j in range(1, len(ids)-1)] + [0.]
        proposed = max(-value for value in delta)
        # Never consume more than a quarter of the existing band height.
        allowance = min(maximum_lowering_m, min(spans[i] for i in ids)/4)
        blend = min(1., allowance/proposed) if proposed else 0.
        for j in range(1, len(ids)-1):
            result[ids[j]] = old[j] + blend*delta[j]
        arcs.append(dict(first_anchor=ids[0], last_anchor=ids[-1], blend=blend,
            downward_correction_m=downward_shift, maximum_allowed_lowering_m=allowance))
    if any(new > old or new <= bottom for new, old, bottom in zip(result, tops, bottoms)):
        raise ValueError('stock fairing exceeded its original rim or inverted its band')
    lowering = [old-new for old, new in zip(tops, result)]
    return result, dict(method='anchored_lower_only_stock_rim_fairing_v1',
        neighbour_passes=3, protected_indices=anchors, arcs=arcs,
        maximum_top_lowering_m=max(lowering), maximum_top_raising_m=0.,
        original_style_anchor_heights_preserved=all(result[i] == tops[i] for i in anchors),
        actual_posed_clearance_accepted=False, native_fit_accepted=False,
        photographic_accepted=False,
        scope='Reconstructed rest-rim smoothing only. Existing radial section sampling and skin weights remain the owner; actual LOD/pose/jaw/coat/tie clearance and photographic review are pending.')
