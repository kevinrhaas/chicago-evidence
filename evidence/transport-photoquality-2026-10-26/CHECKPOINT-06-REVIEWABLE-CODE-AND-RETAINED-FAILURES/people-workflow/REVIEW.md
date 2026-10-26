# External T1789 registered-workflow patch

This packet is a review proposal, not an application commit. Base is exact checked/pushed `1cbb1817508593562f99ed378b6932368b5699b9`. Only `.github/workflows/chicago-4d-humans.yml` appears in `APPLICATION.diff`; the complete proposed YAML is `chicago-4d-humans.yml`. The application checkout and index remain clean. No package install, source publish, BPy/browser execution, workflow dispatch or blocked artifact fetch occurred.

The existing workflow is already registered. This proposal avoids requiring a new default-branch workflow registration or a main promotion. Adopt through the required interactive owner-visible PR and normal feature/dev review; no adoption or remote execution is authorized by this packet. PR1346 is the existing source-review surface.

## Exact change

Add default-false `build_dress_study`, default-empty `source_ref`, a precheckout request guard, conditional same-source fixture checkout/binding, and a separately gated dress job depending on the existing full fixture job. The only executable study source allowed is checked1cbb. Invalid/ref-injection or mixed male/seated+dress requests fail before study checkout. Non-dress default, PR and push checkouts retain the original action. All original fixture setup/byte/browser/actor command steps are unchanged. The entire original male job is unchanged structurally except the already accepted T3169/PR1339 Ubuntu24.04 runner repair; its exact accepted comment/change is included explicitly because1cbb predates that fix. No male recipe, variant, seated behavior or male artifact path changed. Existing permissions, triggers and concurrency are unchanged.

Both study source checkouts disable persisted credentials. No secrets, write permissions, arbitrary repository or arbitrary command/path input are added. The fixture job exports its actual verified source SHA; the dress job checks out and independently verifies that exact SHA, records workflow-definition SHA/ref separately, and hashes its actual source inputs. Existing cache pins and normal export gates remain in use. The exact-source allowlist must be changed through review for any later source revision; it is not a general unreviewed-source executor.

The new fixed variant is `flynn_mary_1835_dress_study`, recipe `adult_dress_1835.json`, umbrella LibertyL418 plus unchanged component Liberty metadata, master under `assets/authored/humans/dress/`. Normal native4.5.3 source preparation/reproduction, normal diagnostics/readback, exporter/contracts, hierarchy control, all eight raw/web LOD validators, fresh measurements, publisher and both-viewport source/published/contact/frame checks remain mandatory. The job refuses existing target master/exports. It saves only successfully refreshed measurement proof; failed jobs can upload partial files and preserve failure logs, without attaching the carried stale measurement file as new evidence. Artifact filenames/manifest identify the actual source and actual output bytes. No seated/driver qualification or production placement is added.

## Validation actually performed

`SOURCE-BOUND-VALIDATION-MATRIX.json` binds the base file, proposed YAML and exact patch hashes. It records normal `git apply --check`, actual native runner checker results, original job/default preservation comparisons, PyYAML parse with the `on` key preserved, shell syntax and inline Python/JS syntax checks, and14 actual executions of the proposed request-guard code, including malformed/mixed/injected/ref cases. Input cases execute only the request validator, not workflow jobs. Listed expected job graphs are static condition analysis.

Actionlint is unavailable and was not installed. GitHub's service-side workflow schema/expression evaluation has not run. Root still needs normal native workflow/owner validation and full required checks on any adopted source commit before commit/push/dispatch. Browser/master/export/photo gates remain unexecuted for this proposed job and new female source.

After reviewed adoption on the dispatch ref, an explicit future request would be:

```
gh workflow run chicago-4d-humans.yml --ref dev \
  -f build_dress_study=true \
  -f source_ref=1cbb1817508593562f99ed378b6932368b5699b9
```

The unchanged workflow concurrency group cancels in-progress runs on the same ref. Check that no run should be preserved before any later authorized dispatch. Generation would not apply the still-pending artifact-host policy or make blocked downloads available. Keep canonical/photo acceptance, dress walk/seated fit and T1789 OPEN.
