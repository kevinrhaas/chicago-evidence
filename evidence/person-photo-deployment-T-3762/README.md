# Photo deployment and surface review — T-3762

[Current native app images](GALLERY.md) show six adult/child/reference faces and four full figures from frozen tree `0aa14db492359069e453a68bae6e02b1db3aca0c`. Source PR: https://github.com/kevinrhaas/chicago/pull/2371. **The corrected candidate is undergoing the complete gate; it has not been deployed to dev yet.**

The library contains 320 adult and 64 child fictional references. NPC defaults use existing community/year context and the approved reference pools; Settings independently retains every compatible adult choice. The named atlas has 27 entries for 26 active people plus one prepared uncast reference; the two Greys keep their existing full skins. Staff stand-ins remain labelled.

The surface correction removes forehead-cap intersections, uses float precision to rebuild compressed cap normals, avoids darkening source-measured eye whites a second time, and keeps source bangs out of new fictional skin albedos. Child head/body/eye geometry and existing curated head fits remain protected. No hair triangles, textures or draw calls are added.

All 535 current photo outputs were actually rebuilt twice with identical bytes and unchanged pinned inputs. The proof protects 493 original pixel files and the original 256 fitted heads. [Reproduction receipt](surface-review-qualification/final-photo-writer-reproduction.json). The canonical rebuild settled, and the [served candidate verification](surface-review-qualification/visual-photo-published-verification.json) confirms all nine renderer modules, three libraries, 26 detail pages, two Stirling period portraits and 7,610 body assignments across the four years.

Added face atlas memory remains 12,873,272 bytes including mipmaps (12.28 MiB), using one shared nearby page. This bound excludes existing body/clothing textures and Grey full skins. Real low-power GPU FPS is unmeasured.

The complete local gate and dev-delivery receipts will be added once they pass. The previous full qualification is preserved in [BASELINE-b085.md](BASELINE-b085.md), with its source-bound [older gallery](GALLERY-b085.md). Its checks qualify that earlier source, not this corrected candidate.
