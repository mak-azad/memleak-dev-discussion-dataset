# test(chaos): induce-to-detect e2e for each chaos scenario

- URL: https://github.com/optiqor/kerno/issues/150
- Repo: optiqor/kerno (language: C)
- State: open; created 2026-05-31T00:43:23Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · btwshivam · 2026-05-31T00:43:23Z · https://github.com/optiqor/kerno/issues/150

the induce-detect-explain loop is the product's core promise and nothing tests it end to end. each scenario in `internal/chaos` already declares a `PairedRule()` (cpu to scheduler_contention, disk-sat to disk_io_bottleneck, fd-leak to fd_leak, tcp-loss to tcp_retransmit_storm, memory to oom_imminent, cgroup-memory to memory_limit_pressure), but there's no test that actually induces a scenario and confirms the paired rule fires.

propose: a privileged integration test (real `ebpf` build) that, per registered scenario, induces it inside the container, runs the doctor cycle, and asserts a finding with the declared `PairedRule()` is present. iterate over the registry so a new scenario is covered automatically, and skip `cascade` (paired rule "multiple") or assert its component rules. this is the regression net for the whole detection path.

depends on the harness (#143), needs the privileged/BTF setup from #148. distinct from the 24h soak in #38, this is per-scenario correctness, not endurance.

## Comment 4618348172

other (NONE) · github-actions[bot] · 2026-06-04T02:10:20Z · https://github.com/optiqor/kerno/issues/150#issuecomment-4618348172

Assigned to @Yogender-verma. Thanks for picking this up! 🚀

**Heads-up**: if there's no activity (comment or PR linked here) within **10 days**, the issue will be auto-released so others can pick it up. Comment any time to reset that timer.

Need help getting started? Check [CONTRIBUTING.md](https://github.com/optiqor/kerno/blob/main/CONTRIBUTING.md) or ask in the issue thread.

## Comment 4679008769

other (NONE) · github-actions[bot] · 2026-06-11T09:14:02Z · https://github.com/optiqor/kerno/issues/150#issuecomment-4679008769

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 4787306878

other (NONE) · github-actions[bot] · 2026-06-24T08:24:11Z · https://github.com/optiqor/kerno/issues/150#issuecomment-4787306878

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 4901686088

other (NONE) · github-actions[bot] · 2026-07-07T08:24:43Z · https://github.com/optiqor/kerno/issues/150#issuecomment-4901686088

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 4916949501

other (NONE) · Yogender-verma · 2026-07-08T16:26:41Z · https://github.com/optiqor/kerno/issues/150#issuecomment-4916949501

see #231 

## Comment 5010325997

other (NONE) · github-actions[bot] · 2026-07-18T07:00:28Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5010325997

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5077476732

other (NONE) · github-actions[bot] · 2026-07-25T07:19:36Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5077476732

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5150413662

other (NONE) · github-actions[bot] · 2026-08-01T07:28:27Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5150413662

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5230017149

other (NONE) · github-actions[bot] · 2026-08-09T05:47:54Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5230017149

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5312265101

other (NONE) · github-actions[bot] · 2026-08-17T05:36:18Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5312265101

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5391175284

other (NONE) · github-actions[bot] · 2026-08-24T05:39:45Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5391175284

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5477622822

other (NONE) · github-actions[bot] · 2026-08-31T11:25:53Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5477622822

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5582631396

other (NONE) · github-actions[bot] · 2026-09-08T09:25:26Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5582631396

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5678142603

other (NONE) · github-actions[bot] · 2026-09-15T09:49:17Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5678142603

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5792633356

other (NONE) · github-actions[bot] · 2026-09-23T09:48:06Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5792633356

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.

## Comment 5909818408

other (NONE) · github-actions[bot] · 2026-09-30T10:59:00Z · https://github.com/optiqor/kerno/issues/150#issuecomment-5909818408

<!-- kerno:stale-claim-warning -->
Hi @Yogender-verma — heads up that this issue has had no activity from you in **7 days**.

If you're still working on it, leave a comment and the timer resets. Otherwise it'll be auto-released in **3 days** so others can pick it up.

Need help getting unstuck? Reply here, no judgement.
