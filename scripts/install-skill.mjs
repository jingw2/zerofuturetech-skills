#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const args = process.argv.slice(2);
const skillAliases = {
  wechat: "zerofuturetech-wechat-publisher",
  "x-essay": "high-agency-x-essay-writer",
  essay: "high-agency-x-essay-writer",
};
const platformTargets = {
  codex: path.join(os.homedir(), ".codex", "skills"),
  openclaw: path.join(os.homedir(), ".openclaw", "skills"),
  claude: path.join(os.homedir(), ".claude", "agents"),
};

function usage() {
  console.log(`Usage:
  zerofuturetech-skills <skill-name-or-alias> [--platform codex|openclaw|claude] [--target <dir>]
  zerofuturetech-skills install <skill-name-or-alias> [--platform codex|openclaw|claude] [--target <dir>]

Examples:
  zerofuturetech-skills wechat
  zerofuturetech-skills x-essay
  zerofuturetech-skills wechat --platform openclaw
  zerofuturetech-skills wechat --platform claude
  zerofuturetech-skills high-agency-x-essay-writer
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

function copyFile(sourceFile, targetFile) {
  fs.mkdirSync(path.dirname(targetFile), { recursive: true });
  fs.copyFileSync(sourceFile, targetFile);
}

if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
  usage();
  process.exit(0);
}

let command = args[0];
let skillName = args[1];

if (command !== "install") {
  skillName = command;
  command = "install";
}

if (!skillName) {
  usage();
  process.exit(1);
}

skillName = skillAliases[skillName] || skillName;

let targetRoot = path.join(os.homedir(), ".codex", "skills");
let platform = "codex";
const platformFlagIndex = args.indexOf("--platform");
if (platformFlagIndex !== -1) {
  const maybePlatform = args[platformFlagIndex + 1];
  if (!maybePlatform || !platformTargets[maybePlatform]) {
    console.error("Invalid value for --platform. Use codex, openclaw, or claude.");
    process.exit(1);
  }
  platform = maybePlatform;
  targetRoot = platformTargets[platform];
}
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
const codexSourceDir = path.join(repoRoot, "skills", skillName);
const claudeSourceFile = path.join(repoRoot, "platforms", "claude", "agents", `${skillName}.md`);

if (!fs.existsSync(codexSourceDir) && !fs.existsSync(claudeSourceFile)) {
  console.error(`Skill not found: ${skillName}`);
  process.exit(1);
}

if (platform === "claude") {
  if (!fs.existsSync(claudeSourceFile)) {
    console.error(`Claude agent not found for: ${skillName}`);
    process.exit(1);
  }
  const targetFile = path.join(targetRoot, `${skillName}.md`);
  copyFile(claudeSourceFile, targetFile);
  console.log(`Installed ${skillName} for Claude Code to ${targetFile}`);
  process.exit(0);
}

const targetDir = path.join(targetRoot, skillName);
copyDir(codexSourceDir, targetDir);

console.log(`Installed ${skillName} for ${platform} to ${targetDir}`);
