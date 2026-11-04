# V3: correct the new Light test's unsupported reason requirement

Runtime is byte-identical to V2. No production consumer requires an approach
reason after Light restoration. Existing serialization saves stopped state,
identity, path and wheels; the restored diagnostic reason is null.

Only new tests change. Initial cold admission still must report approach before
publication. Restored Light actors must report null while strongly preserving
stopped identity, actual pose, path distance and wheel angles. Blocked Continue
must fail; clear Continue resumes the same actor. The composed actual-adapter
test checks first restored visual frame zero, next frame +.125, and first
Continue journey frame zero with independent stopped looking preserved.

The original combined V2 failure remains immutable. No original tests/assertions
or runtime behavior changed. Rerun only test_driven_assembly after separate Root
GO; transport_loop and all runtime bytes are unchanged from the passed receipt.
No APP writes, test execution, browser work or canonical lock use occurred here.
