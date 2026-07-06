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

3. Create a **user-level** (not project-level) junction for Synapse's registered custom agents, if
   it doesn't already exist. This only needs to happen once per machine, not once per project —
   some skills (e.g. `goal-oriented-development`) depend on custom agent types (`codebase-explorer`,
   `goal-surveyor`, `goal-writer`, `goal-fulfiller`) that must live under `~/.claude/agents/` to be
   discoverable at all, and that location is already global to every project on the machine:
   ```powershell
   New-Item -ItemType Directory -Force "$HOME\.claude\agents" | Out-Null
   if (-not (Test-Path "$HOME\.claude\agents\synapse")) {
     New-Item -ItemType Junction -Path "$HOME\.claude\agents\synapse" -Target "$HOME\.claude\synapse\.claude\agents\synapse"
   }
   ```

### Disable Synapse skills

```powershell
Remove-Item ".claude\skills\synapse" -Force
```

This only removes the per-project skills junction. It deliberately does **not** touch
`~/.claude/agents/synapse` — that junction is shared machine-wide, and other projects may still
depend on it. There's no per-project "disable" for the agents junction; removing it is a
machine-wide decision (`Remove-Item "$HOME\.claude\agents\synapse" -Force`), only worth doing if
you're done with Synapse everywhere, not just in one project.

### Check status

```powershell
Test-Path ".claude\skills\synapse"
Test-Path "$HOME\.claude\agents\synapse"
```

## What It Does

- **enable** — Clones Synapse from GitHub into `~/.claude/synapse` (or pulls if already present),
  then creates a directory junction at `.claude/skills/synapse` pointing to the cloned skills (all
  five core skills become available to the project), and ensures the user-level
  `~/.claude/agents/synapse` junction exists (machine-wide, created once, reused by every project).
- **disable** — Removes the per-project skills junction, reverting to project-local skills only.
  Leaves the machine-wide agents junction alone.
- **status** — Checks whether both junctions exist.

## Why GitHub?

Single source of truth that works on any machine. Cloning once into `~/.claude/synapse` means all projects on the machine share the same skill cache. Updates flow in via `git pull`.
