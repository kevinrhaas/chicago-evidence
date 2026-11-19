# Make your case: four more cases (T-3678), 19 November 2026

Source branch `claude/project-thread-kxj31w-t3678` (kevinrhaas/chicago), commit noted in the PR.

Pictures are a no-world native DOM fixture (`fixture/web-fixture.html`), not the walked town:
the app's own stylesheets, a completed-outing card built like jaunt-preview.js's, and the real
`jauntInvestigation` model and `renderInvestigation` view, fed the compiled student telling with
the published reader overlay applied (as the app does). `fixture/shoot.cjs` checks boxes, fills
the claim and uncertainty, opens the review, presses Save, then mounts the real field notebook
(`mountFieldNotebook`) and renders the real export (`notebookHTML`). 1280x800 and 390x780 at
deviceScaleFactor 2. `fixture/shoot-report.json`: every save reported "Saved", no page or console
errors, no horizontal overflow.

Files per case (`where-attack` 1812, `trading-post` 1812, `chappel` 1835, `bronze-rescue` 1904):
`*-top-*` the viewport at the question, `*-case-*` the whole case after Save, `*-notebook-*` the
saved entry in the notebook, `*-export-*` the downloaded/printed notebook page.
