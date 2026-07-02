// Minimal stub so tests/repoContext.test.ts can import github/repoContext.ts
// (which has a top-level `import * as vscode from 'vscode'`) without the
// real vscode module being available under Vitest/Node. Only
// parseOwnerRepoFromRemoteUrl is actually exercised by tests, so these
// stand-ins are never invoked — they just need to satisfy module resolution.
export const workspace = {
  getConfiguration: () => ({ get: () => '' }),
};

export const extensions = {
  getExtension: () => undefined,
};
