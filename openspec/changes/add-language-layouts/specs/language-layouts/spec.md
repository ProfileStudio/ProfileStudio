# Spec Delta

## Purpose

Lets users choose how the language stack is drawn without changing the data.

## ADDED Requirements

### Requirement: Layout option
`languages_layout` SHALL accept `bars`, `compact` and `donut`, defaulting to `bars`.

#### Scenario: Donut
- **WHEN** `languages_layout` is `donut`
- **THEN** the card shows a donut chart with a legend
