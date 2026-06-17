# Future Work

Ideas and design decisions captured from real working sessions. These should become GitHub issues once synapse has a remote.

---

## #1 — Global skill distribution via GitHub + junction

**Problem:** Skills currently live only inside the synapse directory. They aren't available in other projects without manual copying, which recreates the isolation problem synapse was built to solve.

**Design:**
- Synapse lives on GitHub (`AllHailSeizure/synapse`)
- A single bootstrapper skill (`synapse-init.md`) lives in `~/.claude/skills/` — placed once manually on any machine
- That skill clones synapse from GitHub and runs `synapse-deploy.ps1`
- `synapse-deploy.ps1` creates a Windows directory junction: `~/.claude/skills/synapse` → `D:\Libraries\synapse\.claude\skills\synapse`
- All skills are globally available from then on; edits in synapse reflect everywhere instantly

**Why junction over symlink:** Windows directory junctions don't require admin or Developer Mode. Functionally identical for this use case.

---

## #2 — Stop hook for automatic commits

**Problem:** Commits accumulate until a 400-file push happens. The issue isn't forgetting — it's that committing requires a conscious decision.

**Design:**
- Add a `Stop` hook to `~/.claude/settings.json`
- After every Claude response, if the working directory has uncommitted git changes, they surface in Claude's context
- Claude handles the commit proactively — the user never has to think about it

**Scope:** Global hook, applies to all projects.

---

## #3 — `/synapse-init` onboarding + recovery flow

**Problem:** Every new project starts cold. Every project that drifts requires a big conscious effort to reset.

**Design:**
- `/synapse-init` runs an onboarding flow: project type (game dev, web app, CLI, Devvit bot, etc.), which skill modules apply, naming conventions, folder structure preferences
- Outputs a project `CLAUDE.md` from the synapse template — session feels like week 3, not day 1
- **Recovery mode:** works retroactively on existing projects. Doesn't promise a full cleanup in one pass — establishes the standard, then cleanup happens opportunistically as files are touched

**Key principle:** cleanup is a side effect of normal work, not a scheduled task.

---

## #4 — Opportunistic cleanup as default behavior

**Problem:** Organizational debt drifts to the bottom of the priority list permanently.

**Design:**
- When Claude touches a file, apply naming/structure standards to anything in scope — not just the new code
- When Claude notices drift (bad variable names, scattered assets, dead code), flag it inline: "while we're here..."
- Never as a project, always as a side effect

**Why this works:** Takes organizational decisions off the user entirely. Claude maintains structure as a background process of normal work.

---

## #5 — Project-type skill modules

**Problem:** Not all synapse skills are relevant to all projects. A game dev project needs different defaults than a Devvit bot.

**Design:**
- Organize skills into modules by project type
- Onboarding flow selects relevant modules
- Per-project CLAUDE.md references only what applies

---

## Note on this document

This file was created mid-session when a conversation about synapse's design drifted away from the main task (llmphysics monorepo restructuring — issue #6). That drift is **exactly** what synapse is meant to address — and exactly the right moment to capture the ideas rather than lose them.

The pattern: a real working conversation surfaces a real problem, produces real design thinking, and that thinking gets logged here before it evaporates. When synapse has a GitHub remote, each item above becomes a GitHub issue. That's the evolution loop in practice.
