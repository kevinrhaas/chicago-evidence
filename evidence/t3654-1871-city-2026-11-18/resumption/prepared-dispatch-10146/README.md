# Historical prepared dispatcher

The frozen helper has SHA256 `10146bc0bac57d14fd9396443ac52a18a838577d1c2220ee9d477fbbf1d2d18c`. Its fixture covers four simulated positive cases and 52 refusal cases, with zero actual dispatches, external commands or repository mutations. It was prepared for either a complete hosted source result or a separately reviewed exact-tree assertion union; it does not turn an incomplete hosted aggregate into a passing aggregate.

This historical prepared version is not authorization to run on 6409. The reviewed verifier and old bindings are preserved under `../../checks/historical-871698-assertion-union/`. Any new source head requires its own explicit, reviewed bindings and fresh evidence, plus current branch/dev/run/job checks and root review of the concrete first dispatch. Do not replay existing run plans. The earlier 45b62 helper remains historical evidence in its original directory.
