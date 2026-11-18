# Proposal

## Why

The profile signal card offers six metrics. Developers who review code, answer discussions or contribute to other projects have no way to show it.

## What Changes

- New tile metrics: reviews, issues opened, discussions answered, merged pull request ratio, repositories contributed to and all-time contributions.
- An optional overall level (off by default), computed from public activity with a documented formula.

## Capabilities

### New Capabilities

- `profile-stats`: The metrics available as tiles in the profile signal card and how each is computed.

### Modified Capabilities

None.

## Impact

GraphQL queries, profile signal card, `profile.json` `tiles` values, skill recommendations.

## Out of Scope

- Private data beyond what the user's token can already read.

## Prior Art

stats-organization/github-stats-extended (MIT), successor of github-readme-stats, offers these metrics and a rank. Idea only.

## Planning

Milestone: v2.0 Maturity · Priority: high · Suggested model: sonnet · Effort: medium
