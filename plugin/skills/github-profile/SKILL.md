---
name: github-profile
description: Design, preview and publish a visual GitHub profile README made of SVG cards with live GitHub data (header with optional animated image or GIF, profile signal, selected work, language stack, toolkit, contribution heatmap), with a quick or a custom setup, and back up or restore earlier versions of the profile. Use when the user wants to create, redesign or refresh their GitHub profile README, says "set up my GitHub profile", or wants to see, keep or go back to a previous version of it.
---

# GitHub profile README generator

Build a profile README in the user's `<login>/<login>` repository. Every visual is an SVG made by
`scripts/generate.py` from `data/profile.json` plus live GitHub API data. Each SVG carries its own
light and dark palette, so one file follows the viewer's theme.

Talk to the user in the language they write in. After the theme, they pick a **quick setup** (you
decide everything from their data and show a preview) or a **custom setup** (they decide content,
texts and header). Read `reference/lessons.md` before step 5. If they only want to see or bring back
an earlier version of their profile, go to step 8.

## Files

| Path | Purpose |
|---|---|
| `scripts/generate.py` | Generator (Python 3.9+, standard library only). Writes `assets/*.svg`, `README.md`, `preview.html`. |
| `scripts/frames.py` | Animated GIF to transparent sprite sheet, for an animated header (Pillow). |
| `scripts/cutout.py` | Removes a solid dark background from a still illustration (Pillow + numpy). |
| `scripts/backup.py` | Backs up the profile repository to `backup/<date>` branches, lists and restores them (git only). |
| `templates/profile.example.json` | Starting point for `data/profile.json`. |
| `templates/update-profile.yml` | Optional weekly refresh workflow (needs a `PROFILE_TOKEN` secret). |
| `templates/gitignore` | Copy as `.gitignore`. |
| `reference/configuration.md` | Every `profile.json` key. |
| `reference/styles/<theme>-<dark|light>.jpg` | Screenshots of the 13 themes, to show the user in step 3. |
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
gh api repos/<login>/<login>/contents/data/profile.json --jq .content | base64 -d   # made by this generator?
gh api user/orgs --jq '.[].login'                               # org repos can be featured too
```

Pick 6 to 8 candidate projects (pinned first, then stars, commit count, recent pushes, a real
README). Read the first lines of each candidate's README: descriptions must come from there.
Never invent features, numbers or job titles.

## 3. Configuration questions

### Round 1: style and setup mode

People like a theme that looks like the system or tool they use every day. 13 themes exist:

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
| `browser` | Browser window: address bar, headings highlighted like the element inspector | Web and frontend developers |
| `sql` | Database console: headings as queries, cards as result sets | Backend and data people |
| `git` | Commit graph in the gutter, headings as commits with hash and refs | Anyone; open source maintainers |

Read `reference/styles/<theme>-dark.jpg` for the candidates so the user sees them. Then ask in one
AskUserQuestion call (an option list holds at most 4 entries, so the style is split in two steps):

1. **Style family**: Terminal and tools / Code editor / Window / Retro. Recommend from what
   step 2 shows: Linux tooling suggests terminal, mostly web code suggests editor or browser,
   databases suggest sql, notebooks suggest notebook, a pixel-art header suggests retro.
2. **Setup mode**, explained like an installer's "express or custom" screen. When step 2 found a
   `data/profile.json` (a profile made by this generator), add a first option and recommend it:
   - **Keep my content, change the style (Recommended)**: "I keep your texts, projects, stats and
     header and only apply the new theme, with the latest generator." Then skip the follow-up
     content questions, update `generate.py`, change `theme` (and `accent`: drop it or set the new
     theme's default, unless they picked one), and go to step 5.
   - **Quick (Recommended)**: "I pick your projects, stats and texts from your GitHub data and show
     you a preview. You approve it, change something, or switch to custom. Nothing is published
     without your OK."
   - **Custom**: "You choose the language, featured projects, stats, header image and every text,
     step by step."

Then one follow-up call with what applies (up to four questions):

- Code editor → which one: Editor (VS Code-like) / IDE / Vim / Notebook.
- Window → which one: Classic (90s) / Windows 11 / macOS / Browser.
- Terminal and tools → which one: Shell terminal / Database console (`sql`) / Git log (`git`).
- Retro → Handheld console / CRT amber / CRT green.
- Shell terminal (asked in one more call, since it depends on the answer above) → which Linux they use, as the accent: Ubuntu / Arch / Debian / Other. On "Other", offer
  Fedora / Mint / CachyOS / a plain color (cyan, green, amber or magenta). A distro sets its color and
  shows `user@<distro>` in the title bar.

- Quick → **header image**, the only content question: "I have an animated GIF / I have an image /
  No, use an info panel". For a file, ask its path next (step 4); with none, build `fetch` from their
  data (top languages, public repos, years on GitHub, location if public).
- Custom → **language** of the README (English / Spanish, `en` / `es`), **right side of the
  header** (an animated GIF / a still image / a neofetch-style info panel `fetch` / nothing) and
  **colors**: "The theme's own (Recommended)" / "My own accent color" (level 1) / "Fine-tune the
  theme's colors" (level 2). On either of the last two, follow "Own colors" below.

Accents are keys of `ACCENTS` in `generate.py`; any of them works with `terminal`, `editor`, `ide`,
`vim`, `notebook`, `win11`, `macos`, `browser`, `sql` and `git`. `crt` takes a phosphor (`amber`, `green`). `classic` and
`handheld` have a fixed palette.

**Own colors.** When the user names colors, a brand or a mood ("black and silver", "my company's
blue"), do not edit `generate.py`: use `accent` as a color (level 1) and `theme_overrides` (level 2),
both in `reference/configuration.md`. Propose the palette as hex values for light and dark, ask
whether it should follow the viewer's theme or always be dark, and fix every `contrast warning` the
generator prints before the preview. A profile whose `scripts/generate.py` differs from the
official one (step 2) is a fork: offer to move its color changes into `profile.json` so it gets
updates again, and say what cannot move (new drawings need code).

### Quick setup: decide, then preview

Skip rounds 2 and 3. Decide with the same rules they use, and list every choice in one short
message with the preview (step 5):

- Language: the one the user writes in (`en` or `es`; English for any other).
- Featured work: the top 4 candidates from step 2. Signal tiles: the four strongest in their data.
- Texts: name and bio from their GitHub profile; role from their bio, company or pinned READMEs,
  never invented (with nothing to go on, describe what they build: "Full-stack developer").
  Project labels, descriptions, stacks and statuses from each README. Pills and toolkit from their
  languages, repository topics and READMEs.
- Existing README content worth keeping (widget, game): keep it at the bottom and say so.
- The "made with" badge stays on (the default). Say so in the summary: "I added a small badge at
  the bottom that links to the generator; tell me if you want it gone" (`"made_with": false`).

Then ask in one AskUserQuestion call: **Publish this (Recommended)** / **Change something** (they
say what; apply it and preview again) / **Switch to custom** (ask the language, then continue with
round 2, keeping the theme and header). Publishing still goes through step 6.

### Custom setup: rounds 2 and 3

Ask these when they chose custom, or switched to it from the quick preview.

### Round 2: content (one AskUserQuestion call, after drafting from step 2)

1. **Featured work**: "Keep these 4: A, B, C, D (Recommended)" / "Let me swap some". On a swap,
   list up to 4 alternatives with one-line reasons.
2. **Signal tiles**: four of `repos`, `contributions`, `prs`, `stars`, `followers`, `production`.
   Recommend the four that look strongest in their data (low stars or followers look weak; skip
   them). Offer one alternative set.
3. **Existing README content** (only if step 2 found something worth keeping, such as a widget or a
   game): keep it at the bottom (`extra_sections`) / drop it.
4. **"Made with" badge**: a small badge at the bottom right, drawn in the profile's own theme,
   links to this generator. "Keep it (Recommended)" / "Remove it" (`"made_with": false`). Never add
   it as a `credits` line: the generator draws it.

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
DevTools → Rendering → "Emulate CSS prefers-color-scheme") and that the header animates. In a
built-in browser pane that cannot inspect `file://` pages, serve the folder and open
`http://localhost:8765/preview.html`, then stop the server when done:

```bash
python3 -m http.server 8765 --directory ~/profile-readme   # run it in the background; pass the folder explicitly
```
 Fix text
running past a card edge or pills crowding the header by shortening text first. Show the preview
and wait for their OK.

## 6. Publish (ask once, with the full list)

Each item is public. List them, ask once, run only what they approve.

0. **Backup first, always** (not a choice; say it is included): if the repository already has
   commits, run `python3 <skill>/scripts/backup.py create` inside the clone before pushing. It saves
   the profile as it is on GitHub now to a `backup/<date>` branch of the same repository (public,
   like the repository) and does nothing when that state is already saved. Tell them the branch name.
1. Commit and push `README.md assets data scripts .gitignore`. If `git push` hangs or asks for a
   password (no credential helper on that machine), push with the `gh` login instead of waiting:
   `git -c credential.helper= -c "credential.helper=!gh auth git-credential" push`. `backup.py`
   already does this on its own.
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
- The profile page shows the README. Image paths carry `?v=<hash>` of each file, so a push shows the
  new cards at once; if one still looks old, Ctrl+F5.
- Report what was published, what was skipped, the backup branch, and how to refresh later: edit
  `data/profile.json`, run `python3 scripts/generate.py`, push. Never edit `README.md` by hand; it is
  generated. To go back, they can ask you to restore a backup (step 8).

## 8. Backups: list and restore

When the user wants to see earlier versions or go back to one:

1. Clone or update their profile repository (`gh repo clone <login>/<login>`, or `git pull`).
2. `python3 <skill>/scripts/backup.py list` prints each backup's name, date, theme and last commit
   message. Show them as a short table and ask which one (AskUserQuestion with up to 4, newest first;
   more on request).
3. `python3 <skill>/scripts/backup.py restore <name>` first backs up the current profile, then adds
   a commit to the default branch with the chosen backup's files. History is never rewritten, so the
   restore itself can be undone the same way.
4. Show the restored README (run `python3 scripts/generate.py` for a fresh preview if the backup
   has `data/profile.json`; its cards will show today's numbers), then ask before
   `git push origin <default branch>`.

Backups are branches, so deleting old ones is `git push origin --delete backup/<date>`; only do it
when they ask, naming each branch first.

## Rules

- Ask before every outward action. Never create, store or print tokens.
- Never invent facts. If something is inferred, say so and ask.
- Before featuring a repo, skim it for anything that looks like a credential; flag it.
