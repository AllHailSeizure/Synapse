# Platform Release Branches

## Purpose

Synapse maintains a shared development branch and independently publishable Claude Code and Codex plugin branches. The release branches must prevent platform-specific files from crossing into the other platform's package.

## Branches

- `master` is the shared workshop branch and may contain Claude Code and Codex work.
- `claude-release` replaces `release` without changing the released Claude Code contents.
- `codex-release` publishes the Codex plugin.
- Shared documentation and platform-neutral skills may be promoted to either release branch.

## Release Content Policy

`claude-release` accepts Claude Code packaging and configuration, including `.claude-plugin/`, `.claude/`, `CLAUDE.md`, and Claude-specific agents. It rejects Codex-specific packaging and configuration, including `.codex-plugin/`, `.codex/`, and `AGENTS.md`.

`codex-release` accepts Codex packaging and configuration, including `.codex-plugin/`, `.codex/`, and `AGENTS.md`. It rejects Claude Code packaging and configuration, including `.claude-plugin/`, `.claude/`, `CLAUDE.md`, and Claude-specific agents.

Both release branches accept common repository files: `README.md`, `docs/`, licensing and repository metadata, and skills explicitly maintained as platform-neutral.

## Enforcement

A GitHub Actions workflow runs on pull requests into both release branches. It determines the target branch, inspects the files changed by the pull request, and fails when a changed path violates that target's policy. The workflow also validates the target platform's plugin manifest.

GitHub branch protection requires the policy workflow to pass and requires pull requests before merging. Direct pushes are disabled for both release branches.

## Bootstrap and Migration

The existing remote `release` branch is renamed to `claude-release`; the Claude Code marketplace and installation documentation change to point to the new name.

`codex-release` starts with the Codex manifest, the existing Codex agents under `.codex/agents/synapse/`, `AGENTS.md`, and only skills confirmed to work in Codex. The README documents the two installation targets.

## Verification

- Test allowed and forbidden path sets for both target branches.
- Validate both plugin manifests.
- Confirm the renamed Claude branch retains the release commit.
- Confirm branch protection requires the policy check and pull requests.
