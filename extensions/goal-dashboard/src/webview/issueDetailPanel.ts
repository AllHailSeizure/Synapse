import * as crypto from 'crypto';
import * as vscode from 'vscode';
import { GitHubClient } from '../github/client';
import { parseIssueBody } from '../template/parser';
import { serializeGoal } from '../template/serializer';
import { ChecklistItem, ParsedGoal } from '../template/types';

interface StructuredSaveMessage {
  type: 'save';
  mode: 'structured';
  currentState: string;
  doneCriteria: string;
  constraints: string[];
  checklist: ChecklistItem[];
}

interface RawSaveMessage {
  type: 'save';
  mode: 'raw';
  body: string;
}

interface ReloadMessage {
  type: 'reload';
}

type WebviewMessage = StructuredSaveMessage | RawSaveMessage | ReloadMessage;

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function nonce(): string {
  return crypto.randomBytes(16).toString('hex');
}

function pageShell(title: string, bodyHtml: string, scriptNonce: string): string {
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-${scriptNonce}';">
<style>
  body { font-family: var(--vscode-font-family); padding: 1rem; color: var(--vscode-foreground); }
  h2 { margin-top: 0; }
  label { display: block; font-weight: 600; margin-top: 1rem; }
  textarea, input[type=text] {
    width: 100%; box-sizing: border-box; font-family: inherit; padding: 0.4rem;
    background: var(--vscode-input-background); color: var(--vscode-input-foreground);
    border: 1px solid var(--vscode-input-border, transparent);
  }
  textarea { min-height: 4rem; }
  .checklist-item { display: flex; align-items: center; gap: 0.5rem; margin-top: 0.3rem; }
  .checklist-item input[type=text] { flex: 1; }
  .actions { margin-top: 1rem; }
  button { margin-right: 0.5rem; }
  #status { margin-left: 0.5rem; opacity: 0.8; }
</style>
<title>${escapeHtml(title)}</title>
</head>
<body>
${bodyHtml}
</body>
</html>`;
}

function saveStatusScript(): string {
  return `
    window.addEventListener('message', (event) => {
      if (event.data && event.data.type === 'saved') {
        const status = document.getElementById('status');
        status.textContent = 'Saved';
        setTimeout(() => { status.textContent = ''; }, 2000);
      }
    });`;
}

function renderLoadingHtml(): string {
  return pageShell('Loading', '<p>Loading…</p>', nonce());
}

function renderStructuredHtml(issueNumber: number, title: string, goal: ParsedGoal): string {
  const scriptNonce = nonce();
  const constraintsText = goal.constraints.join('\n');

  const body = `
  <h2>#${issueNumber} ${escapeHtml(title)}</h2>

  <label for="currentState">Current State</label>
  <textarea id="currentState">${escapeHtml(goal.currentState)}</textarea>

  <label for="doneCriteria">Done Criteria</label>
  <textarea id="doneCriteria">${escapeHtml(goal.doneCriteria)}</textarea>

  <label for="constraints">Constraints (one per line)</label>
  <textarea id="constraints">${escapeHtml(constraintsText)}</textarea>

  <label>Checklist</label>
  <div id="checklist"></div>
  <button id="addItem" type="button">+ Add item</button>

  <div class="actions">
    <button id="save" type="button">Save</button>
    <button id="reload" type="button">Reload from GitHub</button>
    <span id="status"></span>
  </div>

  <script nonce="${scriptNonce}">
    const vscode = acquireVsCodeApi();
    const checklistEl = document.getElementById('checklist');
    const checklist = ${JSON.stringify(goal.checklist)};

    function renderChecklist() {
      checklistEl.innerHTML = '';
      checklist.forEach((item, index) => {
        const row = document.createElement('div');
        row.className = 'checklist-item';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = item.checked;
        checkbox.addEventListener('change', () => { item.checked = checkbox.checked; });

        const text = document.createElement('input');
        text.type = 'text';
        text.value = item.text;
        text.addEventListener('input', () => { item.text = text.value; });

        const remove = document.createElement('button');
        remove.type = 'button';
        remove.textContent = '\\u00d7';
        remove.addEventListener('click', () => {
          checklist.splice(index, 1);
          renderChecklist();
        });

        row.appendChild(checkbox);
        row.appendChild(text);
        row.appendChild(remove);
        checklistEl.appendChild(row);
      });
    }
    renderChecklist();

    document.getElementById('addItem').addEventListener('click', () => {
      checklist.push({ text: '', checked: false });
      renderChecklist();
    });

    document.getElementById('save').addEventListener('click', () => {
      vscode.postMessage({
        type: 'save',
        mode: 'structured',
        currentState: document.getElementById('currentState').value,
        doneCriteria: document.getElementById('doneCriteria').value,
        constraints: document.getElementById('constraints').value.split('\\n').map((s) => s.trim()).filter(Boolean),
        checklist: checklist.filter((item) => item.text.trim().length > 0),
      });
    });

    document.getElementById('reload').addEventListener('click', () => {
      vscode.postMessage({ type: 'reload' });
    });
    ${saveStatusScript()}
  </script>`;

  return pageShell(`#${issueNumber} ${title}`, body, scriptNonce);
}

function renderRawHtml(issueNumber: number, title: string, rawBody: string): string {
  const scriptNonce = nonce();

  const body = `
  <h2>#${issueNumber} ${escapeHtml(title)}</h2>
  <p>This issue's body doesn't match the goal-writer template — editing as raw markdown.</p>
  <textarea id="body" style="min-height: 20rem;">${escapeHtml(rawBody)}</textarea>

  <div class="actions">
    <button id="save" type="button">Save</button>
    <button id="reload" type="button">Reload from GitHub</button>
    <span id="status"></span>
  </div>

  <script nonce="${scriptNonce}">
    const vscode = acquireVsCodeApi();
    document.getElementById('save').addEventListener('click', () => {
      vscode.postMessage({ type: 'save', mode: 'raw', body: document.getElementById('body').value });
    });
    document.getElementById('reload').addEventListener('click', () => {
      vscode.postMessage({ type: 'reload' });
    });
    ${saveStatusScript()}
  </script>`;

  return pageShell(`#${issueNumber} ${title}`, body, scriptNonce);
}

export class IssueDetailPanel {
  private static current: IssueDetailPanel | undefined;

  private readonly panel: vscode.WebviewPanel;
  private readonly disposables: vscode.Disposable[] = [];
  private client!: GitHubClient;
  private issueNumber = -1;
  private loadedUpdatedAt = '';

  static async show(client: GitHubClient, issueNumber: number): Promise<void> {
    if (IssueDetailPanel.current) {
      IssueDetailPanel.current.panel.reveal(vscode.ViewColumn.Active);
      await IssueDetailPanel.current.load(client, issueNumber);
      return;
    }

    const panel = vscode.window.createWebviewPanel('goalDashboard.issueDetail', 'Goal', vscode.ViewColumn.Active, {
      enableScripts: true,
      retainContextWhenHidden: true,
    });

    const instance = new IssueDetailPanel(panel);
    IssueDetailPanel.current = instance;
    panel.onDidDispose(
      () => {
        IssueDetailPanel.current = undefined;
        instance.dispose();
      },
      null,
      instance.disposables
    );

    await instance.load(client, issueNumber);
  }

  private constructor(panel: vscode.WebviewPanel) {
    this.panel = panel;
    this.panel.webview.onDidReceiveMessage(
      (message: WebviewMessage) => {
        void this.handleMessage(message);
      },
      null,
      this.disposables
    );
  }

  private async load(client: GitHubClient, issueNumber: number): Promise<void> {
    this.client = client;
    this.issueNumber = issueNumber;
    this.panel.title = `Goal #${issueNumber}`;
    this.panel.webview.html = renderLoadingHtml();

    const issue = await client.getIssue(issueNumber);
    this.loadedUpdatedAt = issue.updatedAt;

    const parseResult = parseIssueBody(issue.body);
    this.panel.webview.html = parseResult.ok
      ? renderStructuredHtml(issue.number, issue.title, parseResult.goal)
      : renderRawHtml(issue.number, issue.title, parseResult.raw);
  }

  private async handleMessage(message: WebviewMessage): Promise<void> {
    if (message.type === 'reload') {
      await this.load(this.client, this.issueNumber);
      return;
    }
    if (message.type === 'save') {
      await this.save(message);
    }
  }

  private async save(message: StructuredSaveMessage | RawSaveMessage): Promise<void> {
    const latest = await this.client.getIssue(this.issueNumber);
    if (latest.updatedAt !== this.loadedUpdatedAt) {
      const choice = await vscode.window.showWarningMessage(
        'This issue changed on GitHub since you opened it.',
        'Overwrite Anyway',
        'Cancel'
      );
      if (choice !== 'Overwrite Anyway') {
        return;
      }
    }

    const body =
      message.mode === 'structured'
        ? serializeGoal({
            currentState: message.currentState,
            doneCriteria: message.doneCriteria,
            constraints: message.constraints,
            checklist: message.checklist,
          })
        : message.body;

    await this.client.updateIssueBody(this.issueNumber, body);
    const refreshed = await this.client.getIssue(this.issueNumber);
    this.loadedUpdatedAt = refreshed.updatedAt;
    void this.panel.webview.postMessage({ type: 'saved' });
  }

  private dispose(): void {
    for (const disposable of this.disposables) {
      disposable.dispose();
    }
  }
}
