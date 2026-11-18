# `data/profile.json` reference

Everything the README shows comes from this file plus live GitHub data. Keys starting with `_` are
ignored, so they can hold notes (remove them before publishing). The file may be saved with or
without a UTF-8 BOM.

## Identity

| Key | Type | Notes |
|---|---|---|
| `login` | string | **Required.** GitHub username; all live data is fetched for it. |
| `name` | string | Display name in the header. |
| `role` | string | One line under the name, e.g. "Backend developer · Company". |
| `bio` | string | Two or three short sentences, about 180 characters. |
| `pills` | string[] | 4 to 6 short tags under the bio. |

## Style

| Key | Values | Default |
|---|---|---|
| `theme` | `terminal`, `editor`, `ide`, `vim`, `notebook`, `classic`, `win11`, `macos`, `handheld`, `crt`, `browser`, `sql`, `git` | `terminal` |
| `accent` | a color (`cyan`, `green`, `amber`, `magenta`), a Linux distro (`ubuntu`, `arch`, `debian`, `fedora`, `mint`, `cachyos`) or a system color (`vscode`, `ide`, `notebook`, `win`, `mac`, `browser`, `sql`, `git`). Or your own color: `"#ff6600"` (both modes) or `{"light": "#4b5563", "dark": "#d4d8de"}`. `crt` uses it as phosphor (`amber`, `green`, `cyan`, `magenta`). `classic` and `handheld` ignore it | terminal `cyan`, editor `vscode`, ide `ide`, vim `green`, notebook `notebook`, win11 `win`, macos `mac`, crt `amber`, browser `browser`, sql `sql`, git `git` |
| `host` | host shown as `user@host` in the terminal title bar | the distro of `accent`, else `github` |
| `lang` | `en`, `es` | `en` |
| `tiles` | four of `repos`, `contributions`, `prs`, `stars`, `followers`, `production` | `repos`, `contributions`, `prs`, `production` |

`production` counts the featured projects whose `kind` is `prod`.

## Custom colors

Two levels, both in `profile.json`, so `scripts/generate.py` stays the official one and keeps
receiving updates. Never edit the script to change colors.

**Level 1, your own accent.** `accent` takes a color instead of a name:

```json
"accent": { "light": "#4b5563", "dark": "#d4d8de" }
```

The light color is used on light backgrounds and the dark one on dark backgrounds, so pick a dark
shade for `light` and a light shade for `dark`. A single `"#ff6600"` is used for both.

**Level 2, fine-tune a theme** with `theme_overrides`:

```json
"theme_overrides": {
  "color_scheme": "dark",
  "dark": { "background": "#050505", "titlebar": "#0d0d0f", "panel": "#0b0b0d",
            "text": "#e8eaed", "muted": "#9aa0a6", "data1": "#f1f3f5" },
  "light": { "background": "#ffffff" },
  "languages": { "Python": "#d4d8de" },
  "css": { "dark": ".frame{stroke-width:2}" }
}
```

| Key | Notes |
|---|---|
| `color_scheme` | `auto` (default) follows the viewer's GitHub theme. `dark` always draws the dark palette, `light` always the light one. |
| `light`, `dark` | Colors per mode, by role (below). Only what you list changes. |
| `languages` | Color of a language in the stack card and project bars, e.g. `{"Python": "#d4d8de"}`. |
| `css` | Extra CSS for the cards, as a string (both modes) or `{"both", "light", "dark"}`. For effects the roles do not cover. No `<` or `>`, and no nested `@` blocks inside `light` or `dark`. Class names differ between themes: read the theme's style in `generate.py`. |

Roles, the same in every theme:

| Role | What it colors |
|---|---|
| `background`, `border` | the window of every card |
| `titlebar` | the title bar |
| `panel`, `panel_border` | tiles, pills and chips inside a card |
| `text`, `muted` | main and secondary text |
| `lines`, `track` | separators; the empty part of progress bars |
| `heatmap_empty` | days without contributions |
| `data1` to `data4` | the four colors of numbers and counters (blue, cyan, purple, green by default) |
| `status_live`, `status_wip` | the dot of a project in production and of a prototype |

Colors are `#rgb`, `#rrggbb`, `rgb(...)`, `hsl(...)` or a CSS color name. A typo in a key or a
color stops the run with the list of valid ones. The generator also prints a `contrast warning`
when text (under 4.5:1), muted text or the accent (under 3:1) is hard to read on the background.

## Header, right side

Use one of these; with none, the text spans the whole card.

| Key | Type | Notes |
|---|---|---|
| `portrait` | path | Image relative to the repo root. Transparent PNG/WebP: drawn as a cutout standing on the bottom edge (works in both themes). JPEG: fills the right side and fades into the card. |
| `portrait_frames` | path | JSON written by `scripts/frames.py`. Turns `portrait` (the sprite sheet) into an animation. |
| `portrait_width` | number | Cutout width in px (default 380; 220 to 300 suits square sprites). |
| `fetch` | `[key, value][]` | neofetch-style panel, e.g. `[["os", "Arch Linux"], ["editor", "Neovim"]]`. Used when there is no `portrait`. |

The animation stops for viewers who enabled "reduce motion" in their OS.

## Featured work

`projects` is a list, best with exactly 4 (two rows of two). Each item:

| Key | Notes |
|---|---|
| `repo` | `owner/name`; may belong to an organization. |
| `title` | Display name. |
| `label` | Small caps line above the title, e.g. `WEB APP · PWA`. |
| `desc` | About 150 characters, from the repo's README. |
| `stack` | 4 short items; a fifth usually wraps to a second row. |
| `status` | Short footer line, e.g. "In production · Vercel" (keep under about 28 characters). |
| `kind` | `prod` (green dot) or `proto` (amber dot). |

Commits, last push date and the language bar are fetched live.

## Languages and toolkit

| Key | Notes |
|---|---|
| `languages_ignore` | Languages left out of the stack card, e.g. `["HTML", "CSS"]`. The card says which. |
| `toolkit` | List of `{ "label": "Backend", "items": ["Django", "FastAPI"] }` groups, 4 to 6 groups. |

## README

| Key | Notes |
|---|---|
| `extra_sections` | List of `{ "heading": "...", "html": "..." }` added after the heatmap, verbatim. |
| `credits` | List of HTML lines shown at the bottom, e.g. art credits. |
| `made_with` | `true` (default) draws `assets/made-with.svg`, a small badge in the profile's theme linking to the generator, at the bottom right; it replaces the footer line. `false` removes it and brings the footer back. An old text "Made with" line in `credits` is skipped while the badge is on. |
| `readme` | `false` stops the generator from writing `README.md`. |
