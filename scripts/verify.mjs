import { existsSync, readFileSync } from "node:fs";

const requiredFiles = [
  "AGENTS.md",
  "CLAUDE.md",
  "HANDOFF-JA.md",
  "docs/vision.md",
  "docs/state.md",
  "docs/decisions.md",
  "docs/issues.md",
  "docs/repo-map.md",
  "tasks.md",
  ".claude/settings.json",
  ".env.example",
  ".gitignore",
  "scripts/verify.mjs",
];

const missing = requiredFiles.filter((file) => !existsSync(file));

if (missing.length > 0) {
  console.error(`Missing required files:\n${missing.map((file) => `- ${file}`).join("\n")}`);
  process.exit(1);
}

const envExample = readFileSync(".env.example", "utf8");
if (!envExample.includes("GEMINI_API_KEY=your_key_here")) {
  console.error(".env.example must include GEMINI_API_KEY=your_key_here");
  process.exit(1);
}

console.log("pm-zero v9.4 minimal structure verified");
