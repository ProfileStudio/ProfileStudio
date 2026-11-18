# Spec Delta

## Purpose

Makes streak numbers match what users expect: whole history, their own time zone, and optional rest days.

## ADDED Requirements

### Requirement: Current streak
The current streak SHALL count consecutive days with contributions up to today in the configured time zone; today without contributions SHALL NOT break it.

#### Scenario: Morning without commits
- **WHEN** the user has a 10-day streak and no contribution yet today
- **THEN** the current streak is 10 days

### Requirement: All-time longest streak
The longest streak SHALL consider every year since the account was created.

#### Scenario: Old record
- **WHEN** the longest streak happened three years ago
- **THEN** it is shown as the longest streak

### Requirement: Excluded weekdays
Days listed in `streak_skip_days` MUST NOT break a streak when they have no contributions.

#### Scenario: Weekend off
- **WHEN** weekends are excluded and the user contributes Monday to Friday
- **THEN** the streak continues across weekends
