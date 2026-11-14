# T-3553: the face library and jaunt hosts who talk (2026-11-14)

Pictures for the pull request that adds the 22-face library and makes a jaunt's host move
their mouth with the voice that reads their stop.

- `face-library-before-after.jpg`: fifteen people (five 1904 men, five 1904 maids, five 1812
  Potawatomi men), each row sharing one body. Top of each pair: the shared skin they wore
  before. Bottom: the face each now draws from the library. Rendered with
  `tools/human_variation_lineup.html` (`&faces=off` for the first of each pair), hats hidden.
- `jaunt-hosts-talking-before-after.jpg`: Frances Glessner. Two close stills from the same
  page (jaw shut, jaw at 6 degrees), and two frames of the running 1904 app during The
  Glessner Household jaunt while her recorded clip played.
- `app-1904-*.png`: the whole frames those crops come from, and John Glessner at his stop.
  Taken headless with software rendering, which draws a frame every few seconds, so they
  are stills and not a recording.

What was measured in the running app while each clip played (sampled in the page):
John Glessner: speaker `glessner_john_j`, level up to 0.49, jaw up to 5.7 degrees, talking hand up.
Frances Glessner: speaker `glessner_frances_m`, level up to 0.52, jaw up to 6.2 degrees; her
voice began on its own when the visitor arrived; the narrator's opening moved nobody; each
was hushed (jaw 0, hand down) when the voice stopped. No page errors.
