---
name: synapse:testing-preferences
description: Testing process for Synapse projects. Defines verification documents, test script requirements, and the publish gate.
type: behavior
applies_to: [all coding projects]
---

# Testing Preferences

## Rule

No feature is complete until it has a verification document and a passing test script. No code reaches the `publish` branch until the verification document records 100% pass.

---

## Step 1: Define tests before writing code

When a new feature or component is scoped, create its verification document before implementation begins. The doc defines what "working" means — features and fail conditions — before any code exists.

Location: `docs/verification/[feature-name].md`

What gets its own verification doc is a project-level decision, defined in the project's CLAUDE.md.

---

## Verification document format

```markdown
# [Feature Name] — Verification

## Test Cases

- [ ] 1. [Description of what is being tested and expected result]
- [ ] 2. [Description]
- [ ] 3. [Fail condition: what should happen when X fails]
...

## Results

| Run | Date | Platform Version | App Version | Commit | Pass/Fail |
|-----|------|-----------------|-------------|--------|-----------|
|     |      |                 |             |        |           |

## Logs
<!-- appended by --verbose -->
```

Test cases are numbered. Numbers match the `-t` flag in the test script.

---

## Step 2: Write the test script

Every feature gets a test script. The script must:

- Auto-test where possible; prompt the tester with instructions where manual action is required
- Use verbose, descriptive logging throughout
- Define and use consistent error codes
- On completion, write results into the verification document (date, platform version, app version, current commit, pass/fail per test case) — unless `-n` is set

**Required flags — every test script must implement all four:**

| Flag | Long form | Behavior |
|------|-----------|----------|
| `-t [int]` | `--test [int]` | Run a single test by number |
| `-n` | `--nowrite` | Run without writing to the verification doc |
| `-m` | `--manual` | Disable auto-testing; human-prompted mode throughout |
| `-v` | `--verbose` | Append full logs to the verification doc |

Script language is project-appropriate (PowerShell, Bash, Python, etc.).

---

## Step 3: Run tests and record results

Run the full test script. The script records results automatically.

All test cases must pass before the feature is considered complete. A partial pass is not complete.

---

## Step 4: Publish gate

When a feature reaches 100% verified:

1. Confirm the verification document is up to date with the latest run
2. Push to the `publish` branch
3. The verification document travels with the code

The `publish` branch contains only verified code. Nothing goes to `publish` without a passing verification doc.

---

## Value of the verification record

The version-stamped results history answers "when did this last work and what has changed since?" — which isolates whether a regression is in your code, a dependency, or the platform. Before debugging, check the last passing run.
