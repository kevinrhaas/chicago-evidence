# Grouped app QA: actual first failure and corrected prepared rerun

The first actual attempt failed the StMary and Beaubien Research assertions: the
fixture compared CSS-uppercased innerText against mixed-case Record, leaving the
real native disclosure closed. Parent stopped that runner; later page/browser-
closed failures are termination fallout. Every failure diagnostic/screenshot and
the exact first script are preserved. No full QA PASS is claimed or manufactured.

Corrected scriptSHA a43327dbfaa4e4ed2d9e381ea8f8cb86732fa0188d1ba9b092bdfb68236f8910
uses native summarytextContent case-insensitively before clicking the actual
summary. The archived diff proves this is the only script change; no Research,
model/source/network/flag assertion was removed. All six cases at bothviewports
remain12requiredcases. Authoritative generator, expected values and assertion
fragments are retained, with its unchanged source-only scriptdependency. Parent
verified exact regeneration; archiver ran no generator or browser.

Corrected actual execution remains UNRUN pending shared heavy-slot release. The
existing checkpointJSON predates this correction; RECOVERY.json independently
pins current correctedsources instead of pretending its oldhashes are current.
Replaying the authoritative generator requires an appropriate then-current app
checkout; this packet adds no canonical snapshot or model result. Running Hogan
heavy gate and every original image-match acceptance remain separate.
