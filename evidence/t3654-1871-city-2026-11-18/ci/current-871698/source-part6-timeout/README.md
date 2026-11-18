# Current hosted source part 6/8: timeout and refused retry

Run 44407494538/job 135167297084 names head 871698. Its completed log checks out bd8bbfdff8f2575f1d7437be255f6617509ce6fc, the merge of task 871698 with dev 169404. The source command reaches the 600-second limit and exits 124 without a final gate verdict. It supplies no passing source coverage; unfinished buffered worker results remain unknown.

The measured command interval is 170.970848 seconds before the publication pool, 95.211237 seconds for publication, and 333.837256 seconds of unfinished post-publication work until timeout (600.019341 seconds total). The 266.182085-second start-to-publication endpoint includes both early phases; it is not publisher duration. Completion would require further time after the observed 333.84-second post-publication interval.

The preserved comparison is the earlier 3f81 part 6/8 pass in 362.456125 seconds. check.sh, runner image, Python 3.11.18 and CHECK_JOBS=4 match, but inputs differ: upstream roofs and source/boot/trace repairs changed. Earlier timing therefore supports a bounded retry investigation, not a guaranteed fit or identical-input performance comparison. CI did not enable CHECK_TIMINGS; no specific unfinished post-publication tool can be blamed from the buffered log.

Root authorized one bounded retry, and the actual API request was refused 403 because sibling jobs were still running. Before-run/job metadata and the unmodified refusal response are retained. **No retry was launched by that request.** Wait for the sibling completion boundary, then reconcile actual run state and that one-retry limit; never treat the refused request as a completed rerun.
