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

// Read package.json for version
let packageVersion = "unknown";
try {
  const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
  const pkgPath = path.join(repoRoot, "package.json");
  const pkgData = JSON.parse(fs.readFileSync(pkgPath, "utf-8"));
  packageVersion = pkgData.version;
} catch (e) {
  // ignore if can't read
}

// Parse SKILL.md frontmatter to extract description and aliases
function parseSkillMetadata(skillDir) {
  try {
    const skillMdPath = path.join(skillDir, "SKILL.md");
    if (!fs.existsSync(skillMdPath)) {
      return { description: "No description available" };
    }
    const content = fs.readFileSync(skillMdPath, "utf-8");
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) {
      return { description: "No description available" };
    }
    const frontmatter = match[1];
    const nameMatch = frontmatter.match(/^name:\s*(.+)$/m);
    const descMatch = frontmatter.match(/^description:\s*(.+?)$/m);
    return {
      description: descMatch ? descMatch[1].trim() : "No description available",
      name: nameMatch ? nameMatch[1].trim() : "unknown",
    };
  } catch (e) {
    return { description: "Error reading skill metadata" };
  }
}

function usage() {
  console.log(`zerofuturetech-skills v${packageVersion}

Usage:
  zerofuturetech-skills <skill-name-or-alias> [--platform codex|openclaw|claude] [--target <dir>]
  zerofuturetech-skills install <skill-name-or-alias> [--platform codex|openclaw|claude] [--target <dir>]
  zerofuturetech-skills --list [--verbose]
  zerofuturetech-skills --version
  zerofuturetech-skills --help

Aliases:
  wechat, x-essay, essay

Platforms:
  codex      Install to ~/.codex/skills (default)
  openclaw   Install to ~/.openclaw/skills
  claude     Install to ~/.claude/agents

Options:
  --dry-run      Show what would be installed without copying files
  --platform     Specify target platform (codex, openclaw, or claude)
  --target       Custom target directory
  --list         List all available skills
  --version      Show version number
  --help         Show this help message

Examples:
  zerofuturetech-skills wechat
  zerofuturetech-skills x-essay --platform claude
  zerofuturetech-skills --list
  zerofuturetech-skills wechat --dry-run
  zerofuturetech-skills high-agency-x-essay-writer --target ~/.custom/skills`);
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

function listSkills() {
  const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
  const skillsDir = path.join(repoRoot, "skills");

  if (!fs.existsSync(skillsDir)) {
    console.error("Skills directory not found");
    process.exit(1);
  }

  const skills = fs.readdirSync(skillsDir).filter(f => {
    const fullPath = path.join(skillsDir, f);
    return fs.statSync(fullPath).isDirectory();
  });

  console.log("Available skills:\n");

  skills.forEach(skillName => {
    const skillDir = path.join(skillsDir, skillName);
    const metadata = parseSkillMetadata(skillDir);

    // Find aliases for this skill
    const aliases = Object.entries(skillAliases)
      .filter(([, value]) => value === skillName)
      .map(([key]) => key);

    const aliasStr = aliases.length > 0 ? ` (alias: ${aliases.join(", ")})` : "";

    // Truncate description if too long
    const desc = metadata.description.length > 80
      ? metadata.description.substring(0, 77) + "..."
      : metadata.description;

    console.log(`• ${skillName}${aliasStr}`);
    console.log(`  ${desc}\n`);
  });
}

// Handle version flag
if (args.includes("--version") || args.includes("-v")) {
  console.log(`zerofuturetech-skills v${packageVersion}`);
  process.exit(0);
}

// Handle list flag
if (args.includes("--list")) {
  listSkills();
  process.exit(0);
}

// Handle help flag
if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
  usage();
  process.exit(0);
}

let command = args[0];
let skillName = args[1];

if (command !== "install" && !command.startsWith("--")) {
  skillName = command;
  command = "install";
}

if (!skillName || skillName.startsWith("--")) {
  console.error("Error: skill name is required\n");
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
    console.error("❌ Invalid value for --platform. Use: codex, openclaw, or claude");
    process.exit(1);
  }
  platform = maybePlatform;
  targetRoot = platformTargets[platform];
}
const targetFlagIndex = args.indexOf("--target");
if (targetFlagIndex !== -1) {
  const maybeTarget = args[targetFlagIndex + 1];
  if (!maybeTarget) {
    console.error("❌ Missing value for --target");
    process.exit(1);
  }
  targetRoot = expandHome(maybeTarget);
}

const dryRun = args.includes("--dry-run");

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const codexSourceDir = path.join(repoRoot, "skills", skillName);
const claudeSourceFile = path.join(repoRoot, "platforms", "claude", "agents", `${skillName}.md`);

if (!fs.existsSync(codexSourceDir) && !fs.existsSync(claudeSourceFile)) {
  // Try to find similar skill names for suggestion
  const skillsDir = path.join(repoRoot, "skills");
  const availableSkills = fs.existsSync(skillsDir)
    ? fs.readdirSync(skillsDir).filter(f => fs.statSync(path.join(skillsDir, f)).isDirectory())
    : [];

  console.error(`❌ Skill not found: ${skillName}`);
  if (availableSkills.length > 0) {
    console.error(`\nAvailable skills: ${availableSkills.join(", ")}`);
    console.error(`\nTip: Run 'zerofuturetech-skills --list' to see all skills with descriptions`);
  }
  process.exit(1);
}

if (platform === "claude") {
  if (!fs.existsSync(claudeSourceFile)) {
    console.error(`❌ Claude agent not found for: ${skillName}`);
    process.exit(1);
  }
  const targetFile = path.join(targetRoot, `${skillName}.md`);

  if (dryRun) {
    console.log(`📋 Dry-run: would install Claude agent`);
    console.log(`   Source: ${claudeSourceFile}`);
    console.log(`   Target: ${targetFile}`);
    process.exit(0);
  }

  copyFile(claudeSourceFile, targetFile);
  console.log(`✅ Installed ${skillName} for Claude Code to ${targetFile}`);
  process.exit(0);
}

const targetDir = path.join(targetRoot, skillName);

if (dryRun) {
  console.log(`📋 Dry-run: would install ${skillName} for ${platform}`);
  console.log(`   Source: ${codexSourceDir}`);
  console.log(`   Target: ${targetDir}`);
  process.exit(0);
}

copyDir(codexSourceDir, targetDir);

console.log(`✅ Installed ${skillName} for ${platform} to ${targetDir}`);
