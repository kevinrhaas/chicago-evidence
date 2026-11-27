# Current desktop report: successful but uncalibrated

Candidate `1605dcbd4b58bedf98084a16d4b32d95a59bd20e`, grid45944016390, desktop job140324483802, attempt1. The original ZIP digest is verified against the GitHub artifact metadata.

The four-core Intel Xeon6975P-C report reads Full6830.5ms, Balanced5795.7ms and Light4227.5ms, with no page errors. This machine has no configured desktop ceilings; the stock tool explicitly warns that all three readings are read but not held. This success therefore does not clear the earlier calibrated EPYC Light7213.1ms reading above7000ms. The hold remains active across the new candidate head.

All other current-head grid cases continue and their outcomes must be inspected before a desktop-only eligibility repeat. A future eligible calibrated reading uses the unchanged CPU-specific limits, measurement samples, viewport, raster, geometry and population. A calibrated failure is retained for investigation. The old B4 failure, its uncalibrated repeat and the independent local paired diagnostic remain in sibling evidence folders. No current-head repeat has yet been requested; this folder is not merge qualification.
