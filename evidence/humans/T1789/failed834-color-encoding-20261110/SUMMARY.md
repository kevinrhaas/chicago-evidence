# Failed834 cloth color diagnostic

This is failed-source diagnostic evidence, not successful producer intake, runtime adoption or fit/photo acceptance. Run42815699269/source834fcb retained its tangent-warning NONPASS.

One Joseph sourceLOD0 was verified by exact206 range, CRCfc88ab5b and SHA256 `8b99c65d7f3e764257aa8a490829ee54d214fd86d0171db341a680d48d79251f`. Whole ZIP digest was not verified. The container stayed in memory; only eleven garment images were decoded. No skin/hair image, .blend, full archive or private job log is included.

| Garment | Old effective linear RGB | Failed834 effective linear RGB |
| --- | --- | --- |
| garment_upper__shirt_linen | 0.389001, 0.327797, 0.203317 | 0.393211, 0.330418, 0.204956 |
| garment_outer__waistcoat_wool | 0.140000, 0.150000, 0.140000 | 0.017391, 0.019621, 0.017391 |
| garment_lower__highwaist_pantaloons | 0.180000, 0.160000, 0.130000 | 0.027226, 0.021991, 0.015329 |
| garment_outer__round_jacket | 0.045000, 0.055000, 0.063000 | 0.003500, 0.004400, 0.005205 |

Means use actual glTF baseColorFactor times IEC-sRGB-decoded color texels; these are uniform texel means, not rendered or surface-weighted appearance. ORM/normal channels are linear data. Wool darkening is observed; the existing shirt already used an encoded image, so it must not be blindly transformed with the factor-only wool. A source correction still needs actual native export/color readback.
