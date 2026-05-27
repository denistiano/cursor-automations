const DATA_URL = "data/site.json";
const REPO_URL = "https://github.com/denistiano/cursor-automations";

const state = {
  data: null,
  route: { view: "home" },
  query: "",
  taskFilter: "open",
};

const main = document.querySelector("#main");
const searchInput = document.querySelector("#searchInput");
const pageTitle = document.querySelector("#pageTitle");
const pageSubtitle = document.querySelector("#pageSubtitle");
const syncStatus = document.querySelector("#syncStatus");
const layout = document.querySelector(".app-layout");

document.addEventListener("DOMContentLoaded", init);

async function init() {
  wireNavigation();
  searchInput.addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    render();
  });

  try {
    const response = await fetch(DATA_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`Could not load ${DATA_URL}`);
    state.data = await response.json();
    layout.dataset.state = "ready";
    updateSyncStatus();
    navigate(parseRoute(), { replace: false });
  } catch (error) {
    layout.dataset.state = "error";
    renderError(error);
  }
}

function wireNavigation() {
  document.querySelector("#sidebarNav").addEventListener("click", (event) => {
    const link = event.target.closest("a[data-route]");
    if (!link) return;
    event.preventDefault();
    navigate({ view: link.dataset.route });
  });

  window.addEventListener("hashchange", () => {
    navigate(parseRoute(), { replace: false });
  });

  main.addEventListener("click", (event) => {
    const docLink = event.target.closest("[data-doc-path]");
    if (docLink) {
      event.preventDefault();
      navigate({ view: "doc", path: docLink.dataset.docPath });
      return;
    }

    const filterBtn = event.target.closest("[data-task-filter]");
    if (filterBtn) {
      state.taskFilter = filterBtn.dataset.taskFilter;
      render();
      return;
    }

    const downloadBtn = event.target.closest("[data-download-path]");
    if (downloadBtn) {
      event.preventDefault();
      downloadDocument(downloadBtn.dataset.downloadPath);
      return;
    }

    const repoLink = event.target.closest("[data-repo-path]");
    if (repoLink) {
      event.preventDefault();
      window.open(repoUrl(repoLink.dataset.repoPath), "_blank", "noreferrer");
    }
  });
}

function parseRoute() {
  const raw = window.location.hash.replace(/^#/, "") || "home";
  if (raw.startsWith("doc/")) {
    return { view: "doc", path: decodeURIComponent(raw.slice(4)) };
  }
  return { view: raw.split("?")[0] || "home" };
}

function navigate(route, options = {}) {
  state.route = route;
  if (options.replace !== false) {
    const hash = route.view === "doc" ? `doc/${encodeURIComponent(route.path)}` : route.view;
    if (window.location.hash.replace("#", "") !== hash) {
      window.location.hash = hash;
    }
  }
  setActiveNav(route.view === "doc" ? "documents" : route.view);
  render();
}

function setActiveNav(view) {
  document.querySelectorAll(".sidebar-nav a").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.route === view);
  });
}

function updateSyncStatus() {
  const generated = new Date(state.data.meta.generatedAt);
  syncStatus.textContent = `Synced ${generated.toLocaleString([], { dateStyle: "medium", timeStyle: "short" })}`;
}

function render() {
  if (!state.data) return;

  const titles = {
    home: ["Home", "Today’s priorities and latest standup"],
    tasks: ["Tasks", "From planning/TODO.md — Denis vs PM/Agent"],
    documents: ["Documents", "Business plans, research, planning, and ops docs"],
    standups: ["Standups", "Daily PM records"],
    careers: ["Careers", "Open roles and job descriptions"],
    research: ["Research", "Competitor watchlist and reports"],
    automations: ["Automations", "Cursor automation prompts and checklists"],
    doc: ["Document", ""],
  };

  const route = state.route;
  if (route.view === "doc") {
    const doc = state.data.documents.documents.find((item) => item.path === route.path);
    pageTitle.textContent = doc?.title || "Document";
    pageSubtitle.textContent = doc?.path || "";
  } else {
    const [title, subtitle] = titles[route.view] || ["HQ", ""];
    pageTitle.textContent = title;
    pageSubtitle.textContent = subtitle;
  }

  const renderers = {
    home: renderHome,
    tasks: renderTasks,
    documents: renderDocuments,
    doc: renderDocumentReader,
    standups: renderStandups,
    careers: renderCareers,
    research: renderResearch,
    automations: renderAutomations,
  };

  main.innerHTML = renderers[route.view]?.() || renderHome();
  applyGlobalSearch();
}

function renderHome() {
  const { todo, standups, documents, jobs } = state.data;
  const latest = standups.latest;
  const openTasks = todo.groups
    .flatMap((group) => group.items.map((item) => ({ ...item, group: group.title })))
    .filter((item) => !item.done)
    .slice(0, 6);

  return `
    <div class="stats-row">
      ${statCard(todo.counts.open, "Open tasks")}
      ${statCard(todo.counts.done, "Done")}
      ${statCard(documents.documents.length, "Documents")}
      ${statCard(jobs.filter((job) => job.hasPositionText).length, "Active roles")}
    </div>

    <div class="grid-2">
      <section class="panel" data-search-scope>
        <div class="panel-header"><h2>Open tasks</h2><a href="#tasks">View all</a></div>
        <div class="panel-body">
          ${
            openTasks.length
              ? `<ul class="task-list">${openTasks.map((item) => taskItem(item)).join("")}</ul>`
              : "<p class=\"empty\">No open tasks.</p>"
          }
        </div>
      </section>

      <section class="panel" data-search-scope>
        <div class="panel-header"><h2>Latest standup</h2><a href="#standups">History</a></div>
        <div class="panel-body">
          ${
            latest
              ? `
                <p><strong>${escapeHtml(latest.date)}</strong></p>
                <h4>Today</h4>
                <ul>${listItems(latest.today)}</ul>
                <h4>Blockers</h4>
                <ul>${listItems(latest.blockers)}</ul>
              `
              : "<p class=\"empty\">No standups yet.</p>"
          }
        </div>
      </section>
    </div>

    <section class="panel" data-search-scope>
      <div class="panel-header"><h2>Recent documents</h2><a href="#documents">Browse library</a></div>
      <div class="panel-body">
        <ul class="task-list">
          ${documents.documents
            .slice(0, 5)
            .map(
              (doc) => `
                <li class="task-item">
                  <a href="#doc/${encodeURIComponent(doc.path)}" data-doc-path="${escapeAttr(doc.path)}">
                    <strong>${escapeHtml(doc.title)}</strong>
                    <span class="page-subtitle"> — ${escapeHtml(doc.category)}</span>
                  </a>
                </li>
              `
            )
            .join("")}
        </ul>
      </div>
    </section>
  `;
}

function renderTasks() {
  const { todo } = state.data;
  const filter = state.taskFilter;

  return `
    <section class="panel" data-search-scope>
      <div class="panel-header">
        <h2>Task board</h2>
        <span class="badge badge-open">${todo.counts.open} open</span>
      </div>
      <div class="panel-body">
        <div class="task-filters">
          ${filterButton("open", "Open", filter)}
          ${filterButton("done", "Done", filter)}
          ${filterButton("all", "All", filter)}
        </div>
        ${todo.groups
          .map((group) => {
            const items = group.items.filter((item) => {
              if (filter === "open") return !item.done;
              if (filter === "done") return item.done;
              return true;
            });
            if (!items.length) return "";
            return `
              <div class="task-group" data-search-text="${escapeAttr(group.title)}">
                <h3>${escapeHtml(group.title)}</h3>
                <ul class="task-list">
                  ${items.map((item) => taskItem(item)).join("")}
                </ul>
              </div>
            `;
          })
          .join("")}
        <p class="page-subtitle">Source: <a href="#" data-repo-path="${escapeAttr(todo.path)}">${escapeHtml(todo.path)}</a></p>
      </div>
    </section>
  `;
}

function renderDocuments() {
  return renderDocumentLayout(null);
}

function renderDocumentReader() {
  const path = state.route.path;
  const doc = state.data.documents.documents.find((item) => item.path === path);
  if (!doc) {
    return `
      <section class="panel">
        <div class="panel-body empty">
          <p>Document not found: ${escapeHtml(path)}</p>
          <a href="#documents">Back to library</a>
        </div>
      </section>
    `;
  }
  return renderDocumentLayout(doc);
}

function renderDocumentLayout(activeDoc) {
  const { documents, categories } = state.data.documents;
  const grouped = categories.map((category) => ({
    category,
    items: documents.filter((doc) => doc.category === category),
  }));

  const reader = activeDoc
    ? `
        <div class="panel-body">
          <div class="doc-toolbar">
            <button type="button" class="btn btn-primary" data-download-path="${escapeAttr(activeDoc.path)}">Download .md</button>
            <a class="btn" href="#" data-repo-path="${escapeAttr(activeDoc.path)}">Open on GitHub</a>
            <span class="page-subtitle">${formatBytes(activeDoc.size)} · ${escapeHtml(activeDoc.category)}</span>
          </div>
          <article class="markdown">${renderMarkdown(activeDoc.content)}</article>
        </div>
      `
    : `
        <div class="panel-body empty">
          <p>Select a document from the list, or use search to filter.</p>
          <p class="page-subtitle">${documents.length} markdown files from planning, business, research, and docs.</p>
        </div>
      `;

  return `
    <div class="doc-layout" data-search-scope>
      <aside class="panel doc-sidebar">
        <div class="panel-header"><h2>Library</h2></div>
        <div class="panel-body">
          ${grouped
            .map(
              (group) => `
                <div class="doc-category">
                  <h3>${escapeHtml(group.category)}</h3>
                  ${group.items
                    .map((doc) => {
                      const isActive = activeDoc?.path === doc.path;
                      return `
                        <a class="doc-link ${isActive ? "is-active" : ""}" href="#doc/${encodeURIComponent(doc.path)}" data-doc-path="${escapeAttr(doc.path)}" data-search-text="${escapeAttr(`${doc.title} ${doc.path} ${doc.excerpt}`)}">
                          ${escapeHtml(doc.title)}
                        </a>
                      `;
                    })
                    .join("")}
                </div>
              `
            )
            .join("")}
        </div>
      </aside>
      <section class="panel doc-reader">${reader}</section>
    </div>
  `;
}

function renderStandups() {
  const { standups } = state.data;

  return `
    <section class="panel" data-search-scope>
      <div class="panel-header"><h2>Standup history</h2></div>
      <div class="panel-body">
        ${
          standups.entries.length
            ? standups.entries
                .map(
                  (entry) => `
                    <article class="standup-card panel" data-search-text="${escapeAttr(JSON.stringify(entry))}">
                      <header>
                        <time>${escapeHtml(entry.date)}</time>
                        <a href="#" data-repo-path="${escapeAttr(entry.path)}">${escapeHtml(entry.path)}</a>
                      </header>
                      <div class="standup-sections">
                        <div><h4>Done</h4><ul>${listItems(entry.done)}</ul></div>
                        <div><h4>Today</h4><ul>${listItems(entry.today)}</ul></div>
                        <div><h4>Blockers</h4><ul>${listItems(entry.blockers)}</ul></div>
                        <div><h4>Agent next</h4><ul>${listItems(entry.agentNextActions)}</ul></div>
                      </div>
                    </article>
                  `
                )
                .join("")
            : "<p class=\"empty\">No standups yet.</p>"
        }
      </div>
    </section>
  `;
}

function renderCareers() {
  const { jobs } = state.data;

  return `
    <section class="panel" data-search-scope>
      <div class="panel-header"><h2>Open roles</h2></div>
      <div class="panel-body">
        ${
          jobs.length
            ? jobs
                .map(
                  (job) => `
                    <article class="panel standup-card" data-search-text="${escapeAttr(job.title)}">
                      <header>
                        <h3>${escapeHtml(job.title)}</h3>
                        <span class="badge ${job.hasPositionText ? "badge-done" : "badge-open"}">
                          ${job.hasPositionText ? "JD in repo" : "Awaiting text"}
                        </span>
                      </header>
                      ${job.status ? `<p><strong>Status:</strong> ${escapeHtml(job.status)}</p>` : ""}
                      ${
                        job.positionText
                          ? `<article class="markdown">${renderMarkdown(job.positionText)}</article>`
                          : "<p class=\"empty\">Position text not added yet.</p>"
                      }
                      <div class="doc-toolbar">
                        <button type="button" class="btn btn-primary" data-download-path="${escapeAttr(job.path)}">Download JD</button>
                        <a class="btn" href="#" data-repo-path="${escapeAttr(job.path)}">Edit on GitHub</a>
                      </div>
                      ${
                        job.checklist.length
                          ? `<h4>Publish checklist</h4><ul>${job.checklist.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`
                          : ""
                      }
                    </article>
                  `
                )
                .join("")
            : "<p class=\"empty\">No job files in business/jobs/.</p>"
        }
      </div>
    </section>
  `;
}

function renderResearch() {
  const { competitors } = state.data.research;

  return `
    <div class="grid-2" data-search-scope>
      <section class="panel">
        <div class="panel-header"><h2>Competitor watchlist</h2></div>
        <div class="panel-body">
          ${
            competitors.watchlist.length
              ? `<div class="markdown">${tableHtml(competitors.watchlist)}</div>`
              : "<p class=\"empty\">No competitors listed.</p>"
          }
        </div>
      </section>
      <section class="panel">
        <div class="panel-header"><h2>Reports</h2></div>
        <div class="panel-body">
          <ul class="task-list">
            ${
              competitors.reports.length
                ? competitors.reports
                    .map(
                      (report) => `
                        <li>
                          <a href="#doc/${encodeURIComponent(report.path)}" data-doc-path="${escapeAttr(report.path)}">
                            ${escapeHtml(report.title || report.path)}
                          </a>
                        </li>
                      `
                    )
                    .join("")
                : "<li>No dated reports yet.</li>"
            }
          </ul>
        </div>
      </section>
    </div>
  `;
}

function renderAutomations() {
  const { automations } = state.data;

  return `
    <section class="panel" data-search-scope>
      <div class="panel-header"><h2>Automation prompts</h2></div>
      <div class="panel-body">
        ${automations
          .map(
            (automation) => `
              <article class="standup-card panel" data-search-text="${escapeAttr(automation.title)}">
                <header>
                  <h3>${escapeHtml(automation.settings.name || automation.title)}</h3>
                  <a href="#" data-repo-path="${escapeAttr(automation.path)}">${escapeHtml(automation.path)}</a>
                </header>
                <p><strong>Trigger:</strong> ${escapeHtml(automation.settings.trigger || "TBD")}</p>
                <p><strong>Tools:</strong> ${escapeHtml(automation.settings.tools || "TBD")}</p>
                <h4>Checklist</h4>
                <ul>${listItems(automation.checklist)}</ul>
                <pre><code>${escapeHtml(automation.promptPreview)}</code></pre>
              </article>
            `
          )
          .join("")}
      </div>
    </section>
  `;
}

function renderError(error) {
  main.innerHTML = `
    <section class="panel error-state">
      <h2>Could not load dashboard data</h2>
      <p>${escapeHtml(error.message)}</p>
      <p>Run <code>node scripts/build-site-data.js</code> then serve the <code>web/</code> folder.</p>
    </section>
  `;
}

function applyGlobalSearch() {
  const query = state.query;
  if (!query) {
    main.querySelectorAll("[data-search-hidden]").forEach((el) => el.classList.remove("hidden"));
    return;
  }

  main.querySelectorAll("[data-search-text], .task-item, .task-group, .standup-card, .doc-link").forEach((el) => {
    const text = (el.dataset.searchText || el.textContent || "").toLowerCase();
    const match = text.includes(query);
    el.classList.toggle("hidden", !match);
    el.dataset.searchHidden = match ? "" : "true";
  });
}

function downloadDocument(path) {
  const doc = state.data.documents.documents.find((item) => item.path === path);
  if (!doc) return;

  const blob = new Blob([doc.content], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = path.split("/").pop() || "document.md";
  anchor.click();
  URL.revokeObjectURL(url);
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const html = [];
  let inCode = false;
  let codeBuffer = [];
  let listType = null;

  const flushList = () => {
    if (!listType) return;
    html.push(`</${listType}>`);
    listType = null;
  };

  for (const line of lines) {
    if (line.trim().startsWith("```")) {
      if (!inCode) {
        flushList();
        inCode = true;
        codeBuffer = [];
      } else {
        html.push(`<pre><code>${escapeHtml(codeBuffer.join("\n"))}</code></pre>`);
        inCode = false;
      }
      continue;
    }

    if (inCode) {
      codeBuffer.push(line);
      continue;
    }

    if (line.trim().startsWith("|")) {
      flushList();
      continue;
    }

    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      flushList();
      const level = heading[1].length;
      html.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }

    const bullet = line.match(/^\s*[-*]\s+(.+)$/);
    if (bullet) {
      if (listType !== "ul") {
        flushList();
        listType = "ul";
        html.push("<ul>");
      }
      html.push(`<li>${inlineMarkdown(bullet[1])}</li>`);
      continue;
    }

    const numbered = line.match(/^\s*\d+\.\s+(.+)$/);
    if (numbered) {
      if (listType !== "ol") {
        flushList();
        listType = "ol";
        html.push("<ol>");
      }
      html.push(`<li>${inlineMarkdown(numbered[1])}</li>`);
      continue;
    }

    if (!line.trim()) {
      flushList();
      continue;
    }

    flushList();
    html.push(`<p>${inlineMarkdown(line)}</p>`);
  }

  flushList();
  return html.join("\n");
}

function inlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
}

function tableHtml(rows) {
  if (!rows?.length) return "";
  const columns = Object.keys(rows[0]);
  return `
    <table>
      <thead><tr>${columns.map((col) => `<th>${escapeHtml(titleCase(col))}</th>`).join("")}</tr></thead>
      <tbody>
        ${rows.map((row) => `<tr>${columns.map((col) => `<td>${escapeHtml(row[col] || "")}</td>`).join("")}</tr>`).join("")}
      </tbody>
    </table>
  `;
}

function taskItem(item) {
  return `
    <li class="task-item ${item.done ? "is-done" : ""}" data-search-text="${escapeAttr(item.text)}">
      <span class="task-check" aria-hidden="true">${item.done ? "✓" : ""}</span>
      <span class="task-text">${escapeHtml(item.text)}</span>
    </li>
  `;
}

function filterButton(value, label, active) {
  return `<button type="button" class="filter-btn ${active === value ? "is-active" : ""}" data-task-filter="${value}">${label}</button>`;
}

function statCard(value, label) {
  return `<div class="stat-card"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(label)}</span></div>`;
}

function listItems(items) {
  const safe = (items || []).filter(Boolean);
  if (!safe.length) return "<li class=\"page-subtitle\">—</li>";
  return safe.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
}

function repoUrl(path) {
  return `${REPO_URL}/blob/master/${path}`;
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  return `${(bytes / 1024).toFixed(1)} KB`;
}

function titleCase(value) {
  return value.replace(/-/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value);
}
