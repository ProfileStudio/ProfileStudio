# Spec Delta

## Purpose

Lets users feature gists next to repositories in the selected work section.

## ADDED Requirements

### Requirement: Gist items
A `projects` entry with a `gist` id SHALL render as a card that links to the gist.

#### Scenario: Gist
- **WHEN** an entry has `gist: abc123`
- **THEN** a card links to the gist page
