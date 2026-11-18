# Proposal

## Why

Visitors like to see when and how someone works (night owl, weekend coder, most used languages lately). It adds personality without inventing anything.

## What Changes

- Optional card with commit activity by hour of day and day of week, in the user's time zone, and the languages of recent commits.

## Capabilities

### New Capabilities

- `coding-habits`: Card with commit timing patterns and recently used languages.

### Modified Capabilities

None.

## Impact

GraphQL history queries per repository (rate-limit aware), new card, `timezone` key.

## Out of Scope

- Editor telemetry (WakaTime) integration.

## Prior Art

metrics' habits plugin (MIT). Idea only.

## Planning

Milestone: v2.0 Maturity · Priority: medium · Suggested model: sonnet · Effort: high
