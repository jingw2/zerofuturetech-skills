#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const args = process.argv.slice(2);

function usage() {
  console.log(`Usage:
  zerofuturetech-skills install <skill-name> [--target <dir>]

Examples:
  zerofuturetech-skills install high-agency-x-essay-writer
  zerofuturetech-skills install high-agency-x-essay-writer --target ~/.codex/skills`);
}

function expandHome(input) {
  if (!input) return input;
  if (input === "~") return os.homedir();
  if (input.startsWith("~/")) return path.join(os.homedir(), input.slice(2));
  return input;
}

function copyDir(sourceDir, targetDir) {
  fs.mkdirSync(path.dirname(targetDir), { recursive: true });
  fs.cpSync(sourceDir, targetDir, { recursive: true, force: true });
}

if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
  usage();
  process.exit(0);
}

const [command, skillName] = args;

if (command !== "install" || !skillName) {
  usage();
  process.exit(1);
}

let targetRoot = path.join(os.homedir(), ".codex", "skills");
const targetFlagIndex = args.indexOf("--target");
if (targetFlagIndex !== -1) {
  const maybeTarget = args[targetFlagIndex + 1];
  if (!maybeTarget) {
    console.error("Missing value for --target");
    process.exit(1);
  }
  targetRoot = expandHome(maybeTarget);
}

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const sourceDir = path.join(repoRoot, "skills", skillName);
const targetDir = path.join(targetRoot, skillName);

if (!fs.existsSync(sourceDir)) {
  console.error(`Skill not found: ${skillName}`);
  process.exit(1);
}

copyDir(sourceDir, targetDir);

console.log(`Installed ${skillName} to ${targetDir}`);
