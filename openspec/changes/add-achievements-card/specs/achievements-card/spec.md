# Spec Delta

## Purpose

Celebrates verifiable milestones from public GitHub data in the profile's own visual style.

## ADDED Requirements

### Requirement: Earned achievements
The card SHALL show only achievements whose threshold the user has reached, each with its level, unless the user asks to show locked ones.

#### Scenario: New user
- **WHEN** the user has 3 stars
- **THEN** the stars achievement is not shown

### Requirement: Documented thresholds
Every achievement and level MUST have a threshold documented in the configuration reference.

#### Scenario: Docs
- **WHEN** a user wonders why a level was given
- **THEN** the reference lists the threshold
