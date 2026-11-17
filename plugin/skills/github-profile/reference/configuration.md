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
| `theme` | `terminal`, `editor`, `ide`, `vim`, `notebook`, `classic`, `win11`, `macos`, `handheld`, `crt` | `terminal` |
| `accent` | a color (`cyan`, `green`, `amber`, `magenta`), a Linux distro (`ubuntu`, `arch`, `debian`, `fedora`, `mint`, `cachyos`) or a system color (`vscode`, `ide`, `notebook`, `win`, `mac`). `crt` uses it as phosphor (`amber`, `green`, `cyan`, `magenta`). `classic` and `handheld` ignore it | terminal `cyan`, editor `vscode`, ide `ide`, vim `green`, notebook `notebook`, win11 `win`, macos `mac`, crt `amber` |
| `host` | host shown as `user@host` in the terminal title bar | the distro of `accent`, else `github` |
| `lang` | `en`, `es` | `en` |
| `tiles` | four of `repos`, `contributions`, `prs`, `stars`, `followers`, `production` | `repos`, `contributions`, `prs`, `production` |

`production` counts the featured projects whose `kind` is `prod`.

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
| `credits` | List of HTML lines shown at the bottom, e.g. art credits or a "Made with" link. |
| `readme` | `false` stops the generator from writing `README.md`. |
