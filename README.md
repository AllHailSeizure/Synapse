# Synapse

Synapse is a personal workflow system for Claude Code and Codex. It keeps
software work deliberate with concise skills, visible evidence, and gates that
scale with risk instead of ceremony.

## Current skill suite

The shared skills live in `skills/` and cover:

- proportional thinking and implementation plans;
- testing, verification, debugging, and code review;
- worktree isolation and bounded subagent delegation;
- finishing branches with verification, push, and pull request creation;
- user-directed GitHub issues and sticky-note bug capture;
- autonomous-work boundaries between user intent and agent execution; and
- report-only surveys of what a repo accumulates on its own — asset churn in a
  branch, worktree and branch sprawl.

See [`skills/README.md`](skills/README.md) for the complete inventory and the
skills that were intentionally dropped or replaced.

## Claude-compatible installation

The shared skills and commands can be copied into the local Claude-compatible
configuration directories:

```powershell
powershell -Command "'.claude','.cursor' | % { Copy-Item 'D:\Libraries\Synapse\skills\*' \"$env:USERPROFILE\$_\skills\" -Recurse -Force; Copy-Item 'D:\Libraries\Synapse\commands\*.md' \"$env:USERPROFILE\$_\commands\" -Force }"
```

The Claude root guidance is in [`CLAUDE.md`](CLAUDE.md), and the Claude agent
adapters are in `agents/`.

The `/bug` command is defined in [`commands/bug.md`](commands/bug.md) and
delegates to the capture-only `bug-capture` skill. The command index is in
[`commands/README.md`](commands/README.md).

## Per-repo configuration

Two kinds of repo-specific configuration live in the repos Synapse operates on,
not in Synapse itself:

- `SYNAPSE.md` at the repo root — the flat manifest the bandaids read at Gate 0.
  Template: [`docs/TEMPLATES/SYNAPSE.md`](docs/TEMPLATES/SYNAPSE.md).
- `.synapse/weedeat.toml` — structured input for the `/weedeat` survey skills:
  which extensions count as assets, where worktrees live, which regenerated
  files carry no work. Template:
  [`docs/TEMPLATES/weedeat.toml`](docs/TEMPLATES/weedeat.toml).

Both skills run without the config file, on generic defaults, and say so in
their own output.

## Codex plugin installation

The repository also contains the Codex package manifest at
`.codex-plugin/plugin.json` and Codex root guidance in `AGENTS.md`. The
registered Codex agents live under `.codex/agents/synapse/`.

Codex plugin manifests expose skills rather than Claude-style slash-command
files, so use the `bug-capture` skill for the same bug-report workflow in
Codex.

For a personal local checkout, place the repository at
`C:\Users\nateb\plugins\synapse`, then refresh and install it from the personal
marketplace:

```powershell
python C:\Users\nateb\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py C:\Users\nateb\plugins\synapse
codex plugin add synapse@personal
```

Start a new Codex task after reinstalling so the updated skills and agent
registrations are loaded.

## Repository structure

```text
skills/                         shared skills
.codex-plugin/plugin.json       Codex plugin manifest
.codex/agents/synapse/          Codex agent registrations
agents/                         Claude-compatible agent adapters
commands/                       Claude-compatible commands
automations/                    Bandaid automations (claude/ live, cursor/ frozen)
docs/                           templates and design history
AGENTS.md                       Codex root guidance
CLAUDE.md                       Claude-compatible root guidance
```
