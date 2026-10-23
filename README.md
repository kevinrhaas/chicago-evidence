# chicago-evidence

Bulky work evidence for 4D Chicago (kevinrhaas/chicago): checkpoint folders, tar/zip
snapshots, gate and smoke transcripts, solver dumps and screenshot runs.

It lives apart from kevinrhaas/chicago-tickets because every gate and steward run
clones the tickets repo, and this material had grown it by 2.4 GB in five days
(chicago-tickets T-3071, 2026-10-23). Nothing in CI clones this repository.

- Layout: `evidence/<topic>-<date>/…`, the same paths these folders had under
  chicago-tickets `evidence/`, so a ticket citing `evidence/<folder>/…` resolves here.
- The seven folders here were copied from chicago-tickets at commit 3be79684. Their
  earlier history stays in that repository.
- Small text research a tool reads (the T-1837 frontage register) stays in
  chicago-tickets `evidence/`.
- Keep single files under 50 MB (GitHub warns above 50 MB and refuses above 100 MB);
  split a larger archive.
