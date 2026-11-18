# Spec Delta

## Purpose

Brings an existing profile's content into ProfileStudio without losing it.

## ADDED Requirements

### Requirement: Mapped content
Recognized links and technologies SHALL be moved into `links` and `toolkit`; unrecognized content MUST be kept in `extra_sections`.

#### Scenario: Badges row
- **WHEN** the old README has technology badges
- **THEN** they become toolkit items
