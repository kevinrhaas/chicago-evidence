# Host recovery and confirmed original CI installer cause

SourceH3290195d/treebac89999 remains unchanged; draftPR1279. Nineteen completed legs are retained: mobile1–13/15 anddesktop1–11. The host actually restarted (uptime248s, no prior driver/supervisor/smoke processes). Desktop12 had only a partial log with no commandresult/cleanupreceipt and is NOTPASS. Its original log is retained. Only incomplete12 is retried under a fresh after-runtime-restart prefix; currentbinding/driverpathsareinqueue-session.

Afterrestart an actualCDNthumbnailGET succeededHTTP200/17,931bytes/SHA259d4477aeb8b2a0bc4328d85410232752bb8943fc2a1d6dc09131dc85eb8285, exactmatchlocalmanifestedbytes. The earliermobile14networkfailure is retained. Both14legs are now queuedforfreshactualattempts after currentunaffected12/13/15 finish. They are notyetpassed.

Officialper-JOBGitHublogAPI nowworks. Originalmovingjob120848672967/run40085901811 confirms actualimageubuntu-26.04, successfulnpmPlaywright1.56.1install, then exacterrors: Cannot install dependencies for ubuntu26.04-x64 with Playwright1.56.1; Playwright does not support chromium on ubuntu26.04-x64. This is now a confirmedcause, not a hypothesis. Whole-runCLIarchivesstillfail atresults-receiver.actions.githubusercontent.com; documentedper-jobroutewasusednormally, withoutalternateproxy/reencoding.

Externalreviewableone-linepatch pinsmoving-framesrunnerubuntu-latest→ubuntu-24.04. IndependentproofchecksinstalledPW1.56.1supporteddependency/downloadmappings; gitapply--checkpassed. It is NOTYETAPPLIED toapp: sourceH/browserinputsstayfixeduntilcurrentmatrixfinishes. Commands/assertions/PWpin/timeoutsarepreserved. Any laterrealfixwillusefreshnormalCI, notrerun/dispatch/adminbypass.

ActualnormalgatejobstdoutnowprovescheckoutQ01977d66 andCHECKPASS1,064steps/383selftests. ReportandwarrantedjobstdoutprovesH329. ThePRcreate-refusedannotationwas an intentionalpassingwrong-repositorynegativecontrol thatopenednothing. Sanitizedlogsandrawhashbindingsareincluded;PRIVATEoriginals/SASqueriesexcluded.

MainCIgate/report/warrantedPASS; movingoriginalFAILretained. No fullbrowsergate/DEVmerge/publicdelivery/productionclaim. Prior timingoverrunsremainrecordedseparatelyfromfunctionalpasses.
