# Redundant 6409 bake cancellation

The hosted warrant for run44421752948 lacked NumPy and could not recompute an input hash. Its warrant step succeeded by requesting a bake. A separate supported read-only decision on clean6409/basec676 with NumPy2.3.5 returned0: all1,126 committed assets matched their inputs, with zero stale assets.

Root reviewed that evidence and authorized cancellation of only this redundant bake. The saved API response is HTTP202, and final metadata records cancellation of the bake and dependent fanout. No generated output was accepted. Current source/supporting validation and unrelated workflows were untouched. This cancellation provides no source, browser or merge acceptance.
