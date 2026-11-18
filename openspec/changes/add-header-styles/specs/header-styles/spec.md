# Spec Delta

## Purpose

Gives users more header layouts and motion while keeping them consistent with the active theme and accessible.

## ADDED Requirements

### Requirement: Typing animation
When `typing` lines are set, the header SHALL animate them one at a time with CSS only and SHALL show the first line still when the viewer prefers reduced motion.

#### Scenario: Reduced motion
- **WHEN** the viewer prefers reduced motion
- **THEN** the first line is shown without animation

### Requirement: Theme colors
Banner shapes MUST use the active theme's colors, including custom colors.

#### Scenario: Custom accent
- **WHEN** the user set a custom accent
- **THEN** the banner gradient uses it
