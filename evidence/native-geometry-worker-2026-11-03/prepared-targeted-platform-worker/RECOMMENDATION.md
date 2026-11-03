# Existing native authoring path and exact-ticket proposal — PREPARED ONLY

No repository source, index, refs, claims, workflow, dispatch, native model or deployment was changed. This folder holds external preimages/postimages and a reviewable patch, not a feature branch or submitted PR.

## Existing path found

Current polecat-platform main was `777f69cd6a45e1567ad52320bebf00fea910fc80`. Exact workflow blob `3be65a00161edf3f6940f53853faae1baadddf95` provisions Chicago's pinned Blender cache. Its public native worker has150 minutes; the private ChatGPT route has180. The public worker already runs code authoring and native generation in one checkout before the source commit. Its current improve.md explicitly says stale data-only source cannot merge and regeneration belongs in the same commit as the record change.

Evidence:
- https://github.com/kevinrhaas/polecat-platform/blob/777f69cd6a45e1567ad52320bebf00fea910fc80/.github/workflows/steward-improve.yml
- https://github.com/kevinrhaas/polecat-platform/blob/777f69cd6a45e1567ad52320bebf00fea910fc80/.github/steward/improve.md

This is the appropriate existing execution mechanism for geometry-before-first-commit. The50-minute cap belongs to Chicago's separate content-bake job and does not govern the150-minute native authoring worker.

However, current public worker uses `ubuntu-latest`, not a literal Ubuntu26.04 pin. Do not describe that existing floating job as a newly qualified pinned production build. The proposed targeted job below fixes this for the new exact task while leaving existing lanes unchanged.

## Every existing selector checked

The workflow accepts app, slice, slices, model, processor, effort, lane, queue_position, max_turns and finish_only. It has no ticket, task, patch or prompt input.

- app selects the repository, not a particular ticket.
- slice/slices and queue_position become the kth workable row in the prompt. The prompt explicitly falls back to another row if that ticket is taken. Queue movement makes an ordinal unsuitable for an exact Jail task.
- lane is an identity/concurrency label, not task text. Its validator rejects arbitrary injected prompt syntax.
- finish_only is compared to literal1. It selects generic resume/stuck PR work and takes no new ticket; passing a PR number does not target that PR.
- model/processor/effort only choose an existing worker configuration. No new model selection is proposed here.

A generic dispatch would therefore risk unrelated work. None was sent.

## Minimal prepared owner-visible change

`targeted-worker.patch` changes exactly three platform files:

1. Add optional `target_ticket`, default blank, and map it to TARGET_TICKET. Existing blank-input runs keep their queue behavior and budgets. Give exact targets a distinct concurrency group.
2. Add targeted-chicago job with literal `runs-on: ubuntu-26.04` and150-minute cap. A YAML steps anchor reuses the complete existing native public worker, rather than duplicating or shortening its validation steps. Existing public/private jobs exclude exact-target runs. Targeted runs do not refill a scheduler slot they did not occupy.
3. Existing validate-run.mjs checks exact T-number syntax, app=chicago, the public native processor, solitary slot, no queue ordinal and no finish-only conflict. Invalid targets fail before an agent starts. The appended target prompt and improve.md require only that exact ticket, no fallback/grouping/new photo follow-ups, normal claim, stop on live ownership, actual affected native outputs before first commit, bounded native commands, all four source parts, both viewport tests and normal green dev PR merge.

The existing native cache reads the actual Chicago pin, currently4.5.3, and the native build owner verifies the pinned tarball SHA. No local Blender invocation or installation is proposed. Credentials/TLS, all source assertions and ordinary protected PR flow remain unchanged.

### Textual policy conflict to acknowledge

Chicago AGENTS still contains the older sentence 'No Blender on the improve runner' and the nightly-source-half wording. The same file also allows geometry-affecting parcels to run Blender, while current platform workflow and its improvement instructions explicitly provision native authoring and forbid stale data-only commits. This proposal does not silently declare those texts identical. The owner-visible workflow PR should expressly designate the new targeted-chicago job as the pinned native authoring worker and record that source, generated assets and the source gate complete before its first source commit. The local cloud runner remains Blender-free. Parent must resolve/record this scoped policy interpretation during review, rather than claiming a generic runtime capability alone waives repository policy.

## Jail invocation after proper review — not executed

Before dispatch, update the EXISTING T2380 recovery section through native ticket sync with the exact current public prepared-source and execution-budget links. Do not create another photo ticket. Reassess its current claim and all16 preimages, especially append-only LIBERTIES after subsequent dev changes.

After review of the platform feature commit and applicable platform CI, dispatch steward-improve.yml ON THAT REVIEWED FEATURE REF with app=chicago, target_ticket=T-2380, slice=1, slices=1 and a distinct native lane name. Leave model/effort unspecified. No platform-main merge is needed just to execute a reviewed definition ref. The normal same-repository feature-ref workflow permissions and GitHub behavior still require actual verification; this packet has not submitted a PR or tested a remote dispatch.

The worker reads current T2380 and its pinned recovery links. It owns the live claim and must not duplicate another active run. It applies the prepared compound source and genuinely qualifies all271 default frame models plus the keeper before source commit, preserving all foreign rows. The retained genuine keeper is reusable only under its full cbc124 input identity. Defaults need actual native MASTER qualification, never predicted recipe updates.

## Native commands and honest cost

Current tools/bake.sh ALWAYS runs an embedded whole check.sh after building and derivation. It has no SKIP_CHECK input. A whole source gate takes21m21 in the latest successful Lake run and29m05 in the earlier measured failed run; it cannot fit a600-second tool call. Do not run bake.sh until timeout and report it as passed, or edit it merely to remove validation.

The existing native authoring worker can execute the existing producer/derivative owners in bounded foreground calls instead: pinned Blender generators/build.py with the272-id selection and --wrote, then actual native web-derivative batches, ordered sidecar/publication owners, all four check.sh parts and appropriate smoke parts. Those are the same native owners, not a new fake build controller. First price a small default batch, then partition any remaining work below600 seconds. Use every selected phase/version actually listed by --wrote, not an assumed count.

Historical one-asset arithmetic gave about227 seconds MASTER work and785 seconds WEB for271 defaults (~17 minutes total), not a new benchmark. After actual new MASTER parity, existing stale_derivatives.py can identify genuinely moved/underived masters; byte-identical defaults can retain their genuinely bound existing WEB bytes, provided full current model/recipe and foreign-row proofs are retained. The stock selected bake.sh always re-encodes selected WEBs, so that reuse is an explicit native-owner sequence, not a claimed stock flag.

Chicago content job worst observed checkout15m58 + latest successful gate21m21 + historical native selection17min =54m19 before setup, keeper, publication or push. Earlier gate29m05 makes62m03. Thus simply raising its cap or adding a patch input is still a separate budget decision; it does not currently fit50. Native public authoring's150 minutes removes that particular cap, but authoring, setup, native measurements, source parts, both viewport checks and hosted PR waiting still need actual budget monitoring. No completion promise is inferred from these estimates.

## Validation actually performed

Exact current main source preimages and blobs saved. External patch applies cleanly via git apply --check. YAML parses, the new target job has literal Ubuntu26.04/150 minutes, and its steps are the exact same anchored object as the full existing public worker. Existing public150/private180 caps and existing public runner label remain unchanged. Nine actual Node validator cases passed: ordinary default, two valid targets, malformed target, wrong app, unsupported worker, finish-only, multiple slots and conflicting queue ordinal. Proper600-second foreground reaper exit0, all children reaped, no cleanup. No app tests, Blender, source PR, hosted platform CI, GitHub Actions anchor server validation, remote worker or image-output qualification is claimed.

Before committing this candidate: wire the selector cases into the platform's persistent test suite, run its existing required CI locally, validate the workflow with the project's actual workflow checker, and review the native targeted scope. This is a concrete future feature PR, not an already-approved execution.
