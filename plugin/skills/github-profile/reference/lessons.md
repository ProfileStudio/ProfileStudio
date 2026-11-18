# Lessons learned

Collected while building the first profile with this generator. Each one cost a round trip once.

## How GitHub renders the README

- README images are served as `<img>` through GitHub's image proxy. Inside an SVG there is no
  JavaScript and no web fonts. Use system font stacks (the generator already does).
- `@media (prefers-color-scheme: dark)` **inside** the SVG works, so one file serves both themes.
  No `<picture>` element is needed.
- HTML `<table>` in a README gets cell borders from GitHub's CSS. For two cards side by side use
  two `<img width="49.5%">` in a row; each SVG carries a 6 px transparent margin as the gutter.
- Images are cached for a few minutes after a push. The README adds `?v=<hash>` (first 8 hex of
  the file's SHA-1) to every image, so a changed card gets a new URL and shows at once. Idea from a
  user's own copy of the generator.

## Themes

- People pick the theme of the system or editor they use daily. Name themes generically
  (`editor`, `classic`) and draw no logos: they are inspired by products, not affiliated with them.
- An option list in AskUserQuestion holds at most 4 entries. With more themes, ask the family first
  (terminal, code editor, OS window, retro) and the variant second.
- `handheld` and `crt` recolor the header image to their palette with an SVG filter, so any
  portrait fits; their body font is monospace, which the width estimate accounts for.
- A blinking cursor drawn as a `<tspan>` follows the text whatever font the viewer has; a
  rectangle placed by estimated width drifts.

## Text in SVG

- SVG text never wraps. The generator wraps by estimated width (0.55 em sans, 0.6 em bold,
  0.62 em mono). It is deliberately conservative because Linux viewers often fall back to wider
  fonts (DejaVu). Always check the preview.
- Chips that do not fit wrap to a second row and make the card taller. Four short stack items per
  project card fit one row; five usually do not.

## Header images

- An image with a black background looks fine in dark mode and like a black box in light mode.
  Remove the background (`scripts/cutout.py`) and use a transparent PNG or WebP: the generator
  draws it as a cutout and it suits both themes.
- Dot-matrix art has black gaps between the dots inside the figure too. A plain threshold turns
  the figure into a sieve; blur first, then close gaps and fill enclosed holes (what the script does).
- Keep the embedded image around 100 KB (WebP, about 2x the displayed height): it is inlined as
  base64 in `header.svg`.
- Animated headers: a GIF inside an SVG `<image>` is not reliably animated and its 1-bit alpha
  leaves jagged edges. `scripts/frames.py` builds a sprite sheet instead, and the generator slides
  it one frame per step with a CSS animation inside a frame-sized clip. CSS animations run in SVG
  shown as `<img>`; verified in Chromium by capturing frames 0.15 s apart. The animation stops
  for viewers with "reduce motion" enabled.
- Pixel art resized with smoothing grows thousands of colors (a 6-frame sheet went from 57 KB to
  464 KB). `frames.py` quantizes to a 128-color palette by default.
- Tenor pages list several related GIFs. Match the media id to the post id before downloading:
  the 11-character id in `media.tenor.com/<id>AAA…` is the post id in base64url.
- Third-party art needs a visible credit (`credits` in `profile.json`). Letting the artist know is
  good practice, not a blocker. Tenor's terms grant no license to re-host files, and fan-art
  tolerance comes from the character's owners, not from the artist of the drawing.
- Put the figure where text cannot reach it. A wider image squeezes the bio into more lines and
  can push text over the figure's laptop or desk.

## Data

- `contributionCalendar.totalContributions` includes private work only if the user enabled
  "Include private contributions" in their profile settings. The API cannot read that setting.
- Commits count toward contributions only if the author email is verified on the account and the
  commits are on the default branch. If a busy repo shows zero contributions, check the email.
- In GitHub Actions, the default `GITHUB_TOKEN` sees only public activity, so a scheduled run
  would overwrite the cards with lower numbers. The workflow template skips itself unless a
  `PROFILE_TOKEN` secret exists.
- Pick the four signal tiles that reflect real strengths (`repos`, `contributions`, `prs`, `stars`,
  `followers`, `production`). The progress bars are decorative, scaled to the next round milestone
  (10, 25, 50, 100…); say so if asked.
- Languages are weighted by bytes. Big HTML or CSS files can dominate; `languages_ignore` drops
  them and the card subtitle states which ones were excluded.

## Account actions

- There is no API to pin repositories: the user does it in the web UI.
- `PATCH /user` (the bio) needs the `user` scope, which `gh` does not request by default.
- Do not run `gh auth refresh` or create tokens for the user; tell them the command.

## Before spotlighting a repo

- Read its README and docs first. In one case a public `DOCUMENTACION.md` contained live access
  codes for a production app. A featured repo gets more visitors, so flag anything that looks
  like a credential, and remember that removing it does not remove it from git history: the
  secret must be rotated.
- A repo without a license is "all rights reserved". Mention it once; do not add a license
  without the owner's decision.

## Windows notes

- PowerShell 5.1 writes JSON with a BOM. The generator reads `profile.json` as `utf-8-sig`.
- Headless Edge or Chrome follow the OS theme for screenshots; to check the light theme there,
  remove the dark `@media` block from a temporary copy of the SVGs.

## Running the skill (from real sessions)

- **git can hang** on fetch or push where git has no credential helper of its own: it waits for a
  password nobody types. `backup.py` sets `GIT_TERMINAL_PROMPT=0` and borrows the `gh` login
  (`credential.helper=!gh auth git-credential`); do the same for a manual `git push`.
- **An existing generated profile** usually wants only a new theme. Offer "keep my content, change
  the style" before any content question; the quick setup would otherwise rewrite texts the user
  already approved.
- **Previewing in a built-in browser pane**: `file://` pages may not be inspectable there. Serve the
  folder with `python3 -m http.server <port> --directory <folder>` (the explicit `--directory`
  avoids serving the wrong folder), started as its own background command, and stop it afterwards.
- **Forks of the generator lose updates.** A user's agent added its own accents by editing
  `generate.py`; from then on no fix or feature reached that profile. Colors belong in
  `profile.json` (`accent` as a color, `theme_overrides`), never in the script.
