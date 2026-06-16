# Synapse: Operational & Setup Guide

This document covers how Synapse is set up and operated—technical details for getting projects wired into the system.

---

## Project Setup: synapse-init

Every project that uses Synapse needs its skills symlinked. Use `synapse-init` to manage this.

### Enable Synapse for a Project

Run from the project root:

```bash
bash D:\Libraries\Synapse\scripts\synapse-init.sh . enable
```

This creates `.claude/skills/synapse/` as a symlink to Synapse's canonical skills. All five core skills become available.

### Disable Synapse for a Project

```bash
bash D:\Libraries\Synapse\scripts\synapse-init.sh . disable
```

Removes the symlink. Use if you're removing the project from Synapse.

### Check Status

```bash
bash D:\Libraries\Synapse\scripts\synapse-init.sh . status
```

Shows whether Synapse skills are linked.

---

## Why Symlinks?

Single source of truth. When skills are updated in Synapse, all projects using symlinks get the updates automatically. No duplication, no sync issues, no maintenance burden.

---

## Skills Organization

**Root skills** (canonical, live in Synapse):
- `.claude/skills/synapse-init.md` — Setup/teardown skill
- `.claude/skills/synapse/over-engineering-guard.md` — YAGNI enforcement
- `.claude/skills/synapse/speccing-first.md` — Spec clarification
- `.claude/skills/synapse/testing-preferences.md` — Testing philosophy
- `.claude/skills/synapse/code-review-standards.md` — Code review approach
- `.claude/skills/synapse/autonomous-work-boundaries.md` — Decision boundaries

**Per-project skills** (if any):
- Projects can add local skills to `.claude/skills/` as needed
- These don't conflict with Synapse skills

---

## File Structure

```
Synapse/
├── CLAUDE.md (root philosophy & conventions)
├── .claude/
│   ├── CLAUDE.md (this file — operational details)
│   └── skills/
│       ├── synapse-init.md
│       └── synapse/ (five core skills)
├── scripts/
│   └── synapse-init.sh (setup script)
├── docs/
│   ├── TEMPLATES/
│   │   └── project-claude-template.md
│   ├── EVOLUTION.md
│   ├── GETTING-STARTED.md
│   └── superpowers/
│       ├── specs/ (design docs)
│       └── plans/ (implementation plans)
└── [projects inherit from root CLAUDE.md]
```

---

## Getting Started

1. Create a new project or navigate to an existing one
2. Copy `.claude/CLAUDE.md` template from Synapse, customize it
3. Run `synapse-init.sh . enable` to link skills
4. Start working with spec-first, YAGNI enforcement, and autonomous integration

---

**Last updated:** 2026-06-15
