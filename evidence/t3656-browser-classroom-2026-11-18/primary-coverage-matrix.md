# Primary renderer coverage at b1

Target baseline: `b1f507400cb743a3985cb1d50de1ebd085bd4f63`, with dev `c676aa2f` integrated.

**DEV has since advanced to 21f609244. This matrix remains b1/c676 evidence.** [Incoming-input review](dev-21f-20261119/coverage-review.md) requires actual folded-DEV integration, current source checks, and fresh stages 13–15 at both sizes before release.
Desktop 1–12 and mobile 1 retain their original results under the [scoped DEV-input review](../t3657-t3658-hunt-accessibility-2026-11-18/integration-c676/t3657-t3658-rebase-c676-plan.md). Desktop 13–15 and mobile 2–15 have fresh exact b1 published results. This is not an all-fresh thirty-stage run.

The [machine-readable matrix](primary-coverage-matrix.json) contains every full SHA-256, source commit, scope, count and elapsed time. Each abbreviated hash below links to that full record. Raw logs retain original identities.

The [independent applicability review](coverage-review/independent-review-20261119.md) checks the changed inputs and the stage 3/5/12 consumers and raw hashes. It found no gap within the stated reuse scope, while explicitly excluding new monument wording, source-backlink text, the complete revised route, and future changed inputs. It ran no new tests.

| Viewport / stages | Evidence | Passed | Staged + always-on | Raw log | SHA-256 record |
| --- | --- | ---: | ---: | --- | --- |
| desktop 1 | Retained 7019f986b | 95 | 82 + 13 | [log](renderer/remote-7019-desktop-1.log) | [`09e045155d326ef0`](primary-coverage-matrix.json) |
| desktop 2 | Retained 7019f986b | 115 | 102 + 13 | [log](renderer/remote-7019-desktop-2.log) | [`b715bc132fea417d`](primary-coverage-matrix.json) |
| desktop 3 | Retained 7019f986b | 107 | 94 + 13 | [log](renderer/current-desktop-3.log) | [`99b557d69fff232e`](primary-coverage-matrix.json) |
| desktop 4 | Retained 7019f986b | 42 | 29 + 13 | [log](renderer/remote-7019-desktop-4.log) | [`50c0a15af658733a`](primary-coverage-matrix.json) |
| desktop 5 | Retained 5034a724d | 30 | 17 + 13 | [log](renderer/remote-5034-desktop-5.log) | [`7f8c865e42ac29fc`](primary-coverage-matrix.json) |
| desktop 6 | Retained 7019f986b | 20 | 7 + 13 | [log](renderer/current-desktop-6.log) | [`5148b6f2e2cee68a`](primary-coverage-matrix.json) |
| desktop 7 | Retained 7019f986b | 39 | 26 + 13 | [log](renderer/remote-7019-desktop-7.log) | [`0641d39a9a7010aa`](primary-coverage-matrix.json) |
| desktop 8 | Retained 7019f986b | 22 | 9 + 13 | [log](renderer/remote-7019-desktop-8.log) | [`e86080b489cfd582`](primary-coverage-matrix.json) |
| desktop 9 | Retained 7019f986b | 27 | 14 + 13 | [log](renderer/remote-7019-desktop-9.log) | [`7c5f8a43e0371aaf`](primary-coverage-matrix.json) |
| desktop 10 | Retained 7019f986b | 31 | 18 + 13 | [log](renderer/current-desktop-10.log) | [`6aa11fdf0077b610`](primary-coverage-matrix.json) |
| desktop 11 | Retained 7019f986b | 21 | 8 + 13 | [log](renderer/current-desktop-11.log) | [`fb182e1738090643`](primary-coverage-matrix.json) |
| desktop 12 | Retained 7019f986b | 29 | 16 + 13 | [log](renderer/remote-7019-desktop-12.log) | [`551de03ad8cdaa4d`](primary-coverage-matrix.json) |
| desktop 13–15 | Fresh b1 | 310 | 297 + 13 | [log](renderer/b1-desktop-13-15/desktop13-15-pass.log) | [`a407a0201dbdb433`](primary-coverage-matrix.json) |
| mobile 1 | Retained 7019f986b | 95 | 82 + 13 | [log](renderer/current-mobile-1.log) | [`459a52c01389d025`](primary-coverage-matrix.json) |
| mobile 2 | Fresh b1 | 115 | 102 + 13 | [log](renderer/b1-mobile-2-12/mobile-2.log) | [`6a64ef76eb97bea9`](primary-coverage-matrix.json) |
| mobile 3 | Fresh b1 | 107 | 94 + 13 | [log](renderer/b1-mobile-2-12/mobile-3.log) | [`1f99b5572ac7aefd`](primary-coverage-matrix.json) |
| mobile 4 | Fresh b1 | 45 | 32 + 13 | [log](renderer/b1-mobile-2-12/mobile-4.log) | [`127f9c6b90c04f5f`](primary-coverage-matrix.json) |
| mobile 5 | Fresh b1 | 30 | 17 + 13 | [log](renderer/b1-mobile-2-12/mobile-5.log) | [`f4b3e7413c8f4627`](primary-coverage-matrix.json) |
| mobile 6 | Fresh b1 | 24 | 11 + 13 | [log](renderer/b1-mobile-2-12/mobile-6.log) | [`8ae8b26657d5938d`](primary-coverage-matrix.json) |
| mobile 7 | Fresh b1 | 39 | 26 + 13 | [log](renderer/b1-mobile-2-12/mobile-7.log) | [`46805d438ac8048e`](primary-coverage-matrix.json) |
| mobile 8 | Fresh b1 | 22 | 9 + 13 | [log](renderer/b1-mobile-2-12/mobile-8.log) | [`a5fd804527462462`](primary-coverage-matrix.json) |
| mobile 9 | Fresh b1 | 27 | 14 + 13 | [log](renderer/b1-mobile-2-12/mobile-9.log) | [`f5ed9319d9cdabe2`](primary-coverage-matrix.json) |
| mobile 10 | Fresh b1 | 31 | 18 + 13 | [log](renderer/b1-mobile-2-12/mobile-10.log) | [`2ad6471e707b09a8`](primary-coverage-matrix.json) |
| mobile 11 | Fresh b1 | 21 | 8 + 13 | [log](renderer/b1-mobile-2-12/mobile-11.log) | [`a9677d833e7e5fb1`](primary-coverage-matrix.json) |
| mobile 12 | Fresh b1 | 29 | 16 + 13 | [log](renderer/b1-mobile-2-12/mobile-12.log) | [`c6c9d3206594453d`](primary-coverage-matrix.json) |
| mobile 13 | Fresh b1 | 157 | 144 + 13 | [log](renderer/b1-mobile-complete/mobile-13.log) | [`d8dcafd984186818`](primary-coverage-matrix.json) |
| mobile 14 | Fresh b1 | 145 | 132 + 13 | [log](renderer/b1-mobile-complete/mobile-14.log) | [`5f6672503047c09c`](primary-coverage-matrix.json) |
| mobile 15 | Fresh b1 | 34 | 21 + 13 | [log](renderer/b1-mobile-complete/mobile-15.log) | [`2eea20743c451bcb`](primary-coverage-matrix.json) |

Fresh desktop 13–15 passed **310/0 in 54m06s**, with 297 staged checks plus 13 always-on checks counted once for the group. Fresh mobile 2–15 passed **826/0 in a summed 69m25s**, with 644 staged checks plus 182 repeated always-on checks. These are software-rendered validation timings, not device benchmarks.

Mobile 2’s original shell-exit receipt was lost across reconnection; its final summary and suite/page/vendor guards are complete. The [operator digest](renderer/b1-mobile-complete/digest.json) retains that limitation and records exit 0 for stages 3–15.

The retained review does not validate revised source-detail edges, changed hidden monument prose or the full revised 50-stop route. Stage 3 asserts unchanged 1835 subsets/counts/layout; stage 12 consumes an identical handout projection across 96 rows. The newly archived primary5034 stage5 receipt exercises the unchanged 1835 geometry and policy; the older b501 QA geometry evidence remains separate.

**Release remains pending:** all eight partitions of source run 44422645793 attempt 2 now passed1394 steps on the b1/c676 baseline, but its separate aggregate job was still queued at02:00UTC. The [latest baseline verification](dev-21f-20261119/verification.json) preserves that distinction. Cancelled attempt1 remains historical. Moving/upload run44422645797 passed on actual PR mergecda72c805, including32 upload checks. These results do not validate new DEV21f: actual folded-DEV integration, current source checks and fresh13–15 at both widths remain required. Neither PR is declared merged.

Earlier failed and capped attempts remain in the archive and are excluded from successful coverage. See [README](README.md), [final phone verification](renderer/b1-mobile-complete/verification.json), and [fresh desktop verification](renderer/b1-desktop-13-15/verification.json).
