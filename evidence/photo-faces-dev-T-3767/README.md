# Default photographic adults and children on dev

Owner-authorized rollout in 1812, 1835, 1871 and 1904. The library contains 256 fictional adults and sixteen fictional child/toddler/teenager sources. Child textures use the existing child heads, morphs, body proportions and native eye placements. This is shared-UV registration, not an independent child shape fit.

`dev-child-gallery.png` shows all sixteen rendered child sources on existing child bodies. `dev-children-residents-before.png` and `dev-children-residents-after.png` show the same four 1812 residents at ages two, five, six and eight; the after image loads the default library without an opt-in flag. Resident-check JSON records identical morphs, options, age and height. The coverage log checks complete population tables across every year: 5,183 adult photo assignments, 2,400 child photo assignments and 27 personal likeness assignments protected.

Two crowd atlases plus a single shared nearby detail page add about 12 MiB of face textures. All rendering evidence here used Chromium SwiftShader: it establishes successful rendering and unchanged child proportions, not a real-GPU performance qualification. Personal historical likenesses retain priority.
