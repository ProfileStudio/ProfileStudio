# Proposal

## Why

Quality must hold for every profile, not only the ones we review. Contrast is checked today; alt text, color-blind safety and file size are not.

## What Changes

- A quality report after each run: contrast, missing or too long alt text, total image size, animation that ignores reduced motion.
- A color-blind friendly heatmap option.

## Capabilities

### New Capabilities

- `quality-report`: Automatic checks printed after generation, and accessibility options.

### Modified Capabilities

None.

## Impact

Generator reporting, heatmap palette option `heatmap_palette`.

## Out of Scope

- Blocking generation on warnings (they stay warnings).

## Prior Art

DenverCoder1/github-readme-streak-stats (MIT) ships color-blind friendly themes. Idea only.

## Planning

Milestone: v2.0 Maturity · Priority: medium · Suggested model: sonnet · Effort: medium
