"""Narrow finite-triangle qualification for an explicitly new upper-lid profile.

Legacy recipes retain their existing fixed-world rotation guard. This module
does not certify mesh crossings, motion, a rendered appearance or acceptance.
"""

import math
from collections import defaultdict

import numpy as np


def refit_profile_normals(positions, normals, triangles, affected):
    """Recompute the finite sampled profile and its one-ring, preserving UV rows."""
    local = set(affected)
    local.update(i for triangle in triangles if any(i in affected for i in triangle) for i in triangle)
    keys = [tuple(round(x, 7) for x in point) for point in positions]
    sums = defaultdict(lambda: np.zeros(3))
    for triangle in triangles:
        vector = normal([positions[i] for i in triangle])
        for i in triangle:
            sums[keys[i]] += vector
    result = list(normals)
    for i in local:
        vector = sums[keys[i]]
        length = float(np.linalg.norm(vector))
        if length <= 1e-20:
            raise ValueError("Finite sampled upper-profile normal is degenerate")
        result[i] = tuple(vector / length)
    return result


def source_coefficients(original_count, added):
    result = [{i: 1.0} for i in range(original_count)]
    for row in added:
        if row["vertex"] != len(result):
            raise ValueError("Every new source row must have ordered exact ancestry")
        if "source_edge" in row:
            a, b = row["source_edge"]
            if max(a, b) >= original_count or row["source_interpolation"] != [.5, .5]:
                raise ValueError("Original source-edge ancestry changed")
            result.append({a: .5, b: .5})
        else:
            ids, weights = row["source_vertex_ids"], row["source_barycentric_weights"]
            if len(ids) != len(weights) or not 1 <= len(ids) <= 3 or len(set(ids)) != len(ids):
                raise ValueError("Explicit original-face barycentric ancestry required")
            if max(ids) >= original_count or min(weights) <= 0 or sum(weights) != 1:
                raise ValueError("Original-face barycentric weights must be positive and sum exactly to one")
            result.append(dict(zip(ids, weights)))
    return result


def source_points(original, coefficients):
    return [tuple(sum(original[i][k] * weight for i, weight in row.items()) for k in range(3))
            for row in coefficients]


def conforming_field_refinement(shaped, original_positions, original_uv, original_joints,
                               original_weights, original_triangles, regions, deformation,
                               normal_transform, minimum_jacobian, serialize):
    """Bisect only actual failing lid edges, sharing every incident indexed edge.

    Every new point samples F at its true undeformed barycentric location. UVs and
    skin are independently rebuilt from original rows, with no influence pruning.
    The fixed limits prevent an unbounded refinement or evasion of the byte cap.
    """
    positions, normals = shaped["positions"], shaped["normals"]
    uv, joints, weights = shaped["uv"], shaped["joints"], shaped["weights"]
    triangles, receipt = shaped["triangles"], shaped["receipt"]
    added = receipt["added_vertices"]
    coefficients = source_coefficients(len(original_positions), added)
    owners = [None] * len(triangles)
    for parent, children in enumerate(receipt["source_face_to_children"]):
        for child in children:
            if owners[child] is not None:
                raise ValueError("A child has duplicate parent ownership")
            owners[child] = parent
    if any(parent is None for parent in owners):
        raise ValueError("A child lacks original parent ownership")
    start_vertices = len(positions)
    history = []

    def edge_key(a, b, source):
        return tuple(sorted((tuple(round(x, 7) for x in source[a]),
                             tuple(round(x, 7) for x in source[b]))))

    for lap in range(4):
        actual = serialize(positions)
        source = source_points(original_positions, coefficients)
        bad = []
        for child, triangle in enumerate(triangles):
            parent = owners[child]
            before, after = [source[i] for i in triangle], [actual[i] for i in triangle]
            try:
                qualify_child(normal([original_positions[i] for i in original_triangles[parent]]),
                              before, after, regions, deformation, normal_transform, minimum_jacobian)
            except ValueError as error:
                message = str(error)
                if region_for(before, after, regions) is None or not (
                        "cofactor-transported" in message or "collapses on its continuous" in message):
                    raise ValueError(f"Non-refinable child parent={parent}, child={child}: {message}") from error
                bad.append((child, message))
        if not bad:
            shaped["positions"] = actual
            break
        if lap == 3:
            diagnostic = {"refinement_laps": history, "additional_rows": len(positions) - start_vertices,
                "remaining_failures": [{"parent": owners[child], "child": child, "reason": message}
                                       for child, message in bad]}
            raise ValueError("Bounded upper-lid refinement did not qualify within three laps: " + str(diagnostic))
        selected = set()
        for child, _ in bad:
            edges = list(zip(triangles[child], triangles[child][1:] + triangles[child][:1]))
            a, b = max(edges, key=lambda edge: (math.dist(source[edge[0]], source[edge[1]]),
                                               edge_key(*edge, source)))
            selected.add(edge_key(a, b, source))
        midpoint_rows = {}

        def midpoint(a, b, parent):
            if edge_key(a, b, source) not in selected:
                return None
            key = tuple(sorted((a, b)))
            if key in midpoint_rows:
                return midpoint_rows[key]
            if len(positions) - start_vertices >= 128:
                raise ValueError("Bounded profile refinement exceeds128additional source rows")
            combined = defaultdict(float)
            for vertex in (a, b):
                for i, weight in coefficients[vertex].items():
                    combined[i] += .5 * weight
            combined = dict(sorted((i, weight) for i, weight in combined.items() if weight > 0))
            if not set(combined) <= set(original_triangles[parent]) or sum(combined.values()) != 1:
                raise ValueError("Refined point left its actual original parent face")
            point = tuple(sum(original_positions[i][k] * value for i, value in combined.items()) for k in range(3))
            target, _ = deformation(point)
            index = len(positions)
            positions.append(target)
            interpolated_normal = np.asarray(normals[a]) + normals[b]
            length = float(np.linalg.norm(interpolated_normal))
            if length <= 1e-20:
                raise ValueError("Profile edge normal interpolation is degenerate")
            normals.append(tuple(interpolated_normal / length))
            uv.append(tuple(sum(original_uv[i][k] * value for i, value in combined.items()) for k in range(2)))
            skin = defaultdict(float)
            for i, value in combined.items():
                for joint, weight in zip(original_joints[i], original_weights[i]):
                    skin[joint] += value * weight
            active = sorted(((joint, weight) for joint, weight in skin.items() if weight > 0),
                            key=lambda row: (-row[1], row[0]))
            if len(active) > 4:
                raise ValueError("Refined profile row needs more than four influences; no pruning allowed")
            total = sum(weight for _, weight in active)
            joints.append(tuple([joint for joint, _ in active] + [0] * (4 - len(active))))
            weights.append(tuple([weight / total for _, weight in active] + [0.] * (4 - len(active))))
            added.append({"vertex": index, "source_parent_face": parent,
                          "source_vertex_ids": list(combined), "source_barycentric_weights": list(combined.values()),
                          "refinement_region": "lid:adaptive_exact_field", "source_interpolation": "original-face barycentric"})
            coefficients.append(combined)
            midpoint_rows[key] = index
            return index

        refined, new_owners = [], []
        for (a, b, c), parent in zip(triangles, owners):
            ab, bc, ca = midpoint(a, b, parent), midpoint(b, c, parent), midpoint(c, a, parent)
            mask = int(ab is not None) + 2 * int(bc is not None) + 4 * int(ca is not None)
            patterns = {0: [(a, b, c)], 1: [(a, ab, c), (ab, b, c)], 2: [(b, bc, a), (bc, c, a)],
                        4: [(c, ca, b), (ca, a, b)], 3: [(b, bc, ab), (a, ab, c), (ab, bc, c)],
                        5: [(a, ab, ca), (ab, b, c), (ab, c, ca)],
                        6: [(c, ca, bc), (a, b, ca), (b, bc, ca)],
                        7: [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]}
            refined.extend(patterns[mask])
            new_owners.extend([parent] * len(patterns[mask]))
        history.append({"lap": lap + 1, "failing_children": len(bad),
                        "new_rows": len(positions) - start_vertices,
                        "original_rejections": [{"child": child, "reason": message} for child, message in bad]})
        triangles, owners = refined, new_owners
    mapping = [[] for _ in original_triangles]
    for child, parent in enumerate(owners):
        mapping[parent].append(child)
    receipt.update(new_vertices=len(positions), new_triangles=len(triangles), source_face_to_children=mapping,
                   adaptive_profile_refinement={"laps": history, "added_rows": len(positions) - start_vertices,
                       "maximum_additional_rows": 128, "maximum_laps": 3,
                       "strategy": "Only failing children select their longest original-source edge; shared edges split conformingly to improve sliver aspect ratio",
                       "source_sampling": "Actual composedF at undeformed original-face barycentric coordinates; all selected shared edges split conformingly"})
    shaped["triangles"] = triangles
    return shaped


def normal(points):
    return np.cross(np.asarray(points[1]) - points[0], np.asarray(points[2]) - points[0])


def area_path(source, target):
    """Analytic squared-area quartic: endpoints plus every real derivative root.

    Positions interpolate linearly. The oriented double-area vector is quadratic,
    so its squared length is quartic. Evaluate vectors directly at the critical
    points to avoid cancellation in a nearly collapsed quartic's scalar value.
    """
    a, b = np.asarray(source, dtype=float), np.asarray(target, dtype=float)
    u, v = a[1] - a[0], a[2] - a[0]
    delta = b - a
    du, dv = delta[1] - delta[0], delta[2] - delta[0]
    n0 = np.cross(u, v)
    n1 = np.cross(du, v) + np.cross(u, dv)
    n2 = np.cross(du, dv)
    initial = float(np.dot(n0, n0))
    if initial <= 1e-28:
        raise ValueError("Source child is degenerate")
    derivative = np.array([2 * np.dot(n0, n1),
                           2 * (np.dot(n1, n1) + 2 * np.dot(n0, n2)),
                           6 * np.dot(n1, n2), 4 * np.dot(n2, n2)], dtype=float) / initial
    times = [0.0, 1.0]
    for root in np.polynomial.polynomial.polyroots(derivative):
        if abs(root.imag) <= 1e-8 and 0 < root.real < 1:
            times.append(float(root.real))
    values = [(float(np.linalg.norm(n0 + t * n1 + t * t * n2)), t) for t in times]
    minimum, time = min(values)
    ratio = minimum / math.sqrt(initial)
    if minimum <= 1e-14 or ratio <= 1e-6:
        raise ValueError("Child collapses on its continuous linear deformation path")
    return {"minimum_double_area_m2": minimum, "minimum_area_ratio": ratio,
            "minimum_at_t": time, "critical_points_checked": len(times)}


def region_for(source, target, regions):
    """Both whole endpoint triangles lie in one convex declared ellipsoid.

    Consequently every vertex and triangle point along the linear path stays in
    that same ellipsoid. No intersecting-parent or one-vertex exemption is used.
    """
    for region in regions:
        if all(sum(((point[k] - region["centre_m"][k]) / region["radii_m"][k]) ** 2
                   for k in range(3)) <= 1 for point in [*source, *target]):
            return region["id"]
    return None


def qualify_child(parent_normal, source, target, regions, deformation, normal_transform,
                  minimum_jacobian):
    old, new = normal(source), normal(target)
    old_length, new_length = float(np.linalg.norm(old)), float(np.linalg.norm(new))
    if old_length <= 1e-14 or new_length <= 1e-14:
        raise ValueError("Actual source/serialized child is degenerate")
    if float(np.dot(old, parent_normal)) <= 0:
        raise ValueError("Child source ancestry reverses canonical parent winding")
    path = area_path(source, target)
    world_dot = float(np.dot(old, new)) / (old_length * new_length)
    region = region_for(source, target, regions)
    result = {"world_normal_dot": world_dot, "region": region, "path": path}
    if region is None:
        if world_dot <= 0:
            raise ValueError("Outside the bounded upper lid, the original world-normal guard still applies")
        return result
    centroid = tuple(sum(point[k] for point in source) / 3 for k in range(3))
    _, jacobian = deformation(centroid)
    transported, determinant = normal_transform(old, jacobian)
    if determinant < minimum_jacobian:
        raise ValueError(f"Source-child centroid violates the unchanged Jacobian bound: actual={determinant:.9g}, minimum={minimum_jacobian:.9g}")
    agreement = float(np.dot(transported, new)) / new_length
    if agreement <= 0:
        raise ValueError("Serialized winding opposes the actual cofactor-transported source child")
    result.update(source_child_centroid_m=centroid, determinant=determinant,
                  cofactor_orientation_dot=agreement)
    return result


def self_test(normal_transform):
    source = [(0., 0., 0.), (1., 0., 0.), (0., 1., 0.)]
    regions = [{"id": "controlled", "centre_m": [0., 0., 0.], "radii_m": [3., 3., 3.]}]
    angle = 2 * math.pi / 3
    rotation = [[1., 0., 0.], [0., math.cos(angle), -math.sin(angle)],
                [0., math.sin(angle), math.cos(angle)]]
    target = [tuple(sum(rotation[i][k] * p[k] for k in range(3)) for i in range(3)) for p in source]
    deform = lambda p: (p, rotation)
    positive = qualify_child(normal(source), source, target, regions, deform, normal_transform, .25)
    assert positive["world_normal_dot"] < 0 and positive["cofactor_orientation_dot"] > .999
    assert positive["path"]["minimum_area_ratio"] > .49

    def refused(action, message):
        try:
            action()
        except ValueError as error:
            assert message in str(error), str(error)
        else:
            raise AssertionError("A real geometry corruption was accepted: " + message)

    # Keep canonical source/ancestry order fixed while reversing serialized target winding.
    refused(lambda: qualify_child(normal(source), source, [target[0], target[2], target[1]],
                                  regions, deform, normal_transform, .25), "cofactor")
    refused(lambda: qualify_child(normal(source), source, target, [], deform, normal_transform, .25),
            "original world-normal")
    refused(lambda: area_path(source, [(0., 0., 0.), (1., 0., 0.), (2., 0., 0.)]), "collapses")
    # Both endpoints have positive area and orientation, but the intermediate t=.5 collapses.
    refused(lambda: area_path(source, [(0., 0., 0.), (-1., 0., 0.), (0., -1., 0.)]), "collapses")
    refused(lambda: qualify_child(normal(source), [source[0], source[2], source[1]], target,
                                  regions, deform, normal_transform, .25), "parent winding")
    return {"proper_120_degree_rotation": "PASS", "reversed_serialized_winding": "REFUSED",
            "outside_region_rotation": "REFUSED", "final_collapse": "REFUSED",
            "intermediate_collapse_with_valid_endpoints": "REFUSED", "wrong_source_ancestry": "REFUSED"}
