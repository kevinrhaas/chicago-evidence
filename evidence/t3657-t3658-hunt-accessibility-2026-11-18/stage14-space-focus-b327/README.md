# Focused stage 14 Space validation

Phone **11/11, exit 0, 55 seconds** and desktop retry **11/11, exit 0, 77 seconds**
passed on frozen runtime `edc7099032cd6d55d7a7e7f0d66d313b15960f10`, exercising
the exact smoke block from `b3272f5a4ac513dc4cd09819d21f4f5acefbff1d`.
The backup commit changes only the smoke tool. Six recorded runtime modules,
both harnesses, the patch and shared assertion block were checked against
immutable Git objects and original reports. The six modules also match 347;
that comparison does not turn these focused runs into a 347 release gate.

The first desktop attempt is preserved as **failed/incomplete, exit 1, 323
seconds**. Four checks passed before execution-context destruction; cleanup
stalled and a null-origin localStorage error was recorded. The retry adds
navigation/warning diagnostics and direct browser cleanup with the identical
assertion block. Its success does not explain or erase the original failure.

The probe reproduces Navigator retaining keyboard focus, verifies native Space
activates that focused control without movement, establishes world focus, and
then checks Space inspection without flight plus Escape and E close behavior.
Both successful reports recorded zero page/console and HTTP errors. Four phone
and ten retry ERR_ABORTED requests remain recorded, as do eight retry warnings.
The cleanup receipt confirms all probe servers and owned Chromium closed.

**Actual official stage: 14.** Historical filenames and the original phone/first
desktop scope strings say stage 13. Those raw artifacts remain unchanged; this
index and verification record correct that attribution. `tested-smoke-block.js`
is one canonical copy of identical bytes from all three attempt folders.

This is a bounded actual 1835 Light-detail town slice using normal `api.step`
frames, with continuous drawing paused between interactions. Later Go-to typing,
the full free-fly sequence and complete official stage 14 are outside this run.
Fresh full 13–15 at both widths and current combined CI remain required. No Jump,
texture-drain or sustained-device-performance result is claimed.

`upstream-2204/review.md` records the separate stage 15 texture-navigation review.
The archive independently verifies its fifteen-line smoke-only change and that
c23 retains it exactly. Its dated successful source gate and queued renderer
dispatches are review observations, not fresh archive-time CI queries. The
prepared diagnostic is **UNRUN** and needs review before use. A merged patch
and this focused Space result do not prove elimination of the texture failure.
