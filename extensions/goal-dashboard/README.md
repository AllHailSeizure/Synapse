# Goal Dashboard

A VS Code extension that lists the open GitHub Milestones/Issues used by Synapse's
`goal-oriented-development` skill, and lets you view and edit an issue's
goal-writer-template fields (Current State, Done Criteria, Constraints, Checklist)
in an editable panel — saving straight back to the GitHub issue.

GitHub Issues stays the single source of truth. There's no local file storage and
no sync with Claude Code sessions; this is a read/edit surface over what already
exists on GitHub.

## What this is (and isn't)

- Sidebar tree of open milestones and their open issues.
- Click an issue to open an editable detail panel. If the issue body matches the
  fixed goal-writer template, fields render as structured editable inputs
  (including a real checklist). If it doesn't match, you get a raw markdown
  textarea instead.
- Saving PATCHes the issue on GitHub via the REST API, with a conflict check
  against the issue's `updated_at` timestamp.
- No "deploy an agent" button, no issue/milestone creation from the UI, no local
  caching to disk. See `CLAUDE.md` for the full list of what's deliberately out
  of scope for this pass.

## Developing

```bash
npm install
npm run compile   # or npm run watch
npm run test      # Vitest unit tests for the pure template/repo-context modules
```

Press `F5` in VS Code (with this folder open) to launch an Extension Development
Host. Open a workspace whose git remote points at a repo with an open milestone
containing an open issue, or set `goalDashboard.repository` in settings to
override the detected repo.
