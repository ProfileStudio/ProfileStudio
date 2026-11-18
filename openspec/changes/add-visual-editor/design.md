# Design

## Context

Cards need GitHub data, which the browser cannot fetch without a token.

## Goals / Non-Goals

**Goals:**
- Edit and preview without leaving the browser.

**Non-Goals:**
- Hosting.

## Decisions

- Preview uses the last generated data snapshot; regeneration still runs the generator.

## Risks / Trade-offs

- Keeping the editor in sync with new options: generate forms from metadata.
