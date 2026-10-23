Read-only claim audit: PASS with one stale queue comment.
Actual remote main `de4a5f2da24cfb3b7ff8578948ff1e55520ad56c`; local clean checkpoint `08064c143d8e3adb6b057c5af1c5187943347346` was three unrelated ticket commits behind. Exact pushed QUEUE/HANDOVER copies and remote comparison are preserved; none of the eleven audited ticket files changed.

| Ticket | Taken UTC | Renew before UTC |
|---|---|---|
| T-1789 | 17:20:12.133Z | 20:20:12.133Z |
| T-2794 | 17:20:16.071Z | 20:20:16.071Z |
| T-2800 | 17:20:19.754Z | 20:20:19.754Z |
| T-2980 | 17:20:23.417Z | 20:20:23.417Z |
| T-2803 | 16:57:01.550Z | 19:57:01.550Z |
| T-2795 | 16:57:06.087Z | 19:57:06.087Z |
| T-2796 | 16:57:10.959Z | 19:57:10.959Z |

All seven are claimed, live at audit, independently root-owned, manual claimed_run:null, group:null. Renewal is required BEFORE each instant: tool considers age>=3h dead. Null Actions URLs are valid manual claims; the pushed ticket commit is the lock. Group size rules concern one explicit group/PR, not these seven independent parallel claims.

T2792, T2799, T2979 and T2981 remain DONE for PR1174, closed2026-10-22T04:16:26Z; none has an active queue row. Their old claimed timestamps are history, not expiring active leases. The latest19:00HANDOVER keeps broad photographic/idle-world/gait/harness/driver/riding work open.

Minor correction: pushedQUEUE line176 still says T2792/T2799 begin in parallel. Replace with factual completed1174 research note without moving entries. Dated old ticket premerge paragraphs may receive an appended final closure note; preserve original failures/history.

Root owns any FF/renew/release/sync. This audit performed no canonical Git/app/ticket writes, no full gate and no browser.
