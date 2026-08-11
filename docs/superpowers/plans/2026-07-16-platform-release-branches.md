# Platform Release Branches Implementation Plan

> **SUPERSEDED 2026-08-11.** `claude-release` and `codex-release` were deleted
> and Synapse moved to a single model-agnostic marketplace on `master`. Keeping
> two platform branches meant implementing every feature twice, and it drifted:
> at deletion the release branches held three features master never got. This
> document is design history — do not implement it.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Synapse as a private local Codex plugin while enforcing separate Claude Code and Codex release branches.

**Architecture:** `master` remains the shared workshop. GitHub Actions evaluates changed paths on pull requests into platform release branches, and branch protection makes that check and PR flow mandatory. The Codex plugin is a `codex-release` worktree at the personal-marketplace plugin path; it contains the Codex manifest, the Codex agent adapters, and the first Codex-ready skill.

**Tech Stack:** Git and linked worktrees, GitHub Actions, GitHub REST API via `gh`, PowerShell, Codex plugins.

## Global Constraints

- `master` may contain both platform implementations; release branches may contain only their platform-specific paths and explicitly shared paths.
- `claude-release` replaces `release` without changing the released Claude Code contents.
- `codex-release` initially publishes `goal-oriented-development` only.
- The repository must be public before GitHub branch protection is configured.
- The Codex plugin is private and registered only in the personal Codex marketplace.
- Cross-platform skill parity is a review/promotion requirement, not a CI semantic-equivalence check.
- Do not stage or commit the unrelated `squishy/` directory.

---

## File Structure

- `.github/scripts/Test-ReleaseBranchPolicy.ps1` — branch-aware changed-path policy checker with self-tests.
- `.github/workflows/release-branch-policy.yml` — pull-request check that invokes the policy checker.
- `.github/branch-protection.json` — required-check and pull-request protection settings applied to both release branches.
- `.codex-plugin/plugin.json` — Codex plugin manifest, present only on `codex-release`.
- `AGENTS.md` — Codex root guidance, present only on `codex-release`.
- `skills/goal-oriented-development/SKILL.md` — Codex-adapted first release skill on `codex-release`.
- `README.md` and `CLAUDE.md` — Claude marketplace documentation changed from `release` to `claude-release` on `master` and `claude-release`.

### Task 1: Add the release-path policy check

**Files:**
- Create: `.github/scripts/Test-ReleaseBranchPolicy.ps1`
- Create: `.github/workflows/release-branch-policy.yml`

**Interfaces:**
- Consumes: `-TargetBranch` (`claude-release` or `codex-release`) and `-ChangedPath` (one or more repository-relative paths).
- Produces: exit code `0` for allowed paths and `1` with each forbidden path listed otherwise.

- [ ] **Step 1: Write the failing self-test cases into `.github/scripts/Test-ReleaseBranchPolicy.ps1`**

```powershell
param(
  [ValidateSet('claude-release', 'codex-release')]
  [string]$TargetBranch,
  [string[]]$ChangedPath,
  [switch]$SelfTest
)

if ($SelfTest) {
  $cases = @(
    @{ Branch = 'claude-release'; Paths = @('.claude-plugin/plugin.json', 'skills/goal-oriented-development/SKILL.md', 'README.md'); Pass = $true },
    @{ Branch = 'claude-release'; Paths = @('.codex-plugin/plugin.json'); Pass = $false },
    @{ Branch = 'codex-release'; Paths = @('.codex/agents/synapse/goal-writer.toml', 'AGENTS.md', 'docs/spec.md'); Pass = $true },
    @{ Branch = 'codex-release'; Paths = @('.claude-plugin/plugin.json', 'CLAUDE.md'); Pass = $false }
  )
  foreach ($case in $cases) {
    & $PSCommandPath -TargetBranch $case.Branch -ChangedPath $case.Paths
    if (($LASTEXITCODE -eq 0) -ne $case.Pass) { throw "Unexpected policy result for $($case.Branch)" }
  }
  exit 0
}
```

- [ ] **Step 2: Run the self-test to verify it fails before policy logic exists**

Run: `pwsh -File .github/scripts/Test-ReleaseBranchPolicy.ps1 -SelfTest`

Expected: FAIL because the checker does not yet reject forbidden paths.

- [ ] **Step 3: Implement the policy checker below the self-test block**

```powershell
$shared = @(
  'README.md', '.gitignore', 'LICENSE', 'LICENSE.md',
  'docs/', 'skills/', '.github/'
)
$platform = @{
  'claude-release' = @('.claude-plugin/', '.claude/', 'CLAUDE.md', 'agents/')
  'codex-release' = @('.codex-plugin/', '.codex/', 'AGENTS.md')
}
$allowed = $shared + $platform[$TargetBranch]
$forbidden = $ChangedPath | Where-Object {
  $path = $_.Replace('\', '/')
  -not ($allowed | Where-Object { $path -eq $_ -or $path.StartsWith($_) })
}
if ($forbidden) {
  $forbidden | ForEach-Object { Write-Error "$_ is not allowed in $TargetBranch" }
  exit 1
}
```

- [ ] **Step 4: Run the self-test to verify the policy passes**

Run: `pwsh -File .github/scripts/Test-ReleaseBranchPolicy.ps1 -SelfTest`

Expected: exit code `0`.

- [ ] **Step 5: Add the pull-request workflow**

```yaml
name: Release branch policy

on:
  pull_request:
    branches: [claude-release, codex-release]

jobs:
  release-branch-policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Check changed paths
        shell: pwsh
        run: |
          $paths = git diff --name-only "origin/${{ github.base_ref }}...${{ github.sha }}"
          ./.github/scripts/Test-ReleaseBranchPolicy.ps1 -TargetBranch "${{ github.base_ref }}" -ChangedPath $paths
      - name: Validate Codex manifest
        if: github.base_ref == 'codex-release'
        run: python3 C:/Users/nateb/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

- [ ] **Step 6: Replace the runner-local manifest validator with a repository script**

Create `.github/scripts/Validate-CodexPlugin.ps1`:

```powershell
$manifestPath = '.codex-plugin/plugin.json'
if (-not (Test-Path -LiteralPath $manifestPath)) { throw "Missing $manifestPath" }
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
foreach ($field in 'name', 'version', 'description', 'skills') {
  if ([string]::IsNullOrWhiteSpace($manifest.$field)) { throw "Missing manifest field: $field" }
}
if ($manifest.version -notmatch '^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$') { throw 'version must be strict semver' }
if ([string]::IsNullOrWhiteSpace($manifest.author.name)) { throw 'Missing manifest field: author.name' }
foreach ($field in 'displayName', 'shortDescription', 'longDescription', 'developerName', 'category', 'defaultPrompt') {
  if ($null -eq $manifest.interface.$field -or [string]::IsNullOrWhiteSpace([string]$manifest.interface.$field)) { throw "Missing interface field: $field" }
}
if ($manifest.interface.capabilities -isnot [System.Collections.IEnumerable]) { throw 'interface.capabilities must be an array' }
if (-not (Test-Path -LiteralPath $manifest.skills)) { throw "Skills path does not exist: $($manifest.skills)" }
Write-Host 'Codex plugin manifest is valid.'
```

Replace the final workflow step with:

```yaml
      - name: Validate Codex manifest
        if: github.base_ref == 'codex-release'
        shell: pwsh
        run: ./.github/scripts/Validate-CodexPlugin.ps1
```

- [ ] **Step 7: Run local verification**

Run: `pwsh -File .github/scripts/Test-ReleaseBranchPolicy.ps1 -SelfTest`

Expected: exit code `0`.

- [ ] **Step 8: Commit the check**

```bash
git add .github/scripts/Test-ReleaseBranchPolicy.ps1 .github/scripts/Validate-CodexPlugin.ps1 .github/workflows/release-branch-policy.yml
git commit -m "ci: enforce platform release paths"
```

### Task 2: Rename and document the Claude release branch

**Files:**
- Modify: `README.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: existing `origin/release` at commit `93460f1`.
- Produces: `origin/claude-release` at the same commit; Claude marketplace commands point at `#claude-release`.

- [ ] **Step 1: Update Claude marketplace references**

Replace each `#release` in `README.md` and `CLAUDE.md` with `#claude-release`. In README prose, replace references to the release branch with `claude-release`.

- [ ] **Step 2: Verify no old marketplace pointer remains**

Run: `rg -n "synapse#release|\brelease\b" README.md CLAUDE.md`

Expected: no installation command still points to `synapse#release`; prose may mention the generic term “release”.

- [ ] **Step 3: Commit the documentation update without staging unrelated files**

```bash
git add README.md CLAUDE.md
git commit -m "docs: rename Claude release branch"
```

- [ ] **Step 4: Create the remote rename and verify the commit is preserved**

```bash
git fetch origin
git push origin origin/release:refs/heads/claude-release
git push origin --delete release
git rev-parse origin/claude-release
```

Expected: the final SHA is `93460f1d74784a91d9dea3797d51e7e35ef58333`.

### Task 3: Make the repository public and protect the Claude release branch

**Files:**
- Create: `.github/branch-protection.json`

**Interfaces:**
- Consumes: public GitHub repository `AllHailSeizure/synapse` and workflow check name `release-branch-policy`.
- Produces: `claude-release` requires pull requests and the release-path policy check; direct pushes are rejected.

- [ ] **Step 1: Create the branch protection request body**

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["release-branch-policy"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismissal_restrictions": {},
    "dismiss_stale_reviews": false,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 0,
    "require_last_push_approval": false,
    "bypass_pull_request_allowances": {}
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": false,
  "lock_branch": false,
  "allow_fork_syncing": false
}
```

- [ ] **Step 2: Commit the reproducible protection configuration**

```bash
git add .github/branch-protection.json
git commit -m "ci: define release branch protection"
git push origin master
```

- [ ] **Step 3: Make the repository public**

Run: `gh repo edit AllHailSeizure/synapse --visibility public --accept-visibility-change-consequences`

Expected: `gh repo view AllHailSeizure/synapse --json visibility --jq .visibility` prints `PUBLIC`.


- [ ] **Step 4: Bootstrap the policy workflow on `claude-release`**

```bash
git worktree add C:\Users\nateb\plugins\synapse-claude-release claude-release
cd C:\Users\nateb\plugins\synapse-claude-release
Copy-Item -Recurse -Force D:\Libraries\Synapse\.github .github
git add .github
git commit -m "ci: enforce platform release paths"
git push origin claude-release
```

Expected: `claude-release` now contains the policy workflow before it is protected.

- [ ] **Step 5: Apply protection to `claude-release`**

```powershell
gh api --method PUT repos/AllHailSeizure/synapse/branches/claude-release/protection --input .github/branch-protection.json
```

- [ ] **Step 6: Verify Claude branch protection**

Run: `gh api repos/AllHailSeizure/synapse/branches/claude-release/protection --jq '.required_status_checks.contexts, .required_pull_request_reviews.required_approving_review_count, .allow_force_pushes.enabled'`

Expected: includes `release-branch-policy`, prints `0`, then `false`.

### Task 4: Create and validate the private Codex plugin release

**Files:**
- Create: `C:\Users\nateb\plugins\synapse\.codex-plugin\plugin.json`
- Create: `C:\Users\nateb\plugins\synapse\AGENTS.md`
- Modify: `C:\Users\nateb\plugins\synapse\skills\goal-oriented-development\SKILL.md`
- Modify: `C:\Users\nateb\.agents\plugins\marketplace.json` through the plugin scaffold helper
- Remove: Claude-only files from the `codex-release` worktree: `.claude-plugin/`, `.claude/`, `CLAUDE.md`, and `agents/`

**Interfaces:**
- Consumes: `master` and the existing `.codex/agents/synapse/*.toml` agent definitions.
- Produces: personal-marketplace plugin `synapse` sourced from `C:\Users\nateb\plugins\synapse`, with `goal-oriented-development` and its four Codex agents.

- [ ] **Step 1: Create the linked Codex release worktree at the personal plugin path**

```bash
git worktree add -b codex-release C:\Users\nateb\plugins\synapse master
cd C:\Users\nateb\plugins\synapse
git rm -r .claude-plugin agents CLAUDE.md
git rm -r skills/speccing-first skills/testing-preferences
```

- [ ] **Step 2: Create the Codex manifest**

```json
{
  "name": "synapse",
  "version": "0.1.0",
  "description": "Personal workflow skills for deliberate, goal-oriented Codex development.",
  "author": {
    "name": "AllHailSeizure",
    "email": "natebosma@gmail.com",
    "url": "https://github.com/AllHailSeizure"
  },
  "homepage": "https://github.com/AllHailSeizure/synapse",
  "repository": "https://github.com/AllHailSeizure/synapse",
  "license": "MIT",
  "keywords": ["codex", "skills", "workflow", "goal-oriented-development"],
  "skills": "./skills/",
  "interface": {
    "displayName": "Synapse",
    "shortDescription": "Goal-oriented development workflows for Codex.",
    "longDescription": "Personal Codex workflows for scoping, tracking, and fulfilling one goal at a time.",
    "developerName": "AllHailSeizure",
    "category": "Productivity",
    "capabilities": ["Interactive", "Write"],
    "defaultPrompt": ["Orient this repository around its next GitHub goal."]
  }
}
```

- [ ] **Step 3: Add Codex root guidance and adapt the released skill**

Copy `D:\Libraries\Synapse\AGENTS.md` into this worktree, correct its skills reference to `skills/`, and remove the obsolete `synapse-init` instruction. In `skills/goal-oriented-development/SKILL.md`, replace Claude-specific wording with Codex wording and name the registered Codex agents: `codebase-explorer`, `goal-writer`, `goal-surveyor`, and `goal-fulfiller`. Preserve the behavioral rules, including session orientation, implementation-drift protection, executable issues, and the reflection gate.

- [ ] **Step 4: Run the Codex manifest and skill checks**

```powershell
pwsh -File .github/scripts/Validate-CodexPlugin.ps1
python C:\Users\nateb\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py C:\Users\nateb\plugins\synapse
rg -n "Claude|\.claude-plugin|CLAUDE\.md|agents/" AGENTS.md skills/goal-oriented-development/SKILL.md
```

Expected: both validators pass; the final command produces no platform-specific references.

- [ ] **Step 5: Register the private plugin through the scaffold helper**

```powershell
python C:\Users\nateb\.codex\skills\.system\plugin-creator\scripts\create_basic_plugin.py synapse --path C:\Users\nateb\plugins --with-marketplace --force
```

After the helper creates the personal-marketplace entry, restore the manifest content from Step 2 if the scaffold overwrote it, then run the Step 4 validators again. Confirm `C:\Users\nateb\.agents\plugins\marketplace.json` contains a `synapse` entry sourced from `./plugins/synapse`.

- [ ] **Step 6: Commit and push the Codex release**

```bash
git add .codex-plugin AGENTS.md .codex skills/goal-oriented-development/SKILL.md README.md .github
git commit -m "feat: publish Codex goal-oriented-development plugin"
git push -u origin codex-release
```

### Task 5: Protect the Codex release branch and verify promotion boundaries

**Files:**
- Modify: `README.md` on `codex-release` to describe the private Codex installation source.

**Interfaces:**
- Consumes: the pushed `claude-release` and `codex-release` branches plus the personal marketplace entry.
- Produces: protected Codex promotion and verified branch boundaries with a locally installable Codex plugin.

- [ ] **Step 1: Apply and verify Codex branch protection**

```powershell
gh api --method PUT repos/AllHailSeizure/synapse/branches/codex-release/protection --input .github/branch-protection.json
gh api repos/AllHailSeizure/synapse/branches/codex-release/protection --jq '.required_status_checks.contexts, .allow_force_pushes.enabled'
```

Expected: includes `release-branch-policy` and prints `false`.

- [ ] **Step 2: Verify each release tree contains no wrong-platform path**

```bash
git ls-tree -r --name-only origin/claude-release | rg '^\.codex-plugin/|^\.codex/|^AGENTS\.md$'
git ls-tree -r --name-only origin/codex-release | rg '^\.claude-plugin/|^\.claude/|^CLAUDE\.md$|^agents/'
```

Expected: both commands return no paths.

- [ ] **Step 3: Test policy failures against synthetic changed paths**

```powershell
pwsh -File .github/scripts/Test-ReleaseBranchPolicy.ps1 -TargetBranch claude-release -ChangedPath .codex-plugin/plugin.json
pwsh -File .github/scripts/Test-ReleaseBranchPolicy.ps1 -TargetBranch codex-release -ChangedPath .claude-plugin/plugin.json
```

Expected: each command exits `1` and identifies the forbidden path.

- [ ] **Step 4: Update the Codex release README and commit it**

Document that Synapse is installed from the user's personal Codex marketplace and its local `C:\Users\nateb\plugins\synapse` checkout. State that platform-neutral skill changes must be reviewed for Claude Code and Codex parity before release promotion.

```bash
git add README.md
git commit -m "docs: describe Codex plugin installation"
git push origin codex-release
```

- [ ] **Step 5: Refresh the installed Codex plugin**

Run: `python C:\Users\nateb\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py C:\Users\nateb\plugins\synapse`

Expected: the plugin cachebuster changes and the Codex app detects the updated local plugin after refresh.

## Self-Review

- Spec coverage: Tasks 1 and 3 enforce platform boundaries and required PR checks; Task 2 renames the Claude release; Task 4 produces the private Codex release with `goal-oriented-development`; Task 5 verifies release contents and documents parity expectations.
- Placeholder scan: no incomplete markers or undefined implementation steps remain.
- Interface consistency: the workflow check name `release-branch-policy`, branch names, worktree path, and plugin name `synapse` are used consistently.
