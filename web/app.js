const DATA_URL = "data/site.json";

const state = { data: null, section: "inbox", query: "", filterKind: "all" };

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
    navigate(getHash() || "inbox");
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

  window.addEventListener("hashchange", () => navigate(getHash() || "inbox", { hash: false }));

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
    if (!tab) return;
    state.filterKind = tab.dataset.filterKind;
    document.querySelectorAll("[data-filter-kind]").forEach((el) => {
      el.classList.toggle("is-active", el.dataset.filterKind === state.filterKind);
    });
    renderSection();
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
  document.getElementById("topbarMetrics").innerHTML = [
    pill(`${m.needsInput} inputs`, "warn"),
    pill(`${m.needsApproval} approvals`, "accent"),
  ].join("");

  sidebarNav.innerHTML = data.ui.nav
    .map((item) => {
      const count = navCount(item, data);
      return `
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
  if (item.role) {
    return (data.roles[item.role]?.actions || []).filter((a) => a.status === "open").length;
  }
  return 0;
}

function renderSection() {
  const { data, section } = state;
  const navItem = data.ui.nav.find((n) => n.id === section) || data.ui.nav[0];

  let html = "";
  if (navItem.view === "reference") html = renderReference();
  else if (navItem.filter === "prompts") html = renderPrompts();
  else if (navItem.filter === "open" || section === "inbox") html = renderInbox();
  else if (navItem.role) html = renderRole(navItem.role);
  else html = renderInbox();

  app.innerHTML = html;
  applySearch();
}

function renderInbox() {
  const actions = filterActions(state.data.inbox);
  return `
    ${pageHeader("Inbox", "Everything waiting on you — copy the batch reply once, or use per-card templates.")}
    ${inboxBatchBlock()}
    ${filterTabs()}
    ${actionList(actions, "No open actions. Check All prompts for role kits.")}`;
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
    ${pageHeader("All prompts", "Copy-paste agent instructions by role.")}
    ${actionList(prompts, "No prompts found.")}`;
}

function renderReference() {
  const ref = state.data.reference || {};
  const watchlist = ref.competitors?.tables?.find((t) => t.name === "watchlist");
  const tracks = ref.roadmapTracks?.tables?.find((t) => t.name === "tracks");
  const course = ref.messaging?.props?.course || {};

  return `
    ${pageHeader("Reference", "Background context — actions live in Inbox and role tabs.")}
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
  if (state.query) {
    list = list.filter((a) => searchBlob(a).includes(state.query));
  }
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
        <pre class="copy-text" id="slack-${escapeAttr(a.slug)}">${escapeHtml(a.slackReply)}</pre>
        <button type="button" class="copy-btn" data-copy="${escapeAttr(a.slackReply)}">Copy reply</button>
      </div>
    </section>`;
}

function promptBlock(a, expanded) {
  return `
    <section class="copy-block ${expanded ? "is-expanded" : ""}">
      <div class="copy-head">
        <span class="copy-label">${expanded ? "Agent prompt" : "Agent prompt (optional)"}</span>
      </div>
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
  document.querySelectorAll(".action-card").forEach((el) => {
    const match = !q || (el.dataset.searchText || "").includes(q);
    el.classList.toggle("hidden", !match);
  });
}

function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    btn.textContent = "Copied!";
    setTimeout(() => { btn.textContent = btn.classList.contains("copy-btn") ? (btn.closest(".copy-block")?.querySelector(".prompt-text") ? "Copy prompt" : "Copy reply") : "Copy"; }, 1200);
  });
}

function searchBlob(a) {
  return [a.title, a.hint, a.slackReply, a.prompt, a.role, a.kind, a.inputLabel].filter(Boolean).join(" ").toLowerCase();
}

function searchAttr(a) {
  return escapeAttr(searchBlob(a));
}

function pill(text, variant = "") {
  return `<span class="metric-pill ${variant}">${escapeHtml(text)}</span>`;
}

function icon(name) {
  return { inbox: "📥", calendar: "📅", search: "🔍", briefcase: "💼", share: "📣", code: "🛠", copy: "📋", book: "📚" }[name] || "•";
}

function escapeHtml(v) {
  return String(v ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function escapeAttr(v) {
  return escapeHtml(v).replace(/`/g, "&#096;");
}
