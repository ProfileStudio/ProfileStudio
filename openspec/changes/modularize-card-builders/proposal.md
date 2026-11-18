# Proposal

## Why

`generate.py` is a single 1,600-line file. Adding the planned cards (achievements, habits, social links, banners) to it would make it hard to review and to contribute to.

## What Changes

- Split the generator into modules: data fetching, theme styles, shared drawing helpers and one module per card, with a small registry that lists the cards a profile uses.
- Keep the distribution promise: a build step bundles the modules into the single `generate.py` that is copied into each profile repository, so users still need only Python.
- Describe each card with metadata (name, options, defaults, data it needs) so documentation and the JSON schema can be generated from it.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None.

## Impact

Source layout under `plugin/skills/github-profile/`; a bundling script; the skill keeps copying one file. Output must be byte-identical before and after (checked by the test suite).

## Out of Scope

- Third-party plugins loaded at run time (a later change).
- Any visual change.

## Prior Art

lowlighter/metrics (MIT) keeps one folder per plugin with metadata.yml that drives docs and tests. Only the idea is reused.

## Planning

Milestone: v2.0 Maturity · Priority: high · Suggested model: opus · Effort: high
