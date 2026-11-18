# Proposal

## Why

The header has one layout per theme. Banner shapes and typing animations are among the most copied profile widgets, always as separate images that ignore the profile's style.

## What Changes

- Header variants: banner shapes (wave, slice, rounded) with gradients from the theme palette.
- Optional typing animation that cycles through short lines, in CSS only.
- Optional matching footer banner.

## Capabilities

### New Capabilities

- `header-styles`: Header layout variants, typing animation and footer banner.

### Modified Capabilities

None.

## Impact

Header card, new footer asset, `profile.json` keys `header_style`, `typing`, `footer`.

## Out of Scope

- Custom fonts (not possible in GitHub images).
- JavaScript animation.

## Prior Art

kyechan99/capsule-render (MIT) and DenverCoder1/readme-typing-svg (MIT). Idea only; shapes and animation are original.

## Planning

Milestone: v2.0 Maturity · Priority: medium · Suggested model: opus · Effort: high
