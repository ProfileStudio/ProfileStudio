# Proposal

## Why

Streaks are computed from the last year only and in UTC, so long-time users see a shorter longest streak and some see the current streak break at the wrong hour.

## What Changes

- Compute the longest streak over the whole account history.
- Use the user's time zone for the current day.
- Optional excluded weekdays (for example weekends) that do not break a streak.

## Capabilities

### New Capabilities

- `contribution-streaks`: How current and longest streaks are computed and displayed.

### Modified Capabilities

None.

## Impact

GraphQL calendar queries per year, activity card, `profile.json` keys `timezone` and `streak_skip_days`.

## Out of Scope

- A separate streak card design (the activity card keeps showing them).

## Prior Art

DenverCoder1/github-readme-streak-stats (MIT) handles time zones and excluded days. Idea only.

## Planning

Milestone: v2.0 Maturity · Priority: medium · Suggested model: sonnet · Effort: medium
