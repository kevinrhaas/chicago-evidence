# Single-owned-browser T2628 qualification module — prepared, NOT executed

Import `runHudQualification` from hud-qualification.mjs and invoke with the already owned Playwright Page after ghost trace has restored NORMAL, overlays off, Home/dock. The module starts/closes NO browser or server; caller owns them and must close finally. It accepts existing same desktop context and resizes page to1280×800,390×780,390×844 (CSS/layout qualification; not device emulation/phoneGPU acceptance). Existing published app must be booted/ready at its actual URL, with navigator+huds available. No npm install or external image/source needed. Actual current page implementation is used; only measurement code lives outside app.

Invocation:

    const {runHudQualification}=await import('/workspace/shared/hud-footprint-f97-harness/hud-qualification.mjs');
    await runHudQualification(page,{output:'/workspace/shared/f97-ghost-budget-diagnosis/hud'});

Leave console/HTTP/GL capture enabled in caller; module doesn't replace handlers. If it throws, report/partial runs are saved in finally. Source-only syntax check passed; no browser/localtown run yet. Root must release shared run before execution.

Each viewport repeats exact T2625lead-in: selectJaunts/Confidence/Move/Settings sequentially and poll the same selector's visiblebox, awaitHome then dock; original T2628popup/help cleanup. Captures initial and final actualdetent/level/rect/nativeanimation state, then exact original2pxvisible-painted union with original transient/street exclusions. Readiness requires originaldockcontract58desktop or136×64phone,level0/correctdetent and no running/pending nativeanimation, bounded60s/100ms polling. No CSS/geometry is hidden or reset by measure. Only known originalsetup docks beforebaseline; noredockinpredicate.

Original10%/nonemptyunion/+0.05plantedbutton/mobileoldrow>10 criteria remain. Screenshots actualbaseline perviewport; originalplantrows temporarily added/removed exactly as smoke. Negative controls: deliberatelyopenactualdevice must remainopen and refuse readiness; realinfiniteconstantopacity1nativeanimation must refusereadiness while visiblypainted (no hiding). Each negative uses2s readinesswall solely to show refusal, not to change normal60swall. Animation is canceledfinally and originalviewport/app/level restorationrequested. Input camera is not changed bymodule, though app selection may affect normalUI; caller may takefinalstate receipts.

A pass would qualify the measured captured states/known lead-in only; no full stage13/fullgate/production/photographic claim. If initiallevelopen after awaitedHome+dock, preserve aspossibleasyncreopen and investigate; no repeated redock to forcepass. If detentrail+width400+runningtransition settles58withcontrolsPASS, this directly confirms proposed instrumentrace. If60swall fails, retain actualstate/footprint and stop, no arbitrary retry.
