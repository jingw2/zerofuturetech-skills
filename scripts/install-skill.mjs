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

function usage() {
  console.log(`Usage:
  zerofuturetech-skills <skill-name-or-alias> [--target <dir>]
  zerofuturetech-skills install <skill-name-or-alias> [--target <dir>]

Examples:
  zerofuturetech-skills wechat
  zerofuturetech-skills x-essay
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
