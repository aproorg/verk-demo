# Feature Specification: Green Frogs in Bottom Corners

**Feature Branch**: `6-green-frogs`

**Created**: 2026-11-17

**Status**: Draft

**Input**: User description: "I want green frogs in the bottom corner of the frontend"

## Clarifications

### Session 2026-11-17

- Q: Is the frog's tight line spacing (line-height 1) acceptable? → A: No, give it more room. Use a larger line-height (1.5) so the frog is not clipped or cramped.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - See decorative frogs in the bottom corners (Priority: P1)

A person opens the app and sees a green frog illustration in each bottom corner of the screen, giving the page a playful look, matching the existing decorative unicorns in the top corners.

**Why this priority**: This is the entire feature; the frogs are purely visual.

**Independent Test**: Open the app in a browser and confirm a green frog is visible in the bottom-left and bottom-right corners.

**Acceptance Scenarios**:

1. **Given** the app is loaded, **When** the page is displayed, **Then** a green frog is visible in the bottom-left corner and one in the bottom-right corner.
2. **Given** the page content is longer than the screen, **When** the user scrolls, **Then** the frogs stay in the bottom corners of the visible screen.

---

### User Story 2 - Frogs never get in the way (Priority: P2)

A person uses the app normally (reading, clicking, typing) and the frogs never block or hide any content or controls.

**Why this priority**: Decoration must not reduce usability.

**Independent Test**: Click and tap on controls located near the bottom corners and confirm they respond as normal.

**Acceptance Scenarios**:

1. **Given** a button or link lies beneath a frog, **When** the user clicks it, **Then** the control responds as if the frog were not there.
2. **Given** a narrow (phone-sized) screen, **When** the page is displayed, **Then** the frogs do not cover the main content in a way that makes it unreadable.

---

### Edge Cases

- Very small screens: frogs shrink or stay small enough not to obscure content.
- Very wide screens: frogs remain anchored to the screen corners, not the content area.
- Frogs and existing top-corner unicorns must not overlap or visually clash.
- Frogs must be fully visible, with no clipped edges, at every size.
- Screen readers must not announce the frogs as meaningful content.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The app MUST display a green frog in the bottom-left corner and in the bottom-right corner of the screen.
- **FR-002**: The frogs MUST be clearly green in colour.
- **FR-003**: The frogs MUST stay fixed in the corners of the visible screen while the user scrolls.
- **FR-004**: The frogs MUST NOT intercept clicks, taps or keyboard focus.
- **FR-005**: The frogs MUST be treated as decoration and hidden from assistive technology.
- **FR-006**: The frogs MUST NOT overlap or displace the existing top-corner unicorns or any existing content.
- **FR-007**: Each frog MUST have enough vertical room around it that no part of it is clipped or cramped.
- **FR-008**: Existing app behaviour (listing, creating, completing tasks and owners) MUST be unchanged.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On first load, 100% of viewers see a green frog in both bottom corners without any interaction.
- **SC-002**: All existing controls remain usable: 100% of clicks on controls near the bottom corners work as before.
- **SC-003**: Frogs are visible and do not hide content on screen widths from phone (320 px) to large desktop.
- **SC-004**: The existing automated checks continue to pass unchanged.

## Assumptions

- "The bottom corner" is read as both bottom corners (left and right), mirroring the decorative unicorns in the top corners. If only one corner is wanted, this is a trivial change.
- "Frogs" means one frog per corner (two total); the same frog image may be mirrored for the other corner.
- The frogs are static decoration; no animation or interaction is required.
- Frogs appear on every screen of the frontend.
- No backend or data changes are needed; this affects only the web frontend.
