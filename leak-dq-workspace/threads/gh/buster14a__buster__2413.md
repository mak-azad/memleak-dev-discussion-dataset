# ci(windows): diagnose arena commit failure when PDB tests start in combined checks

- URL: https://github.com/buster14a/buster/issues/2413
- Repo: buster14a/buster (language: C)
- State: open; created 2026-10-02T18:31:58Z; status ok; passes main

## Issue body

reporter (MEMBER) · davidgmbb · 2026-10-02T18:31:58Z · https://github.com/buster14a/buster/issues/2413

A removed normal queue group failed a real Windows workload; this remains unresolved despite subsequent PR-head success.

Observed group `b4edcfc3c2c47cb535ce1873624bca9b955268f7`, tree `de22ce80ef62c5b283fafd0c569454f5c5af063f`, parents main `353c338398173120a36bbe18221d6ce032ec4cd3` and reader-repair head `7cf3f7a5e8620166d200be489d3bddf0991b1547`. [Buster CI37042702390](https://github.com/buster14a/buster/actions/runs/37042702390), [Windows x86-64 checks job110957105817](https://github.com/buster14a/buster/actions/runs/37042702390/job/110957105817):

```text
TEST_MODULE_TIMING ... module=codeview_tests ... passed=46748 failed=0 ... status=pass
TEST_FIXTURE_START_V1 kind=module module=pdb_tests fixture=body index=0
arena commit failed at D:/a/buster/buster/src/buster/lib/arena.c:115 in arena_allocate_commit
CI_UNIT_PROCESS_V1 group=rest workers=2 ... exit=1 native_status=1 timed_out=0 capture_failed=0 cleanup_failed=0 status=fail
```

The failure occurred at18:04:08Z; coverage/matrix publication then failed. Linux x86-64 checks was cancelled separately. [CI complete110964208451](https://github.com/buster14a/buster/actions/runs/37042702390/job/110964208451) correctly rejected workload failure/cancellation in one snapshot, with zero failed API reads. No failing PDB assertion or precise allocation request/Windows error/commit limit was emitted. Host memory exhaustion, excessive allocation, invalid commit request and resource contention are **unproved explanations**. Do not label this harmless flakiness or solve it by weakening/skipping checks.

#2396 changes five Python/workflow-reader files, with no arena/PDB/OS source edit. Comparison of that source head with b4ed adds11 main assembly/frontend/test/documentation files; arena/PDB/OS files remain unchanged. The fresh same-head [PR CI37044472621](https://github.com/buster14a/buster/actions/runs/37044472621) and [self-host37044472716](https://github.com/buster14a/buster/actions/runs/37044472716) passed, but this is a different tree/host observation and does not establish the failed group's cause or successful repaired integration.

Deduplication: bounded all-state exact-message/Windows/PDB/arena-commit issue and PR searches found our #2388/#2396 reports, historical #647 (different debug-seed allocation cause) and #691 (prefault semantics), but no dedicated owner for this current workload failure. General CI efficiency #709 and memory PR #2352 retain their own scope; no competing production memory fix is claimed.

Next action for CI/Windows allocator-test maintainers: claim a bounded diagnostic packet, retain this failed evidence, capture the actual failing allocation/arena position and bounds plus Windows commit failure reason/resource context, and reproduce against appropriate unchanged baseline and candidate on hosted correctness infrastructure. Apply a demonstrated bounded repair and run fresh full workload/group validation; success on an unrelated head is insufficient. No successor has accepted this diagnostic/repair scope. Root retains only #2396/#2312 source ownership.

Related: #2388/#2396 normal-integration acceptance and Clang campaign #2280. The current #2172 → #2173 admission hold is separate and remains in force; no queue/ruleset/authority/generated/frozen changes or local compiler/performance runs are requested or claimed.

License: Buster first-party grant remains unselected/unresolved (#621), verified from [LICENSES/README.md at353c338](https://github.com/buster14a/buster/blob/353c338398173120a36bbe18221d6ce032ec4cd3/LICENSES/README.md). No external implementation is imported.

## Comment 5962681667

reporter (MEMBER) · davidgmbb · 2026-10-02T22:48:19Z · https://github.com/buster14a/buster/issues/2413#issuecomment-5962681667

Read-only source/log investigation at main353c338: arena.c, os.c, arena_test.c and compiler/pdb/pdb_test.c are byte-identical to the retained failed b4ed group. The failure is a false arena_commit_attempt during tree2 Clang Release sanitize_on/rest/PDB; no timeout/capture/cleanup failure is reported. VirtualAlloc(MEM_COMMIT) is the Windows OS branch; prefaulting runs only after success. Immediate GetLastError, request address/size, arena bounds and contemporaneous system/process commitment were not recorded. Initial16,378MiB RAM does not establish exhaustion; the precise cause and PDB helper remain unknown.

The forced-test seam is not supported as the cause: setters are confined to arena_test.c, one-shot recovery assertions passed and intentional fatal probes run captured children. A diagnostic should still identify forced versus OS origin and capture the numeric error immediately, using nonallocating writes. Failure-only system CommitTotal/CommitLimit/page size and process commit charge would address the resource gap, without becoming a causal verdict. No diagnostic branch/code edit; no defect source owner or successor has accepted.

Fresh2396 normal group2345996f is running with no failure observed; its outcome cannot erase the original failure or prove the cause. No retry or waiver. License remains unselected per pinnedLICENSES/README.md.

## Comment 5976429577

reporter (MEMBER) · davidgmbb · 2026-10-04T04:08:42Z · https://github.com/buster14a/buster/issues/2413#issuecomment-5976429577

Claiming the bounded #2413 Windows arena diagnostic packet under the shared #1751 coordination ledger.

Owner: ROOT; sole writer on `codex/2413-windows-arena-diagnostics`, based on live main `70999b4fbec759552896d9f75a552a1ad4231490`. Refreshed issue/comments and all-state matching searches show no accepted successor or competing repair PR.

Scope: preserve the retained failed group evidence and add nonallocating failure diagnostics at the Windows arena commit boundary: distinguish forced-test versus OS failure, capture `GetLastError()` immediately, emit the requested address/size plus arena bounds/position, and record bounded Windows commit/resource context without asserting an unproved cause. Add focused seam/format coverage where the existing test architecture permits. No skipped checks, gate weakening, retry/dispatch, local compiler/runtime, benchmark, physical host, generated/frozen edit, dependency, or license change. Hosted runners provide correctness validation.

## Comment 5976515479

reporter (MEMBER) · davidgmbb · 2026-10-04T04:19:08Z · https://github.com/buster14a/buster/issues/2413#issuecomment-5976515479

Published bounded diagnostic packet as draft PR #2574.

Exact source head `9063213c8ff0a557a2e8a446aaa61eff24bb68d3`, tree `c58fcf61540ead472d7fec9b42ef90c21b914549`, parent/live main `70999b4fbec759552896d9f75a552a1ad4231490`. The uploaded tree is byte-identical to the reviewed local tree.

The patch preserves `GetLastError()` immediately after a failed `VirtualAlloc(MEM_COMMIT)`, distinguishes forced-test and OS failures, emits request/arena bounds through an allocation-free fatal reporter, and records best-effort Windows system/process commit context. The existing boolean `os_commit()` API remains unchanged for other callers and does no resource-query work on success. Registered arena coverage checks the fatal field set and native Windows error preservation.

`git diff --check` passed. Hosted validation is pending; no local compiler/build/runtime, retry/dispatch, benchmark, physical host, generated/frozen edit, gate change or dependency was used. This is diagnostic enablement, not proof of the retained failure's cause or repair; #2413 remains open. ROOT retains sole branch/review/integration ownership.

## Comment 5976525217

reporter (MEMBER) · davidgmbb · 2026-10-04T04:20:45Z · https://github.com/buster14a/buster/issues/2413#issuecomment-5976525217

PR #2574 advanced to corrected exact head `7912627a8e4257880c0727776ff567f05acdda9e`, tree `670907dd0d7b98177866623054f56fe343c900e3`. Initial hosted compile exposed and the new head fixes one `-Wconditional-uninitialized` source defect; no retry was used. Fresh checks pending; issue remains open and no root cause is claimed.

## Comment 5976667734

reporter (MEMBER) · davidgmbb · 2026-10-04T04:44:26Z · https://github.com/buster14a/buster/issues/2413#issuecomment-5976667734

PR #2574 corrected exact head `7912627a8e4257880c0727776ff567f05acdda9e`, tree `670907dd0d7b98177866623054f56fe343c900e3`, remains draft on unchanged main `70999b4fbec759552896d9f75a552a1ad4231490`. Exact-head COMMENT review `5404339156` found no source blocker. Fresh hosted census: 40 checks = 35 success + 3 intentional skip + 2 in progress, no failure; only Windows x86-64 checks and Clang analyzer aggregation remain active. Self-host fixed point/compiler regressions and every native/release lane are green. PR identity text was corrected to the current head/tree. No retry/dispatch, local compiler/runtime, queue action, generated/frozen edit, gate change, physical host, or dependency. #2413 remains open because this packet adds evidence, not a proven causal repair.

## Comment 5976761854

reporter (MEMBER) · davidgmbb · 2026-10-04T05:00:17Z · https://github.com/buster14a/buster/issues/2413#issuecomment-5976761854

PR #2574 exact source head `7912627a8e4257880c0727776ff567f05acdda9e`, tree `670907dd0d7b98177866623054f56fe343c900e3`, completed ready-state validation and entered the protected queue at 2026-10-04T04:59:18Z. Exact merge group `285dec38e442d7d16a9a5581d8251fde1e0fd31e` has the same reviewed tree and parents unchanged main `70999b4fbec759552896d9f75a552a1ad4231490` + source head. Initial group census: 30 checks = 5 success + 3 skip + 22 in progress, no failure. Exact-head review `5404339156` has no blocker. ROOT retains sole integration ownership; no source push while queued, direct merge, retry/dispatch, local compiler/runtime, physical host, generated/frozen edit, gate change or dependency. #2413 remains open because this packet is diagnostic enablement, not a causal repair.

## Comment 5977680894

reporter (MEMBER) · davidgmbb · 2026-10-04T07:24:37Z · https://github.com/buster14a/buster/issues/2413#issuecomment-5977680894

Protected group `285dec38e442d7d16a9a5581d8251fde1e0fd31e` was correctly removed after the Android x86-64 job `111366299292` stopped communicating during `Test (Android)`. Aggregate job `111373119166` classified it as `runner-communication-lost`: last progress `2026-10-04T05:00:48Z`, finalized `05:47:45Z`, `2817.0` seconds silent. The direct job-log endpoint now returns `404 BlobNotFound`; the aggregate retained the classification and rejected mobile admission.

All other terminal group contexts were 37 success / 3 intentional skip. That is not a source-causality proof in either direction. The infrastructure incident is now separated as #2575. No source edit, retry/dispatch, generated/frozen change, dependency, or gate change was made. PR #2574 remains open on head `7912627a8e4257880c0727776ff567f05acdda9e` / tree `670907dd0d7b98177866623054f56fe343c900e3`; #2413 remains open for the underlying Windows arena failure.

## Comment 5977690838

reporter (MEMBER) · davidgmbb · 2026-10-04T07:26:10Z · https://github.com/buster14a/buster/issues/2413#issuecomment-5977690838

Fresh protected admission created after separating the prior Android runner-loss incident to #2575. New exact merge group `5c6151133dd63c4f9352b0b93f3bac576e7d94be` preserves tree `670907dd0d7b98177866623054f56fe343c900e3` and ordered parents unchanged main `70999b4fbec759552896d9f75a552a1ad4231490` + reviewed source `7912627a8e4257880c0727776ff567f05acdda9e`.

This is a new normal protected queue group, not a workflow dispatch or failed-job retry. ROOT retains sole integration ownership; no source push while queued, direct merge, local compiler/runtime, physical host, generated/frozen edit, dependency, or gate change. #2413 and #2575 remain open.

## Comment 5978384739

reporter (MEMBER) · davidgmbb · 2026-10-04T09:08:40Z · https://github.com/buster14a/buster/issues/2413#issuecomment-5978384739

#2413 diagnostic packet complete through protected integration: PR #2574 merged at `2026-10-04T07:54:48Z` as exact group/main commit `5c6151133dd63c4f9352b0b93f3bac576e7d94be`, tree `670907dd0d7b98177866623054f56fe343c900e3`, parents prior main `70999b4fbec759552896d9f75a552a1ad4231490` + reviewed source `7912627a8e4257880c0727776ff567f05acdda9e`. The replacement protected admission completed and GitHub merged it; no direct merge, workflow dispatch/retry, local compiler/runtime, physical host, generated/frozen edit, dependency, or gate change was used.

Current main has since advanced to `94976eccad9c31776cf264a33dcda960dd8ed51a`; its first parent is `5c6151133dd63c4f9352b0b93f3bac576e7d94be`, so the integrated tree is retained. ROOT releases the #2574 branch/integration claim. Issue #2413 remains open because diagnostics are enablement, not a causal repair; the separate Android runner-loss incident remains #2575.
