# Proposal

## Why

`profile.json` has grown to dozens of keys. Mistakes are caught only when the generator runs, and editors cannot help users write it.

## What Changes

- Publish a JSON Schema for `profile.json` and reference it from the example file, so editors offer autocompletion and inline errors.
- The generator validates the file against the same rules before calling GitHub and lists every problem at once.

## Capabilities

### New Capabilities

- `profile-config-validation`: Validation of `profile.json` with a published schema and clear errors before any network call.

### Modified Capabilities

None.

## Impact

New `schema/profile.schema.json`; `templates/profile.example.json` gains `$schema`; generator validation (standard library only).

## Out of Scope

- Validating card text quality (length, tone).

## Planning

Milestone: v2.0 Maturity · Priority: medium · Suggested model: sonnet · Effort: medium
