"""Build the reviewed source-bounded near anatomy with a locally refined hoof mesh.

All parent BIN bytes are retained. New selected body streams are appended, with
explicit source-face/edge ancestry for added geometry and skin/UV rows. Original
eye UVs/globes, images, hair, rig, original weight rows, binds and standing clip
remain immutable. New topology is not claimed to inherit an old physical proof.
"""

import argparse
import copy
import json
import math
from pathlib import Path
import struct

import generate_anatomy_v1 as base
import anatomy_topology_v2 as topology


D = Path(__file__).resolve().parent
APP = D.parents[3]
SCHEMA = "standing-horse-source-bounded-anatomy-recipe-v2"


def read_attribute(document, binary, index):
    accessor = document["accessors"][index]
    view = document["bufferViews"][accessor["bufferView"]]
    components = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[accessor["type"]]
    kind, size = {5121: ("B", 1), 5123: ("H", 2), 5125: ("I", 4), 5126: ("f", 4)}[accessor["componentType"]]
    base.require(not accessor.get("sparse") and not accessor.get("normalized"), "Dense parent attributes required")
    offset = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
    stride = view.get("byteStride", size * components)
    return [struct.unpack_from("<" + kind * components, binary, offset + i * stride)
            for i in range(accessor["count"])]


def f32(values):
    return [struct.unpack("<" + "f" * len(value), struct.pack("<" + "f" * len(value), *value)) for value in values]


def gated_field(point, controls):
    displacement = [0.0, 0.0, 0.0]
    jacobian = [[float(i == j) for j in range(3)] for i in range(3)]
    for control in controls:
        relative = [point[i] - control["centre_m"][i] for i in range(3)]
        radius = math.sqrt(sum((relative[i] / control["radii_m"][i]) ** 2 for i in range(3)))
        if radius >= 1:
            continue
        weight = (1 - radius) ** 4 * (4 * radius + 1)
        gradient = [-20 * (1 - radius) ** 3 * relative[i] / control["radii_m"][i] ** 2 for i in range(3)]
        if "lower_y_gate_m" in control:
            low, high = control["lower_y_gate_m"]
            t = min(1.0, max(0.0, (point[1] - low) / (high - low)))
            gate = topology.smoothstep(t)
            derivative = 30 * t ** 2 * (1 - t) ** 2 / (high - low) if 0 < t < 1 else 0.0
            gradient = [x * gate for x in gradient]
            gradient[1] += weight * derivative
            weight *= gate
        for i in range(3):
            displacement[i] += control["delta_m"][i] * weight
            for j in range(3):
                jacobian[i][j] += control["delta_m"][i] * gradient[j]
    return tuple(point[i] + displacement[i] for i in range(3)), jacobian


def append_stream(document, binary, values, kind, component_type, target):
    components = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[kind]
    fmt = {5123: "H", 5126: "f"}[component_type]
    binary.extend(b"\0" * (-len(binary) % 4))
    offset = len(binary)
    for value in values:
        binary.extend(struct.pack("<" + fmt * components, *value))
    view = len(document["bufferViews"])
    document["bufferViews"].append({"buffer": 0, "byteOffset": offset,
                                  "byteLength": len(binary) - offset, "target": target})
    accessor = {"bufferView": view, "componentType": component_type, "count": len(values), "type": kind}
    if component_type == 5126:
        accessor["min"] = [min(value[k] for value in values) for k in range(components)]
        accessor["max"] = [max(value[k] for value in values) for k in range(components)]
    index = len(document["accessors"])
    document["accessors"].append(accessor)
    return index


def upper_lid_profile(point, settings):
    """Contract only the projecting rim toward the protected globe's upper arc.

    The globe is unchanged. A compact C2 gate keeps the brow, cheek and lower lid
    outside this operation. The small declared skin offset is reconstructed, not
    an anatomical measurement. Return the exact analytical profile Jacobian.
    """
    result = tuple(point)
    matrix = [[float(i == j) for j in range(3)] for i in range(3)]
    if not settings:
        return result, matrix

    def gate(value, lo, hi):
        t = (value - lo) / (hi - lo)
        derivative = 30 * t ** 2 * (1 - t) ** 2 / (hi - lo) if 0 < t < 1 else 0.0
        return topology.smoothstep(t), derivative

    for row in settings["regions"]:
        relative = [point[k] - row["centre_m"][k] for k in range(3)]
        radius = math.sqrt(sum((relative[k] / row["radii_m"][k]) ** 2 for k in range(3)))
        if radius >= 1:
            continue
        fall, fall_d = gate(radius, settings["core_radius"], 1)
        weight = 1 - fall
        gradient = [-fall_d * relative[k] / (row["radii_m"][k] ** 2 * radius)
                    if radius > 0 else 0.0 for k in range(3)]
        centre, radii, side = row["globe_centre_m"], row["globe_radii_m"], row["side"]
        dy, dz = point[1] - centre[1], point[2] - centre[2]
        q = (dy / radii[1]) ** 2 + (dz / radii[2]) ** 2
        q_gradient = [0.0, 2 * dy / radii[1] ** 2, 2 * dz / radii[2] ** 2]
        q_fade, q_derivative = gate(q, *settings["ellipse_fade_q"])
        upper, upper_derivative = gate(point[1], centre[1] + .004, centre[1] + .014)
        gradient = [gradient[k] * (1 - q_fade) * upper
                    - weight * q_derivative * q_gradient[k] * upper
                    + (weight * (1 - q_fade) * upper_derivative if k == 1 else 0.0)
                    for k in range(3)]
        weight *= (1 - q_fade) * upper
        if weight == 0:
            continue
        # Smooth positive square-root argument, including at the ellipse edge.
        term = 1 - q
        root = math.sqrt(term * term + .03 ** 2)
        positive = (term + root) / 2
        target = side * centre[0] + radii[0] * math.sqrt(positive) + settings["skin_offset_m"]
        target_q_derivative = -radii[0] * (1 + term / root) / (4 * math.sqrt(positive))
        excess = side * point[0] - target
        if excess <= 0:
            continue
        # C1 positive hinge: no displacement and no normal jump at zero excess.
        epsilon = settings.get("hinge_transition_m", .0005)
        inset = settings["strength"] * excess ** 2 / (excess + epsilon)
        inset_derivative = settings["strength"] * excess * (excess + 2 * epsilon) / (excess + epsilon) ** 2
        bound = settings["maximum_inset_m"]
        transition = settings.get("cap_transition_m", .0005)
        if inset >= bound + transition:
            inset, inset_derivative = bound, 0.0
        elif inset > bound - transition:
            u = (inset - (bound - transition)) / (2 * transition)
            integral = u - 2.5 * u ** 4 + 3 * u ** 5 - u ** 6
            inset = bound - transition + 2 * transition * integral
            inset_derivative *= 1 - topology.smoothstep(u)
        excess_gradient = [side, -target_q_derivative * q_gradient[1], -target_q_derivative * q_gradient[2]]
        delta = -side * inset * weight
        result = (point[0] + delta, point[1], point[2])
        for k in range(3):
            matrix[0][k] -= side * (inset_derivative * excess_gradient[k] * weight + inset * gradient[k])
        break  # The two compact opposite-side regions cannot overlap.
    return result, matrix


def deformation(point, recipe):
    target, matrix = gated_field(point, recipe["controls"])
    target, profile_matrix = upper_lid_profile(target, recipe.get("upper_lid_profile"))
    return target, [[sum(profile_matrix[i][k] * matrix[k][j] for k in range(3))
                     for j in range(3)] for i in range(3)]


def derive(parent, recipe, sidecar, source_directory):
    base.require(base.digest(parent) == base.PARENT_SHA256, "Selected eye-UV parent drift")
    base.require(recipe["schema"] == SCHEMA and recipe["parent_sha256"] == base.PARENT_SHA256,
                 "Exact anatomy V2 recipe and true parent required")
    base.require(recipe["frame"] == {"units": "metres", "up": "+Y", "forward": "+Z", "anatomical_left": "+X"},
                 "Canonical frame changed")
    base.require(0 < recipe["maximum_body_displacement_m"] <= .04 and 0 < recipe["minimum_local_jacobian"] <= 1,
                 "Bound the declared body correction")
    source_ids = set()
    for reference in recipe["reference_bindings"]:
        source_id = reference["source_id"]
        source = json.loads((source_directory / (source_id + ".json")).read_text())
        base.require(source["id"] == source_id and source["rights_status"] in ["public_domain", "cleared"],
                     "Every anatomy source must resolve and permit asset derivation")
        source_ids.add(source_id)
    for control in recipe["controls"]:
        base.require(set(control["source_ids"]) <= source_ids and control["confidence"] == "reconstructed"
                     and control["reason"], "Every body choice needs a cleared source and declared reasoning")
        for key in ["centre_m", "radii_m", "delta_m"]:
            base.require(len(control[key]) == 3 and all(math.isfinite(x) for x in control[key]), "Nonfinite control")
        base.require(all(x > 0 for x in control["radii_m"]), "Positive field radii required")
        if "lower_y_gate_m" in control:
            low, high = control["lower_y_gate_m"]
            base.require(math.isfinite(low) and math.isfinite(high) and low < high, "Invalid lower-lid gate")
    hoof = recipe["hoof_refinement"]
    upper_lid = recipe.get("upper_lid_refinement")
    if upper_lid:
        base.require(set(upper_lid["source_ids"]) <= source_ids and upper_lid["confidence"] == "reconstructed"
                     and upper_lid["reason"], "Upper-lid refinement needs cleared sources and reasoning")
        base.require(len(upper_lid["regions"]) == 2 and len({row["id"] for row in upper_lid["regions"]}) == 2,
                     "Declare two distinct local upper-lid regions")
        for row in upper_lid["regions"]:
            base.require(len(row["centre_m"]) == len(row["radii_m"]) == 3
                         and all(math.isfinite(x) for x in row["centre_m"] + row["radii_m"])
                         and all(0 < x <= .1 for x in row["radii_m"])
                         and .05 < abs(row["centre_m"][0]) < .2
                         and 1.4 < row["centre_m"][1] < 1.7 and 1.2 < row["centre_m"][2] < 1.5,
                         "Upper-lid region must remain bounded to the orbital rim")
        base.require(upper_lid["regions"][0]["centre_m"][0] * upper_lid["regions"][1]["centre_m"][0] < 0,
                     "Upper-lid regions must describe opposite sides")
        base.require(0 <= upper_lid["original_vertex_fairing"] <= 1
                     and 0 <= upper_lid["edge_fairing"] <= 1
                     and 0 < upper_lid["maximum_old_vertex_shift_m"] <= .008
                     and 0 < upper_lid["maximum_edge_curvature_m"] <= .004,
                     "Upper-lid fairing must retain explicit small geometric bounds")
    base.require(set(hoof["source_ids"]) <= source_ids and hoof["confidence"] == "reconstructed" and hoof["reason"],
                 "Hoof reconstruction needs resolved cleared sources and reasoning")
    base.require(0 <= hoof["ground_anchor_band_m"] <= .02 and
                 0 < hoof["full_fairing_below_m"] < hoof["region_top_m"] <= .4 and
                 0 < hoof["region_radius_m"] <= .3 and
                 0 <= hoof["original_vertex_fairing"] <= 1 and 0 <= hoof["edge_fairing"] <= 1 and
                 0 < hoof["maximum_old_vertex_shift_m"] <= .02 and 0 < hoof["maximum_edge_curvature_m"] <= .02,
                 "Hoof recipe must declare bounded geometry choices")
    document, original_binary = base.read_glb(parent)
    original_document = copy.deepcopy(document)
    primitive = document["meshes"][1]["primitives"][0]
    base.require(primitive["attributes"] == {"JOINTS_0": 205, "NORMAL": 204, "POSITION": 203,
                 "TEXCOORD_0": 6, "TEXCOORD_1": 6, "WEIGHTS_0": 206} and primitive["indices"] == 7,
                 "Pinned body primitive layout changed")
    original_positions, original_normals = read_attribute(document, original_binary, 203), read_attribute(document, original_binary, 204)
    profile = recipe.get("upper_lid_profile")
    profile_qualification = None
    if profile:
        if "orientation_qualification" in profile:
            base.require(profile["orientation_qualification"] == "cofactor_and_continuous_area_v1" and upper_lid,
                         "Only the explicit bounded upper-lid qualification is supported")
            import anatomy_profile_qualification as profile_qualification
            base.require(upper_lid["original_vertex_fairing"] == upper_lid["edge_fairing"] == 0,
                         "The new profile samples its exact source field, without post-warp head Loop fairing")
        base.require(set(profile["source_ids"]) <= source_ids and profile["confidence"] == "reconstructed"
                     and profile["reason"], "Upper-lid profile needs cleared sources and reasoning")
        base.require(0 < profile["strength"] <= 1 and 0 < profile["maximum_inset_m"] <= .008
                     and .001 <= profile["skin_offset_m"] <= .005 and 0 <= profile["core_radius"] < .8
                     and len(profile["regions"]) == 2
                     and {row["side"] for row in profile["regions"]} == {-1, 1}
                     and 0 < profile["ellipse_fade_q"][0] < profile["ellipse_fade_q"][1] <= 1.3,
                     "Upper-lid profile needs small declared contraction/skin bounds")
        base.require(0 < profile.get("hinge_transition_m", .0005) <= .003
                     and 0 < profile.get("cap_transition_m", .0005) <= .003
                     and profile.get("cap_transition_m", .0005) < profile["maximum_inset_m"],
                     "Profile transitions must remain small and below the unchanged inset bound")
        eye_positions = read_attribute(document, original_binary, document["meshes"][2]["primitives"][0]["attributes"]["POSITION"])
        for row in profile["regions"]:
            side = row["side"]
            base.require(side in [-1, 1] and len(row["centre_m"]) == len(row["radii_m"]) == 3
                         and all(math.isfinite(x) for x in row["centre_m"] + row["radii_m"])
                         and all(0 < x <= .1 for x in row["radii_m"]), "Bound profile to its actual orbital region")
            points = [p for p in eye_positions if side * p[0] > 0]
            actual_centre = [(min(p[k] for p in points) + max(p[k] for p in points)) / 2 for k in range(3)]
            actual_radii = [(max(p[k] for p in points) - min(p[k] for p in points)) / 2 for k in range(3)]
            base.require(all(abs(a - b) < 1e-8 for a, b in zip(actual_centre, row["globe_centre_m"]))
                         and all(abs(a - b) < 1e-8 for a, b in zip(actual_radii, row["globe_radii_m"])),
                         "Profile arc must come from the unchanged source globe bounds")
    uv = read_attribute(document, original_binary, 6)
    joints, weights = read_attribute(document, original_binary, 205), read_attribute(document, original_binary, 206)
    indices = [value[0] for value in read_attribute(document, original_binary, 7)]
    triangles = [tuple(indices[i:i + 3]) for i in range(0, len(indices), 3)]
    positions, normals, changed, minimum_det = [], [], [], 1.0
    for i, (position, normal) in enumerate(zip(original_positions, original_normals)):
        target, jacobian = deformation(position, recipe)
        distance = math.dist(position, target)
        base.require(distance <= recipe["maximum_body_displacement_m"], "Body control exceeds declared bound")
        if distance:
            new_normal, determinant = base.normal_transform(normal, jacobian)
            base.require(determinant >= recipe["minimum_local_jacobian"], "Body field exceeds declared compression")
            changed.append(i)
            minimum_det = min(minimum_det, determinant)
        else:
            new_normal = normal
        positions.append(target)
        normals.append(new_normal)
    positions, normals = f32(positions), f32(normals)
    shaped = topology.refine(positions, normals, uv, joints, weights, triangles, sidecar, recipe["hoof_refinement"], upper_lid)
    sampled_head_rows = set()
    if profile_qualification:
        for row in shaped["receipt"]["added_vertices"]:
            if str(row.get("refinement_region", "")).startswith("lid:"):
                a, b = row["source_edge"]
                source_midpoint = tuple((original_positions[a][k] + original_positions[b][k]) / 2 for k in range(3))
                shaped["positions"][row["vertex"]], _ = deformation(source_midpoint, recipe)
                sampled_head_rows.add(row["vertex"])
        shaped = profile_qualification.conforming_field_refinement(shaped, original_positions, uv, joints,
            weights, triangles, upper_lid["regions"], lambda point: deformation(point, recipe),
            base.normal_transform, recipe["minimum_local_jacobian"], f32)
        sampled_head_rows.update(row["vertex"] for row in shaped["receipt"]["added_vertices"]
                                 if str(row.get("refinement_region", "")).startswith("lid:"))
    positions, normals = f32(shaped["positions"]), f32(shaped["normals"])
    if profile_qualification:
        normals = f32(profile_qualification.refit_profile_normals(positions, normals, shaped["triangles"],
                                                                 sampled_head_rows | set(changed)))
    base.require(all(math.dist(old, new) <= recipe["maximum_body_displacement_m"]
                     for old, new in zip(original_positions, positions)),
                 "Combined field and refinement exceed declared body displacement")
    for row in shaped["receipt"]["added_vertices"]:
        if "source_edge" in row:
            a, b = row["source_edge"]
            source_point = tuple((original_positions[a][k] + original_positions[b][k]) / 2 for k in range(3))
        else:
            base.require(profile_qualification is not None, "Legacy ancestry cannot change")
            source_point = tuple(sum(original_positions[i][k] * value
                for i, value in zip(row["source_vertex_ids"], row["source_barycentric_weights"])) for k in range(3))
        base.require(math.dist(source_point, positions[row["vertex"]]) <= recipe["maximum_body_displacement_m"],
                     "Refined edge exceeds declared body displacement from its source midpoint")
    minimum_dot = 1.0
    profile_proof = None
    source_child_positions = list(original_positions)
    if profile_qualification:
        coefficients = profile_qualification.source_coefficients(len(original_positions), shaped["receipt"]["added_vertices"])
        source_child_positions = profile_qualification.source_points(original_positions, coefficients)
        profile_proof = {"method": "cofactor_and_continuous_area_v1", "checked_children": 0,
            "inside_lid_children": 0, "outside_lid_children": 0, "world_normal_nonpositive_inside": [],
            "minimum_path_area_ratio": 1.0, "minimum_path_double_area_m2": float("inf"),
            "minimum_cofactor_orientation_dot": 1.0, "minimum_centroid_jacobian": 1.0,
            "region_child_counts": {row["id"]: 0 for row in upper_lid["regions"]},
            "bounded_child_records": [], "old_world_normal_guard_preserved_outside_lids": True,
            "exact_field_sampled_source_edge_midpoints": len(sampled_head_rows),
            "proper_crossing_qualification_required": True, "photographic_acceptance": False}
    for fi, triangle in enumerate(triangles):
        a, b, c = [original_positions[i] for i in triangle]
        old = topology.cross(tuple(b[k] - a[k] for k in range(3)), tuple(c[k] - a[k] for k in range(3)))
        length = math.sqrt(sum(x * x for x in old))
        if length < 1e-14:
            continue
        for child in shaped["receipt"]["source_face_to_children"][fi]:
            a, b, c = [positions[i] for i in shaped["triangles"][child]]
            actual = topology.cross(tuple(b[k] - a[k] for k in range(3)), tuple(c[k] - a[k] for k in range(3)))
            current_length = math.sqrt(sum(x * x for x in actual))
            base.require(current_length > 1e-14, "Serialized body develops a degenerate triangle")
            dot = sum(x * y for x, y in zip(old, actual)) / length / current_length
            if profile_qualification:
                try:
                    result = profile_qualification.qualify_child(old,
                        [source_child_positions[i] for i in shaped["triangles"][child]],
                        [positions[i] for i in shaped["triangles"][child]], upper_lid["regions"],
                        lambda point: deformation(point, recipe), base.normal_transform,
                        recipe["minimum_local_jacobian"])
                except ValueError as error:
                    raise ValueError(f"Upper-lid child qualification parent={fi}, child={child}: {error}") from error
                profile_proof["checked_children"] += 1
                profile_proof["minimum_path_area_ratio"] = min(profile_proof["minimum_path_area_ratio"], result["path"]["minimum_area_ratio"])
                profile_proof["minimum_path_double_area_m2"] = min(profile_proof["minimum_path_double_area_m2"], result["path"]["minimum_double_area_m2"])
                if result["region"] is None:
                    profile_proof["outside_lid_children"] += 1
                else:
                    profile_proof["inside_lid_children"] += 1
                    profile_proof["region_child_counts"][result["region"]] += 1
                    profile_proof["minimum_cofactor_orientation_dot"] = min(profile_proof["minimum_cofactor_orientation_dot"], result["cofactor_orientation_dot"])
                    profile_proof["minimum_centroid_jacobian"] = min(profile_proof["minimum_centroid_jacobian"], result["determinant"])
                    profile_proof["bounded_child_records"].append({"parent": fi, "child": child, **result})
                    if dot <= 0:
                        profile_proof["world_normal_nonpositive_inside"].append({"parent": fi, "child": child, "dot": dot})
            else:
                base.require(dot > 0, f"Serialized body/hoof reverses a source triangle: parent={fi}, child={child}, dot={dot:.9g}")
            minimum_dot = min(minimum_dot, dot)
    if profile_proof:
        base.require(profile_proof["checked_children"] == len(shaped["triangles"])
                     and all(profile_proof["region_child_counts"].values()),
                     "Every actual body child and both bounded lids need complete qualification")
    for vertex in shaped["receipt"]["ground_support_anchor_vertex_ids"]:
        base.require(positions[vertex] == original_positions[vertex], "Named source ground-support anchor moved")
    binary = bytearray(original_binary)
    attributes = {}
    for name, values, kind, component in [("POSITION", positions, "VEC3", 5126), ("NORMAL", normals, "VEC3", 5126),
            ("TEXCOORD_0", shaped["uv"], "VEC2", 5126), ("JOINTS_0", shaped["joints"], "VEC4", 5123),
            ("WEIGHTS_0", shaped["weights"], "VEC4", 5126)]:
        attributes[name] = append_stream(document, binary, values, kind, component, 34962)
    attributes["TEXCOORD_1"] = attributes["TEXCOORD_0"]
    primitive["attributes"] = attributes
    primitive["indices"] = append_stream(document, binary, [(i,) for tri in shaped["triangles"] for i in tri], "SCALAR", 5123, 34963)
    document["buffers"][0]["byteLength"] = len(binary)
    binary.extend(b"\0" * (-len(binary) % 4))
    base.require(bytes(binary[:len(original_binary)]) == original_binary, "An immutable parent BIN byte changed")
    document["asset"].setdefault("extras", {})["chicago4d_anatomy_master_v2"] = {
        "parent_sha256": base.PARENT_SHA256, "source_credit": "Horse by sevketkabatas, CC BY4.0, via Objaverse",
        "recipe_sha256": base.digest(json.dumps(recipe, sort_keys=True).encode()),
        "changes": "Reconstructed eyelid rest surface and adaptive hoof-wall/coronet geometry; no historical individual or breed",
        "parent_BIN_bytes_preserved": True, "body_topology_changed": True,
        "old_physical_proof_inherited": False, "photographic_acceptance": False}
    # The only parent JSON changes are body stream selection, buffer length and
    # the explicit ancestry notice. Every original accessor/view stays intact.
    restored = copy.deepcopy(document)
    restored["meshes"][1]["primitives"][0] = original_document["meshes"][1]["primitives"][0]
    restored["buffers"] = original_document["buffers"]
    restored["accessors"] = restored["accessors"][:len(original_document["accessors"])]
    restored["bufferViews"] = restored["bufferViews"][:len(original_document["bufferViews"])]
    del restored["asset"]["extras"]["chicago4d_anatomy_master_v2"]
    base.require(restored == original_document, "Unexpected protected parent JSON change")
    packed = json.dumps(document, separators=(",", ":")).encode()
    packed += b" " * (-len(packed) % 4)
    output = struct.pack("<4sII", b"glTF", 2, 28 + len(packed) + len(binary))
    output += struct.pack("<II", len(packed), 0x4E4F534A) + packed
    output += struct.pack("<II", len(binary), 0x004E4942) + binary
    base.require(len(output) <= 4 * 1024 * 1024, "Retain the unchanged 4MiB standing-asset byte ceiling")
    return output, {"body_field_changed_vertices": changed, "body_field_minimum_local_jacobian": minimum_det,
                    "bounded_upper_lid_profile_qualification": profile_proof,
                    "serialized_minimum_parent_child_face_normal_dot": minimum_dot,
                    "parent_BIN_prefix_exact": True, "parent_JSON_protection": True,
                    "hoof_refinement": shaped["receipt"], "selected_body_attributes": attributes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent", type=Path, default=D / base.PARENT_FILE)
    parser.add_argument("--recipe", type=Path, default=D / "anatomy-v2-recipe.json")
    parser.add_argument("--sidecar", type=Path, default=APP / "tools/fixtures/horse-anatomy-parent-sidecar-v1.json")
    parser.add_argument("--reference-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    base.require(not args.output_dir.exists(), "Fresh output directory required")
    args.output_dir.mkdir(parents=True)
    parent, recipe_bytes, sidecar_bytes = args.parent.read_bytes(), args.recipe.read_bytes(), args.sidecar.read_bytes()
    recipe = json.loads(recipe_bytes)
    receipt = {"schema": "standing-horse-anatomy-v2-source-derivation", "state": "STARTED",
               "parent_sha256": base.digest(parent), "recipe_sha256": base.digest(recipe_bytes),
               "generator_sha256": base.digest(Path(__file__).read_bytes()),
               "topology_source_sha256": base.digest((D / "anatomy_topology_v2.py").read_bytes()),
               "profile_qualification_source_sha256": base.digest((D / "anatomy_profile_qualification.py").read_bytes())
                   if recipe.get("upper_lid_profile", {}).get("orientation_qualification") else None,
               "photographic_acceptance": False, "fresh_loaded_deformation_contact_acceptance": False}
    try:
        base.require(base.digest(sidecar_bytes) == recipe["parent_sidecar_sha256"], "Pinned contact witness sidecar drift")
        for reference in recipe["reference_bindings"]:
            base.require(base.digest((args.reference_dir / reference["file"]).read_bytes()) == reference["sha256"],
                         "Actual cleared reference-image bytes drifted")
        candidate, proof = derive(parent, recipe, json.loads(sidecar_bytes), APP / "data/sources")
        file = args.output_dir / "horse-sevket-anatomy-v2.glb"
        file.write_bytes(candidate)
        base.require(base.digest(args.parent.read_bytes()) == base.PARENT_SHA256, "Original source changed")
        receipt.update(state="CANDIDATE_NOT_INSTALLED_OR_ACCEPTED", candidate_sha256=base.digest(candidate),
                       candidate_bytes=len(candidate), candidate_file=str(file), source_boundary=proof)
    except Exception as error:
        receipt.update(state="DERIVATION_REJECTED", error=str(error))
        raise
    finally:
        (args.output_dir / "DERIVATION-RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
