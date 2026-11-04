Canonical liberties repair changes only top-level count 992→993; all 993 entries, 890 names, IDs, titles and citations remain byte-equivalent after the single scalar substitution.

Normal producer: python3 tools/compile_liberties.py. Direct downstream producer: python3 tools/compile_source_use.py, which emits public source sidecars, scene use maps, coverage report and its own manifest ownership list. Source-use reads entries and titles, not the top-level count. Reader text reads titles, summaries read IDs, and jaunts read unchanged Markdown headings. No downstream tracked artifact is causally forced by the count repair alone.

Before a fresh four-part gate, the original finite checks are python3 tools/compile_liberties.py --check and python3 tools/compile_source_use.py --check. A real reported downstream drift should be rebuilt by its normal producer, never hand-edited. Publication later copies the changed JSON and must be regenerated normally.

The 558.520s part1 failure remains NONPASS. All four parts must run freshly on ROOT's final new staged tree; no old positive part is reused. No APP edits, checks, derivations or helper execution were performed by this audit.

The independent original source-use check subsequently failed only docs/measurements/source_use_coverage.md. This is actual latent merged-report drift; ROOT is rebuilding it with compile_source_use.py and verifying --check under canonical supervision. The count-only repair still changes no source-use input projection. The final source must include both canonical repairs before the new full four-part run.
