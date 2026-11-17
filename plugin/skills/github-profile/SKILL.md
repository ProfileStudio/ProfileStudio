---
name: github-profile
description: Design, preview and publish a visual GitHub profile README made of SVG cards with live GitHub data (header with optional animated image or GIF, profile signal, selected work, language stack, toolkit, contribution heatmap). Use when the user wants to create, redesign or refresh their GitHub profile README, or says "set up my GitHub profile".
---

# GitHub profile README generator

Build a profile README in the user's `<login>/<login>` repository. Every visual is an SVG made by
`scripts/generate.py` from `data/profile.json` plus live GitHub API data. Each SVG carries its own
light and dark palette, so one file follows the viewer's theme.

Talk to the user in the language they write in. Ask the configuration questions below; decide the
rest from their data and say what you decided. Read `reference/lessons.md` before step 5.

## Files

| Path | Purpose |
|---|---|
| `scripts/generate.py` | Generator (Python 3.9+, standard library only). Writes `assets/*.svg`, `README.md`, `preview.html`. |
| `scripts/frames.py` | Animated GIF to transparent sprite sheet, for an animated header (Pillow). |
| `scripts/cutout.py` | Removes a solid dark background from a still illustration (Pillow + numpy). |
| `templates/profile.example.json` | Starting point for `data/profile.json`. |
| `templates/update-profile.yml` | Optional weekly refresh workflow (needs a `PROFILE_TOKEN` secret). |
| `templates/gitignore` | Copy as `.gitignore`. |
| `reference/configuration.md` | Every `profile.json` key. |
| `reference/styles/<theme>-<dark|light>.jpg` | Screenshots of the ten themes, to show the user in step 3. |
| `reference/lessons.md` | Known pitfalls. |

`<skill>` below means the folder that holds this file.

## 1. Check the environment (no questions)

- `gh auth status` shows a login with `repo` scope. If `gh` is missing, give the install command for
  their OS (`brew install gh`, `winget install GitHub.cli`, `sudo apt install gh`, `sudo pacman -S github-cli`)
  and stop until it works. They run `gh auth login` themselves.
- `python3 --version` (or `python` on Windows) is 3.9+; `git` exists.
- For an animated or edited header, Pillow is needed: `python3 -m pip install --user pillow numpy`.

## 2. Gather facts (no questions)

```bash
gh api user --jq '{login,name,bio,company,location,blog,public_repos,followers,created_at}'
gh api "users/<login>/repos?per_page=100&type=owner" --paginate \
  --jq '.[] | select(.fork|not) | [.stargazers_count, .language, .pushed_at[0:10], .name, (.description // "")] | @tsv'
gh api graphql -f query='{user(login:"<login>"){pinnedItems(first:6){nodes{... on Repository{nameWithOwner}}}
  contributionsCollection{contributionCalendar{totalContributions} totalPullRequestContributions}}}'
gh api repos/<login>/<login>/readme --jq .content | base64 -d   # current profile README, if any
gh api user/orgs --jq '.[].login'                               # org repos can be featured too
```

Pick 6 to 8 candidate projects (pinned first, then stars, commit count, recent pushes, a real
README). Read the first lines of each candidate's README: descriptions must come from there.
Never invent features, numbers or job titles.

## 3. Configuration questions

### Round 1: style

People like a theme that looks like the system or tool they use every day. Ten themes exist:

| `theme` | Looks like | Suits |
|---|---|---|
| `terminal` | Terminal window, shell prompts as headings, one accent; Linux distro variants | Linux users, tooling, backend |
| `editor` | Code editor: tabs, line numbers, syntax colors, data written as code | Anyone living in VS Code-like editors |
| `ide` | Full IDE: run toolbar, tool window strip, Kotlin-style code | Java, Kotlin, Python IDE users |
| `vim` | Modal editor: mode in the status line, relative line numbers, markdown | Vim and Neovim users |
| `notebook` | Notebook: numbered cells, code input and output | Data science, Python, students |
| `classic` | 90s desktop: gray bevels, navy title bar, block progress bars | Retro fans; stands out the most |
| `win11` | Modern Windows: flat rounded windows, caption buttons, system accent | Windows users |
| `macos` | Mac windows: traffic lights, unified title bar, system blue | Mac users |
| `handheld` | 90s handheld console screen, four greens; the portrait is recolored | Pixel-art headers, game devs |
| `crt` | Phosphor screen, scan lines and glow, amber or green | Retro computing fans |

Read `reference/styles/<theme>-dark.jpg` for the candidates so the user sees them. Then ask in one
AskUserQuestion call (an option list holds at most 4 entries, so the style is split in two steps):

1. **Style family**: Terminal / Code editor / Operating system window / Retro. Recommend from
   what step 2 shows: Linux tooling suggests terminal, mostly web code suggests editor, notebooks
   suggest the notebook theme, a pixel-art header suggests retro.
2. **Language** of the README: English / Spanish (`en`, `es`).
3. **Right side of the header**: an animated GIF / a still image / a neofetch-style info panel
   (`fetch`) / nothing.

Then one follow-up call, only for the family that needs it:

- Code editor → which one: Editor (VS Code-like) / IDE / Vim / Notebook.
- Operating system window → which one: Classic (90s) / Windows 11 / macOS.
- Retro → Handheld console / CRT amber / CRT green.
- Terminal → which Linux they use, as the accent: Ubuntu / Arch / Debian / Other. On "Other", offer
  Fedora / Mint / CachyOS / a plain color (cyan, green, amber or magenta). A distro sets its color and
  shows `user@<distro>` in the title bar.

Accents are keys of `ACCENTS` in `generate.py`; any of them works with `terminal`, `editor`, `ide`,
`vim`, `notebook`, `win11` and `macos`. `crt` takes a phosphor (`amber`, `green`). `classic` and
`handheld` have a fixed palette.

### Round 2: content (one AskUserQuestion call, after drafting from step 2)

1. **Featured work**: "Keep these 4: A, B, C, D (Recommended)" / "Let me swap some". On a swap,
   list up to 4 alternatives with one-line reasons.
2. **Signal tiles**: four of `repos`, `contributions`, `prs`, `stars`, `followers`, `production`.
   Recommend the four that look strongest in their data (low stars or followers look weak; skip
   them). Offer one alternative set.
3. **Existing README content** (only if step 2 found something worth keeping, such as a widget or a
   game): keep it at the bottom (`extra_sections`) / drop it.
4. **"Made with" link**: add a small line at the bottom pointing to this generator
   (`https://github.com/WaltherMoraRivera/github-profile-readme-generator`) / no. Purely optional.

### Round 3: texts (plain message)

Show, in one message, the drafts for: display name, role line, bio (about 180 characters), header
pills (4 to 6), each project's label, description (about 150 characters), stack (4 short items) and
status line, and the toolkit groups. Ask "anything to change?". Facts you inferred (job, school,
company, OS) must be confirmed, not assumed.

## 4. Header media

Skip if they chose a neofetch panel or nothing. Ask for the file path.

- **Animated GIF** (pixel art works best):
  ```bash
  python3 <skill>/scripts/frames.py <file.gif> data/portrait-sheet.png --bg <white|black|none> --native auto --height 450
  ```
  `--bg`: the GIF's solid background color, or `none` if it is already transparent. `--native auto`
  detects upscaled pixel art and keeps it sharp. Add `--fade-sides 0.12` if the figure is cut by
  the left and right edges, and `--colors 0` with it (a palette makes the fade look banded).
  Then set `portrait` = `data/portrait-sheet.png`, `portrait_frames` = `data/portrait-sheet.json`,
  `portrait_width` 220 to 300.
- **Still image with transparency** (PNG or WebP): use it as is in `portrait`.
- **Still image on a solid dark background**: `python3 <skill>/scripts/cutout.py <file> data/portrait.webp`.
- **Photo or JPEG**: use it as is; it fills the right side and fades into the card.

Show the result on a light and a dark background before going on. If the art is not theirs, add a
visible credit line in `credits` (required) and suggest telling the artist (good practice, not a
blocker). See the third-party art notes in `reference/lessons.md`.

## 5. Generate and preview

```bash
gh repo clone <login>/<login> ~/profile-readme 2>/dev/null || gh repo create <login>/<login> --public --clone
cd ~/profile-readme
mkdir -p scripts data
cp <skill>/scripts/generate.py scripts/
cp <skill>/templates/gitignore .gitignore
# write data/profile.json (see reference/configuration.md); copy header media into data/
python3 scripts/generate.py
```

`gh repo create` makes a public repository: ask before running it. GitHub shows the README of a
public repository named exactly like the account on the profile page.

Open `preview.html` (it imitates GitHub's README column). Check both themes (OS theme, or Chromium
DevTools → Rendering → "Emulate CSS prefers-color-scheme") and that the header animates. Fix text
running past a card edge or pills crowding the header by shortening text first. Show the preview
and wait for their OK.

## 6. Publish (ask once, with the full list)

Each item is public. List them, ask once, run only what they approve.

1. Commit and push `README.md assets data scripts .gitignore` (any old README stays in git history).
2. Missing descriptions or topics on the featured repos: `gh repo edit <owner>/<repo> --description "..." --add-topic a,b`.
   If a repo already has a description, ask before replacing it.
3. Weekly refresh: copy `templates/update-profile.yml` to `.github/workflows/`. It does nothing until
   they add a `PROFILE_TOKEN` secret (a read-only token they create themselves).

Only the user can do these (say so; do not try):
- Pin repositories: profile → "Customize your pins" (no API).
- Settings → Public profile → "Include private contributions on my profile".
- `gh auth refresh -s user` if they want you to edit their profile bio.

## 7. Verify and hand over

- `curl -sI https://raw.githubusercontent.com/<login>/<login>/main/assets/header.svg` returns 200.
- The profile page shows the README (Ctrl+F5 if images look old; GitHub caches them for minutes).
- Report what was published, what was skipped, and how to refresh later: edit `data/profile.json`,
  run `python3 scripts/generate.py`, push. Never edit `README.md` by hand; it is generated.

## Rules

- Ask before every outward action. Never create, store or print tokens.
- Never invent facts. If something is inferred, say so and ask.
- Before featuring a repo, skim it for anything that looks like a credential; flag it.
