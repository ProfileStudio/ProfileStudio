# Spec Delta

## Purpose

Lets cards be generated in the user's language with correct layout and formats.

## ADDED Requirements

### Requirement: Locale files
`lang` SHALL accept any supported locale and every card text MUST come from that locale's file.

#### Scenario: Portuguese
- **WHEN** `lang` is `pt`
- **THEN** all card labels are in Portuguese

### Requirement: Wide scripts
Text width estimation MUST account for the script, so CJK text does not overflow cards.

#### Scenario: Japanese title
- **WHEN** a project title is in Japanese
- **THEN** it stays inside its card
