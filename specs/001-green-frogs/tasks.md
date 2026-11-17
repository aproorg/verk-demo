# Tasks: Green Frogs in Bottom Corners

**Input**: `/specs/001-green-frogs/` (plan.md, spec.md, research.md, data-model.md, quickstart.md)
**Tests**: None added. The web app has no test runner and adding one needs approval (CLAUDE.md). Verification is `task check` plus the manual steps in quickstart.md.
**Branch**: `6-green-frogs`. Never commit on `main`. Code and identifiers in English.

## Format: `[ID] [P?] [Story] Description`

Setup and Foundational phases are empty: no new packages, models or API changes (`api/` and `web/src/api.ts` stay untouched). Only `web/src/App.tsx` and `web/src/style.css` change.

---

## Phase 1: User Story 1 - See decorative frogs in the bottom corners (Priority: P1) 🎯 MVP

**Goal**: A green 🐸 is visible in the bottom-left and bottom-right corners, fixed to the viewport while scrolling.

**Independent Test**: `task dev`, open http://localhost:3000, confirm a frog in each bottom corner (left one mirrored), and that both stay in place when scrolling.

- [X] T001 [P] [US1] In `web/src/style.css`, directly after the `.unicorn-right` rule, add `.frog { position: fixed; bottom: 0.5rem; font-size: 2.5rem; line-height: 1.5; pointer-events: none; user-select: none; }`, `.frog-left { left: 0.5rem; transform: scaleX(-1); }` and `.frog-right { right: 0.5rem; }`. Use `line-height: 1.5`, not 1 (FR-007). Do not touch the `.unicorn` rules.
- [X] T002 [P] [US1] In `web/src/App.tsx`, directly after the two unicorn spans inside `<main>`, add `<span className="frog frog-left" aria-hidden="true">🐸</span>` and `<span className="frog frog-right" aria-hidden="true">🐸</span>`, formatted like the unicorn spans.

**Checkpoint**: Both frogs render in the bottom corners and stay put on scroll.

---

## Phase 2: User Story 2 - Frogs never get in the way (Priority: P2)

**Goal**: Frogs never block clicks, focus, screen readers, unicorns or content.

**Independent Test**: Click controls near the bottom corners; inspect DOM for `aria-hidden="true"`; resize to 320 px and wide.

Most of US2 is delivered by T001/T002 (`pointer-events: none`, `aria-hidden`). This phase verifies it.

- [X] T003 [US2] Run `task dev` and verify per quickstart.md: controls near the bottom corners respond to clicks (FR-004, SC-002); frog spans have `aria-hidden="true"` (FR-005); at 320 px and on a wide window the frogs do not overlap the unicorns or make content unreadable, and no frog is clipped (FR-006, FR-007, SC-003). If content is covered at 320 px, reduce `.frog` `font-size` in `web/src/style.css` (e.g. `2rem`); do not add body padding.

---

## Phase 3: Polish

- [X] T004 Run `task check` (test, lint, build) from the repo root; all must be green (FR-008, SC-004). Run `task format` if lint complains about formatting.
- [X] T005 Confirm `git diff --stat` shows only `web/src/App.tsx` and `web/src/style.css` (plus `specs/`), per issue scope.

---

## Dependencies & Execution Order

- T001 and T002 touch different files: parallel.
- T003 needs T001 and T002 (US2 verifies US1's output).
- T004 and T005 come last.

```text
T001 ─┐
      ├─► T003 ─► T004 ─► T005
T002 ─┘
```

## Implementation Strategy

MVP is US1 (T001 + T002): that is the whole visible feature. US2 and Polish are verification only, so the full feature is five small tasks.
