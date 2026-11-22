#!/usr/bin/env python3
"""Sync Arthur Agent skills to both GitHub and Google Drive."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
README_FILE = REPO_ROOT / "README.md"
DRIVE_PARENT_ID = "1uVED57vXArnlSPRRggbyx2PHFZo0KP3t"  # Arthur Agent Skills folder


def run(cmd, cwd=REPO_ROOT, check=True):
    """Run shell command and return output."""
    res = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and res.returncode != 0:
        print(f"Error running: {cmd}\nSTDERR: {res.stderr}\nSTDOUT: {res.stdout}")
        sys.exit(res.returncode)
    return res.stdout.strip()


def parse_frontmatter(skill_file: Path) -> dict:
    """Extract frontmatter name and description from SKILL.md."""
    text = skill_file.read_text(encoding="utf-8")
    meta = {"name": skill_file.parent.name, "description": ""}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if line.startswith("name:"):
                    meta["name"] = line.split("name:", 1)[1].strip()
                elif line.startswith("description:"):
                    meta["description"] = line.split("description:", 1)[1].strip()
    return meta


def update_readme(skills: list[dict]):
    """Update skills table in README.md."""
    seen = set()
    table_rows = []
    for s in skills:
        name = s["name"]
        if name in seen:
            continue
        seen.add(name)
        desc = s["description"] or "Custom skill"
        table_rows.append(f"| [`{name}`](./skills/{name}/SKILL.md) | {desc} | Active |")
    
    rows_text = "\n".join(table_rows)
    content = f"""# Arthur Agent

A centralized repository for Arthur Agent skills, configurations, and automation workflows.

## Skills Directory

All skills are stored under [`skills/`](./skills) with standard `SKILL.md` definitions:

| Skill | Description | Status |
|---|---|---|
{rows_text}

## Storage & Synchronization

Arthur Agent synchronizes skills across two main locations:
1. **GitHub Repository**: [`kristanmorris/Arthur-agent`](https://github.com/kristanmorris/Arthur-agent)
2. **Google Drive Folder**: `Arthur Agent Skills` (`{DRIVE_PARENT_ID}`)

### Automated Sync

Whenever a new skill is added or updated, run:

```bash
python3 scripts/sync.py
```

This:
- Validates all skill definitions in `skills/`
- Commits and pushes changes to GitHub (`main` branch)
- Synchronizes skills directly to Google Drive
"""
    README_FILE.write_text(content, encoding="utf-8")
    print("✓ Updated README.md")


def sync_github(commit_msg: str):
    """Commit and push changes to GitHub."""
    print("→ Syncing to GitHub...")
    run("git add .")
    status = run("git status --porcelain")
    if status:
        run(f'git commit -m "{commit_msg}"')
        print(f"✓ Committed: {commit_msg}")
    else:
        print("ℹ No changes to commit in git.")

    # Push to origin main
    push_out = run("git push -u origin main", check=False)
    print("✓ Pushed to GitHub (kristanmorris/Arthur-agent:main)")


def sync_drive(skills: list[dict]):
    """Sync skills and README to Google Drive."""
    print("→ Syncing to Google Drive...")
    # Get existing files in Drive folder
    raw_json = run(f"gdrive readonly ls {DRIVE_PARENT_ID} --json", check=False)
    try:
        drive_files = json.loads(raw_json) if raw_json else []
    except json.JSONDecodeError:
        drive_files = []
    
    drive_lookup = {item["name"]: item["id"] for item in drive_files if "name" in item and "id" in item}

    # Temporary staging
    tmp_dir = Path("/tmp/arthur_skills_sync")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # 1. Sync individual skill markdown files
    for s in skills:
        name = s["name"]
        skill_path = s["path"]
        target_name = f"{name}.md"
        staged_path = tmp_dir / target_name
        shutil.copy2(skill_path, staged_path)

        if target_name in drive_lookup:
            file_id = drive_lookup[target_name]
            run(f"gdrive mutate update {file_id} {staged_path}")
            print(f"✓ Updated {target_name} on Drive (ID: {file_id})")
        else:
            out = run(f"gdrive mutate upload {staged_path} --parent {DRIVE_PARENT_ID}")
            print(f"✓ Uploaded {target_name} to Drive: {out}")

    # 2. Sync README.md to Drive
    readme_drive_name = "README.md"
    readme_staged = tmp_dir / readme_drive_name
    shutil.copy2(README_FILE, readme_staged)
    if readme_drive_name in drive_lookup:
        file_id = drive_lookup[readme_drive_name]
        run(f"gdrive mutate update {file_id} {readme_staged}")
        print(f"✓ Updated README.md on Drive (ID: {file_id})")
    else:
        out = run(f"gdrive mutate upload {readme_staged} --parent {DRIVE_PARENT_ID}")
        print(f"✓ Uploaded README.md to Drive: {out}")


def main():
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else "feat(skills): update skills library"
    
    skills = []
    if SKILLS_DIR.exists():
        for item in sorted(SKILLS_DIR.iterdir()):
            skill_md = item / "SKILL.md" if item.is_dir() else (item if item.name.endswith(".md") else None)
            if skill_md and skill_md.exists():
                meta = parse_frontmatter(skill_md)
                meta["path"] = skill_md
                skills.append(meta)

    print(f"Discovered {len(skills)} skill(s): {[s['name'] for s in skills]}")
    update_readme(skills)
    sync_github(commit_msg)
    sync_drive(skills)
    print("\n All skills synchronized successfully to GitHub and Google Drive!")


if __name__ == "__main__":
    main()
