import * as vscode from 'vscode';

export interface OwnerRepo {
  owner: string;
  repo: string;
}

const SSH_REMOTE = /^git@github\.com:([^/]+)\/(.+?)(\.git)?$/;
const HTTPS_REMOTE = /^https:\/\/github\.com\/([^/]+)\/(.+?)(\.git)?$/;

// Pure: no vscode/network imports, so this is directly unit-testable.
export function parseOwnerRepoFromRemoteUrl(url: string): OwnerRepo | null {
  const match = SSH_REMOTE.exec(url) ?? HTTPS_REMOTE.exec(url);
  if (!match) {
    return null;
  }
  return { owner: match[1], repo: match[2] };
}

function getConfiguredRepository(): OwnerRepo | null {
  const configured = vscode.workspace.getConfiguration('goalDashboard').get<string>('repository', '').trim();
  if (!configured) {
    return null;
  }
  const [owner, repo] = configured.split('/');
  return owner && repo ? { owner, repo } : null;
}

// vscode.git's exported API isn't covered by @types/vscode, so this reaches
// into its exports at the one boundary that needs to; everything downstream
// of this function stays typed.
function getWorkspaceRemoteUrl(): string | null {
  const gitExtension = vscode.extensions.getExtension('vscode.git');
  const gitApi = gitExtension?.exports?.getAPI?.(1);
  const repository = gitApi?.repositories?.[0];
  const remotes = repository?.state?.remotes ?? [];
  const remote = remotes.find((r: { name: string }) => r.name === 'origin') ?? remotes[0];
  return remote?.fetchUrl ?? remote?.pushUrl ?? null;
}

export function resolveOwnerRepo(): OwnerRepo {
  const configured = getConfiguredRepository();
  if (configured) {
    return configured;
  }

  const remoteUrl = getWorkspaceRemoteUrl();
  const parsed = remoteUrl ? parseOwnerRepoFromRemoteUrl(remoteUrl) : null;
  if (!parsed) {
    throw new Error(
      'Could not determine a GitHub repository from the workspace git remote. Set "goalDashboard.repository" in settings (e.g. "owner/repo").'
    );
  }
  return parsed;
}
