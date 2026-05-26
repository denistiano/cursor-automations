#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const root = path.resolve(__dirname, "..");
const outputPath = path.join(root, "web", "data", "site.json");

function readMaybe(relativePath) {
  const filePath = path.join(root, relativePath);
  if (!fs.existsSync(filePath)) return "";
  return fs.readFileSync(filePath, "utf8").replace(/\r\n/g, "\n");
}

function exists(relativePath) {
  return fs.existsSync(path.join(root, relativePath));
}

function listFiles(relativeDir, predicate = () => true) {
  const start = path.join(root, relativeDir);
  if (!fs.existsSync(start)) return [];

  const results = [];
  const stack = [start];
  while (stack.length > 0) {
    const current = stack.pop();
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(fullPath);
      } else {
        const relativePath = toRepoPath(fullPath);
        if (predicate(relativePath)) results.push(relativePath);
      }
    }
  }

  return results.sort();
}

function toRepoPath(filePath) {
  return path.relative(root, filePath).split(path.sep).join("/");
}

function getGitSha() {
  if (process.env.GITHUB_SHA) return process.env.GITHUB_SHA;
  try {
    return execFileSync("git", ["rev-parse", "HEAD"], {
      cwd: root,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
  } catch (_error) {
    return null;
  }
}

function cleanInline(value) {
  return value
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1")
    .replace(/_([^_]+)_/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .trim();
}

function slugify(value) {
  return cleanInline(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function parseMarkdownTable(lines, startIndex) {
  const rows = [];
  let index = startIndex;

  while (index < lines.length && !lines[index].trim().startsWith("|")) index += 1;
  if (index + 1 >= lines.length) return { rows, nextIndex: index };

  const headers = splitTableRow(lines[index]);
  const separator = splitTableRow(lines[index + 1]);
  if (headers.length === 0 || separator.some((cell) => !/^:?-{2,}:?$/.test(cell.trim()))) {
    return { rows, nextIndex: index };
  }

  index += 2;
  while (index < lines.length && lines[index].trim().startsWith("|")) {
    const cells = splitTableRow(lines[index]);
    const row = {};
    headers.forEach((header, headerIndex) => {
      row[slugify(header) || `column_${headerIndex + 1}`] = cleanInline(cells[headerIndex] || "");
    });
    if (Object.values(row).some(Boolean)) rows.push(row);
    index += 1;
  }

  return { rows, nextIndex: index };
}

function splitTableRow(line) {
  const trimmed = line.trim().replace(/^\|/, "").replace(/\|$/, "");
  const cells = [];
  let current = "";
  let inCode = false;

  for (const char of trimmed) {
    if (char === "`") inCode = !inCode;
    if (char === "|" && !inCode) {
      cells.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }

  cells.push(current.trim());
  return cells;
}

function parseSections(markdown, depth = 2) {
  const lines = markdown.split("\n");
  const headingPattern = new RegExp(`^#{${depth}}\\s+(.+)$`);
  const sections = [];
  let current = null;

  for (const line of lines) {
    const match = line.match(headingPattern);
    if (match) {
      if (current) current.content = current.lines.join("\n").trim();
      current = {
        title: cleanInline(match[1]),
        slug: slugify(match[1]),
        lines: [],
        content: "",
      };
      sections.push(current);
      continue;
    }

    if (current) current.lines.push(line);
  }

  if (current) current.content = current.lines.join("\n").trim();
  return sections.map(({ lines: _lines, ...section }) => section);
}

function parseListItems(content) {
  return content
    .split("\n")
    .map((line) => line.match(/^\s*(?:[-*]|\d+\.)\s+(.*)$/))
    .filter(Boolean)
    .map((match) => cleanInline(match[1].replace(/^\[[ xX]\]\s+/, "")))
    .filter(Boolean);
}

function parseTodo() {
  const relativePath = "planning/TODO.md";
  const markdown = readMaybe(relativePath);
  const groups = parseSections(markdown).map((section) => {
    const items = section.content
      .split("\n")
      .map((line) => {
        const match = line.match(/^\s*-\s+\[([ xX])\]\s+(.*)$/);
        if (!match) return null;
        return {
          text: cleanInline(match[2]),
          done: match[1].toLowerCase() === "x",
          raw: match[2].trim(),
        };
      })
      .filter(Boolean);

    return { title: section.title, slug: section.slug, items };
  });

  const allItems = groups.flatMap((group) => group.items);
  return {
    path: relativePath,
    groups,
    counts: {
      total: allItems.length,
      done: allItems.filter((item) => item.done).length,
      open: allItems.filter((item) => !item.done).length,
    },
  };
}

function parseStandups() {
  const files = listFiles("planning/standups", (relativePath) =>
    /^planning\/standups\/\d{4}-\d{2}-\d{2}\.md$/.test(relativePath)
  );

  const entries = files
    .map((relativePath) => {
      const markdown = readMaybe(relativePath);
      const date = path.basename(relativePath, ".md");
      const sections = parseSections(markdown);
      const sectionBySlug = Object.fromEntries(sections.map((section) => [section.slug, section]));

      return {
        date,
        path: relativePath,
        done: parseListItems(sectionBySlug.done?.content || ""),
        today: parseListItems(sectionBySlug["today-max-3"]?.content || sectionBySlug.today?.content || ""),
        blockers: parseListItems(sectionBySlug["blockers-decisions-for-denis"]?.content || ""),
        agentNextActions: parseListItems(sectionBySlug["agent-next-actions"]?.content || ""),
      };
    })
    .sort((a, b) => b.date.localeCompare(a.date));

  return {
    entries,
    latest: entries[0] || null,
  };
}

function parseReadme() {
  const relativePath = "README.md";
  const markdown = readMaybe(relativePath);
  const lines = markdown.split("\n");
  const title = cleanInline((lines.find((line) => line.startsWith("# ")) || "# Course Business HQ").slice(2));
  const description = cleanInline(lines.find((line) => line.trim() && !line.startsWith("#")) || "");
  const areas = parseMarkdownTable(lines, lines.findIndex((line) => line.includes("| Area | Path | Purpose |"))).rows;

  const statusItems = lines
    .map((line) => {
      const match = line.match(/^- \[([ xX])\]\s+(.*)$/);
      if (!match) return null;
      return {
        text: cleanInline(match[2]),
        done: match[1].toLowerCase() === "x",
      };
    })
    .filter(Boolean);

  return { path: relativePath, title, description, areas, statusItems };
}

function parseBusinessPlan() {
  const relativePath = "business/plan-v1.md";
  const markdown = readMaybe(relativePath);
  const status = (markdown.match(/\*\*Status:\*\*\s*(.+)/) || [null, ""])[1].trim();
  const lastUpdated = (markdown.match(/\*\*Last updated:\*\*\s*(.+)/) || [null, ""])[1].trim();
  const sections = parseSections(markdown).map((section) => ({
    ...section,
    bullets: parseListItems(section.content),
    tables: extractTables(section.content),
  }));

  return { path: relativePath, status, lastUpdated, sections };
}

function extractTables(markdown) {
  const lines = markdown.split("\n");
  const tables = [];
  for (let index = 0; index < lines.length; index += 1) {
    if (!lines[index].trim().startsWith("|")) continue;
    const parsed = parseMarkdownTable(lines, index);
    if (parsed.rows.length > 0) tables.push(parsed.rows);
    index = Math.max(index, parsed.nextIndex - 1);
  }
  return tables;
}

function parseApprovedMessaging() {
  const relativePath = "business/approved-messaging.md";
  const markdown = readMaybe(relativePath);
  const sections = Object.fromEntries(parseSections(markdown).map((section) => [section.slug, section]));
  const course = {};

  for (const line of (sections["course-fill-in-with-denis"]?.content || "").split("\n")) {
    const match = line.match(/^-\s+\*\*([^:]+):\*\*\s*(.*)$/);
    if (match) course[slugify(match[1])] = cleanInline(match[2]);
  }

  return {
    path: relativePath,
    course,
    pricingAndLaunch: extractTables(sections["pricing-launch"]?.content || "")[0] || [],
    allowedClaims: parseListItems(sections["claims-we-allow"]?.content || ""),
    disallowedClaims: parseListItems(sections["claims-we-do-not-allow-until-approved"]?.content || ""),
  };
}

function parseCompetitors() {
  const relativePath = "research/competitors/COMPETITORS.md";
  const markdown = readMaybe(relativePath);
  const lines = markdown.split("\n");
  const tableStart = lines.findIndex((line) => line.includes("| Name | URL | Notes | Priority |"));
  const watchlist = parseMarkdownTable(lines, tableStart).rows;
  const reports = listFiles("research/competitors", (file) =>
    /^research\/competitors\/\d{4}-\d{2}-\d{2}-.+\.md$/.test(file)
  ).map((file) => ({
    path: file,
    title: cleanInline((readMaybe(file).split("\n").find((line) => line.startsWith("# ")) || "").replace(/^#\s+/, "")),
  }));

  return {
    path: relativePath,
    watchlist,
    reports,
    triggerHints: parseListItems(parseSections(markdown).find((section) => section.slug === "how-to-trigger-research")?.content || ""),
  };
}

function parseAutomationDoc(relativePath) {
  const markdown = readMaybe(relativePath);
  const lines = markdown.split("\n");
  const title = cleanInline((lines.find((line) => line.startsWith("# ")) || "# Automation").slice(2));
  const settingsIndex = lines.findIndex((line) => line.trim() === "## Settings");
  const settingsRows = parseMarkdownTable(lines, settingsIndex).rows;
  const settings = Object.fromEntries(
    settingsRows
      .filter((row) => row.field && row.value)
      .map((row) => [slugify(row.field), row.value])
  );
  const checklist = parseListItems(parseSections(markdown).find((section) => section.slug === "denis-checklist")?.content || "");
  const prompt = extractFirstCodeFence(markdown);

  return {
    path: relativePath,
    id: slugify(title),
    title,
    settings,
    checklist,
    promptPreview: prompt.split("\n").slice(0, 12).join("\n").trim(),
  };
}

function extractFirstCodeFence(markdown) {
  const match = markdown.match(/```(?:\w+)?\n([\s\S]*?)```/);
  return match ? match[1].trim() : "";
}

function parseAutomations() {
  return listFiles("docs/automations", (file) => /^docs\/automations\/\d{2}-.+\.md$/.test(file)).map(parseAutomationDoc);
}

function parseSocial() {
  const files = listFiles("content/social", (file) => file.endsWith(".md") && !file.endsWith("/_template.md"));
  const drafts = files.map((file) => {
    const markdown = readMaybe(file);
    const frontmatter = parseFrontmatter(markdown);
    return {
      path: file,
      title: cleanInline((markdown.split("\n").find((line) => line.startsWith("# ")) || "").replace(/^#\s+/, "")),
      platform: frontmatter.platform || "unknown",
      approved: frontmatter.approved === "true",
      scheduledAt: frontmatter.scheduled_at || null,
      postId: frontmatter.post_id || null,
    };
  });

  return {
    templatePath: exists("content/social/_template.md") ? "content/social/_template.md" : null,
    drafts,
    counts: {
      total: drafts.length,
      approved: drafts.filter((draft) => draft.approved).length,
      pending: drafts.filter((draft) => !draft.approved).length,
    },
  };
}

function parseFrontmatter(markdown) {
  if (!markdown.startsWith("---\n")) return {};
  const end = markdown.indexOf("\n---", 4);
  if (end === -1) return {};

  return markdown
    .slice(4, end)
    .split("\n")
    .reduce((frontmatter, line) => {
      const match = line.match(/^([^:]+):\s*(.*)$/);
      if (match) frontmatter[match[1].trim()] = match[2].trim();
      return frontmatter;
    }, {});
}

function buildData() {
  const readme = parseReadme();
  const todo = parseTodo();
  const standups = parseStandups();
  const businessPlan = parseBusinessPlan();
  const approvedMessaging = parseApprovedMessaging();
  const competitors = parseCompetitors();
  const automations = parseAutomations();
  const social = parseSocial();

  return {
    meta: {
      generatedAt: new Date().toISOString(),
      generator: "scripts/build-site-data.js",
      gitSha: getGitSha(),
      sources: [
        readme.path,
        todo.path,
        ...standups.entries.map((entry) => entry.path),
        businessPlan.path,
        approvedMessaging.path,
        competitors.path,
        ...competitors.reports.map((report) => report.path),
        ...automations.map((automation) => automation.path),
        social.templatePath,
        ...social.drafts.map((draft) => draft.path),
      ].filter(Boolean),
    },
    readme,
    todo,
    standups,
    business: {
      plan: businessPlan,
      approvedMessaging,
    },
    research: {
      competitors,
    },
    automations,
    social,
  };
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(buildData(), null, 2)}\n`);
console.log(`Wrote ${toRepoPath(outputPath)}`);
