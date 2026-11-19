# Current partial-proof refusal snapshot

The frozen dispatcher SHA256 is `9c8aa1fbceb42830f9671d98eb0fcaa6adc09f736d4ca15b579e782e7e9f78f7`. Its prepared plan is a dated recovery record. Four simulated positive cases and 53 refusal controls run without actual dispatches or external commands. A separate authorization-only call on the real incomplete 6409 proof correctly refuses: only 175 of 1,379 declarations are covered. That refusal leaves the ledger unchanged and launches no workflow.

The explicit empty and partial bindings, raw evidence and reviewed verifier are mapped under `../../checks/source-6409-part6/`. The exact head/tree/base/run identity, fresh coverage and live job state must still be checked for any later proposal. This snapshot does not authorize browser dispatch or merge, and it does not rewrite the canonical hosted gate as green.
