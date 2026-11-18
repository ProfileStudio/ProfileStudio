# Design

## Context

The generator is copied into every user's profile repository and run there by people and by a weekly workflow. Python alone, one file, no installs.

## Goals / Non-Goals

**Goals:**
- Cards can be added by contributors without reading the whole generator.
- The copied artifact stays one standard-library file.

**Non-Goals:**
- Changing the output.
- Run-time plugins.

## Decisions

- Source modules in a `profilestudio/` package next to the skill; `scripts/build.py` concatenates them in dependency order into `generate.py` (alternative: zipapp, rejected because users and agents read and diff the file).
- A registry maps card ids to builders and metadata; `profile.json` lists the cards in order (default: today's order).
- Card metadata (options, defaults, required API scopes) feeds docs and the JSON schema.

## Risks / Trade-offs

- Bundling bugs: guarded by a CI check that rebuilds and diffs.
- Contributors editing the bundle by hand: header comment and CI check.
