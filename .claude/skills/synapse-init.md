---
name: synapse-init
description: Set up or tear down Synapse skill symlinks in the current project. Run from project root.
type: behavior
---

# Synapse Init

Enables or disables Synapse skills for the current project via symlinks.

## Usage

Run one of these from the project root:

**Enable Synapse skills:**
```bash
bash D:\Libraries\Synapse\scripts\synapse-init.sh . enable
```

**Disable Synapse skills:**
```bash
bash D:\Libraries\Synapse\scripts\synapse-init.sh . disable
```

**Check status:**
```bash
bash D:\Libraries\Synapse\scripts\synapse-init.sh . status
```

## What It Does

- **enable** — Creates `.claude/skills/synapse/` as a symlink pointing to Synapse's canonical skills directory. All five core skills become available to the project.
- **disable** — Removes the symlink, reverting to project-local skills.
- **status** — Shows whether Synapse skills are currently linked.

## Why Symlinks?

Single source of truth. When Synapse skills are updated, all projects using symlinks get the updates automatically. No duplication, no sync issues.
