#!/usr/bin/env python3
"""Turns OpenSpec changes into GitHub issues: one issue per change, with labels and milestone.

    python tools/openspec_issues.py            # dry run: shows what would be created
    python tools/openspec_issues.py --apply    # creates labels, milestones and missing issues
    python tools/openspec_issues.py --apply --project 1   # also adds them to org project #1

Metadata comes from each change's `.openspec.yaml` (x-milestone, x-type, x-area, x-priority,
x-model, x-effort). After creating an issue the script writes `x-issue: <number>` back, so running
it again never duplicates issues. Needs the GitHub CLI (`gh`) signed in. Standard library only.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = "ProfileStudio/ProfileStudio"
CHANGES = Path(__file__).resolve().parent.parent / "openspec" / "changes"
LABEL_COLORS = {
    "type": "1d76db", "area": "5319e7", "priority": "d93f0b", "model": "0e8a16", "effort": "fbca04",
}
PRIORITY_COLORS = {"high": "b60205", "medium": "d93f0b", "low": "f9d0c4"}
MILESTONES = {
    "v2.0 Maturity": "Foundations and the features that put ProfileStudio on par with, and ahead of, other profile tools.",
    "v2.x Showcase": "Visual editor and showcase features after v2.0.",
    "Internationalization": "Cards in 12 languages, in three waves, once the system is mature.",
    "Community": "Community health files, policies and contribution flow.",
}


def gh(*args, check=True):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode:
        sys.exit(f"gh {' '.join(args[:3])} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def read_meta(path):
    meta = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"([\w-]+):\s*(.*)", line)
        if m:
            meta[m.group(1)] = m.group(2).strip()
    return meta


def section(text, name):
    m = re.search(rf"^## {re.escape(name)}\n\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def labels_for(meta):
    return [f"{k}: {meta['x-' + k]}" for k in ("type", "area", "priority", "model", "effort") if meta.get("x-" + k)]


def body_for(cid, folder):
    proposal = (folder / "proposal.md").read_text(encoding="utf-8")
    tasks = (folder / "tasks.md").read_text(encoding="utf-8").split("\n", 1)[1].strip()
    tasks = re.sub(r"^## ", "### ", tasks, flags=re.M)
    parts = [f"> OpenSpec change: [`openspec/changes/{cid}`](https://github.com/{REPO}/tree/main/openspec/changes/{cid}). "
             "Edit the spec there; this issue mirrors it.",
             "## Why\n\n" + section(proposal, "Why"),
             "## What changes\n\n" + section(proposal, "What Changes"),
             "## Out of scope\n\n" + section(proposal, "Out of Scope")]
    if section(proposal, "Prior Art"):
        parts.append("## Prior art\n\n" + section(proposal, "Prior Art"))
    parts.append("## Tasks\n\n" + tasks)
    parts.append("## Planning\n\n" + section(proposal, "Planning"))
    return "\n\n".join(parts) + "\n"


def title_for(cid, folder):
    words = cid.replace("-", " ")
    return words[0].upper() + words[1:]


def ensure_labels(needed, apply):
    existing = {l["name"] for l in json.loads(gh("label", "list", "-R", REPO, "--limit", "200", "--json", "name"))}
    for name in sorted(needed - existing):
        kind, value = name.split(": ", 1)
        color = PRIORITY_COLORS.get(value) if kind == "priority" else LABEL_COLORS[kind]
        print(f"label  {name}")
        if apply:
            gh("label", "create", name, "-R", REPO, "--color", color, "--force")


def ensure_milestones(needed, apply):
    existing = {m["title"]: m["number"] for m in json.loads(gh("api", f"repos/{REPO}/milestones?state=all&per_page=100"))}
    for title in sorted(needed - set(existing)):
        print(f"milestone  {title}")
        if apply:
            gh("api", f"repos/{REPO}/milestones", "-f", f"title={title}", "-f", f"description={MILESTONES.get(title, '')}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apply", action="store_true", help="create things (default: dry run)")
    parser.add_argument("--project", type=int, help="number of the ProfileStudio org project to add issues to")
    args = parser.parse_args()

    changes = []
    for folder in sorted(p for p in CHANGES.iterdir() if p.is_dir() and p.name != "archive"):
        meta = read_meta(folder / ".openspec.yaml")
        changes.append((folder.name, folder, meta))
    ensure_labels({l for _, _, m in changes for l in labels_for(m)}, args.apply)
    ensure_milestones({m["x-milestone"] for _, _, m in changes if m.get("x-milestone")}, args.apply)

    # issues are numbered in this order: milestones as listed, foundations first, then by priority
    stage = {name: i for i, name in enumerate(MILESTONES)}
    kind = {"tooling": 0, "refactor": 1}
    order = {"high": 0, "medium": 1, "low": 2}
    for cid, folder, meta in sorted(changes, key=lambda c: (stage.get(c[2].get("x-milestone"), 9),
                                                           kind.get(c[2].get("x-type"), 2),
                                                           order.get(c[2].get("x-priority"), 3), c[0])):
        if meta.get("x-issue"):
            print(f"skip   {cid} (issue #{meta['x-issue']})")
            continue
        labels = labels_for(meta)
        print(f"issue  {cid}  [{', '.join(labels)}]  {meta.get('x-milestone', '')}")
        if not args.apply:
            continue
        cmd = ["issue", "create", "-R", REPO, "--title", title_for(cid, folder), "--body", body_for(cid, folder)]
        for l in labels:
            cmd += ["--label", l]
        if meta.get("x-milestone"):
            cmd += ["--milestone", meta["x-milestone"]]
        url = gh(*cmd)
        number = url.rstrip("/").rsplit("/", 1)[1]
        with open(folder / ".openspec.yaml", "a", encoding="utf-8") as f:
            f.write(f"x-issue: {number}\n")
        if args.project:
            gh("project", "item-add", str(args.project), "--owner", REPO.split("/")[0], "--url", url)
        print(f"       -> {url}")


if __name__ == "__main__":
    main()
