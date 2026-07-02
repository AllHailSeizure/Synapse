import * as vscode from 'vscode';
import { GitHubClient } from './github/client';
import { resolveOwnerRepo } from './github/repoContext';
import { MilestonesTreeProvider } from './tree/milestonesTreeProvider';
import { IssueDetailPanel } from './webview/issueDetailPanel';

function toErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

export function activate(context: vscode.ExtensionContext): void {
  let client: GitHubClient | undefined;

  function getClient(): GitHubClient {
    if (!client) {
      client = new GitHubClient(resolveOwnerRepo());
    }
    return client;
  }

  const treeProvider = new MilestonesTreeProvider(getClient);
  const treeView = vscode.window.createTreeView('goalDashboard.milestones', {
    treeDataProvider: treeProvider,
  });

  context.subscriptions.push(
    treeView,
    vscode.commands.registerCommand('goalDashboard.refresh', () => treeProvider.refresh()),
    vscode.commands.registerCommand('goalDashboard.openIssue', async (issueNumber: number) => {
      try {
        await IssueDetailPanel.show(getClient(), issueNumber);
      } catch (error) {
        vscode.window.showErrorMessage(`Goal Dashboard: ${toErrorMessage(error)}`);
      }
    })
  );

  void treeProvider.refresh();
}

export function deactivate(): void {}
