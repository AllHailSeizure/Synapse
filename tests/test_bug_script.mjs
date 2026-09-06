import assert from "node:assert/strict";
import test from "node:test";
import { parseCaptureArgs, issueTitle, kickBody, runCapture } from "../commands/bug.mjs";

test("parseCaptureArgs defaults to p3 and kick", () => {
  assert.deepEqual(parseCaptureArgs(["jump", "is", "floaty"]), {
    help: false,
    kick: true,
    priority: "p3",
    text: "jump is floaty",
  });
});

test("parseCaptureArgs takes a leading priority token", () => {
  assert.equal(parseCaptureArgs(["p0", "hard", "crash"]).priority, "p0");
  assert.equal(parseCaptureArgs(["p0", "hard", "crash"]).text, "hard crash");
});

test("parseCaptureArgs reads priority from a single argument blob", () => {
  const parsed = parseCaptureArgs(["p0 hard crash"]);
  assert.equal(parsed.priority, "p0");
  assert.equal(parsed.text, "hard crash");
});

test("parseCaptureArgs treats --no-kick as opt out", () => {
  const parsed = parseCaptureArgs(["--no-kick", "jump", "is", "floaty"]);
  assert.equal(parsed.kick, false);
  assert.equal(parsed.text, "jump is floaty");
});

test("parseCaptureArgs strips a leading opt-out phrase", () => {
  const parsed = parseCaptureArgs(["capture", "only", "the", "jump", "is", "floaty"]);
  assert.equal(parsed.kick, false);
  assert.equal(parsed.text, "the jump is floaty");
});

test("issueTitle uses the first line, capped at 72 characters", () => {
  assert.equal(issueTitle("short\nmore"), "short");
  const long = "x".repeat(80);
  assert.equal(issueTitle(long).length, 72);
});

test("kickBody starts with @bug-bandaid then title then body", () => {
  assert.equal(
    kickBody("jump is floaty", "jump is floaty\non ice"),
    "@bug-bandaid\n\nTitle: jump is floaty\n\njump is floaty\non ice",
  );
});

test("runCapture creates a labeled issue and kicks the bandaid", async () => {
  const calls = [];
  const gh = async (args) => {
    calls.push(args);
    if (args[0] === "issue" && args[1] === "create") {
      return "https://github.com/ex/repo/issues/12\n";
    }
    return "";
  };
  const stdout = { text: "", write(chunk) { this.text += chunk; } };
  const stderr = { text: "", write(chunk) { this.text += chunk; } };

  const code = await runCapture({
    argv: ["p1", "save", "fails"],
    gh,
    stdout,
    stderr,
  });

  assert.equal(code, 0);
  assert.equal(stdout.text, "https://github.com/ex/repo/issues/12\n");
  assert.deepEqual(calls[0], [
    "issue",
    "create",
    "--title",
    "save fails",
    "--body",
    "save fails",
    "--label",
    "bug",
    "--label",
    "p1",
  ]);
  assert.equal(calls[1][0], "issue");
  assert.equal(calls[1][1], "comment");
  assert.equal(calls[1][2], "12");
  assert.match(calls[1][calls[1].indexOf("--body") + 1], /^@bug-bandaid\n/);
});

test("runCapture skips the kick when opted out", async () => {
  const calls = [];
  const gh = async (args) => {
    calls.push(args);
    return "https://github.com/ex/repo/issues/3\n";
  };
  const stdout = { text: "", write(chunk) { this.text += chunk; } };
  const stderr = { text: "", write(chunk) { this.text += chunk; } };

  await runCapture({
    argv: ["--no-kick", "cosmetic", "gap"],
    gh,
    stdout,
    stderr,
  });

  assert.equal(calls.length, 1);
  assert.equal(calls[0][1], "create");
});

test("runCapture retries without labels when they are missing", async () => {
  const gh = async (args) => {
    if (args.includes("--label")) {
      const err = new Error("label not found");
      err.stderr = "could not add label";
      throw err;
    }
    return "https://github.com/ex/repo/issues/9\n";
  };
  const stdout = { text: "", write(chunk) { this.text += chunk; } };
  const stderr = { text: "", write(chunk) { this.text += chunk; } };

  const code = await runCapture({
    argv: ["unlabeled", "repo"],
    gh,
    stdout,
    stderr,
  });

  assert.equal(code, 0);
  assert.equal(stdout.text, "https://github.com/ex/repo/issues/9\n");
  assert.match(stderr.text, /without labels/);
});

test("runCapture still prints the URL when the kick comment fails", async () => {
  const gh = async (args) => {
    if (args[1] === "comment") throw new Error("denied");
    return "https://github.com/ex/repo/issues/4\n";
  };
  const stdout = { text: "", write(chunk) { this.text += chunk; } };
  const stderr = { text: "", write(chunk) { this.text += chunk; } };

  const code = await runCapture({ argv: ["x"], gh, stdout, stderr });
  assert.equal(code, 0);
  assert.equal(stdout.text, "https://github.com/ex/repo/issues/4\n");
  assert.match(stderr.text, /comment failed/);
});

test("runCapture errors when there is no report text", async () => {
  const stdout = { text: "", write(chunk) { this.text += chunk; } };
  const stderr = { text: "", write(chunk) { this.text += chunk; } };
  const code = await runCapture({ argv: [], gh: async () => "", stdout, stderr });
  assert.equal(code, 1);
  assert.match(stderr.text, /missing report/);
});
