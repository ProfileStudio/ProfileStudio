# Spec Delta

## Purpose

Defines which activity metrics a profile can show as tiles and how each one is counted, so numbers are explainable and stable.

## ADDED Requirements

### Requirement: Selectable metrics
The `tiles` list SHALL accept repos, contributions, prs, stars, followers, production, reviews, issues, discussions_answered, merged_pr_ratio, contributed_to and contributions_all_time.

#### Scenario: Reviewer profile
- **WHEN** `tiles` includes `reviews`
- **THEN** the card shows the number of pull request reviews in the last year

### Requirement: Optional level
An overall level MUST NOT be shown unless the user enables it.

#### Scenario: Default
- **WHEN** the user does not set a level option
- **THEN** no level appears
