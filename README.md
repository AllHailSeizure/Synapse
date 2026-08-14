# Synapse

Synapse is a personal workflow system for Claude Code and Codex. It keeps
software work deliberate with concise skills, visible evidence, and gates that
scale with risk instead of ceremony.

## Current skill suite

The shared skills live in `skills/` and cover:

- read-only collaborative thinking, feature specifications, and implementation plans;
- testing, verification, debugging, and code review;
- worktree isolation and bounded subagent delegation;
- finishing branches with verification, push, and pull request creation;
- user-directed GitHub issues and sticky-note bug capture;
- autonomous-work boundaries between user intent and agent execution; and
- report-only surveys of what a repo accumulates on its own — asset churn in a
  branch, worktree and branch sprawl.

See [`skills/README.md`](skills/README.md) for the complete inventory and the
skills that were intentionally dropped or replaced.

## Claude installation

Synapse publishes itself as a marketplace via
[`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json), so the
skills, commands, and bandaids install as one plugin rather than being copied:

```bash
claude plugin marketplace add AllHailSeizure/Synapse
```

```bash
claude plugin install synapse@synapse
```

Root `skills/` and `commands/` are discovered by convention, so a new skill
directory or command file ships with the next release — no manifest edit.
Publishing means landing it on the branch the marketplace tracks.

Skills and commands can still be copied into the local configuration
directories instead, for a checkout you're actively editing:

```powershell
powershell -Command "'.claude','.cursor' | % { Copy-Item 'D:\Libraries\Synapse\skills\*' \"$env:USERPROFILE\$_\skills\" -Recurse -Force; Copy-Item 'D:\Libraries\Synapse\commands\*.md' \"$env:USERPROFILE\$_\commands\" -Force }"
```

The Claude root guidance is in [`CLAUDE.md`](CLAUDE.md), and the Claude agent
adapters are in `agents/`.

The `/bug` command is defined in [`commands/bug.md`](commands/bug.md) and
delegates to the capture-only `bug-capture` skill. The command index is in
[`docs/COMMANDS.md`](docs/COMMANDS.md) — kept out of `commands/`, since every
`.md` in that directory ships as a slash command.

## Per-repo configuration and artifacts

A repo that Synapse operates on stores configuration in one `.synapse/`
directory — no skills or scripts. Feature specification artifacts live
separately in `synapse/specs/`. Each tool reads only the files it needs:

```text
.synapse/identity.md    repo, base, stack          every tool
.synapse/bandaids.md    Secrets, Verify, Repro,    the bandaids
                        Protected, Ignore
.synapse/weedeat.md     Assets, Worktrees          the /weedeat surveys
synapse/specs/*.md      feature intent             writing-specs + implementation
```

The bandaids stop at Gate 0 on a missing section. The `/weedeat` surveys degrade
to documented defaults instead and say so in their own output.

There is **no fallback** to the old root `SYNAPSE.md`. That single file was a
contention point — every workstream edited it, and an uncommitted edit was once
reset away by another before it was committed. Reading it as a fallback would
also mean silently serving standards from a file nobody remembers, so a tool
that can't find `.synapse/` fails loudly or uses defaults you can read here. If
a root `SYNAPSE.md` is still lying around, delete it.

Schema: [`docs/TEMPLATES/synapse/`](docs/TEMPLATES/synapse/). Worked example:
[`docs/EXAMPLES/synapse.hotel-kline-game.md`](docs/EXAMPLES/synapse.hotel-kline-game.md).

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
