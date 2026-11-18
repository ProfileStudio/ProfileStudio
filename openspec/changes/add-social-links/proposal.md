# Proposal

## Why

Profiles have no way to show where to reach the person (website, LinkedIn, email, blog). Every competing generator has a social links section.

## What Changes

- Add a row of contact links under the header, each a small themed icon image wrapped in its own link (GitHub does not allow links inside an SVG shown as an image).
- Support common networks plus generic website, email and RSS; generic icons for brands that are not in simple-icons.

## Capabilities

### New Capabilities

- `social-links`: Themed contact and social links rendered as linked icon images.

### Modified Capabilities

None.

## Impact

New assets `assets/social-*.svg`, README layout, `profile.json` key `links`.

## Out of Scope

- Follower counts from other networks.
- Visitor counters.

## Prior Art

rahuldkjain/github-profile-readme-generator (Apache-2.0) and maurodesouza/profile-readme-generator (MIT) offer social sections. Idea only.

## Planning

Milestone: v2.0 Maturity · Priority: high · Suggested model: sonnet · Effort: medium
