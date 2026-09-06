import assert from "node:assert/strict";
import test from "node:test";
import { kickBody, runCapture } from "../commands/patch.mjs";

test("kickBody starts with @fastpatch then title then body", () => {
  assert.equal(
    kickBody("jump is floaty", "jump is floaty\non ice"),
    "@fastpatch\n\nTitle: jump is floaty\n\njump is floaty\non ice",
  );
});

test("runCapture comments @fastpatch on the new issue", async () => {
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
    argv: ["save", "fails"],
    gh,
    stdout,
    stderr,
  });

  assert.equal(code, 0);
  assert.match(calls[1][calls[1].indexOf("--body") + 1], /^@fastpatch\n/);
  assert.doesNotMatch(calls[1][calls[1].indexOf("--body") + 1], /@bug-bandaid/);
});
