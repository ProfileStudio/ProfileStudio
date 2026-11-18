# Proposal

## Why

The generator has no automated tests: every change is checked by hand on screenshots, which will not scale to more cards, themes and contributors.

## What Changes

- Add a test suite that runs the generator against recorded GitHub API responses (no network, no token).
- Add SVG snapshot tests for every theme in light and dark, plus checks that no text overflows its card (estimated widths against card bounds).
- Run the suite in GitHub Actions on every pull request.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None.

## Impact

New `tests/` folder and fixtures, a CI workflow. The generator gains a seam to replace network calls with fixtures; no user-visible behavior changes.

## Out of Scope

- Pixel-level visual regression (screenshots) in CI.
- Tests for the Claude Code skill flow.

## Prior Art

lowlighter/metrics (MIT) tests plugins against mocked GitHub data; shields (Apache-2.0) keeps snapshots. Only the approach is reused.

## Planning

Milestone: v2.0 Maturity · Priority: high · Suggested model: sonnet · Effort: medium
