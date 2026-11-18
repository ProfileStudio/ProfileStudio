#!/usr/bin/env python3
"""Backs up and restores a GitHub profile repository with backup/* branches.

Run it inside the clone of <login>/<login>. Standard library only; needs git.

    python scripts/backup.py create [--no-push]   # branch backup/YYYY-MM-DD-HHMM from the remote's current state
    python scripts/backup.py list                 # backups with date, theme and commit message
    python scripts/backup.py restore NAME         # backs up the current state, then commits NAME's files on top

A backup keeps everything the profile had (README, images, data). Restoring never rewrites
history: it adds a new commit with the old files, so the restore itself can be undone. Nothing is
pushed by `restore`; push when the user approves.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

PREFIX = "backup/"


NETWORK = ("fetch", "push")
_GH = None


def gh_login():
    """True when the GitHub CLI is signed in; then git borrows its login for fetch and push."""
    global _GH
    if _GH is None:
        try:
            _GH = subprocess.run(["gh", "auth", "token"], capture_output=True, timeout=30).returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            _GH = False
    return _GH


def git(*args, check=True):
    cmd, env = ["git"], dict(os.environ)
    if args[0] in NETWORK:
        # Never wait for a password prompt nobody will answer: fail fast instead of hanging.
        env.update(GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
        if gh_login():  # use the gh login even where git has no credential helper of its own
            cmd += ["-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential"]
    try:
        r = subprocess.run(cmd + list(args), capture_output=True, text=True, encoding="utf-8", env=env,
                           timeout=180 if args[0] in NETWORK else 60)
    except subprocess.TimeoutExpired:
        sys.exit(f"git {args[0]} timed out. Check the connection, or run `gh auth login` and `gh auth setup-git`.")
    if check and r.returncode:
        hint = ""
        if args[0] in NETWORK and re.search(r"auth|credential|terminal prompts|403|401", r.stderr, re.I):
            hint = "\nSign in with `gh auth login` (the script then uses that login)."
        sys.exit(f"git {' '.join(args)} failed: {r.stderr.strip()}{hint}")
    return r.stdout.strip()


def default_branch():
    ref = git("symbolic-ref", "--quiet", "refs/remotes/origin/HEAD", check=False)
    if ref:
        return ref.rsplit("/", 1)[1]
    for name in ("main", "master"):
        if git("rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{name}", check=False):
            return name
    return None


def fetch():
    git("fetch", "--quiet", "origin", f"+refs/heads/*:refs/remotes/origin/*")


def describe(ref):
    """Theme of a backup: the generator's profile.json if it had one, else a plain README."""
    raw = git("show", f"{ref}:data/profile.json", check=False)
    if raw:
        try:
            cfg = json.loads(raw.lstrip("﻿"))
            return f"theme {cfg.get('theme', 'terminal')}" + (f", accent {cfg['accent']}" if cfg.get("accent") else "")
        except ValueError:
            pass
    return "README not made by this generator"


def create(push=True):
    fetch()
    base = default_branch()
    if not base:
        print("Nothing to back up: the repository has no commits yet.")
        return None
    same = git("for-each-ref", "--points-at", f"origin/{base}", "--format=%(refname:short)",
               "refs/remotes/origin/backup", "refs/heads/backup").split()
    if same:  # this exact state is already saved
        name = same[0].removeprefix("origin/")
        if push and not any(ref.startswith("origin/") for ref in same):  # saved before with --no-push
            git("push", "--quiet", "origin", name)
        print(f"Already backed up as {name} ({describe(same[0])})")
        return name
    name = PREFIX + dt.datetime.now().strftime("%Y-%m-%d-%H%M")
    existing = set(git("for-each-ref", "--format=%(refname:short)", "refs/heads/backup", "refs/remotes/origin/backup").split())
    n, candidate = 1, name
    while candidate in existing or f"origin/{candidate}" in existing:
        n += 1
        candidate = f"{name}-{n}"
    git("branch", candidate, f"origin/{base}")
    if push:
        git("push", "--quiet", "origin", candidate)
    print(f"Backup {candidate} ({describe(candidate)}){'' if push else ' (local only)'}")
    return candidate


def backups():
    fetch()
    out = git("for-each-ref", "--sort=-refname", "--format=%(refname:short)\t%(committerdate:short)\t%(subject)",
              "refs/remotes/origin/backup")
    seen, rows = set(), []
    for line in filter(None, out.splitlines()):
        ref, date, subject = line.split("\t", 2)
        name = ref.removeprefix("origin/")
        seen.add(name)
        rows.append((name, date, describe(ref), subject))
    for name in git("for-each-ref", "--sort=-refname", "--format=%(refname:short)", "refs/heads/backup").split():
        if name not in seen:  # created with --no-push
            rows.append((name, git("log", "-1", "--format=%cs", name), describe(name) + ", local only",
                         git("log", "-1", "--format=%s", name)))
    return rows


def list_backups():
    rows = backups()
    if not rows:
        print("No backups yet.")
    for name, date, desc, subject in rows:
        print(f"{name}\t{date}\t{desc}\t{subject}")


def restore(name):
    if not name.startswith(PREFIX):
        name = PREFIX + name
    if git("status", "--porcelain"):
        sys.exit("The working tree has uncommitted changes; commit or discard them first.")
    names = {row[0] for row in backups()}
    if name not in names:
        sys.exit(f"No backup named {name}. Run `list` to see them.")
    ref = name if git("rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{name}", check=False) == "" else f"origin/{name}"
    base = default_branch()
    safety = create()  # the current profile, so the restore can be undone
    git("checkout", "--quiet", base)
    git("merge", "--quiet", "--ff-only", f"origin/{base}")
    git("rm", "-r", "-q", "--ignore-unmatch", ".")
    git("checkout", ref, "--", ".")
    git("commit", "--quiet", "-m", f"restore: profile from {name}")
    print(f"Restored {name} as a new commit on {base} (not pushed). The previous state is in {safety}.")
    print(f"Publish with: git push origin {base}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create", help="back up the profile as it is on GitHub now")
    c.add_argument("--no-push", action="store_true", help="keep the backup branch local")
    sub.add_parser("list", help="list backups")
    r = sub.add_parser("restore", help="bring back a backup as a new commit")
    r.add_argument("name", help="backup name, with or without the backup/ prefix")
    args = parser.parse_args()
    if not git("rev-parse", "--is-inside-work-tree", check=False):
        sys.exit("Run this inside the profile repository clone.")
    if args.cmd == "create":
        create(push=not args.no_push)
    elif args.cmd == "list":
        list_backups()
    else:
        restore(args.name)


if __name__ == "__main__":
    main()
