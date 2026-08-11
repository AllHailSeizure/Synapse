# Platform Release Branches

> **SUPERSEDED 2026-08-11.** `claude-release` and `codex-release` were deleted
> and Synapse moved to a single model-agnostic marketplace on `master`. Design
> history — the branches this describes no longer exist.

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

The repository is public because the current GitHub plan only supports branch protection for public repositories. GitHub branch protection requires the policy workflow to pass and requires pull requests before merging. Direct pushes are disabled for both release branches.

## Bootstrap and Migration

The existing remote `release` branch is renamed to `claude-release`; the Claude Code marketplace and installation documentation change to point to the new name.

`codex-release` starts with the Codex manifest, the existing Codex agents under `.codex/agents/synapse/`, `AGENTS.md`, and `goal-oriented-development` as its first validated skill. The README documents the two installation targets.

The Codex plugin is installed privately through the user's personal Codex marketplace from a local checkout of `codex-release`. No public marketplace listing is created.

## Cross-Platform Skill Parity

Shared skills have one behavioral intent across Claude Code and Codex. A change to such a skill must assess both platform implementations before it is promoted. When both platforms support the change, update their skill and agent adapters together. When they intentionally differ, document the platform-specific behavior and its reason in the changed skill or its release pull request.

This is a review and promotion requirement rather than a CI path rule: automated checks can enforce platform file boundaries, but cannot determine whether two implementations remain behaviorally equivalent.

## Verification

- Test allowed and forbidden path sets for both target branches.
- Validate both plugin manifests.
- Confirm the renamed Claude branch retains the release commit.
- Confirm branch protection requires the policy check and pull requests.
