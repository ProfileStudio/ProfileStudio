# Proposal

## Why

Cards speak English and Spanish only. The goal is any developer, in their language.

## What Changes

- Move card texts to locale files and support 12 languages in three waves: en, es, pt; hi, zh-Hans, ja, ko; id, de, ru, fr, zh-Hant.
- Measure text width by script (CJK and Hangul are about twice as wide) and format numbers and dates per locale.
- Mark machine translations as pending native review.

## Capabilities

### New Capabilities

- `card-localization`: Locale files, script-aware text width and locale formatting.

### Modified Capabilities

None.

## Impact

Strings, width estimation, number and date formatting, docs, contribution guide for translators.

## Out of Scope

- Translating the documentation into 12 languages (community-driven later).

## Prior Art

github-readme-stats (MIT) and streak-stats (MIT) accept translations by pull request.

## Planning

Milestone: Internationalization · Priority: medium · Suggested model: opus · Effort: high
