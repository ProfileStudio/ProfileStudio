# Spec Delta

## Purpose

Gives every user a quick quality check of their generated profile.

## ADDED Requirements

### Requirement: Report
After generating, the tool SHALL print a report listing contrast, alt text, size and motion problems, or that none were found.

#### Scenario: Large header
- **WHEN** the header image is over the size budget
- **THEN** the report names the file and its size
