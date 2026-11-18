# Spec Delta

## Purpose

Adds technology logos to the toolkit card while keeping profiles static, offline after the first run, and consistent with the active theme.

## ADDED Requirements

### Requirement: Logos in toolkit pills
When `toolkit_icons` is enabled (default), each toolkit item with a known icon SHALL show the logo before its label, in the theme's text color unless `brand` colors are requested.

#### Scenario: Known technology
- **WHEN** the toolkit lists `Django`
- **THEN** its pill shows the Django logo and the label

#### Scenario: Unknown technology
- **WHEN** the toolkit lists `MyInternalTool`
- **THEN** its pill shows the label only and the run does not fail

### Requirement: Pinned, cached icons
Icons MUST come from one pinned simple-icons release and be stored in the profile repository; a later run SHALL NOT download an icon that is already cached.

#### Scenario: Offline rerun
- **WHEN** all icons are cached and there is no network for icon downloads
- **THEN** the toolkit card is generated with the same icons
