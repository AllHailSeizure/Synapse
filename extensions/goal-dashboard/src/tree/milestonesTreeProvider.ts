import * as vscode from 'vscode';
import { GitHubClient, IssueSummary, MilestoneWithIssues } from '../github/client';

export class MilestoneTreeItem extends vscode.TreeItem {
  constructor(public readonly milestone: MilestoneWithIssues) {
    super(milestone.title, vscode.TreeItemCollapsibleState.Expanded);
    this.contextValue = 'goalDashboard.milestone';
    this.iconPath = new vscode.ThemeIcon('milestone');
  }
}

export class IssueTreeItem extends vscode.TreeItem {
  constructor(public readonly issue: IssueSummary) {
    super(`#${issue.number} ${issue.title}`, vscode.TreeItemCollapsibleState.None);
    this.contextValue = 'goalDashboard.issue';
    this.iconPath = new vscode.ThemeIcon('issues');
    this.command = {
      command: 'goalDashboard.openIssue',
      title: 'Open Goal',
      arguments: [issue.number],
    };
  }
}

class MessageTreeItem extends vscode.TreeItem {
  constructor(message: string) {
    super(message, vscode.TreeItemCollapsibleState.None);
    this.contextValue = 'goalDashboard.message';
  }
}

type GoalDashboardTreeItem = MilestoneTreeItem | IssueTreeItem | MessageTreeItem;

export class MilestonesTreeProvider implements vscode.TreeDataProvider<GoalDashboardTreeItem> {
  private readonly onDidChangeTreeDataEmitter = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this.onDidChangeTreeDataEmitter.event;

  // In-memory only — no disk writes, discarded on window reload. Refresh is
  // a manual pull via the title-bar button, never a background poll.
  private cache: MilestoneWithIssues[] = [];
  private loadError: string | undefined;

  // Takes a factory rather than a client instance so that repo-resolution
  // failures (e.g. no git remote, no override configured) surface through
  // this method's existing error handling instead of throwing during
  // extension activation.
  constructor(private readonly getClient: () => GitHubClient) {}

  async refresh(): Promise<void> {
    try {
      const client = this.getClient();
      this.cache = await client.getMilestonesWithIssues();
      this.loadError = undefined;
    } catch (error) {
      this.cache = [];
      this.loadError = error instanceof Error ? error.message : String(error);
    }
    this.onDidChangeTreeDataEmitter.fire();
  }

  getTreeItem(element: GoalDashboardTreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: GoalDashboardTreeItem): GoalDashboardTreeItem[] {
    if (!element) {
      if (this.loadError) {
        return [new MessageTreeItem(`Error: ${this.loadError}`)];
      }
      if (this.cache.length === 0) {
        return [new MessageTreeItem('No open milestones found.')];
      }
      return this.cache.map((milestone) => new MilestoneTreeItem(milestone));
    }
    if (element instanceof MilestoneTreeItem) {
      return element.milestone.issues.map((issue) => new IssueTreeItem(issue));
    }
    return [];
  }
}
