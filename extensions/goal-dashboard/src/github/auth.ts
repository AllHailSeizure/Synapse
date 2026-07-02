import * as vscode from 'vscode';

const GITHUB_AUTH_SCOPES = ['repo'];

export async function getGitHubSession(): Promise<vscode.AuthenticationSession> {
  return vscode.authentication.getSession('github', GITHUB_AUTH_SCOPES, { createIfNone: true });
}
