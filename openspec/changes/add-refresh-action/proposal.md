# Proposal

## Why

Stats go stale unless the user reruns the generator. A copied workflow template is easy to break and hard to update.

## What Changes

- Publish a reusable GitHub Action (`ProfileStudio/ProfileStudio@v2`) that regenerates the profile on a schedule and commits only when something changed.
- The skill offers it at publish time and explains the token it needs.

## Capabilities

### New Capabilities

- `refresh-action`: Scheduled regeneration of a profile through a published GitHub Action.

### Modified Capabilities

None.

## Impact

New `action.yml`, release tags, skill publish step, docs.

## Out of Scope

- Hosting a service.

## Prior Art

stats-organization/github-readme-stats-action (MIT) and lowlighter/metrics (MIT) run as Actions.

## Planning

Milestone: v2.0 Maturity · Priority: high · Suggested model: sonnet · Effort: medium
