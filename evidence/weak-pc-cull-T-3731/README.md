# T-3731 — structure batches cull off cached bounds (PR kevinrhaas/chicago#2310)

- `frame-time-before-after.png`: median JS ms per frame, old cull path against new, same page, same frames (1904, `?device=weak`, Balanced, 1920x1080, Prairie walk, turn and aloft poses; cloud machine, software renderer).
- `*-before-after.jpg`: one held frame drawn by the old path and by the new, two stands.
- `*-only-difference.jpg`: the only pixels that differ between the two (red): a person turning and a horse arriving between the two renders. The structures' draw lists were identical: 23,386 compared, 23,386 the same.
