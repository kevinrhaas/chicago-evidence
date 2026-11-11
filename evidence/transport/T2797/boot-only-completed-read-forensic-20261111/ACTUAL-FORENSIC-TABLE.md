HTTP200 and complete data/EOF coexist with CDP failure in this instrumented forensic cell. Original six failures remain NONPASS; internal owner remains unknown.

| CDP ID | Fetch / reader | HTTP | Content-Length / CDP data / native EOF | Source SHA | Saved line EOF → failure |
|---|---|---:|---|---|---|
| 1965742.834 | fetch:29 / reader:43 | 200 | 474250 / 474250 / 474250 | 1d1dd60640643a53c7994f1b83aa4646a956eb63050d0054b9e1e3918030c29d | 5191 → 5192 |
| 1965742.835 | fetch:31 / reader:47 | 200 | 170195 / 170195 / 170195 | 280791f90fa8fda0244ceaf2ecf35f45e157bee8fd6d2631934d4e02cec909f3 | 5196 → 5197 |

Full URLs, native/CDP timestamps and uncorrelated synthetic buffer IDs are in ACTUAL-FORENSIC-TABLE.json. No client SHA was measured.
