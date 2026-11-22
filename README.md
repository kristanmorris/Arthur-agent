# Arthur Agent

A centralized repository for Arthur Agent skills, configurations, and automation workflows.

## Skills Directory

All skills are stored under [`skills/`](./skills) with standard `SKILL.md` definitions:

| Skill | Description | Status |
|---|---|---|
| [`ecc`](./skills/ecc/SKILL.md) | Harness-native engineering system providing structured test-driven development (TDD), implementation planning, code reviews, build repairs, security scanning (AgentShield), and multi-agent coordination. | Active |
| [`file-organizer`](./skills/file-organizer/SKILL.md) | Intelligently organizes your files and folders across your computer by understanding context, finding duplicates, suggesting better structures, and automating cleanup tasks. Reduces cognitive load and keeps your digital workspace tidy without manual effort. | Active |
| [`windows-mcp`](./skills/windows-mcp/SKILL.md) | Control and automate the Windows operating system using the Windows-MCP server for desktop UI automation, accessibility tree inspection, mouse and keyboard simulation, app management, PowerShell, and system tasks. | Active |

## Storage & Synchronization

Arthur Agent synchronizes skills across two main locations:
1. **GitHub Repository**: [`kristanmorris/Arthur-agent`](https://github.com/kristanmorris/Arthur-agent)
2. **Google Drive Folder**: `Arthur Agent Skills` (`1uVED57vXArnlSPRRggbyx2PHFZo0KP3t`)

### Automated Sync

Whenever a new skill is added or updated, run:

```bash
python3 scripts/sync.py
```

This:
- Validates all skill definitions in `skills/`
- Commits and pushes changes to GitHub (`main` branch)
- Synchronizes skills directly to Google Drive
