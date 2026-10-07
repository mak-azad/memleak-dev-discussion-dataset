# [M7.4] Leaks and Use-After-Free

- URL: https://github.com/johnatorres226/foundations-of-programming-c/issues/55
- Repo: johnatorres226/foundations-of-programming-c (language: HTML)
- State: open; created 2026-09-13T00:19:28Z; status ok; passes main

## Issue body

reporter (OWNER) · johnatorres226 · 2026-09-13T00:19:28Z · https://github.com/johnatorres226/foundations-of-programming-c/issues/55

**Blocked by:** #25
_Indirectly, through the above:_ #1 · #2

**Module 7 — Dynamic Memory** · **Chapter 7.4** · Difficulty ●●● · Exercises: 4 · One sitting (~1 hour) · Agent: Sonnet

## Outcome — from SYLLABUS.md
On finishing this chapter, the learner can: **Reproduce a leak and a use-after-free, then find both with AddressSanitizer**

## Context for a cold start
- **Recap source.** Previous chapter **7.3 Ownership** — declared outcome: "State who is responsible for freeing a pointer, and design functions with a clear ownership contract"
- **Zoom Out target.** Next chapter **8.1 How Memory Is Laid Out** — declared outcome: "Describe text, static, stack, and heap regions and say where any given variable lives"
- Write the Recap against that *declared outcome*, never against the neighbouring chapter's prose — that is what lets chapters be written in parallel (PRD §3).

## Files
| Path | |
|---|---|
| `src/modules/7-module-dynamic-memory/4-chapter-leaks-and-use-after-free/tests/` | written **first**; layout per #1 |
| `src/back-of-the-book/module-7/` | reference solutions + `ANSWERS.md`; layout per #1 |
| `src/modules/7-module-dynamic-memory/4-chapter-leaks-and-use-after-free/exercises/` | learner stubs |
| `src/modules/7-module-dynamic-memory/4-chapter-leaks-and-use-after-free/exercises/HOMEWORK.html` | copy `.claude/templates/homework-template.html`; bridges chapter to exercises (PRD §9); asset paths → `../../../../../assets/` |
| `src/modules/7-module-dynamic-memory/4-chapter-leaks-and-use-after-free/CONTENT.html` | copy `.claude/templates/chapter-template.html`; asset paths → `../../../../assets/` |
| `src/modules/7-module-dynamic-memory/4-chapter-leaks-and-use-after-free/QUIZ.html` | copy `.claude/templates/quiz-template.html`; edit only the JSON |
| `src/modules/7-module-dynamic-memory/4-chapter-leaks-and-use-after-free/README.md` | flip status to ✅ |

## Work order — TDD, in this order (PRD §9)
1. [ ] **Tests** — 4 exercises, `assert`-based, together proving the outcome above. They fail against the stubs.
2. [ ] **Reference solution** — passes `make check`.
3. [ ] **Exercise stubs** — compile clean under `-Werror`; fail the tests until the learner finishes them.
4. [ ] **Prose** — `CONTENT.html` (six sections, chapter table of contents in the header), `exercises/HOMEWORK.html` (one part per exercise, linking back to the `.how` subsection it exercises), `QUIZ.html` (a `why` on every option), chapter `README.md`.

## Definition of done (PRD §13)
- [ ] Tests written before the solution (enforced per #2)
- [ ] Six sections in order: Recap → Big Picture → Core Idea → How It Works → Try It → Zoom Out
- [ ] `.chapter-toc` in the header, right after `<h1>`, nesting How It Works' subsections, plus a final Homework → entry if this chapter has one (PRD §3)
- [ ] `exercises/HOMEWORK.html` present, copied from the template, one part per exercise, each linking back to its `.how` subsection — the full solution stays in back-of-the-book, not here (PRD §9)
- [ ] Core Idea is **one sentence**
- [ ] Recap is 2–3 sentences, written against the declared outcome above
- [ ] Every quiz option has a `why`; back-of-the-book holds correct answers + reasoning only
- [ ] Every new term defined on first use; no banned words
- [ ] Citations respect the tiers; every URL checked live
- [ ] Opens from `file://` with wifi off; readable at phone width
- [ ] **About one sitting.** If it won't fit, propose a continuation chapter instead of overflowing (PRD §5)
- [ ] Word count in the PRD §5 depth band (3,500–5,200 across Big Picture + How It Works + Zoom Out), or a documented reason if not
- [ ] Footer feedback link title is `[M7C4]`
- [ ] `make check` and `make lint` pass; CI green
- [ ] No `CHANGELOG.md` or module `README.md` edits here — per CONTRIBUTING.md § Git workflow (the actual resolution of #2), those update once when the whole module's chapters close, not per chapter

## Rules that bite
- **Readability: 6th grade.** Short sentences. Define every term on first use. Never "simply", "just", "obviously", "of course", "as you know". (PRD §4)
- **Offline.** Renders from `file://` with wifi off. No CDN, no web fonts, no network. (PRD §2)
- **Code:** `-std=c17 -Wall -Wextra -Werror`, sanitizers on, `clang-format` clean. Every shown example compiles as shown. (PRD §8)
- **Citations:** cite, never mirror. learn-c.org, CS50x (Week 1), cppreference from Module 1. **Beej's Guide only from Module 6.** *Modern C* is CC BY-NC-ND — link only. Check every URL is live. (PRD §7)
- **No saved state.** No `localStorage`. (PRD §2)
- **Diagrams required.** Inline SVG by default (`currentColor`, labelled, dark-mode safe). This is where learners quit.

