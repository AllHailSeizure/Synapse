---
name: synapse-init
description: Set up or tear down Synapse skills in the current project by cloning from GitHub. Run from project root.
type: behavior
---

# Synapse Init

Enables or disables Synapse skills for the current project using a GitHub clone.

## Usage

### Enable Synapse skills

1. Clone (or pull) the Synapse repo to a local cache:
   ```powershell
   if (Test-Path "$HOME\.claude\synapse") {
     git -C "$HOME\.claude\synapse" pull
   } else {
     git clone https://github.com/AllHailSeizure/synapse "$HOME\.claude\synapse"
   }
   ```

2. Create a junction from the project's skills directory to the cloned repo:
   ```powershell
   New-Item -ItemType Directory -Force ".claude\skills" | Out-Null
   New-Item -ItemType Junction -Path ".claude\skills\synapse" -Target "$HOME\.claude\synapse\.claude\skills\synapse"
   ```

### Disable Synapse skills

```powershell
Remove-Item ".claude\skills\synapse" -Force
```

### Check status

```powershell
Test-Path ".claude\skills\synapse"
```

## What It Does

- **enable** — Clones Synapse from GitHub into `~/.claude/synapse` (or pulls if already present), then creates a directory junction at `.claude/skills/synapse` pointing to the cloned skills. All five core skills become available to the project.
- **disable** — Removes the junction, reverting to project-local skills only.
- **status** — Checks whether the junction exists.

## Why GitHub?

Single source of truth that works on any machine. Cloning once into `~/.claude/synapse` means all projects on the machine share the same skill cache. Updates flow in via `git pull`.
