# Optional male hat finish — people agent owns integration

Apply `HAT-FINISH.patch` to `tools/human_period_wardrobe.py` only after reviewing the opt-in. The original function result remains byte-for-byte equivalent when `profile["hat"]` has no `finish` field. Do not alter the female assembly or the no-hat Joseph profile.

For an isolated canonical Blender 4.5.3 preview, use an external recipe copy with `"finish": "rounded_felt_v1"` inside the hat specs of `teamster_waistcoat_hat` (Otis) and `teamster_short_jacket_hat` (Martin). Keep the original recipe, male body, hair, rig, identity, source and production-eligibility fields unchanged.

The optional grayscale felt roughness data is explicitly Non-Color. It avoids changing the existing reconstructed hat color or sharing the female color-encoding work. This small optional hook can be placed after the existing material dictionary is built in `human_teamster_blend.py`; the people agent must merge it into their own working material block, not replace that file:

```python
hat_spec = (wardrobe or {}).get('hat') or {}
if hat_spec.get('finish') == 'rounded_felt_v1':
    from human_period_wardrobe import felt_roughness_pixels
    felt = bpy.data.images.new('original_reconstructed_felt_roughness', width=128, height=128, alpha=False)
    felt.colorspace_settings.name = 'Non-Color'
    felt.pixels = felt_roughness_pixels(128)
    felt.file_format = 'PNG'
    felt.pack()
    material = materials['headwear__felt_hat']
    nodes, links = material.node_tree.nodes, material.node_tree.links
    texture = nodes.new('ShaderNodeTexImage')
    texture.name = 'Original reconstructed matte felt roughness'
    texture.image = felt
    texture.interpolation = 'Linear'
    bsdf = nodes['Principled BSDF']
    bsdf.inputs['Roughness'].default_value = 1.0
    links.new(texture.outputs['Color'], bsdf.inputs['Roughness'])
```

Actual packed texture/export/PBR behavior and source/web preview remain UNRUN. No source photograph pixels, derived normal maps, new material slot, rig or identity are introduced. The one existing hat material and head-bone ownership remain.
