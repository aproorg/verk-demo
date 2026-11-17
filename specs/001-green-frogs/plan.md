# Implementation Plan: Green Frogs in Bottom Corners

**Branch**: `6-green-frogs` | **Date**: 2026-11-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-green-frogs/spec.md`

## Summary

Add a green frog in each bottom corner of the frontend. Reuse the pattern from the unicorn feature (commit 70a9dd8, issue #3): two decorative, `aria-hidden`, click-through, viewport-fixed spans containing the 🐸 emoji, with the left one mirrored and a `line-height` of 1.5 (not 1) so the glyph is not clipped; both face inward. Change is confined to `web/src/App.tsx` and `web/src/style.css`.

## Technical Context

**Language/Version**: TypeScript, React (function components)

**Primary Dependencies**: Existing only (Vite, React). No new packages.

**Storage**: N/A

**Testing**: `task build` (tsc + vite build) and `task check`; manual visual check via `task dev`. The web app has no test runner and adding one needs approval (CLAUDE.md), so none is added.

**Target Platform**: Browser, 320 px phone to large desktop

**Project Type**: web application (only `web/` is touched)

**Performance Goals**: N/A (static decoration)

**Constraints**: No clicks/focus intercepted; hidden from assistive tech; no overlap with unicorns or content

**Scale/Scope**: 2 elements, ~20 lines

## Constitution Check

| Principle | Status |
|-----------|--------|
| I. Layering | Pass: no API or `fetch` changes |
| II. Tests follow behaviour | Pass, N/A: no new service/endpoint behaviour, so no pytest applies. `task check` must stay green |
| III. One API contract | Pass: no model changes, `api.ts` untouched |
| IV. Simplicity | Pass: no new packages, state or UI library; function components only |
| V. Narrow scope | Pass: only the two frontend files for this issue (#6) |
| Constraints | Pass: decorative only, no user-visible text (so no Icelandic copy needed), no real data, `aria-hidden` honours accessibility |

No violations; Complexity Tracking not needed. Re-checked after design: still passes.

## Project Structure

### Documentation (this feature)

```text
specs/001-green-frogs/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── tasks.md             # created by /speckit-tasks
```

No `contracts/`: no API or interface changes.

### Source Code (repository root)

```text
web/src/
├── App.tsx      # add two frog spans next to the unicorn spans
└── style.css    # add .frog, .frog-left, .frog-right
```

**Structure Decision**: Existing `web/` layout; edit two files, add none.
