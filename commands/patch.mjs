#!/usr/bin/env node
import { createCapture, runCli } from "./issue-capture.mjs";

export const { parseCaptureArgs, issueTitle, kickBody, runCapture } =
  createCapture({
    name: "patch",
    kick: "@fastpatch",
    script: "commands/patch.mjs",
  });

await runCli({
  parseCaptureArgs,
  runCapture,
  importMetaUrl: import.meta.url,
});
