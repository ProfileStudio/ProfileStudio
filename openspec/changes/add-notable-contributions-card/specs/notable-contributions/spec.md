# Spec Delta

## Purpose

Shows the open-source work a user did in other people's repositories.

## ADDED Requirements

### Requirement: External repositories only
The card SHALL list repositories not owned by the user where they have merged pull requests or commits, ordered by stars.

#### Scenario: Own repository
- **WHEN** the user's own repository has many commits
- **THEN** it does not appear in the card

### Requirement: Empty state
When there are no external contributions the card MUST NOT be generated.

#### Scenario: No contributions
- **WHEN** the user never contributed elsewhere
- **THEN** no card and no empty section
