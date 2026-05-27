const DATA_URL = "data/site.json";

const state = { data: null, section: "overview", query: "" };

const app = document.querySelector("#app");
const sidebarNav = document.querySelector("#sidebarNav");
const searchInput = document.querySelector("#searchInput");

document.addEventListener("DOMContentLoaded", init);

async function init() {
  wireControls();
  try {
    const response = await fetch(DATA_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`Could not load ${DATA_URL}`);
    state.data = await response.json();
    renderChrome();
    navigate(getSectionFromHash() || "overview");
  } catch (error) {
    app.innerHTML = `
      <section class="empty-state">
        <p class="eyebrow">Data unavailable</p>
        <h2>Could not load dashboard.</h2>
        <p>${escapeHtml(error.message)}</p>
        <p class="meta">Run <code>python3 scripts/build_site.py</code> from the repo root.</p>
      </section>`;
  }
}

function wireControls() {
  sidebarNav.addEventListener("click", (event) => {
    const link = event.target.closest("[data-section]");
    if (!link) return;
    event.preventDefault();
    navigate(link.dataset.section);
  });

  searchInput.addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    applySearch();
  });

  window.addEventListener("hashchange", () => navigate(getSectionFromHash() || "overview", { hash: false }));

  document.querySelector("#sidebarToggle").addEventListener("click", () => {
    document.body.classList.toggle("sidebar-open");
  });
}

function getSectionFromHash() {
  return window.location.hash.replace("#", "") || null;
}

function navigate(section, options = {}) {
  state.section = section;
  if (options.hash !== false) window.location.hash = section;
  document.querySelectorAll(".nav-link").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.section === section);
  });
  renderSection();
  document.body.classList.remove("sidebar-open");
}

function renderChrome() {
  const { data } = state;
  const generated = new Date(data.meta.generatedAt);
  document.querySelector("#generatedAt").textContent = `Updated ${generated.toLocaleString([], { dateStyle: "medium", timeStyle: "short" })}`;

  sidebarNav.innerHTML = data.ui.nav
    .map(
      (item) => `
        <a class="nav-link" href="#${escapeAttr(item.id)}" data-section="${escapeAttr(item.id)}">
          <span class="nav-icon">${icon(item.icon)}</span>
          <span>${escapeHtml(item.label)}</span>
        </a>`
    )
    .join("");

  const m = data.metrics;
  document.querySelector("#topbarMetrics").innerHTML = [
    metricPill(`${m.openTasks} open`),
    metricPill(`${m.standups} standups`),
    metricPill(`${m.automations} automations`),
  ].join("");
}

function metricPill(text) {
  return `<span class="metric-pill">${escapeHtml(text)}</span>`;
}

function renderSection() {
  const { data, section } = state;
  const navItem = data.ui.nav.find((item) => item.id === section) || data.ui.nav[0];
  const collection = navItem?.collection;
  const layoutConfig = collection ? data.ui.collections[collection] : null;

  const renderers = {
    overview: renderOverview,
  };

  if (collection && layoutConfig) {
    app.innerHTML = renderCollectionPage(navItem, collection, layoutConfig);
  } else {
    app.innerHTML = renderers[section]?.() || renderOverview();
  }
  applySearch();
}

function renderOverview() {
  const { project, metrics, entriesByCollection, ui } = state.data;
  const latestStandup = (entriesByCollection.standups || []).sort((a, b) =>
    (b.props.date || "").localeCompare(a.props.date || "")
  )[0];
  const blockers = (entriesByCollection.tasks || []).find((e) => e.slug === "blockers");
  const businessPlan = (entriesByCollection.business || []).find((e) => e.slug === "plan");
  const messaging = (entriesByCollection.business || []).find((e) => e.slug === "messaging");

  return `
    ${pageHeader("Overview", project.description || "SQLite-backed command center for the course business.")}
    <div class="stat-grid">
      ${statCard("Open tasks", metrics.openTasks, "warn")}
      ${statCard("Done tasks", metrics.doneTasks, "good")}
      ${statCard("Standups", metrics.standups)}
      ${statCard("Entries", metrics.entries)}
    </div>
    <div class="panel-grid two">
      ${panel(
        "Latest standup",
        latestStandup
          ? `
            <p class="eyebrow">${escapeHtml(latestStandup.props.date || latestStandup.slug)}</p>
            <h3>Today</h3>
            ${listItems(latestStandup.listItems.filter((i) => i.section === "today"))}
            <h3>Blockers</h3>
            ${listItems(latestStandup.listItems.filter((i) => i.section === "blockers"))}
          `
          : "<p class=\"muted\">No standups yet.</p>"
      )}
      ${panel(
        "Active blockers",
        blockers?.listItems?.length
          ? listItems(blockers.listItems.filter((i) => i.section === "items"), { showOwner: true })
          : "<p class=\"muted\">No blockers recorded.</p>"
      )}
    </div>
    <div class="panel-grid two">
      ${panel(
        "Business signal",
        `
          <p><strong>Plan status:</strong> ${escapeHtml(businessPlan?.status || "Unknown")}</p>
          <p><strong>Working title:</strong> ${escapeHtml(messaging?.props?.course?.["working-title"] || "TBD")}</p>
          <div class="chip-row">${chip("SQLite source of truth")}${chip("Generic collections model")}</div>
        `
      )}
      ${panel(
        "Collections",
        `<div class="chip-row">${ui.nav
          .filter((n) => n.collection)
          .map((n) => chip(n.label))
          .join("")}</div>`
      )}
    </div>`;
}

function renderCollectionPage(navItem, collection, layoutConfig) {
  const entries = state.data.entriesByCollection[collection] || [];
  const collectionMeta = state.data.collections.find((c) => c.slug === collection);
  const layout = layoutConfig.layout;

  const body = {
    checklist_groups: () => renderChecklistGroups(entries, layoutConfig, collectionMeta),
    timeline: () => renderTimeline(entries, layoutConfig, collectionMeta),
    roadmap: () => renderRoadmap(entries, layoutConfig, collectionMeta),
    documents: () => renderDocuments(entries, layoutConfig, collectionMeta),
    tracker: () => renderTracker(entries, layoutConfig, collectionMeta),
    research: () => renderResearch(entries, layoutConfig, collectionMeta),
    cards: () => renderCards(entries, layoutConfig, collectionMeta),
    names: () => renderNames(entries, layoutConfig, collectionMeta),
    automations: () => renderAutomations(entries, layoutConfig, collectionMeta),
  }[layout]?.() || renderCards(entries, layoutConfig, collectionMeta);

  return `${pageHeader(navItem.label, collectionMeta?.description || "")}${body}`;
}

function renderChecklistGroups(entries, config) {
  const groups = entries.filter((e) => e.props.kind === "group" || (e.slug !== "blockers" && e.slug !== "project-status"));
  const blockers = entries.find((e) => e.slug === "blockers");

  return `
    <div class="panel-grid two">
      ${groups
        .map((group) =>
          panel(
            group.title,
            group.listItems.filter((i) => i.section === "items").length
              ? checklist(group.listItems.filter((i) => i.section === "items"))
              : "<p class=\"muted\">No items.</p>",
            { owner: group.owner }
          )
        )
        .join("")}
    </div>
    ${
      config.showBlockers && blockers
        ? panel("Blockers", listItems(blockers.listItems.filter((i) => i.section === "items"), { showOwner: true }))
        : ""
    }`;
}

function renderTimeline(entries, config) {
  const sorted = [...entries].sort((a, b) => (b.props[config.dateField] || b.slug).localeCompare(a.props[config.dateField] || a.slug));
  const sections = config.listSections || ["done", "today", "blockers", "agent_next"];

  return `
    <div class="timeline">
      ${
        sorted.length
          ? sorted
              .map(
                (entry) => `
                  <article class="panel timeline-item" data-search-text="${searchText(entry)}">
                    <header class="panel-head">
                      <div>
                        <p class="eyebrow">${escapeHtml(entry.props.date || entry.slug)}</p>
                        <h3>${escapeHtml(entry.title)}</h3>
                      </div>
                    </header>
                    <div class="panel-grid two">
                      ${sections
                        .map(
                          (section) => `
                            <div>
                              <h4>${escapeHtml(titleCase(section))}</h4>
                              ${listItems(entry.listItems.filter((i) => i.section === section))}
                            </div>`
                        )
                        .join("")}
                    </div>
                  </article>`
              )
              .join("")
          : panel("No entries", "<p class=\"muted\">Nothing in this collection yet.</p>")
      }
    </div>`;
}

function renderRoadmap(entries) {
  const tracks = entries.find((e) => e.slug === "tracks");
  const phases = entries.find((e) => e.slug === "phases");
  const nearTerm = entries.find((e) => e.slug === "near-term");

  return `
    <div class="panel-grid">
      ${tracks ? panel("Launch tracks", dataTable(tracks.tables.find((t) => t.name === "tracks"))) : ""}
      ${phases ? panel("Phases", dataTable(phases.tables.find((t) => t.name === "phases"))) : ""}
      ${nearTerm ? panel("Near-term queue", listItems(nearTerm.listItems.filter((i) => i.section === "items"))) : ""}
    </div>`;
}

function renderDocuments(entries, config) {
  const slugs = config.primarySlugs || [];
  const primary = entries.filter((e) => slugs.includes(e.slug));

  return `
    <div class="panel-grid">
      ${primary
        .map((entry) => {
          const tables = entry.tables.map((t) => dataTable(t)).join("");
          const sections = [...new Set(entry.listItems.map((i) => i.section))];
          const lists = sections
            .map(
              (section) => `
                <h4>${escapeHtml(titleCase(section))}</h4>
                ${listItems(entry.listItems.filter((i) => i.section === section))}`
            )
            .join("");
          return panel(
            entry.title,
            `
              ${entry.status ? `<p><strong>Status:</strong> ${escapeHtml(entry.status)}</p>` : ""}
              ${bodyPreview(entry.body)}
              ${lists}
              ${tables}
            `
          );
        })
        .join("")}
      ${renderChildSections(entries, slugs)}
    </div>`;
}

function renderChildSections(entries, excludeSlugs) {
  const children = entries.filter((e) => excludeSlugs.includes(e.slug) === false && e.parentId);
  if (!children.length) return "";
  return `
    <div class="panel-grid two">
      ${children
        .slice(0, 12)
        .map((child) =>
          panel(
            child.title,
            `${bodyPreview(child.body)}${child.tables.map((t) => dataTable(t)).join("")}`
          )
        )
        .join("")}
    </div>`;
}

function renderTracker(entries, config) {
  const entry = entries.find((e) => e.slug === config.primarySlug) || entries[0];
  if (!entry) return panel("Empty", "<p class=\"muted\">No tracker entry.</p>");

  const criteria = entry.tables.find((t) => t.name === "criteria");
  const shortlist = entry.tables.find((t) => t.name === "shortlist");

  return `
    <div class="panel-grid two">
      ${panel(
        entry.title,
        `
          ${entry.status ? `<p><strong>Status:</strong> ${escapeHtml(entry.status)}</p>` : ""}
          ${bodyPreview(entry.body, 6)}
        `
      )}
      ${criteria ? panel("Criteria", dataTable(criteria)) : ""}
    </div>
    ${shortlist ? panel("Shortlist", dataTable(shortlist)) : ""}`;
}

function renderResearch(entries, config) {
  const root = entries.find((e) => e.slug === config.primarySlug) || entries.find((e) => !e.parentId);
  const reports = entries.filter((e) => e.parentId === root?.id);

  return `
    <div class="panel-grid two">
      ${root ? panel("Watchlist", dataTable(root.tables.find((t) => t.name === "watchlist"))) : ""}
      ${root ? panel("Triggers", listItems(root.listItems.filter((i) => i.section === "triggers"))) : ""}
    </div>
    <div class="panel-grid">
      ${
        reports.length
          ? reports.map((r) => panel(r.title, bodyPreview(r.body, 4))).join("")
          : panel("Reports", "<p class=\"muted\">No dated reports yet.</p>")
      }
    </div>`;
}

function renderCards(entries, config) {
  const roots = entries.filter((e) => !e.parentId);
  return `
    <div class="panel-grid two">
      ${roots
        .map((entry) => {
          const approved = entry.props.approved;
          const statusChip =
            config.statusField && approved !== undefined
              ? chip(approved ? "approved" : "pending", approved ? "good" : "warn")
              : entry.status
                ? chip(entry.status)
                : "";
          const tables = (config.showTables || [])
            .map((name) => {
              const table = entry.tables.find((t) => t.name === name);
              return table ? `<h4>${escapeHtml(titleCase(name))}</h4>${dataTable(table)}` : "";
            })
            .join("");
          return panel(
            entry.title,
            `
              <div class="chip-row">
                ${entry.props.platform ? chip(entry.props.platform) : ""}
                ${statusChip}
              </div>
              ${entry.props.scheduled_at ? `<p><strong>Scheduled:</strong> ${escapeHtml(entry.props.scheduled_at)}</p>` : ""}
              ${bodyPreview(entry.body, 8)}
              ${checklist(entry.listItems.filter((i) => i.section === "checklist"))}
              ${tables}
            `
          );
        })
        .join("")}
    </div>`;
}

function renderNames(entries, config) {
  const entry = entries.find((e) => e.slug === config.primarySlug) || entries[0];
  if (!entry) return panel("Empty", "<p class=\"muted\">No naming data.</p>");

  const namesTable = entry.tables.find((t) => t.name === "names");
  const decision = entry.props.decision || {};

  return `
    ${panel("Decision", `<p><strong>Chosen:</strong> ${escapeHtml(decision.chosen || "Pending")}</p><p><strong>Rejected:</strong> ${escapeHtml(decision.rejected || "—")}</p>`)}
    ${namesTable ? panel("Options", dataTable(namesTable)) : ""}
    ${panel("Criteria", checklist(entry.listItems.filter((i) => i.section === "criteria")))}`;
}

function renderAutomations(entries, config) {
  const lines = config.showBodyPreviewLines || 12;
  return `
    <div class="panel-grid two">
      ${entries
        .map((entry) => {
          const settings = entry.props.settings || {};
          return panel(
            entry.title,
            `
              <div class="chip-row">
                ${settings.trigger ? chip(settings.trigger, "warn") : ""}
                ${settings.repo ? chip(settings.repo) : ""}
              </div>
              <p><strong>Tools:</strong> ${escapeHtml(settings.tools || "TBD")}</p>
              ${checklist(entry.listItems.filter((i) => i.section === "checklist"))}
              <pre class="code-preview">${escapeHtml((entry.body || "").split("\n").slice(0, lines).join("\n"))}</pre>
            `
          );
        })
        .join("")}
    </div>`;
}

function pageHeader(title, description) {
  return `
    <header class="page-header">
      <div>
        <p class="eyebrow">${escapeHtml(state.section)}</p>
        <h1>${escapeHtml(title)}</h1>
        <p class="lede">${escapeHtml(description)}</p>
      </div>
    </header>`;
}

function panel(title, body, options = {}) {
  const owner = options.owner ? `<span class="owner-tag">${escapeHtml(options.owner)}</span>` : "";
  return `
    <article class="panel" data-search-text="${searchText({ title, body, owner: options.owner })}">
      <header class="panel-head">
        <h3>${escapeHtml(title)}</h3>
        ${owner}
      </header>
      <div class="panel-body">${body}</div>
    </article>`;
}

function statCard(label, value, variant = "") {
  return `
    <div class="stat-card ${escapeAttr(variant)}" data-search-text="${searchText({ label, value })}">
      <strong>${escapeHtml(value)}</strong>
      <span>${escapeHtml(label)}</span>
    </div>`;
}

function checklist(items) {
  if (!items?.length) return "<p class=\"muted\">Nothing here.</p>";
  return items
    .map(
      (item) => `
        <div class="check-row">
          <span class="check-box ${item.done ? "is-done" : ""}" aria-hidden="true">${item.done ? "✓" : ""}</span>
          <span class="${item.done ? "done" : ""}">${escapeHtml(item.text)}</span>
        </div>`
    )
    .join("");
}

function listItems(items, options = {}) {
  if (!items?.length) return "<p class=\"muted\">Nothing recorded.</p>";
  return `<ul class="plain-list">${items
    .map((item) => {
      const owner = options.showOwner && item.meta?.owner ? ` <span class="muted">(${escapeHtml(item.meta.owner)})</span>` : "";
      return `<li>${escapeHtml(item.text)}${owner}</li>`;
    })
    .join("")}</ul>`;
}

function dataTable(table) {
  if (!table?.rows?.length) return "<p class=\"muted\">No rows yet.</p>";
  const columns = table.columns?.length ? table.columns : Object.keys(table.rows[0] || {});
  return `
    <div class="table-wrap">
      <table>
        <thead><tr>${columns.map((c) => `<th>${escapeHtml(titleCase(c))}</th>`).join("")}</tr></thead>
        <tbody>
          ${table.rows
            .map(
              (row) =>
                `<tr>${columns.map((c) => `<td>${escapeHtml(String(row[c] ?? ""))}</td>`).join("")}</tr>`
            )
            .join("")}
        </tbody>
      </table>
    </div>`;
}

function bodyPreview(body, maxLines = 10) {
  const text = (body || "").split("\n").filter((line) => line.trim() && !line.startsWith("#")).slice(0, maxLines).join("\n");
  if (!text) return "";
  return `<div class="body-preview">${escapeHtml(text).replace(/\n/g, "<br />")}</div>`;
}

function chip(label, variant = "") {
  return `<span class="chip ${escapeAttr(variant)}">${escapeHtml(label || "TBD")}</span>`;
}

function icon(name) {
  const icons = {
    home: "⌂",
    "check-square": "☑",
    map: "◎",
    calendar: "▦",
    briefcase: "◫",
    building: "▣",
    search: "⌕",
    users: "👥",
    tag: "🏷",
    zap: "⚡",
    share: "↗",
    folder: "▤",
  };
  return icons[name] || "•";
}

function applySearch() {
  const query = state.query;
  const nodes = app.querySelectorAll("[data-search-text]");
  let visible = 0;
  nodes.forEach((node) => {
    const matches = !query || node.dataset.searchText.toLowerCase().includes(query);
    node.classList.toggle("hidden-by-search", !matches);
    if (matches) visible += 1;
  });
  app.querySelector(".empty-state")?.remove();
  if (query && nodes.length && !visible) {
    app.appendChild(document.querySelector("#emptyStateTemplate").content.cloneNode(true));
  }
}

function searchText(value) {
  return escapeAttr(typeof value === "string" ? value : JSON.stringify(value));
}

function titleCase(value) {
  return String(value).replace(/_/g, " ").replace(/-/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function escapeAttr(value) {
  return escapeHtml(value).replace(/`/g, "&#096;");
}
