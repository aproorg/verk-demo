# Quickstart: Validate Green Frogs

**Prerequisites**: dependencies installed; on branch `6-green-frogs`.

1. `task check` — expect test, lint and build all green.
2. `task dev`, open http://localhost:3000.
3. Verify against the spec:
   - A green frog is in the bottom-left and bottom-right corners; the left one is mirrored (SC-001, FR-001/002).
   - Scroll the page (add tasks if needed): the frogs stay in the corners (FR-003).
   - Click buttons/inputs near a bottom corner: they respond normally (FR-004, SC-002).
   - Inspect the DOM: frog elements have `aria-hidden="true"` (FR-005).
   - Resize to 320 px and to a wide window: no overlap with unicorns or content (FR-006, SC-003).
   - Each frog is fully visible, with no clipped edges (FR-007).
   - Create/complete a task: existing behaviour unchanged (FR-008).
