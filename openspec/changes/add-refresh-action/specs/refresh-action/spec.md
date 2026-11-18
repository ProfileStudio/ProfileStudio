# Spec Delta

## Purpose

Keeps a profile's numbers current without manual work.

## ADDED Requirements

### Requirement: Commit only on change
The action SHALL commit only when generated files differ from the repository.

#### Scenario: No change
- **WHEN** nothing changed since the last run
- **THEN** no commit is created
