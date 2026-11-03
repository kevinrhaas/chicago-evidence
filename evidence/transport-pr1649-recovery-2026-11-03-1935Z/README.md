# PR 1649 recovery checkpoint, 3 November 2026

This preserves an **uncommitted** integration of public PR head `ae762df51dad3bd48e7d5307e0bda3cd0ce05e31` and reviewed DEV `073a337e4ed89b362469246c1c5aa927c70975cd`, followed by the exact-bounds cache proposal. No app commit, DEV merge, full gate pass, or broad-ticket completion is claimed.

The actual Chromium 141 native 1904 mobile memory gate **failed**: 422071758 bytes against 419430400 bytes. Original publish/check/memory transcripts, source bindings, resource checks and child cleanup are preserved. The CPU bounds controls passed their original 5-second caps; they do not replace the failed scene-memory gate. Derived-owner and Mayer repair receipts describe their own earlier integration source without retargeting them to a later source.

`SOURCE-SNAPSHOT/TREE.ls-tree.z.gz` records every tracked path, mode and object. Only blobs absent from the union of the two public parents are included in `novel-blobs/`; incoming models already in those parents are not duplicated. `RECOVERY-RECIPE/recover_tree.py` reconstructs and verifies the exact Git tree without changing a checkout or index. Its actual isolated-repository roundtrip result is included.

`RUNTIME-AND-INTEGRATION/` preserves helpers and the fresh resource epoch. The helpers contain explicit old/current source, path, browser and baseline assumptions; review those before reuse after any environment restart. No execution plan or preparation file is a passing result.
