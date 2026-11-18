# Historical supporting CI at 8d59

These logs and final metadata bind source commit `8d59e79cd657f58f483533246973e0e1c00ebf51`; they are not a complete source gate or a current `1dfe13b` acceptance result.

- Run 44379109448 completed successfully: moving-frames job 135066171098 passed its frame ceilings, and upload-release job 135066171928 passed 32 checks. Both job logs and completed workflow metadata are preserved.
- Source run 44379109373 has completed job logs for part 1/8 (176 steps, none red), part 8/8 (174 steps, none red), and part 2/8 (176 steps, one real failure: the stale three-destination Navigator expectation). That expectation is repaired in the later focused checkpoint. The earlier supersession metadata records five other parts cancelled and the aggregate gate job still queued. The later final metadata records the whole workflow cancelled after an authorized administrative cancellation of that obsolete queued aggregate, once all eight parts were finalized, to unblock the corrected commit. Before-state/job metadata and the HTTP 202 response are preserved. This aggregate cancellation does not erase the actual part 2 assertion failure.
- Portable-humans run 44379109304 is recorded as cancelled after the new head. Its metadata is retained; no passing result is invented.

The historical source-job failure remains a failure even when other jobs or the parent workflow were later cancelled. See `../../repairs/navigator/checks.log` for the focused repair result.
