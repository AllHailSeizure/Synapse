#!/usr/bin/env node
import { createCapture, runCli } from "./issue-capture.mjs";

export const { parseCaptureArgs, issueTitle, kickBody, runCapture } =
  createCapture({
    name: "bug",
    kick: "@bug-bandaid",
    script: "commands/bug.mjs",
  });

await runCli({
  parseCaptureArgs,
  runCapture,
  importMetaUrl: import.meta.url,
});
