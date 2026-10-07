# Stage 2 pair divergences: Text-literal initializers and value `if`/`match` end positions

- URL: https://github.com/kofun-lang/kofun/issues/1679
- Repo: kofun-lang/kofun (language: C)
- State: open; created 2026-09-24T19:00:12Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · hjosugi · 2026-09-24T19:00:12Z · https://github.com/kofun-lang/kofun/issues/1679

## Metadata

- State: in-progress
- Kind: implementation
- Area: Compiler / Stage 2 pair agreement
- Priority: P2
- Size: S
- Blocked by: none
- Consolidated: #1681 (value `if`/`match` end positions) folded in on 2026-09-26
- Audited against: #1679 on `origin/main@57600b24`; #1681 on the #1662 branch at `871da77c` (stacked on `origin/main@5d269925`). The shapes below contain no `?`, so the #1662 change does not affect them.

## Goal

Make the two halves of the canonical Stage 2 pair — the C `compiler.c` and the
Kofun `compiler.kofun` run under `bootstrap/stage2/host-driver.mjs` — agree on
the two divergence classes below, and pin each shape with a pair-agreement
fixture in an existing gate.

## Current behavior and evidence

### 1. Text-annotated binding initialised from a string literal (#1679)

The two halves disagree on a Text-annotated binding initialised from a string
literal.

```kofun
fn main() -> Int {
    let a: Text = "x"
    print(a)
    return 0
}
```

Measured on `origin/main@57600b24`:

| Half | Invocation | Exit | Output |
|---|---|---|---|
| C (`compiler.c`, `cc -std=c11 -O2`) | `kofun-stage2 --compile-outcome t.kofun t.c t.ir t.tokens` | 0 | `t.c` written |
| Kofun (`compiler.kofun` under `bootstrap/stage2/host-driver.mjs`) | `compile_file(t.kofun, tk.c, tk.ir, tk.tokens)` | 1 | `error[E2S15]: initializer type mismatch at byte 37` |

So a Stage 2 program the shipped C compiler accepts is rejected by the Kofun
source it transliterates. Found while working #1658 (PR #1677); that work also
saw six operator probes disagree the same way on `main`, and #1483 (native
self-compilation) will surface it as a behaviour change.

**Lead (not yet verified line-by-line).** The #1658 investigation points at the
Kofun `initializer_type_bounded`, which reportedly lacks the string-literal →
`Text` rule that the C half has had since #658. The next step is to confirm the
exact rule in both halves and measure every other initializer shape with a
literal operand.

### 2. value `if`/`else if`/`match` end positions (#1681)

Found while fixing a review blocker on #1662 (PR #1678). Without any `?` in the
source, the two halves disagree on where a value `if` or `match` ends.

| Source shape | C half (`compiler.c`) | Kofun half (`compiler.kofun`) |
|---|---|---|
| `let scored = match ready { … }` on an enum scrutinee | exit 0; scope-HIR visibility of `scored` = 125 | exit 1; visibility = 200 |
| a `let` initialised by an `else if` chain | visibility 51 | visibility 85 |
| `let c = if flag { 1 } else { 2 }` with `flag` a `Bool` binding | compiles | `value_if_end` crashes with "compiler index out of bounds" |

In the first row, C's `value_end` returns -1 and falls back to
`token_end(match)`, while the Kofun half measures the whole construct. These
rows come from the #1662 subagent's differential run and have not been
independently re-measured. For the enum `match` case the visibility should
cover the whole construct, which is what the Kofun half measures.

## Scope

In scope:

- reproduce each row above on current `main` in both halves and decide which
  half is right;
- fix the Kofun half's `value_if_end` crash and the end-position disagreement;
- pin every shape with a pair-agreement fixture run through both halves.

Out of scope:

- #1662's `?`-propagation rules, which have landed;
- any divergence class not listed here — file it as its own issue rather than
  growing this one.

## Acceptance criteria

- [ ] Both halves produce the same exit, diagnostic bytes, scope-HIR and
      emitted C for `let a: Text = "x"` and its value-position variants:
      `return "x"`, a `Text` argument, a `Text` comparison.
- [ ] Both halves agree (exit, diagnostic bytes, scope-HIR, emitted C) on value
      `if`/`else if`/`match` initialisers, including a `Bool`-binding condition
      and an enum scrutinee.
- [ ] The Kofun half no longer crashes on `let c = if flag { 1 } else { 2 }`.
- [ ] A pair-agreement fixture pins each shape, run through both halves (the
      canonical interpreter and the C build), in an existing gate.
- [ ] No other tracked `.kofun` source changes outcome in either half.

## Validation

| Check | Command | Expected result |
|---|---|---|
| Pair agreement, value `if`/`match` | `task else-if-chain` extended with the #1681 shapes | both halves agree on exit, bytes and scope-HIR |
| Pair agreement, Text literal | an existing Stage 2 pairing lane extended with the #1679 shapes | both halves agree on exit, bytes and emitted C |
| Full regression | `task verify` | green |

## History

#1681 was consolidated into this issue on 2026-09-26. Both were filed during
the v0.13.2-seed release queue (PR #1677 for #1679, PR #1678 for #1681) and are
known defects carried forward from `v0.13.1-seed`, not created by that range.



## Comment 5841560627

reporter (COLLABORATOR) · hjosugi · 2026-09-26T00:34:35Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5841560627

## Consolidated: #1681 folded in

Tracker correction only; no claim.

#1681 reported a second divergence class between the same two halves —
value `if`/`else if`/`match` end positions — found at the same time as this
issue's Text-literal case (both during the v0.13.2-seed release queue, PR #1677
and PR #1678). Both are `P2`, `size:S`, in the same area, and both are pinned by
the same shape of pair-agreement fixture run through both halves, so they are one
bounded artifact rather than two.

The body now carries:

- both evidence sections, with their own audited revisions (`57600b24` here,
  the #1662 branch `871da77c` for #1681);
- a single `## Scope` and one combined acceptance-criteria list;
- a `## Validation` table.
- `- Consolidated: #1681 ...` in the metadata.

State stays `needs-detail`: each #1681 row still needs reproduction on current
`main` in both halves, and the exact gate for the Text-literal fixture is not yet
chosen.


## Comment 5842241398

reporter (COLLABORATOR) · hjosugi · 2026-09-26T02:07:21Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5842241398

**Re-measured on the release commit** `8f708f0c0769413eaa33f541f9dcf5dfd2318dd6`
(`v0.13.2-seed`), so the premise is current after the release queue landed.

Source:

```kofun
fn main() -> Int {
    let a: Text = "x"
    print(a)
    return 0
}
```

| Half | Invocation | Exit | Output |
|---|---|---|---|
| C (`compiler.c`, `cc -std=c11 -O2 -Wall -Wextra -Werror -pedantic`) | `kofun-stage2 --compile-outcome t.kofun t.c t.ir t.tokens` | 0 | `t.c` written |
| Kofun (`compiler.kofun` under `bootstrap/stage2/host-driver.mjs`, `validate: () => ''`) | `compile_file(t.kofun, tk.c, tk.ir, tk.tokens)` | 1 | `error[E2S15]: initializer type mismatch at byte 37` |

The divergence is unchanged, so the issue is implementable from current `main`.

On the owner's direction I am minimising this issue's cases before starting:
the bounded artifact is the **single Text-literal reproducer above plus the one
`let c = if flag { 1 } else { 2 }` crash** from the consolidated #1681, each
pinned by one pair-agreement fixture in an existing gate. The value-position
Text variants (`return "x"`, Text argument, Text comparison), the `else if`
chain, and the enum-scrutinee `match` are recorded here and deferred until 1.0
rather than grown into this change.


## Comment 5842350897

reporter (COLLABORATOR) · hjosugi · 2026-09-26T02:24:29Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5842350897

### agent-claim:v1
- agent_id: grok-opencode-pair-divergence-1679-20260926
- status: active
- base: `8f708f0c0769413eaa33f541f9dcf5dfd2318dd6`

Taking this with the minimised bound recorded above: the single Text-literal
reproducer and the one `value_if_end` crash, each pinned by one pair-agreement
fixture. The variant matrix is deferred to 1.0.


## Comment 5842577031

reporter (COLLABORATOR) · hjosugi · 2026-09-26T02:58:37Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5842577031

### agent-claim:v1
- agent_id: grok-opencode-pair-divergence-1679-20260926
- status: pr-open
- pr: #1687
- base: `8f708f0c0769413eaa33f541f9dcf5dfd2318dd6`

**Two of the three listed classes are fixed and verified; one remains.**

Fixed, each reproduced first-hand on the release commit `8f708f0c` and then
agreed by both halves on exit, printed outcome, IR, tokens, emitted C and scope
HIR:

- the Text-literal initialiser (`initializer_type_bounded` had no
  `kind == "string"` rule);
- the `value_if_end` `compiler index out of bounds` abort on a bare Bool
  binding;
- four locals named `value_end`, initialised by calling `value_end(...)`, that
  shadowed the function and made the value `if` path abort as a use before
  initialisation once the crash above was passed.

Remaining, and why it is not in #1687: the value **`else if` chain** records a
different scope-HIR binding visibility (C `47`, Kofun `74`). The C half refuses
the chain at `--compile-outcome` with `E2S18: expected `{` after `else`` —
`parse_value_if` accepts only a block after `else` — and its scope-HIR path then
swallows that refusal and truncates the binding's visibility to the `if` token's
end. The Kofun half measures the whole chain through `value_end`. Aligning them
means teaching the C half value-position `else if` chains, which is a distinct
hemisphere of the C compiler and not the two classes this change grew from. It
stays open here rather than being closed over.

The three shapes now have pair-agreement fixtures in
`tests/conformance/result-propagation` (PR #1687).


## Comment 5843070681

reporter (COLLABORATOR) · hjosugi · 2026-09-26T04:14:14Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5843070681

### agent-claim:v1
- agent_id: grok-opencode-pair-divergence-1679-20260926
- status: active
- merged_pr: #1687
- merge_commit: `84d96cf2c9095c55dd985b76ebd26e77daa8fdc0`

PR #1687 merged. The Text-literal initialiser and the `value_if_end`
`compiler index out of bounds` abort are fixed on `main`, with three
pair-agreement fixtures in `tests/conformance/result-propagation`.

The only remaining part is the value **`else if` chain** scope-HIR binding
visibility (C `47` vs Kofun `74`), where the C half refuses the chain with
`E2S18` at `--compile-outcome` and its scope-HIR path then truncates the
visibility. The canonical Stage 2 pair is a single lock, so I am running #1660
first and returning to this.


## Comment 5847491658

reporter (COLLABORATOR) · hjosugi · 2026-09-26T15:30:56Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5847491658

**Row 2 is a feature gap, not a visibility tweak.** Investigated on `main@944eecbe`:

- The C half's `parse_value_if` accepts only a block after `else`
  (`expected `{` after `else``, `E2S18`), so a value `else if` chain refuses at
  `--compile-outcome`. Its scope-HIR path swallows that refusal and truncates the
  binding's visibility to the `if` token's end.
- The Kofun half measures the whole chain in `value_end` (scope HIR), but its
  own value-if parser also refuses `else if` at compile-outcome — so the halves
  agree on the *refusal* and differ only on the rejected program's scope HIR.
- Aligning them means teaching **both** halves value-position `else if` chains
  (parse, emit, and the scope-HIR extent), not changing one end computation.

So it is a distinct slice. The two classes this issue grew from — the
Text-literal initialiser and the `value_if_end` abort — are on `main` via
#1687 with pair-agreement fixtures. I am keeping this issue open for the chain
rather than closing over it, and will take it when the pair next frees.


## Comment 5891224630

reporter (COLLABORATOR) · hjosugi · 2026-09-29T13:25:16Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5891224630

Pair lock notice: I have claimed [#1666](https://github.com/kofun-lang/kofun/issues/1666) and hold the canonical Stage 2 pair (`compiler.kofun`, `compiler.c`, `SHA256SUMS`, `trusted_seed_sha256`) from now until it merges or is released. Your last note said you would take the value `else if` chain when the pair next frees — it is taken for #1666, then #1667 lands after it. No action needed; this is only so the pair is not taken twice.


## Comment 5916745572

reporter (COLLABORATOR) · hjosugi · 2026-09-30T17:54:53Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5916745572

Pair lock released: [#1666](https://github.com/kofun-lang/kofun/issues/1666) and [#1667](https://github.com/kofun-lang/kofun/issues/1667) have merged (`4536bb65`, `feddb49e`), so the canonical Stage 2 pair is free. The value `else if` chain on this issue is the next holder and rebases onto `feddb49e`.

## Comment 5965313725

reporter (COLLABORATOR) · hjosugi · 2026-10-03T03:58:48Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5965313725

Release window open: [v0.13.4-seed is freezing](https://github.com/kofun-lang/kofun/issues/1705) (`feddb49e`). It carries #1666 and #1667 and touches no compiler source, so **the canonical Stage 2 pair is yours** — this window does not take it. The only thing to hold is `main`: do not land a merge there until the THAW on #1705 names the final SHA and tag. Your value `else if` chain work can proceed on the pair meanwhile.

## Comment 5965702416

reporter (COLLABORATOR) · hjosugi · 2026-10-03T04:53:02Z · https://github.com/kofun-lang/kofun/issues/1679#issuecomment-5965702416

Pair lock: the HTTP C11 Stage 2 batch ([#1694](https://github.com/kofun-lang/kofun/issues/1694) onward) is taking the canonical Stage 2 pair now. Your value `else if` chain is not in this batch. If you are still active on it, say so here and I will yield the pair and rebase the batch after you; otherwise I hold it through the batch. Recorded on #1694.
