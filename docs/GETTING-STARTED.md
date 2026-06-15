# Getting Started with Synapse

## What Is This?

Synapse is a personal workflow system that helps you and Claude work as integrated co-workers on coding projects. It's built on shared understanding, not repeated instructions.

## Current State

**Phase 1 is complete:** You have a root CLAUDE.md, core skills, and templates ready to use.

## Setting Up a New Project

1. **Create the project directory:**
   ```bash
   mkdir ~/path/to/new-project
   cd ~/path/to/new-project
   git init
   ```

2. **Copy the CLAUDE.md template:**
   ```bash
   cp ../Synapse/docs/TEMPLATES/project-claude-template.md CLAUDE.md
   ```

3. **Customize CLAUDE.md for this project:**
   - Add project purpose
   - Specify boundaries (what Claude can/can't do)
   - Add architecture notes
   - Update skills that apply

4. **Create the project structure:**
   ```bash
   mkdir src tests docs
   ```

5. **Commit the initial setup:**
   ```bash
   git add CLAUDE.md
   git commit -m "init: project setup with CLAUDE.md"
   ```

## Working on a Project

1. **Describe the feature:** What should it do?
2. **Claude clarifies spec** (uses `synapse:speccing-first`)
3. **You approve spec**
4. **Claude builds** (writes tests, implements, commits)
5. **You review or Claude continues autonomously**

While you're on another project, Claude works independently within boundaries.

## After a Project

1. **Reflect together** (use checklist in `docs/EVOLUTION.md`)
2. **Identify patterns** to codify
3. **Update root CLAUDE.md or create skills** as needed
4. **Commit changes** so future projects inherit improvements

---

## Key Files

- `CLAUDE.md` (root) — Philosophy, baseline conventions, autonomy model
- `.claude/skills/synapse/` — Core skills (over-engineering guard, speccing-first, etc.)
- `docs/TEMPLATES/` — Template for per-project CLAUDE.mds
- `docs/EVOLUTION.md` — How to reflect and evolve the system
- `docs/superpowers/specs/` — Spec docs for Synapse itself
- `docs/superpowers/plans/` — Implementation plans

---

## Useful Commands

**See all Synapse skills:**
```bash
ls .claude/skills/synapse/
```

**Review root conventions:**
```bash
cat CLAUDE.md
```

**Set up a new project:**
```bash
cp docs/TEMPLATES/project-claude-template.md ~/new-project/CLAUDE.md
```

---

For questions or updates, see `docs/EVOLUTION.md` and `docs/superpowers/specs/2026-06-12-synapse-vision-design.md`.
