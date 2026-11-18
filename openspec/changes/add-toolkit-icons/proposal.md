# Proposal

## Why

The toolkit card shows technologies as text-only pills. Every popular profile tool shows logos; it is the most visible gap.

## What Changes

- Show each technology's logo inside its pill, drawn in the theme's colors (monochrome by default, brand color optional).
- Download only the icons a profile uses from simple-icons at a pinned version and keep them in the profile repository, so later runs work offline.
- Fall back to the text pill when an icon is unknown or was removed by its brand.

## Capabilities

### New Capabilities

- `toolkit-icons`: Technology logos in toolkit pills, sourced from a pinned simple-icons release and cached in the profile repository.

### Modified Capabilities

None.

## Impact

Toolkit card drawing; new cache folder `data/icons/`; `profile.json` option `toolkit_icons`.

## Out of Scope

- Icons in project cards and the header (possible follow-ups).
- Bundling all 3,400 icons.

## Prior Art

simple-icons (CC0-1.0) provides the icon data; tandpfun/skill-icons (MIT) and rahuldkjain's generator (Apache-2.0) show technology logos. Brand logos remain trademarks of their owners.

## Planning

Milestone: v2.0 Maturity · Priority: high · Suggested model: sonnet · Effort: medium
