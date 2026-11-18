# Design

## Context

Headers are drawn per theme; banners must not break the window metaphor of each theme.

## Goals / Non-Goals

**Goals:**
- Variants that fit every theme family.
- Accessible motion.

**Non-Goals:**
- Arbitrary SVG uploads as banners (users can already use their own image).

## Decisions

- Shapes are paths computed from the card width; gradients use @AL@/@AD@ accent tokens.
- Typing uses CSS steps() over a clipped text width per line; widths come from text_width.

## Risks / Trade-offs

- Text width estimation errors clip letters: measure with conservative widths and test long lines.
