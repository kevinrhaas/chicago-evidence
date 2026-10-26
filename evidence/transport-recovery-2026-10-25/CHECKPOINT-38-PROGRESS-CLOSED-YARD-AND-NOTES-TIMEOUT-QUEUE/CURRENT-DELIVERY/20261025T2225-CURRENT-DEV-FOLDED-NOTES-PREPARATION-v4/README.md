# Notes observer v4 — normal inherited-proxy build probe, UNRUN

The first actual D3 notes attempt closed1/cleanup0. Both contexts stopped BEFORE navigation/UI at Playwright APIRequestContext.get(build.json), with DNS EAI_AGAIN, zero UI actions and no page errors. The original report and frozen V3helper6952 remain unchanged. Root’s normal inherited-proxy curl health and HTTP14 calls succeeded; this was an instrument route/setup issue, not observed app or visual failure.

V4 changes ONLY publicBuild(page). It calls normal curl via execFileSync with the inherited environment/proxy/CA, --no-insecure, --proto '=https', no-location/max-redirs0, Cache-Control:no-cache, connect20/max60. It requires exit0, actualHTTP200 and exactraw equality with the retained official build bytes. Each call saves unique official-build-NN body, headers, rawstatus, bytes/hashes and command/outcome JSON. No browser proxy override, direct-route override or TLS bypass is introduced.

EVERYotherbyte is unchanged from V3: exact actualdeployed fullD/input/review hash CLI, native source/Git/HTTP14 checks, externalM/foldfouritems, native14 registry/message policy, actualresponsiveDEVidentity, normal trusted About/news path, bothwidth100140, screenshots, allpage/console/request/HTTPerror checks and bodytasks AFTERcontext/browserclose. The result schema stays observationalv3 intentionally; the helper path/hash identifies this V4 instrument correction. No app/source/assertion changes.

ROOT alone may review/syntax-check then run ONCE, sequentially after other browser jobs close. Root should first confirm the retained actual D3build still serves; a changed build is a preserved stop/newinput preparation, never ignored. Suggested fresh concrete invocation:

```sh
source /workspace/.cloud-setup/transport-activate.sh
python3 /workspace/.cloud-setup/transport-supervise.py --prefix /workspace/.cloud-setup/logs/transport-recovery/deployed-D3-folded-notes-proxy-observation2 --cwd /workspace --timeout 1800 -- node /workspace/.cloud-setup/logs/transport-recovery/20261025T2225-CURRENT-DEV-FOLDED-NOTES-PREPARATION-v4/observe-current-dev-folded-notes-v4.mjs --execute-current-dev-notes-observation --expected-deployed-head 9f7a31e35864e6ff7af221c5089b90c5160441d8 --input-binding /workspace/.cloud-setup/logs/transport-recovery/current-deployed-D3-NOTES-INPUTS/INPUT-BINDING.json --input-binding-sha256 ab134adc3ddf638eeeab9eae959e8af32ae66de4fbd416500872c3bf7e50377c --review-contract /workspace/.cloud-setup/logs/transport-recovery/current-deployed-D3-SELECTED-HTTP/REVIEW-ANNOTATIONS-INPUT-BINDING.json --review-contract-sha256 abdb0c32be56ea1d9acfaa2460420758034cc486cdbdedb0c295463de907e7fa --out /workspace/.cloud-setup/logs/transport-recovery/deployed-D3-folded-notes-proxy-observation2-output
```

The input generator remains unchanged at V3. This preparation ran no helper, browser, curl/network, import/syntax or primary Git command. Actual screenshots still need ROOT visual review.1800s is an operational cap, not a600s budget claim.
