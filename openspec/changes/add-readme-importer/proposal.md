# Proposal

## Why

Users who already have a hand-written README lose content when switching, or the agent keeps it as opaque HTML.

## What Changes

- Recognize common README parts (intro lines, social links, technology lists, stats widgets) and map them to `profile.json` fields, keeping the rest as extra sections.

## Capabilities

### New Capabilities

- `readme-import`: Mapping an existing README into profile.json fields.

### Modified Capabilities

None.

## Impact

Skill step 2, a helper script, tests with sample READMEs.

## Out of Scope

- Perfect round-trip of arbitrary HTML.

## Prior Art

maurodesouza/profile-readme-generator (MIT) imports existing READMEs. Idea only.

## Planning

Milestone: v2.0 Maturity · Priority: low · Suggested model: sonnet · Effort: medium
