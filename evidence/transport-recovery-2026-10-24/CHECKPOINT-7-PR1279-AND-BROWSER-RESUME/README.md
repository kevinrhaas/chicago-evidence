# PR1279 and browser continuation

DraftPR: https://github.com/kevinrhaas/chicago/pull/1279 . SourceHEAD3290195d/treebac89999 remains unchanged from passed1,063-step preflight (checkpoint6). OnlyT3083/T3086/T3087 were renewed and moved into review using actualPR1279 and normalCLI; they are notdone untilordinarygreenmerge/settle.

Mobile stages1-2:194passed0failed/181staged checks, command0/cleanupcomplete. Mobile3-4:138passed0failed/125stagedchecks, command0/cleanupcomplete. Bothzero pageerrors. Originalbatch3-4outer120was retained. A separate controlledreproduction proves closedstdout produces CPythonflush120 evenwith successfulchild0andcleanreceipts. The separate hash-bound reconciliation preserves the distinction. Correctedexternalwrapperusesunbufferedstatuswrite; closedstdout checks preserve success0 and childfailure7.

Newdriverreusesonlyverifiedpersistedcommand/log/cleanupreceipts, verifies unchangedcommittedHEAD/tree/all59filehashes beforeeveryleg, redirectsalloutputtofile, and resumesfrommobile5-6. Remainingmobile/desktopcoverageispending. SnapshotresumeJSON is notfinalbrowseracceptance.

ActualGitHubAPIworksagain despiteeffectivedomainmetadata; no alternateendpoint/proxywasused. PRgate/moving-frameswereIN_PROGRESS atcapture; pushreportandcontentbuildwarrantedSUCCESS, downstreambakescorrectlySKIPPED. Actualrun/checkoutbindingreviewisongoing. NoPRchecksuccess, ordinaryDEVmerge or publicdeliveryclaim. PRstaysdraftuntilrequiredlocalbrowsercoverageandfreshCIreviewcomplete. No productionpromotion.
