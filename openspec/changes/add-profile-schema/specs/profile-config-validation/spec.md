# Spec Delta

## Purpose

Checks `profile.json` before generating anything, so users get every mistake at once with its location instead of a failure halfway through.

## ADDED Requirements

### Requirement: Validate before fetching data
The generator SHALL validate `profile.json` against the published schema before it makes any GitHub API call.

#### Scenario: Invalid key
- **WHEN** `profile.json` contains an unknown key `tiels`
- **THEN** the run stops before any API call and names `tiels` and the closest valid key

#### Scenario: Several errors
- **WHEN** two values have the wrong type
- **THEN** both errors are listed in one run, each with its JSON path

### Requirement: Editor support
Profiles written by the skill and the example file MUST reference the schema through `$schema`.

#### Scenario: Editor autocompletion
- **WHEN** a user opens `profile.json` in an editor with JSON Schema support
- **THEN** keys and allowed values are suggested and errors are underlined
