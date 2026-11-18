# Spec Delta

## Purpose

Describes when the user usually commits and what they used recently, from public data.

## ADDED Requirements

### Requirement: Timing in the user's time zone
Hours and weekdays SHALL be computed in the configured time zone.

#### Scenario: Night owl
- **WHEN** most commits happen at 23:00 local time
- **THEN** the hour chart peaks at 23

### Requirement: API budget
Collecting habits MUST stay within a documented maximum number of API calls.

#### Scenario: Many repositories
- **WHEN** the user owns 300 repositories
- **THEN** only the most recently pushed ones are scanned
