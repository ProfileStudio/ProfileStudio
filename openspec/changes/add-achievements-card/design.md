# Design

## Context

Trophy-style cards exist but use one look. ProfileStudio draws everything per theme.

## Goals / Non-Goals

**Goals:**
- Original artwork that fits all 13 themes.
- Thresholds that make sense for new and experienced users.

**Non-Goals:**
- Copying another project's trophy art or level names.

## Decisions

- Achievements: stars, followers, years on GitHub, languages used, pull requests merged, reviews, repositories contributed to, organizations.
- Levels I to V with roughly logarithmic thresholds.
- Artwork as shapes built from theme classes, so custom colors apply automatically.

## Risks / Trade-offs

- Motivation versus comparison anxiety: earned-only by default, no global ranking.
