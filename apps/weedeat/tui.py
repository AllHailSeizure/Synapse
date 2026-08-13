"""Textual interface for reviewing worktrees that are not auto-safe."""

from __future__ import annotations

import subprocess
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from apps.weedeat.prune import prune_reviewed_branch, prune_reviewed_worktree
from apps.weedeat.scan import git, read_manifest


def review_base(root: str) -> str:
    """Resolve the configured baseline, then fall back to a conventional branch."""
    manifest = read_manifest(root)
    configured = manifest.get("worktrees", {}).get("base", [])
    if configured:
        return configured[-1]

    identity = Path(root) / ".synapse" / "identity.md"
    if identity.is_file():
        section = ""
        for line in identity.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if stripped.startswith("## "):
                section = stripped[3:].strip().lower()
            elif section == "identity" and stripped.lower().startswith("base:"):
                branch = stripped.partition(":")[2].strip()
                if branch:
                    remote = f"origin/{branch}"
                    if git("rev-parse", "--verify", "--quiet", remote, cwd=root):
                        return remote
                    return branch

    remote_head = git(
        "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD", cwd=root
    )
    if remote_head:
        return remote_head
    for candidate in ("main", "master"):
        if git("rev-parse", "--verify", "--quiet", candidate, cwd=root):
            return candidate
    return "HEAD"


def branch_diff(root: str, base: str, branch: str) -> str:
    result = subprocess.run(
        ["git", "diff", f"{base}...{branch}"], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        return result.stderr.strip() or "git diff failed"
    return result.stdout or "No committed diff from the baseline."


class WorktreeItem(ListItem):
    def __init__(self, entry: dict) -> None:
        self.entry = entry
        label = entry["branch"] or "(detached)"
        text = f"{label}  [{entry['tier']}]\n{entry['reason']}\n{entry['path']}"
        super().__init__(Label(text, markup=False))


class DiffScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back"), ("q", "app.pop_screen", "Back")]

    def __init__(self, title: str, diff: str) -> None:
        super().__init__()
        self.diff_title = title
        self.diff = diff

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll():
            yield Static(self.diff_title, id="diff-title", markup=False)
            yield Static(self.diff, id="diff-body", markup=False)
        yield Footer()


class ConfirmDelete(ModalScreen[bool]):
    BINDINGS = [
        ("y", "confirm", "Delete"),
        ("n", "cancel", "Keep"),
        ("escape", "cancel", "Keep"),
    ]

    def __init__(self, branch: str) -> None:
        super().__init__()
        self.branch = branch

    def compose(self) -> ComposeResult:
        with Container(id="confirm-dialog"):
            yield Static(
                f"Delete worktree for {self.branch}? y/n", markup=False,
                id="confirm-question",
            )

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)


class WeedeatApp(App[None]):
    TITLE = "weedeat review"
    BINDINGS = [
        ("d", "show_diff", "Diff"),
        ("x", "delete", "Delete"),
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]
    CSS = """
    ListView { height: 1fr; }
    ListItem { padding: 1 2; height: auto; }
    ListItem.--highlight { background: $accent; }
    #diff-title { text-style: bold; padding: 1 2; }
    #diff-body { padding: 0 2 2 2; }
    ConfirmDelete { align: center middle; }
    #confirm-dialog { width: auto; height: auto; padding: 1 2; border: round $warning; background: $surface; }
    """

    def __init__(self, root: str, remainder: list[dict]) -> None:
        super().__init__()
        self.root = root
        self.remainder = [entry for entry in remainder if not entry.get("locked")]
        self.base = review_base(root)

    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(*(WorktreeItem(entry) for entry in self.remainder), id="remainder")
        yield Footer()

    def highlighted(self) -> WorktreeItem | None:
        item = self.query_one("#remainder", ListView).highlighted_child
        return item if isinstance(item, WorktreeItem) else None

    def action_show_diff(self) -> None:
        item = self.highlighted()
        if item is None:
            return
        entry = item.entry
        branch = entry.get("branch")
        if not branch:
            self.notify("Detached worktree has no branch diff.", severity="warning")
            return
        diff = branch_diff(self.root, self.base, branch)
        self.push_screen(DiffScreen(f"git diff {self.base}...{branch}", diff))

    def action_delete(self) -> None:
        item = self.highlighted()
        if item is None:
            return
        label = item.entry.get("branch") or "(detached)"
        self.push_screen(ConfirmDelete(label), self._delete_if_confirmed)

    def _delete_if_confirmed(self, confirmed: bool | None) -> None:
        if not confirmed:
            return
        item = self.highlighted()
        if item is None:
            return
        entry = item.entry
        success, message = prune_reviewed_worktree(self.root, entry)
        if not success:
            self.notify(message, title="Worktree deletion failed", severity="error")
            return

        branch = entry.get("branch")
        if branch:
            branch_success, branch_message = prune_reviewed_branch(self.root, branch)
            if not branch_success:
                self.notify(
                    branch_message, title="Worktree removed; branch deletion failed",
                    severity="warning",
                )
            else:
                self.notify(f"Deleted worktree and branch {branch}.")
        else:
            self.notify("Deleted detached worktree.")
        item.remove()


def review(root: str, remainder: list[dict]) -> None:
    """Run the interactive review app and return when the user quits."""
    WeedeatApp(root, remainder).run()
