import { spawn } from "node:child_process";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

const OPT_OUT =
  /^(?:capture only|don't kick(?:\s+@[\w-]+)?|dont kick|no bandaid|don't trigger|dont trigger|don't start|no kick)\s+/i;

export function createCapture({ name, kick, script }) {
  function parseCaptureArgs(argv) {
    const result = {
      help: false,
      kick: true,
      priority: "p3",
      text: "",
    };
    const rest = [];

    for (const arg of argv) {
      if (arg === "--help" || arg === "-h") result.help = true;
      else if (arg === "--no-kick") result.kick = false;
      else rest.push(arg);
    }

    let text = rest.join(" ").trim();
    const priority = text.match(/^(p[0-3])(?:\s+|$)/i);
    if (priority) {
      result.priority = priority[1].toLowerCase();
      text = text.slice(priority[0].length).trim();
    }
    const opt = text.match(OPT_OUT);
    if (opt) {
      result.kick = false;
      text = text.slice(opt[0].length).trim();
    }
    result.text = text;
    return result;
  }

  function issueTitle(text) {
    const first = text.split(/\r?\n/, 1)[0].trim();
    if (first.length <= 72) return first;
    return first.slice(0, 72).trimEnd();
  }

  function kickBody(title, body) {
    return `${kick}\n\nTitle: ${title}\n\n${body}`;
  }

  function helpText() {
    return `Capture a GitHub issue from a sticky-note report.

Usage:
  node ${script} [p0|p1|p2|p3] [--no-kick] <report>
  node ${script} --no-kick <report>

Default priority is p3. Default is to comment ${kick} on the new issue.
Opt out with --no-kick or a leading phrase such as "capture only" or "no bandaid".
`;
  }

  async function runCapture({ argv, gh, stdout, stderr }) {
    const parsed = parseCaptureArgs(argv);
    if (parsed.help) {
      stdout.write(helpText());
      return 0;
    }
    if (!parsed.text) {
      stderr.write(`${name}: missing report text\n`);
      return 1;
    }

    const title = issueTitle(parsed.text);
    let url;
    try {
      url = (
        await gh([
          "issue",
          "create",
          "--title",
          title,
          "--body",
          parsed.text,
          "--label",
          "bug",
          "--label",
          parsed.priority,
        ])
      ).trim();
    } catch {
      try {
        url = (
          await gh([
            "issue",
            "create",
            "--title",
            title,
            "--body",
            parsed.text,
          ])
        ).trim();
        stderr.write(
          `${name}: created without labels (missing bug or priority label)\n`,
        );
      } catch (error) {
        stderr.write(`${name}: failed to create issue: ${error.message}\n`);
        return 1;
      }
    }

    const number = url.match(/\/issues\/(\d+)/)?.[1];
    if (parsed.kick && number) {
      try {
        await gh([
          "issue",
          "comment",
          number,
          "--body",
          kickBody(title, parsed.text),
        ]);
      } catch {
        stderr.write(
          `${name}: issue created but ${kick} comment failed\n`,
        );
      }
    }

    stdout.write(`${url}\n`);
    return 0;
  }

  return { parseCaptureArgs, issueTitle, kickBody, runCapture };
}

function runGh(args) {
  return new Promise((resolve, reject) => {
    const child = spawn("gh", args, {
      shell: process.platform === "win32",
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) resolve(stdout);
      else {
        const error = new Error(stderr.trim() || `gh exited ${code}`);
        error.stderr = stderr;
        reject(error);
      }
    });
  });
}

async function readStdin() {
  if (process.stdin.isTTY) return "";
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8").trim();
}

export async function runCli({ parseCaptureArgs, runCapture, importMetaUrl }) {
  const invokedDirectly =
    Boolean(process.argv[1]) &&
    resolve(process.argv[1]) === fileURLToPath(importMetaUrl);
  if (!invokedDirectly) return;

  const argv = process.argv.slice(2);
  const parsed = parseCaptureArgs(argv);
  if (!parsed.text && !parsed.help) {
    const stdin = await readStdin();
    if (stdin) argv.push(stdin);
  }
  const code = await runCapture({
    argv,
    gh: runGh,
    stdout: process.stdout,
    stderr: process.stderr,
  });
  process.exit(code);
}
