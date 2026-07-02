# Goal Dashboard — CLAUDE.md

**Inherits from:** Root CLAUDE.md in Synapse
**Project purpose:** VS Code extension that shows GitHub Milestones/Issues (as used by the goal-oriented-development skill) in a sidebar, and lets you view/edit an issue's goal-writer-template fields in an editable panel, saving back to GitHub directly.
**Status:** In development (validation experiment — small and disposable by design)

---

## Overview

Synapse's `goal-oriented-development` skill (see `.claude/skills/synapse/goal-oriented-development/`, currently on branch `feat/goal-oriented-development-skill`) structures work as GitHub Milestones containing Issues written in a fixed markdown template. Today that content is only visible/editable by asking Claude or going to github.com. This extension is a minimal "view + edit gate": a TreeView of open milestones/issues, and a webview panel that parses an issue body against the fixed template and lets you edit fields (including checklist checkboxes) and save straight back to the GitHub issue via the REST API. GitHub Issues stays the single source of truth — no local storage, no sync.

---

## Project-Specific Conventions

- TypeScript throughout; VS Code Extension API (`vscode` module) + `@octokit/rest` for GitHub access.
- No webview bundler — webview HTML/JS is a plain template string in `webview/issueDetailPanel.ts`. Revisit only if the form grows enough to need componentization.
- `template/parser.ts` and `template/serializer.ts` must stay pure functions (no `vscode` or network imports) — that's what makes them unit-testable; don't let I/O leak into them.
- Test framework: Vitest, for pure-function unit tests only (see Known Issues below for what's intentionally untested).

---

## Boundaries for This Project

**Claude can work autonomously on:**
- [ ] Writing implementations that match spec
- [ ] Refactoring code for efficiency
- [ ] Running unit tests and verification
- [ ] Creating commits
- [ ] Wiring up TreeView/WebviewPanel per this plan

**Claude needs approval for:**
- [ ] Adding dependencies beyond `@octokit/rest` and Vitest (e.g. a webview bundler, a UI framework)
- [ ] Major architecture changes (e.g. moving to a webview-only UI, adding local storage/sync)
- [ ] Adding issue/milestone creation from the UI (explicitly out of scope for this pass)
- [ ] Setting up `@vscode/test-electron` / Extension Test Runner (deferred; revisit only if this experiment validates)

**Claude is blocked from:**
- [ ] Publishing the extension to the VS Code Marketplace
- [ ] Adding any Claude Code hook/session integration

---

## How This Project Uses Skills

This project uses these Synapse skills:

- `synapse:speccing-first` — How we clarify intent before building
- `synapse:testing-preferences` — Testing approach (adapted here: pure-function unit tests only, integration tests deferred — see Known Issues)
- `synapse:code-review-standards` — How feedback works
- `synapse:autonomous-work-boundaries` — Decision boundaries

No customizations beyond what's noted above.

---

## Key Context

### Architecture

Sidebar TreeView (`tree/milestonesTreeProvider.ts`) lists open milestones and their open issues, fetched via `github/client.ts` on activation and on manual refresh, cached in memory only. Selecting an issue opens a `WebviewPanel` (`webview/issueDetailPanel.ts`) that runs the issue body through `template/parser.ts`; if it matches the goal-writer template it renders editable structured fields (including an interactive checklist), otherwise it falls back to a raw-markdown textarea. Saving reassembles the fields via `template/serializer.ts` and PATCHes the issue through `github/client.ts`, after a lightweight `updated_at` check to warn on remote changes since load (last-write-wins with confirmation, no field-level merge).

### What's In Flight

Initial build per the plan in this file's originating design session (2026-07-02).

### Known Issues / Constraints

- Template parsing is intentionally binary (full structured parse or full raw-text fallback) — no partial-field fallback. If this proves too coarse in practice, that's a signal worth reflecting on, not a bug to silently patch around.
- No `@vscode/test-electron` integration test suite yet — tree/webview/auth/PATCH behavior is manually verified. Deferred deliberately given this project's validation-experiment scope; add if the experiment continues past this pass.
- Depends on the `goal-oriented-development` skill's exact template staying stable; if that template changes, `parser.ts`/`serializer.ts` need corresponding updates.

---

## How We Work on This Project

1. **You describe a feature.** What should it do?
2. **Claude clarifies spec.** Questions, proposed approaches, scope check.
3. **You approve spec.** Or iterate until aligned.
4. **Claude builds.** Spec-compliant implementation with tests.
5. **You review.** Approve or ask for changes.
6. **Claude commits.** Submits changes.

---

## Reflection (Post-Project)

After this validation pass, reflect: was the sidebar+webview split worth it? Did the binary parse-fallback hold up? Is this worth extending (issue creation from UI, integration tests) or was the answer "not worth it"? Log the answer in `docs/EVOLUTION.md` per Synapse's evolution loop.

---

**Last updated:** 2026-07-02
