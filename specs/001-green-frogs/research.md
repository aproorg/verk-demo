# Research: Green Frogs in Bottom Corners

## Decision: Use the 🐸 emoji in `aria-hidden` fixed spans
- **Rationale**: Identical to the accepted unicorn solution (commit 70a9dd8). No assets, no packages, naturally green, scales via `font-size`.
- **Alternatives**: SVG/PNG image (needs asset handling, more code); CSS-drawn frog (overkill); icon library (new package, forbidden without approval).

## Decision: Fixed positioning at `bottom`/`left`/`right`, `pointer-events: none`
- **Rationale**: Satisfies FR-003 and FR-004; mirrors the unicorn CSS.
- **Alternatives**: Absolute positioning (scrolls away with content, violates FR-003).

## Decision: Mirror the left frog with `scaleX(-1)`
- **Rationale**: Both frogs face inward, matching the unicorns.

## Decision: Both bottom corners
- **Rationale**: Spec assumption; singular "corner" read as a pair to mirror the unicorns.

## Decision: Small size, `line-height: 1.5`, no body padding change
- **Rationale**: Sizes similar to unicorns (2.5rem) keep content readable at 320 px. `line-height: 1` was judged too tight (clarified 2026-11-17), so 1.5 gives the emoji room. Unicorns keep their own `line-height: 1`; not touched (issue scope). Content is a short list, so overlap is unlikely; verify visually at 320 px.

## Decision: No automated web test added
- **Rationale**: No web test runner exists; adding one is a new package. Verification is `task check` plus a manual look (see quickstart.md).

All unknowns resolved; no NEEDS CLARIFICATION remain.
