const DATA_URL = "data/site.json";

const state = { data: null, section: "overview", query: "", filterKind: "all", taskBoard: "all" };

const app = document.getElementById("app");
const sidebarNav = document.getElementById("sidebarNav");
const searchInput = document.getElementById("searchInput");

document.addEventListener("DOMContentLoaded", init);

async function init() {
  wireControls();
  try {
    const res = await fetch(DATA_URL, { cache: "no-store" });
    if (!res.ok) throw new Error(`Could not load ${DATA_URL}`);
    state.data = await res.json();
    renderChrome();
    navigate(getHash() || "overview");
  } catch (err) {
    app.innerHTML = `<section class="empty-state"><h2>Could not load HQ</h2><p>${escapeHtml(err.message)}</p></section>`;
  }
}

function wireControls() {
  sidebarNav.addEventListener("click", (e) => {
    const link = e.target.closest("[data-section]");
    if (!link) return;
    e.preventDefault();
    navigate(link.dataset.section);
  });

  searchInput.addEventListener("input", (e) => {
    state.query = e.target.value.trim().toLowerCase();
    renderSection();
  });

  window.addEventListener("hashchange", () => navigate(getHash() || "overview", { hash: false }));

  document.getElementById("sidebarToggle").addEventListener("click", () => {
    document.body.classList.toggle("sidebar-open");
  });

  app.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-copy]");
    if (!btn) return;
    copyText(btn.dataset.copy, btn);
  });

  app.addEventListener("click", (e) => {
    const tab = e.target.closest("[data-filter-kind]");
    if (tab) {
      state.filterKind = tab.dataset.filterKind;
      document.querySelectorAll("[data-filter-kind]").forEach((el) => {
        el.classList.toggle("is-active", el.dataset.filterKind === state.filterKind);
      });
      renderSection();
      return;
    }
    const boardTab = e.target.closest("[data-task-board]");
    if (boardTab) {
      state.taskBoard = boardTab.dataset.taskBoard;
      document.querySelectorAll("[data-task-board]").forEach((el) => {
        el.classList.toggle("is-active", el.dataset.taskBoard === state.taskBoard);
      });
      renderSection();
    }
  });
}

function getHash() {
  return window.location.hash.replace("#", "") || null;
}

function navigate(section, opts = {}) {
  state.section = section;
  state.filterKind = "all";
  if (opts.hash !== false) window.location.hash = section;
  document.querySelectorAll(".nav-link").forEach((l) => l.classList.toggle("is-active", l.dataset.section === section));
  renderSection();
  document.body.classList.remove("sidebar-open");
}

function renderChrome() {
  const { data } = state;
  document.getElementById("generatedAt").textContent = `Updated ${new Date(data.meta.generatedAt).toLocaleString([], { dateStyle: "medium", timeStyle: "short" })}`;

  const m = data.metrics;
  const tt = m.tasks || {};
  document.getElementById("topbarMetrics").innerHTML = [
    pill(`${m.needsInput} inputs`, "warn"),
    pill(`${tt.todo ?? 0} tasks`, "accent"),
  ].join("");

  let lastGroup = null;
  sidebarNav.innerHTML = data.ui.nav
    .map((item) => {
      const groupHdr =
        item.navGroup && item.navGroup !== lastGroup
          ? `<p class="nav-group-label">${escapeHtml(item.navGroup)}</p>`
          : "";
      if (item.navGroup) lastGroup = item.navGroup;
      const count = navCount(item, data);
      return `${groupHdr}
        <a class="nav-link" href="#${item.id}" data-section="${item.id}">
          <span class="nav-icon">${icon(item.icon)}</span>
          <span>${escapeHtml(item.label)}</span>
          ${count ? `<span class="nav-badge">${count}</span>` : ""}
        </a>`;
    })
    .join("");
}

function navCount(item, data) {
  if (item.id === "inbox") return data.inbox.length;
  if (item.id === "tasks") return (data.metrics.tasks?.todo ?? 0) + (data.metrics.tasks?.in_progress ?? 0);
  if (item.role) {
    return (data.roles[item.role]?.actions || []).filter((a) => a.status === "open").length;
  }
  return 0;
}

function renderSection() {
  const { data, section } = state;
  const navItem = data.ui.nav.find((n) => n.id === section) || data.ui.nav[0];

  let html = "";
  const view = navItem.view || navItem.filter || (navItem.role ? "role" : "inbox");
  if (view === "overview") html = renderOverview();
  else if (view === "tasks") html = renderTasks();
  else if (view === "planning") html = renderPlanning();
  else if (view === "research") html = renderResearch();
  else if (view === "reference") html = renderReference();
  else if (navItem.filter === "prompts") html = renderPrompts();
  else if (navItem.filter === "open" || section === "inbox") html = renderInbox();
  else if (navItem.role) html = renderRole(navItem.role);
  else html = renderOverview();

  app.innerHTML = html;
  applySearch();
}

function renderOverview() {
  const { data } = state;
  const m = data.metrics;
  const tt = m.tasks || {};
  const standup = data.planning?.standups?.[0];
  const blockers = (data.tasks?.boards || []).find((b) => b.slug === "blockers");

  return `
    ${pageHeader("Overview", data.project.description || "Course business HQ — tasks, planning, research, and agent inbox.")}
    <div class="stat-grid">
      ${statCard("Inbox", m.needsInput, "inputs waiting", "#inbox")}
      ${statCard("Approvals", m.needsApproval, "green-lights", "#inbox")}
      ${statCard("Tasks", (tt.todo ?? 0) + (tt.in_progress ?? 0), "active items", "#tasks")}
      ${statCard("Listings", data.planning?.officeListings?.count ?? 0, "office under €800", "#planning")}
    </div>
    ${standup ? standupPanel(standup) : ""}
    ${blockers ? blockersPanel(blockers) : ""}
    <section class="section-block">
      <h2 class="section-title">Quick links</h2>
      <div class="quick-links">
        <a class="quick-link" href="#tasks">Task boards</a>
        <a class="quick-link" href="#planning">Planning & office</a>
        <a class="quick-link" href="#research">Research hub</a>
        <a class="quick-link" href="#inbox">Action inbox</a>
      </div>
    </section>`;
}

function statCard(label, value, sub, hash) {
  return `
    <a class="stat-card" href="${hash}">
      <span class="stat-value">${value}</span>
      <span class="stat-label">${escapeHtml(label)}</span>
      <span class="stat-sub">${escapeHtml(sub)}</span>
    </a>`;
}

function standupPanel(standup) {
  const today = (standup.sections.today || []).slice(0, 3);
  const blockers = (standup.sections.blockers || []).slice(0, 4);
  return `
    <section class="panel-card">
      <div class="panel-head">
        <h2>Latest standup · ${escapeHtml(standup.slug)}</h2>
        <a class="text-link" href="#planning">All standups</a>
      </div>
      <div class="standup-cols">
        <div>
          <h3>Today</h3>
          <ul>${today.map((t) => `<li>${escapeHtml(t)}</li>`).join("") || "<li class='muted'>—</li>"}</ul>
        </div>
        <div>
          <h3>Blockers</h3>
          <ul>${blockers.map((t) => `<li>${escapeHtml(t)}</li>`).join("") || "<li class='muted'>—</li>"}</ul>
        </div>
      </div>
    </section>`;
}

function blockersPanel(board) {
  const open = [...(board.columns.todo || []), ...(board.columns.in_progress || [])];
  return `
    <section class="panel-card panel-warn">
      <div class="panel-head"><h2>Blockers (${open.length} open)</h2><a class="text-link" href="#tasks">Task board</a></div>
      <ul class="compact-list">${open.map((i) => `<li>${escapeHtml(i.text)}</li>`).join("")}</ul>
    </section>`;
}

function renderTasks() {
  const boards = state.data.tasks?.boards || [];
  const cols = state.data.ui.taskColumns || [];
  const activeBoards =
    state.taskBoard === "all" ? boards : boards.filter((b) => b.slug === state.taskBoard);

  const boardTabs = `
    <div class="filter-tabs" role="tablist">
      <button type="button" class="filter-tab ${state.taskBoard === "all" ? "is-active" : ""}" data-task-board="all">All boards</button>
      ${boards.map((b) => `<button type="button" class="filter-tab ${state.taskBoard === b.slug ? "is-active" : ""}" data-task-board="${escapeAttr(b.slug)}">${escapeHtml(b.title)}</button>`).join("")}
    </div>`;

  return `
    ${pageHeader("Tasks", "Jira-style boards — status from checklist state and inbox metadata.")}
    ${boardTabs}
    ${activeBoards.map((b) => taskBoardHtml(b, cols)).join("")}`;
}

function taskBoardHtml(board, cols) {
  const ownerLabel = board.owner ? ` · ${board.owner}` : "";
  return `
    <section class="board-section" data-search-text="${escapeAttr(board.title)}">
      <header class="board-header">
        <h2>${escapeHtml(board.title)}${ownerLabel ? `<span class="board-meta">${escapeHtml(ownerLabel)}</span>` : ""}</h2>
        <span class="board-totals">${cols.map((c) => `${board.counts[c.id] || 0} ${c.label}`).join(" · ")}</span>
      </header>
      <div class="kanban">
        ${cols.map((col) => kanbanColumn(col, board.columns[col.id] || [])).join("")}
      </div>
    </section>`;
}

function kanbanColumn(col, items) {
  return `
    <div class="kanban-col" data-column="${escapeAttr(col.id)}">
      <header class="kanban-col-head">
        <span>${escapeHtml(col.label)}</span>
        <span class="kanban-count">${items.length}</span>
      </header>
      <div class="kanban-cards">
        ${items.length ? items.map(kanbanCard).join("") : `<p class="kanban-empty">—</p>`}
      </div>
    </div>`;
}

function kanbanCard(item) {
  const owner = item.owner ? `<span class="kanban-owner">${escapeHtml(item.owner)}</span>` : "";
  return `
    <article class="kanban-card" data-search-text="${searchAttr({ title: item.text, hint: item.owner })}">
      <p>${escapeHtml(item.text)}</p>
      ${owner}
    </article>`;
}

function renderPlanning() {
  const p = state.data.planning || {};
  const listings = p.officeListings || {};
  const maxBudget = listings.maxBudgetEur ?? 800;

  return `
    ${pageHeader("Planning", "Roadmap, near-term queue, standups, and Plovdiv office search.")}
    ${p.nearTerm ? nearTermSection(p.nearTerm) : ""}
    ${p.tracks?.tables?.length ? roadmapTable("Launch tracks", p.tracks.tables[0]) : ""}
    ${p.phases?.tables?.length ? roadmapTable("Phases", p.phases.tables[0]) : ""}
    ${officeSection(p, listings, maxBudget)}
    ${standupsSection(p.standups || [])}`;
}

function nearTermSection(entry) {
  const items = (entry.listItems || []).filter((i) => !i.done);
  return `
    <section class="section-block">
      <h2 class="section-title">Near-term queue</h2>
      <ul class="numbered-list">${items.map((i, n) => `<li data-search-text="${escapeAttr(i.text)}">${escapeHtml(i.text)}</li>`).join("")}</ul>
    </section>`;
}

function roadmapTable(title, table) {
  return `
    <section class="section-block">
      <h2 class="section-title">${escapeHtml(title)}</h2>
      <div class="data-table-wrap">${renderTableHtml(table)}</div>
    </section>`;
}

function officeSection(planning, listings, maxBudget) {
  const brief = planning.officeBrief || planning.office?.body || "";
  const rows = (listings.listings || []).filter((l) => (l.priceEur || 0) <= maxBudget || l.priceEur === 0);
  const errors = listings.scrapeErrors || [];

  return `
    <section class="section-block office-section">
      <h2 class="section-title">Office · Plovdiv (under €${maxBudget}/mo)</h2>
      ${brief ? `<div class="brief-block"><pre class="brief-text">${escapeHtml(brief.slice(0, 800))}</pre></div>` : ""}
      ${errors.length ? `<p class="hint warn-hint">Scrape notes: ${escapeHtml(errors.join("; "))}</p>` : ""}
      <p class="hint">${rows.length} listings · updated ${listings.generatedAt ? new Date(listings.generatedAt).toLocaleDateString() : "—"}</p>
      <div class="data-table-wrap">
        <table class="data-table office-table">
          <thead><tr><th>Title</th><th>€/mo</th><th>m²</th><th>Source</th></tr></thead>
          <tbody>
            ${rows.map((l) => `
              <tr data-search-text="${escapeAttr([l.title, l.snippet].join(" "))}">
                <td><strong>${escapeHtml((l.title || "").slice(0, 72))}</strong>${l.snippet ? `<div class="cell-sub">${escapeHtml((l.snippet || "").slice(0, 120))}…</div>` : ""}</td>
                <td>${l.priceEur ? l.priceEur : "—"}</td>
                <td>${l.sqm || "—"}</td>
                <td>${escapeHtml(l.source || "")}</td>
              </tr>`).join("")}
          </tbody>
        </table>
      </div>
    </section>`;
}

function standupsSection(standups) {
  return `
    <section class="section-block">
      <h2 class="section-title">Standups</h2>
      <div class="standup-stack">
        ${standups.map(standupExpand).join("")}
      </div>
    </section>`;
}

function standupExpand(standup) {
  const order = ["done", "today", "blockers", "agent_next"];
  return `
    <details class="standup-details" data-search-text="${escapeAttr(standup.slug)}">
      <summary>${escapeHtml(standup.slug)}</summary>
      <div class="standup-sections">
        ${order.filter((s) => standup.sections[s]?.length).map((s) => `
          <div class="standup-block">
            <h4>${escapeHtml(s.replace("_", " "))}</h4>
            <ul>${standup.sections[s].map((t) => `<li>${escapeHtml(t)}</li>`).join("")}</ul>
          </div>`).join("")}
      </div>
    </details>`;
}

function renderResearch() {
  const hub = state.data.researchHub || {};
  const entries = hub.entries || [];
  const competitors = entries.find((e) => e.slug === "competitors");
  const reports = entries.filter((e) => e.slug !== "competitors");

  return `
    ${pageHeader("Research", "Market scans, competitor watchlist, and landscape reports.")}
    ${competitors ? researchCompetitors(competitors) : ""}
    <section class="section-block">
      <h2 class="section-title">Reports</h2>
      <div class="research-grid">
        ${reports.map(researchReportCard).join("") || "<p class='empty-inline'>No reports yet.</p>"}
      </div>
    </section>`;
}

function researchCompetitors(entry) {
  const table = entry.tables?.find((t) => t.name === "watchlist");
  if (!table) return "";
  return `
    <section class="section-block">
      <h2 class="section-title">Competitor watchlist</h2>
      <div class="data-table-wrap">${renderTableHtml(table)}</div>
    </section>`;
}

function renderTableHtml(table) {
  const cols = table.columns || [];
  const rows = table.rows || [];
  return `
    <table class="data-table">
      <thead><tr>${cols.map((c) => `<th>${escapeHtml(c)}</th>`).join("")}</tr></thead>
      <tbody>
        ${rows.map((r) => `<tr data-search-text="${escapeAttr(cols.map((c) => r[c]).join(" "))}">${cols.map((c) => `<td>${escapeHtml(r[c] || "")}</td>`).join("")}</tr>`).join("")}
      </tbody>
    </table>`;
}

function researchReportCard(entry) {
  const date = entry.props?.report_date || "";
  return `
    <article class="research-card" data-search-text="${searchAttr({ title: entry.title, hint: entry.excerpt })}">
      <header>
        <h3>${escapeHtml(entry.title)}</h3>
        ${date ? `<span class="research-date">${escapeHtml(date)}</span>` : ""}
      </header>
      <pre class="research-excerpt">${escapeHtml(entry.excerpt)}</pre>
      <footer class="research-meta">${entry.bodyLength} chars in hq.db · slug <code>${escapeHtml(entry.slug)}</code></footer>
    </article>`;
}

function renderInbox() {
  const actions = filterActions(state.data.inbox);
  return `
    ${pageHeader("Inbox", "Everything waiting on you — copy the batch reply once, or use per-card templates.")}
    ${inboxBatchBlock()}
    ${filterTabs()}
    ${actionList(actions, "No open actions. Check Prompts for role kits.")}`;
}

function inboxBatchBlock() {
  const batch = state.data.inboxBatch;
  if (!batch?.slackReply || !batch.count) return "";
  const channel = batch.channel || "#vibe-standup";
  return `
    <section class="batch-block copy-block">
      <div class="copy-head">
        <span class="copy-label">Batched standup (${batch.count} items) → ${escapeHtml(channel)}</span>
      </div>
      <p class="hint">Paste one numbered reply in Slack; agents map answers to inbox cards.</p>
      <div class="copy-row">
        <pre class="copy-text batch-text">${escapeHtml(batch.slackReply)}</pre>
        <button type="button" class="copy-btn copy-btn-primary" data-copy="${escapeAttr(batch.slackReply)}">Copy batch</button>
      </div>
    </section>`;
}

function renderRole(role) {
  const roleData = state.data.roles[role] || { meta: {}, actions: [], prompts: [] };
  const meta = roleData.meta || {};
  const open = filterActions((roleData.actions || []).filter((a) => a.status === "open"));
  const prompts = roleData.prompts || [];

  return `
    ${pageHeader(meta.label || role, `Post in ${meta.channel || "Slack"} — copy a reply or prompt below.`)}
    ${prompts.length ? `<section class="section-block"><h2 class="section-title">Role prompt kit</h2>${actionList(prompts)}</section>` : ""}
    <section class="section-block">
      <h2 class="section-title">Your inputs & approvals</h2>
      ${filterTabs()}
      ${actionList(open, `Nothing open for ${meta.label}.`)}
    </section>`;
}

function renderPrompts() {
  const prompts = filterActions(state.data.actions.filter((a) => a.kind === "prompt"));
  return `
    ${pageHeader("Prompts", "Copy-paste agent instructions by role.")}
    ${actionList(prompts, "No prompts found.")}`;
}

function renderReference() {
  const ref = state.data.reference || {};
  const watchlist = ref.competitors?.tables?.find((t) => t.name === "watchlist");
  const tracks = ref.roadmapTracks?.tables?.find((t) => t.name === "tracks");
  const course = ref.messaging?.props?.course || {};

  return `
    ${pageHeader("Reference", "Background context — use Research and Planning for live data.")}
    <div class="action-grid">
      ${actionCard({
        slug: "ref-messaging",
        title: "Approved messaging",
        kind: "reference",
        role: "business",
        hint: "Source of truth for copy",
        slackReply: "",
        prompt: `Working title: ${course["working-title"] || "TBD"}\nOne-liner: ${course["one-liner"] || "TBD"}\nWho it's for: ${course["who-it-s-for"] || course["who-its-for"] || "TBD"}`,
      })}
      ${watchlist ? referenceTableCard("Competitor watchlist", watchlist) : ""}
      ${tracks ? referenceTableCard("Roadmap tracks", tracks) : ""}
    </div>`;
}

function referenceTableCard(title, table) {
  const cols = table.columns || [];
  const preview = (table.rows || [])
    .slice(0, 5)
    .map((r) => cols.map((c) => `${c}: ${r[c] || ""}`).join(" | "))
    .join("\n");
  return actionCard({
    slug: `ref-${title}`,
    title,
    kind: "reference",
    role: "research",
    hint: `${(table.rows || []).length} rows`,
    prompt: preview,
  });
}

function filterTabs() {
  return `
    <div class="filter-tabs" role="tablist">
      <button type="button" class="filter-tab ${state.filterKind === "all" ? "is-active" : ""}" data-filter-kind="all">All</button>
      <button type="button" class="filter-tab ${state.filterKind === "input" ? "is-active" : ""}" data-filter-kind="input">Needs input</button>
      <button type="button" class="filter-tab ${state.filterKind === "approve" ? "is-active" : ""}" data-filter-kind="approve">Green-light</button>
    </div>`;
}

function filterActions(actions) {
  let list = actions;
  if (state.filterKind !== "all") list = list.filter((a) => a.kind === state.filterKind);
  if (state.query) list = list.filter((a) => searchBlob(a).includes(state.query));
  return list;
}

function actionList(actions, emptyMsg = "Nothing here.") {
  if (!actions.length) return `<p class="empty-inline">${escapeHtml(emptyMsg)}</p>`;
  return `<div class="action-grid">${actions.map(actionCard).join("")}</div>`;
}

function actionCard(a) {
  const kinds = state.data.ui.actionKinds || {};
  const kindMeta = kinds[a.kind] || { label: a.kind, badge: a.kind };
  const roles = state.data.ui.roles || {};
  const roleMeta = roles[a.role] || { label: a.role, channel: a.slackChannel };

  const showSlack = a.kind !== "prompt" && a.slackReply;
  const showPrompt = a.prompt && a.kind !== "reference";
  const priority = a.priority === 1 ? `<span class="priority">P1</span>` : "";

  return `
    <article class="action-card kind-${escapeAttr(a.kind)}" data-search-text="${searchAttr(a)}">
      <header class="action-head">
        <div class="badges">
          <span class="badge role">${escapeHtml(roleMeta.label || a.role)}</span>
          <span class="badge kind">${escapeHtml(kindMeta.label)}</span>
          ${priority}
        </div>
        <h3>${escapeHtml(a.title)}</h3>
        ${a.hint ? `<p class="hint">${escapeHtml(a.hint)}</p>` : ""}
      </header>
      ${a.inputLabel ? `<p class="input-label"><strong>${escapeHtml(a.inputLabel)}</strong>${a.inputExample ? ` — e.g. ${escapeHtml(a.inputExample)}` : ""}</p>` : ""}
      ${showSlack ? slackBlock(a, roleMeta) : ""}
      ${showPrompt ? promptBlock(a, a.kind === "prompt") : ""}
      ${a.kind === "reference" && a.prompt ? promptBlock(a, false) : ""}
    </article>`;
}

function slackBlock(a, roleMeta) {
  const channel = a.slackChannel || roleMeta.channel || "#vibe-code";
  const trigger = a.slackTrigger ? `<span class="trigger">Trigger: <code>${escapeHtml(a.slackTrigger)}</code></span>` : "";
  return `
    <section class="copy-block">
      <div class="copy-head">
        <span class="copy-label">Slack → ${escapeHtml(channel)}</span>
        ${trigger}
      </div>
      <div class="copy-row">
        <pre class="copy-text">${escapeHtml(a.slackReply)}</pre>
        <button type="button" class="copy-btn" data-copy="${escapeAttr(a.slackReply)}">Copy reply</button>
      </div>
    </section>`;
}

function promptBlock(a, expanded) {
  return `
    <section class="copy-block ${expanded ? "is-expanded" : ""}">
      <div class="copy-head"><span class="copy-label">${expanded ? "Agent prompt" : "Agent prompt (optional)"}</span></div>
      <div class="copy-row">
        <pre class="copy-text prompt-text">${escapeHtml(a.prompt)}</pre>
        <button type="button" class="copy-btn" data-copy="${escapeAttr(a.prompt)}">Copy prompt</button>
      </div>
    </section>`;
}

function pageHeader(title, desc) {
  return `
    <header class="page-header">
      <p class="eyebrow">${escapeHtml(state.section)}</p>
      <h1>${escapeHtml(title)}</h1>
      <p class="lede">${escapeHtml(desc)}</p>
    </header>`;
}

function applySearch() {
  const q = state.query;
  document.querySelectorAll("[data-search-text], .action-card, .kanban-card, .research-card, .data-table tbody tr, .numbered-list li, .standup-details").forEach((el) => {
    const text = (el.dataset.searchText || el.textContent || "").toLowerCase();
    const match = !q || text.includes(q);
    el.classList.toggle("hidden", !match);
  });
}

function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const orig = btn.textContent;
    btn.textContent = "Copied!";
    setTimeout(() => { btn.textContent = orig; }, 1200);
  });
}

function searchBlob(a) {
  return [a.title, a.hint, a.slackReply, a.prompt, a.role, a.kind, a.inputLabel].filter(Boolean).join(" ").toLowerCase();
}

function searchAttr(a) {
  return escapeAttr(typeof a === "string" ? a : searchBlob(a));
}

function pill(text, variant = "") {
  return `<span class="metric-pill ${variant}">${escapeHtml(text)}</span>`;
}

function icon(name) {
  return {
    home: "◆",
    board: "▦",
    calendar: "📅",
    search: "🔍",
    inbox: "📥",
    target: "🎯",
    microscope: "🔬",
    briefcase: "💼",
    share: "📣",
    code: "🛠",
    copy: "📋",
    book: "📚",
  }[name] || "•";
}

function escapeHtml(v) {
  return String(v ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function escapeAttr(v) {
  return escapeHtml(v).replace(/`/g, "&#096;");
}
