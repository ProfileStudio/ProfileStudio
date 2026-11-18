# Spec Delta

## Purpose

Lets visitors reach the profile owner through clearly labeled, theme-consistent links that work inside GitHub's README rendering.

## ADDED Requirements

### Requirement: Linked icons
Each entry in `links` SHALL render as its own image wrapped in a link to its URL, with alternative text naming the destination.

#### Scenario: Website link
- **WHEN** `links` contains a website URL
- **THEN** the README shows a website icon that opens that URL and has alt text

### Requirement: Safe destinations
Only `https:` and `mailto:` URLs MUST be accepted.

#### Scenario: Unsafe URL
- **WHEN** a link uses `javascript:`
- **THEN** the run stops with an error naming the entry
