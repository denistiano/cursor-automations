const DATA_URL = "data/site.json";

const state = {
  data: null,
  section: "home",
  query: "",
  filterKind: "all",
  filterRole: "all",
  taskBoard: "all",
  officeSort: "overall",
  officeMaxPrice: null,
  officeMinSqm: 40,
  officeLocalQuery: "",
  officeView: "rankings",
  officeRankTab: "overall",
};

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
    const officeCfg = state.data.ui?.officeListings || {};
    state.officeMaxPrice = officeCfg.maxBudgetEur ?? 800;
    state.officeMinSqm = officeCfg.minSqmDefault ?? 40;
    state.officeSort = officeCfg.defaultSort ?? "overall";
    state.officeView = officeCfg.defaultView ?? "rankings";
    state.officeRankTab = officeCfg.rankTabs?.[0]?.id ?? "overall";
    renderChrome();
    navigate(getHash() || "home");
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

  window.addEventListener("hashchange", () => navigate(getHash() || "home", { hash: false }));

  document.getElementById("sidebarToggle").addEventListener("click", () => {
    document.body.classList.toggle("sidebar-open");
  });

  app.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-copy]");
    if (btn) copyText(btn.dataset.copy, btn);
  });

  app.addEventListener("click", (e) => {
    const tab = e.target.closest("[data-filter-kind]");
    if (tab) {
      state.filterKind = tab.dataset.filterKind;
      syncTabState("[data-filter-kind]", "filterKind");
      renderSection();
      return;
    }
    const roleTab = e.target.closest("[data-filter-role]");
    if (roleTab) {
      state.filterRole = roleTab.dataset.filterRole;
      syncTabState("[data-filter-role]", "filterRole");
      renderSection();
      return;
    }
    const boardTab = e.target.closest("[data-task-board]");
    if (boardTab) {
      state.taskBoard = boardTab.dataset.taskBoard;
      syncTabState("[data-task-board]", "taskBoard");
      renderSection();
      return;
    }
    const sortBtn = e.target.closest("[data-office-sort]");
    if (sortBtn) {
      state.officeSort = sortBtn.dataset.officeSort;
      syncTabState("[data-office-sort]", "officeSort", "officeSort");
      renderSection();
      return;
    }
    const viewBtn = e.target.closest("[data-office-view]");
    if (viewBtn) {
      state.officeView = viewBtn.dataset.officeView;
      syncTabState("[data-office-view]", "officeView", "officeView");
      renderSection();
      return;
    }
    const rankTab = e.target.closest("[data-office-rank-tab]");
    if (rankTab) {
      state.officeRankTab = rankTab.dataset.officeRankTab;
      syncTabState("[data-office-rank-tab]", "officeRankTab", "officeRankTab");
      renderSection();
    }
  });

  app.addEventListener("input", (e) => {
    if (e.target.matches("[data-office-max-price]")) {
      state.officeMaxPrice = Number(e.target.value) || 800;
      renderSection();
    }
    if (e.target.matches("[data-office-min-sqm]")) {
      state.officeMinSqm = Number(e.target.value) || 0;
      renderSection();
    }
    if (e.target.matches("[data-office-local-query]")) {
      state.officeLocalQuery = e.target.value.trim().toLowerCase();
      renderSection();
    }
  });
}

function syncTabState(selector, key, datasetKey = key) {
  document.querySelectorAll(selector).forEach((el) => {
    el.classList.toggle("is-active", el.dataset[datasetKey] === state[key]);
  });
}

function getHash() {
  return window.location.hash.replace("#", "") || null;
}

function navigate(section, opts = {}) {
  state.section = section;
  if (section !== "inbox") {
    state.filterKind = "all";
    state.filterRole = "all";
  }
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
    pill(`${m.needsInput} waiting on you`, "warn"),
    pill(`${m.needsApproval} to approve`, "accent"),
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
  if (item.id === "brand") {
    const sprint = data.planning?.brandSprint;
    if (!sprint?.props?.current_day) return 0;
    const day = sprint.props.current_day;
    const sections = sprint.sections || {};
    const key = `day${day}`;
    const tasks = sections[key] || [];
    return tasks.length;
  }
  if (item.id === "office") return data.planning?.officeListings?.countWithinBudget ?? data.planning?.officeListings?.count ?? 0;
  if (item.id === "work") return (data.metrics.tasks?.todo ?? 0) + (data.metrics.tasks?.in_progress ?? 0);
  return 0;
}

function renderSection() {
  const { data, section } = state;
  const navItem = data.ui.nav.find((n) => n.id === section) || data.ui.nav[0];
  const view = navItem.view || "home";

  const renderers = {
    home: renderHome,
    inbox: renderInbox,
    office: renderOffice,
    brand: renderBrand,
    work: renderWork,
    research: renderResearch,
  };

  app.innerHTML = (renderers[view] || renderHome)();
  applySearch();
}

/* ── Home ── */

function renderHome() {
  const { data } = state;
  const m = data.metrics;
  const open = data.inbox.filter((a) => a.status === "open" || a.status === "in_progress");
  const standup = data.planning?.standups?.[0];
  const blockers = (data.tasks?.boards || []).find((b) => b.slug === "blockers");
  const openBlockers = blockers
    ? [...(blockers.columns.todo || []), ...(blockers.columns.in_progress || [])]
    : [];

  return `
    ${pageHeader("Home", "What needs your attention today.")}
    <div class="stat-grid">
      ${statCard("Waiting on you", m.needsInput, "replies needed", "#inbox")}
      ${statCard("To approve", m.needsApproval, "agent runs", "#inbox")}
      ${statCard("Office listings", data.planning?.officeListings?.countWithinBudget ?? 0, "under budget", "#office")}
      ${statCard("Active tasks", (m.tasks?.todo ?? 0) + (m.tasks?.in_progress ?? 0), "in progress", "#work")}
    </div>
    ${open.length ? priorityActionsPanel(open.slice(0, 4)) : ""}
    ${data.planning?.brandSprint ? brandSprintHomePanel(data.planning.brandSprint) : ""}
    ${standup ? standupPanel(standup) : ""}
    ${openBlockers.length ? blockersPanel(openBlockers) : ""}`;
}

function priorityActionsPanel(actions) {
  return `
    <section class="panel-card">
      <div class="panel-head">
        <h2>Needs you now</h2>
        <a class="text-link" href="#inbox">Open inbox →</a>
      </div>
      <div class="priority-list">
        ${actions.map((a) => `
          <a class="priority-row" href="#inbox" data-search-text="${searchAttr(a)}">
            <span class="badge kind">${escapeHtml((state.data.ui.actionKinds[a.kind] || {}).label || a.kind)}</span>
            <span>${escapeHtml(a.title)}</span>
          </a>`).join("")}
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
  const ongoing = (standup.sections.ongoing || []).slice(0, 4);
  const today = (standup.sections.today || []).slice(0, 3);
  const blockers = (standup.sections.blockers || []).slice(0, 3);
  return `
    <section class="panel-card">
      <div class="panel-head">
        <h2>Latest standup · ${escapeHtml(standup.slug)}</h2>
        <a class="text-link" href="#work">All standups</a>
      </div>
      <div class="standup-cols">
        <div>
          <h3>Ongoing</h3>
          <ul>${ongoing.map((t) => `<li>${escapeHtml(t)}</li>`).join("") || "<li class='muted'>—</li>"}</ul>
        </div>
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

function blockersPanel(items) {
  return `
    <section class="panel-card panel-warn">
      <div class="panel-head"><h2>Blockers (${items.length})</h2><a class="text-link" href="#work">Task boards</a></div>
      <ul class="compact-list">${items.map((i) => `<li>${escapeHtml(i.text)}</li>`).join("")}</ul>
    </section>`;
}

/* ── Inbox (unified: all roles + prompts) ── */

function renderInbox() {
  const allOpen = filterInboxActions(state.data.inbox);
  const prompts = filterInboxActions(state.data.actions.filter((a) => a.kind === "prompt"));
  const showingPrompts = state.filterKind === "prompt";

  return `
    ${pageHeader("Inbox", "Everything waiting on you — copy a Slack reply or agent prompt.")}
    ${inboxBatchBlock()}
    ${inboxFilterTabs()}
    ${roleFilterTabs()}
    ${showingPrompts
      ? actionList(prompts, "No prompts found.")
      : actionList(allOpen, "Nothing waiting on you right now.")}`;
}

function inboxFilterTabs() {
  return `
    <div class="filter-tabs" role="tablist">
      <button type="button" class="filter-tab ${state.filterKind === "all" ? "is-active" : ""}" data-filter-kind="all">All</button>
      <button type="button" class="filter-tab ${state.filterKind === "input" ? "is-active" : ""}" data-filter-kind="input">Needs reply</button>
      <button type="button" class="filter-tab ${state.filterKind === "approve" ? "is-active" : ""}" data-filter-kind="approve">Approve</button>
      <button type="button" class="filter-tab ${state.filterKind === "prompt" ? "is-active" : ""}" data-filter-kind="prompt">Prompts</button>
    </div>`;
}

function roleFilterTabs() {
  if (state.filterKind === "prompt") return "";
  const roles = state.data.ui.roles || {};
  const tabs = [
    `<button type="button" class="filter-tab filter-tab-sm ${state.filterRole === "all" ? "is-active" : ""}" data-filter-role="all">All roles</button>`,
    ...Object.entries(roles).map(
      ([id, meta]) =>
        `<button type="button" class="filter-tab filter-tab-sm ${state.filterRole === id ? "is-active" : ""}" data-filter-role="${escapeAttr(id)}">${escapeHtml(meta.label)}</button>`
    ),
  ];
  return `<div class="filter-tabs filter-tabs-secondary" role="tablist">${tabs.join("")}</div>`;
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

function filterInboxActions(actions) {
  let list = actions;
  if (state.filterKind === "prompt") {
    list = list.filter((a) => a.kind === "prompt");
  } else if (state.filterKind !== "all") {
    list = list.filter((a) => a.kind === state.filterKind);
  } else {
    list = list.filter((a) => a.kind !== "prompt");
  }
  if (state.filterRole !== "all") list = list.filter((a) => a.role === state.filterRole);
  if (state.query) list = list.filter((a) => searchBlob(a).includes(state.query));
  return list;
}

/* ── Office search ── */

function renderOffice() {
  const p = state.data.planning || {};
  const listings = p.officeListings || {};
  const cfg = state.data.ui.officeListings || {};
  const maxBudget = cfg.maxBudgetEur ?? 800;
  const rankings = listings.rankings || {};
  const rankTabs = cfg.rankTabs || [
    { id: "overall", label: "Overall" },
    { id: "location", label: "Best location" },
    { id: "luxury", label: "Most luxurious" },
    { id: "price", label: "Best price" },
  ];
  const filtered = filterOfficeListings(listings.listings || [], maxBudget);
  const sorted = sortOfficeListings(filtered);
  const alsoCheck = listings.alsoCheck || [];
  const criteria = parseOfficeBrief(p.officeBrief || "");
  const rankCriteria = rankings.criteria || {};
  const top10 = rankings.top10 || {};
  const activeRankList = top10[state.officeRankTab] || top10.overall || [];

  return `
    ${pageHeader(
      "Office search — Plovdiv",
      `Training space for ~20 students. Soft budget ~€${maxBudget}/mo — rankings include premium options.`
    )}
    ${criteriaPanel(criteria, maxBudget, rankCriteria)}
    ${alsoCheck.length ? externalLinksBar(alsoCheck) : ""}
    ${officeViewTabs(cfg)}
    ${state.officeView === "rankings"
      ? officeAllRankingsSections(rankTabs, top10)
      : ""}
    ${state.officeView === "all"
      ? `${officeControls(cfg, maxBudget, sorted.length, listings)}
    <div class="office-grid">
      ${sorted.length
        ? sorted.map((l) => officeCard(l)).join("")
        : `<p class="empty-inline">No listings match your filters. Try raising the budget or clearing filters.</p>`}
    </div>`
      : ""}
    ${p.officeShortlist?.rows?.length ? shortlistSection(p.officeShortlist) : ""}`;
}

function parseOfficeBrief(brief) {
  const lines = brief.split("\n").filter(Boolean);
  const criteria = [];
  for (const line of lines) {
    const m = line.match(/^\*\*(.+?):\*\*\s*(.+)/);
    if (m) criteria.push({ label: m[1], value: m[2].replace(/\*\*/g, "") });
  }
  return criteria;
}

function officeViewTabs(cfg) {
  const views = [
    { id: "rankings", label: "Top 10 rankings" },
    { id: "all", label: "All listings" },
  ];
  return `
    <div class="filter-tabs filter-tabs-secondary" role="tablist">
      ${views.map((v) => `
        <button type="button" class="filter-tab filter-tab-sm ${state.officeView === v.id ? "is-active" : ""}" data-office-view="${escapeAttr(v.id)}">${escapeHtml(v.label)}</button>`).join("")}
    </div>`;
}

function officeAllRankingsSections(rankTabs, top10) {
  const total = rankTabs.reduce((n, t) => n + (top10[t.id]?.length || 0), 0);
  return `
    <section class="section-block office-rankings-all">
      <h2 class="section-title">Top 10 × 4 — ${total} suggestions</h2>
      <p class="hint">All four ranked lists below (some overlap). Click titles for listing links. 🍳 / ☕ = kitchen / leisure room mentioned in text.</p>
      ${rankTabs.map((t) => officeRankingsBlock(t, top10[t.id] || [])).join("")}
    </section>`;
}

function officeRankingsBlock(tab, rows) {
  const scoreKey = tab.id === "price" ? "priceValue" : tab.id;
  return `
    <section class="section-block office-rankings" id="office-rank-${escapeAttr(tab.id)}">
      <h3 class="section-subtitle">${escapeHtml(tab.label)}</h3>
      <ol class="office-rank-list">
        ${rows.length
          ? rows.map((l) => officeRankRow(l, scoreKey)).join("")
          : `<li class="empty-inline">No listings in this category.</li>`}
      </ol>
    </section>`;
}

function officeRankRow(l, scoreKey) {
  const score = l.scores?.[scoreKey] ?? l.scores?.overall;
  const scoreLabel = score != null ? `${Math.round(score * 100)}%` : "—";
  const price = l.priceEur != null ? `€${l.priceEur}/mo` : "Price TBD";
  const sqm = l.sqm ? `${l.sqm} m²` : "—";
  const location = l.location || "Plovdiv";
  const title = (l.title || "Office listing").replace(/">$/, "");
  const budgetBadge = l.withinSoftBudget === false
    ? `<span class="badge badge-warn">Over €800</span>`
    : "";
  const am = l.amenities || {};
  const amenityBadges = [
    am.hasKitchen ? `<span class="badge badge-good" title="Kitchen mentioned">🍳 kitchen</span>` : "",
    am.hasLeisureRoom ? `<span class="badge badge-good" title="Leisure room mentioned">☕ leisure</span>` : "",
  ].filter(Boolean).join(" ");
  const titleHtml = l.url
    ? `<a class="office-rank-title" href="${escapeAttr(l.url)}" target="_blank" rel="noopener">${escapeHtml(title)} ↗</a>`
    : `<strong>${escapeHtml(title)}</strong>`;
  return `
    <li class="office-rank-item" data-search-text="${escapeAttr([title, location, l.snippet].join(" "))}">
      <span class="office-rank-num">#${l.rank ?? "—"}</span>
      <div class="office-rank-body">
        <div class="office-rank-head">
          ${titleHtml}
          ${amenityBadges}
          ${budgetBadge}
          <span class="office-rank-score" title="Match score">${scoreLabel}</span>
        </div>
        <div class="office-rank-meta">
          <span>${escapeHtml(location)}</span>
          <span>${escapeHtml(price)}</span>
          <span>${escapeHtml(sqm)}</span>
          <span class="office-rank-source">${escapeHtml(l.source || "")}</span>
        </div>
      </div>
    </li>`;
}

function criteriaPanel(criteria, maxBudget, rankCriteria = {}) {
  const defaults = [
    { label: "Budget", value: `~€${maxBudget} / month (flexible for exceptional spaces)` },
    { label: "City", value: "Plovdiv — central preferred" },
    {
      label: "Use",
      value: rankCriteria.use || "Training room ~20 students (≥40 m²)",
    },
    {
      label: "Size",
      value: rankCriteria.targetSqm
        ? `${rankCriteria.minSqm || 40}–${rankCriteria.targetSqm}+ m² target`
        : "≥40 m² (exclude tiny listings)",
    },
  ];
  const items = criteria.length ? criteria : defaults;
  return `
    <section class="criteria-panel">
      ${items.map((c) => `
        <div class="criteria-item">
          <span class="criteria-label">${escapeHtml(c.label)}</span>
          <span class="criteria-value">${escapeHtml(c.value)}</span>
        </div>`).join("")}
    </section>`;
}

function externalLinksBar(links) {
  const items = links.map((l) => {
    const label = typeof l === "string" ? l.replace(/^https?:\/\/(www\.)?/, "") : l.label;
    const url = typeof l === "string" ? l : l.url;
    return `<a class="ext-link" href="${escapeAttr(url)}" target="_blank" rel="noopener">${escapeHtml(label)} ↗</a>`;
  });
  return `
    <section class="ext-links-bar">
      <span class="ext-links-label">Search more:</span>
      ${items.join("")}
    </section>`;
}

function officeControls(cfg, maxBudget, count, listingsMeta) {
  const sortOpts = cfg.sortOptions || [
    { id: "price-asc", label: "Price ↑" },
    { id: "price-desc", label: "Price ↓" },
    { id: "sqm-desc", label: "Size ↓" },
  ];
  const updated = listingsMeta.generatedAt
    ? new Date(listingsMeta.generatedAt).toLocaleDateString()
    : "—";

  return `
    <section class="office-controls">
      <div class="office-filters">
        <label class="filter-field">
          <span>Max €/mo</span>
          <input type="range" min="200" max="1200" step="50" value="${state.officeMaxPrice ?? maxBudget}" data-office-max-price />
          <strong>€${state.officeMaxPrice ?? maxBudget}</strong>
        </label>
        <label class="filter-field">
          <span>Min m²</span>
          <input type="number" min="0" max="200" value="${state.officeMinSqm}" data-office-min-sqm />
        </label>
        <label class="filter-field filter-field-grow">
          <span>Search listings</span>
          <input type="search" placeholder="Neighborhood, street…" value="${escapeAttr(state.officeLocalQuery)}" data-office-local-query />
        </label>
      </div>
      <div class="filter-tabs" role="tablist">
        ${sortOpts.map((o) => `
          <button type="button" class="filter-tab ${state.officeSort === o.id ? "is-active" : ""}" data-office-sort="${escapeAttr(o.id)}">${escapeHtml(o.label)}</button>`).join("")}
      </div>
      <p class="hint">${count} listing${count === 1 ? "" : "s"} · updated ${updated}${listingsMeta.scrapeErrors?.length ? ` · ${listingsMeta.scrapeErrors.length} source warning(s)` : ""}</p>
    </section>`;
}

function filterOfficeListings(listings, maxBudget) {
  const max = state.officeMaxPrice ?? maxBudget;
  const minSqm = state.officeMinSqm || 0;
  const q = state.officeLocalQuery || state.query;

  return listings.filter((l) => {
    const price = l.priceEur;
    if (price != null && price > max) return false;
    if (minSqm && (l.sqm || 0) < minSqm) return false;
    if (q) {
      const blob = [l.title, l.location, l.snippet, l.source].join(" ").toLowerCase();
      if (!blob.includes(q)) return false;
    }
    return true;
  });
}

function sortOfficeListings(listings) {
  const s = state.officeSort;
  const copy = [...listings];
  const num = (v) => (v == null ? Infinity : v);
  const score = (r, key) => r.scores?.[key] ?? 0;
  copy.sort((a, b) => {
    if (s === "overall") return score(b, "overall") - score(a, "overall");
    if (s === "price-desc") return num(b.priceEur) - num(a.priceEur);
    if (s === "sqm-desc") return num(b.sqm) - num(a.sqm);
    if (s === "sqm-asc") return num(a.sqm) - num(b.sqm);
    if (s === "pricePerSqm-asc") return num(a.pricePerSqm) - num(b.pricePerSqm);
    return num(a.priceEur) - num(b.priceEur);
  });
  return copy;
}

function officeCard(l) {
  const price = l.priceEur != null ? `€${l.priceEur}` : "Price TBD";
  const sqm = l.sqm ? `${l.sqm} m²` : "—";
  const perSqm = l.pricePerSqm ? `€${l.pricePerSqm}/m²` : "";
  const location = l.location || "Plovdiv";
  const title = (l.title || "Office listing").replace(/">$/, "");
  const link = l.url
    ? `<a class="office-card-link" href="${escapeAttr(l.url)}" target="_blank" rel="noopener">View on ${escapeHtml(l.source || "site")} ↗</a>`
    : `<span class="office-card-link muted">No direct link — search ${escapeHtml(l.source || "alo.bg")}</span>`;

  return `
    <article class="office-card" data-search-text="${escapeAttr([title, location, l.snippet].join(" "))}">
      <header class="office-card-head">
        <h3>${escapeHtml(title)}</h3>
        <span class="office-card-location">${escapeHtml(location)}</span>
      </header>
      <div class="office-card-stats">
        <span class="office-stat office-stat-price">${price}<small>/mo</small></span>
        <span class="office-stat">${sqm}</span>
        ${perSqm ? `<span class="office-stat office-stat-muted">${perSqm}</span>` : ""}
      </div>
      ${l.snippet ? `<details class="office-details"><summary>Details</summary><p>${escapeHtml(cleanSnippet(l.snippet))}</p></details>` : ""}
      <footer class="office-card-foot">${link}</footer>
    </article>`;
}

function cleanSnippet(s) {
  return s.replace(/\s+/g, " ").slice(0, 280) + (s.length > 280 ? "…" : "");
}

function shortlistSection(table) {
  return `
    <section class="section-block">
      <h2 class="section-title">Your shortlist</h2>
      <div class="data-table-wrap">${renderTableHtml(table, { linkColumns: ["address"] })}</div>
    </section>`;
}

/* ── Brand sprint ── */

function renderBrand() {
  const sprint = state.data.planning?.brandSprint;
  if (!sprint) {
    return `${pageHeader("Brand sprint", "No sprint configured.")}<p class="empty-inline">Run scripts/apply_brand_sprint_2026_06_19.py</p>`;
  }
  const props = sprint.props || {};
  const day = props.current_day || 1;
  const sections = sprint.sections || {};
  const budget = (sprint.tables || []).find((t) => t.name === "budget_scenarios");
  const brandActions = (state.data.inbox || []).filter((a) => /brand-sprint-day-\d/i.test(a.title || ""));
  const dayLabels = { 1: "Positioning", 2: "Identity", 3: "Channels", 4: "Budget" };

  return `
    ${pageHeader(
      "Brand sprint",
      `4-day plan (${props.sprint_start || "?"} → ${props.sprint_end || "?"}). Complete one day at a time — copy Slack replies from Inbox.`
    )}
    <div class="stat-grid brand-stat-grid">
      ${statCard("Current day", day, dayLabels[day] || "Focus", "#brand")}
      ${statCard("Days left", Math.max(0, 4 - day), "until sign-off", "#brand")}
      ${statCard("Inbox items", brandActions.filter((a) => a.status === "open").length, "brand replies", "#inbox")}
    </div>
    ${brandDayTabs(day)}
    ${brandDayPanel(day, sections[`day${day}`] || [])}
    ${budget ? brandBudgetSection(budget) : ""}
    ${brandResourcesSection(sections.resources || [])}
    ${brandPlanLink(props.plan_doc)}
    ${brandAllDaysOverview(sections, day)}`;
}

function brandSprintHomePanel(sprint) {
  const day = sprint.props?.current_day || 1;
  const tasks = (sprint.sections?.[`day${day}`] || []).slice(0, 3);
  return `
    <section class="panel-card panel-brand">
      <div class="panel-head">
        <h2>Brand sprint · Day ${day}</h2>
        <a class="text-link" href="#brand">Open sprint →</a>
      </div>
      <p class="hint">Complete your marketing plan by ${escapeHtml(sprint.props?.sprint_end || "22 Jun")}.</p>
      <ul class="compact-list">${tasks.map((t) => `<li>${escapeHtml(t.text)}</li>`).join("")}</ul>
    </section>`;
}

function brandDayTabs(currentDay) {
  const labels = ["Day 1", "Day 2", "Day 3", "Day 4"];
  return `
    <div class="filter-tabs" role="tablist">
      ${labels.map((label, i) => {
        const d = i + 1;
        const active = d === currentDay ? "is-active" : "";
        return `<span class="filter-tab ${active}" title="Progress via inbox replies">${escapeHtml(label)}${d < currentDay ? " ✓" : ""}</span>`;
      }).join("")}
    </div>`;
}

function brandDayPanel(day, tasks) {
  const brandActions = (state.data.inbox || []).filter((a) => /brand-sprint-day-\d/i.test(a.title || ""));
  const action = brandActions.find((a) => new RegExp(`day\\s*${day}\\b`, "i").test(a.title || ""));
  const slackBlock = action?.slackReply
    ? `
      <div class="copy-block brand-copy">
        <div class="copy-head"><span class="copy-label">Slack reply → ${escapeHtml(action.slackChannel || "#vibe-code")}</span></div>
        <div class="copy-row">
          <pre class="copy-text">${escapeHtml(action.slackReply)}…</pre>
          <button type="button" class="copy-btn" data-copy="${escapeAttr(action.slackReply)}">Copy prefix</button>
        </div>
      </div>`
  : "";
  return `
    <section class="section-block brand-day-panel">
      <h2 class="section-title">Today — Day ${day}</h2>
      <ol class="numbered-list brand-task-list">
        ${tasks.map((t) => `<li data-search-text="${escapeAttr(t.text)}">${escapeHtml(t.text)}</li>`).join("") || "<li class='muted'>—</li>"}
      </ol>
      ${slackBlock}
      ${action ? `<p class="hint"><a class="text-link" href="#inbox">Open Inbox</a> for full reply template.</p>` : ""}
    </section>`;
}

function brandBudgetSection(table) {
  return `
    <section class="section-block">
      <h2 class="section-title">Budget scenarios (months 1–3)</h2>
      <div class="data-table-wrap">${renderTableHtml(table)}</div>
      <p class="hint">Lean recommended until waitlist landing is live. BG training ads often see €3–6 cost per inquiry at scale.</p>
    </section>`;
}

function brandResourcesSection(resources) {
  if (!resources.length) return "";
  return `
    <section class="section-block">
      <h2 class="section-title">Prep resources</h2>
      <ul class="resource-list">
        ${resources.map((r) => {
          const urlMatch = r.text.match(/https?:\/\/\S+/);
          if (urlMatch) {
            const label = r.text.split("—")[0].trim();
            return `<li><a class="table-link" href="${escapeAttr(urlMatch[0])}" target="_blank" rel="noopener">${escapeHtml(label)} ↗</a></li>`;
          }
          return `<li>${escapeHtml(r.text)}</li>`;
        }).join("")}
      </ul>
    </section>`;
}

function brandPlanLink(planDoc) {
  if (!planDoc) return "";
  return `
    <section class="section-block">
      <h2 class="section-title">Draft plan</h2>
      <p class="hint">Full marketing plan: <code>${escapeHtml(planDoc)}</code> — agents merge your day 1–4 replies into business/plan after sign-off.</p>
    </section>`;
}

function brandAllDaysOverview(sections, currentDay) {
  const days = [1, 2, 3, 4];
  const blocks = days
    .filter((d) => d !== currentDay && (sections[`day${d}`] || []).length)
    .map((d) => `
      <details class="standup-details">
        <summary>Day ${d} preview</summary>
        <ul>${(sections[`day${d}`] || []).map((t) => `<li>${escapeHtml(t.text)}</li>`).join("")}</ul>
      </details>`)
    .join("");
  if (!blocks) return "";
  return `<section class="section-block"><h2 class="section-title">Upcoming days</h2><div class="standup-stack">${blocks}</div></section>`;
}

/* ── Work plan (tasks + roadmap + standups) ── */

function renderWork() {
  const p = state.data.planning || {};
  return `
    ${pageHeader("Work plan", "Tasks, roadmap, and standup history.")}
    ${renderTasksContent()}
    ${p.nearTerm ? nearTermSection(p.nearTerm) : ""}
    ${p.tracks?.tables?.length ? roadmapTable("Launch tracks", p.tracks.tables[0]) : ""}
    ${p.phases?.tables?.length ? roadmapTable("Phases", p.phases.tables[0]) : ""}
    ${standupsSection(p.standups || [])}`;
}

function renderTasksContent() {
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
    <section class="section-block">
      <h2 class="section-title">Task boards</h2>
      ${boardTabs}
      ${activeBoards.map((b) => taskBoardHtml(b, cols)).join("")}
    </section>`;
}

function nearTermSection(entry) {
  const items = (entry.listItems || []).filter((i) => !i.done);
  return `
    <section class="section-block">
      <h2 class="section-title">Near-term queue</h2>
      <ul class="numbered-list">${items.map((i) => `<li data-search-text="${escapeAttr(i.text)}">${escapeHtml(i.text)}</li>`).join("")}</ul>
    </section>`;
}

function roadmapTable(title, table) {
  return `
    <section class="section-block">
      <h2 class="section-title">${escapeHtml(title)}</h2>
      <div class="data-table-wrap">${renderTableHtml(table)}</div>
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
  const order = ["done", "ongoing", "today", "blockers", "agent_next"];
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

/* ── Research ── */

function renderResearch() {
  const hub = state.data.researchHub || {};
  const entries = hub.entries || [];
  const competitors = entries.find((e) => e.slug === "competitors");
  const reports = entries.filter((e) => e.slug !== "competitors");

  return `
    ${pageHeader("Research", "Competitors and market reports — click any link to open the source.")}
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
      <div class="data-table-wrap">${renderTableHtml(table, { linkColumns: ["url"] })}</div>
    </section>`;
}

function researchReportCard(entry) {
  const date = entry.props?.report_date || "";
  return `
    <article class="research-card" data-search-text="${searchAttr({ title: entry.title, hint: entry.excerpt })}">
      <header>
        <h3>${escapeHtml(entry.title)}</h3>
        ${date ? `<span class="research-date">${escapeHtml(date)}</span>` : ""}
      </header>
      <p class="research-excerpt">${escapeHtml(entry.excerpt)}</p>
    </article>`;
}

/* ── Shared components ── */

function renderTableHtml(table, opts = {}) {
  const cols = table.columns || [];
  const rows = table.rows || [];
  const linkCols = new Set(opts.linkColumns || []);
  return `
    <table class="data-table">
      <thead><tr>${cols.map((c) => `<th>${escapeHtml(c)}</th>`).join("")}</tr></thead>
      <tbody>
        ${rows.map((r) => `
          <tr data-search-text="${escapeAttr(cols.map((c) => r[c]).join(" "))}">
            ${cols.map((c) => `<td>${cellHtml(r[c], linkCols.has(c))}</td>`).join("")}
          </tr>`).join("")}
      </tbody>
    </table>`;
}

function cellHtml(value, isLink) {
  const v = String(value ?? "");
  if (!v) return "";
  if (isLink && /^https?:\/\//i.test(v)) {
    const label = v.replace(/^https?:\/\/(www\.)?/, "").slice(0, 48);
    return `<a class="table-link" href="${escapeAttr(v)}" target="_blank" rel="noopener">${escapeHtml(label)} ↗</a>`;
  }
  return escapeHtml(v);
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
  const priority = a.priority === 1 ? `<span class="priority">Priority</span>` : "";

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
  const navItem = state.data.ui.nav.find((n) => n.id === state.section);
  const eyebrow = navItem?.label || state.section;
  return `
    <header class="page-header">
      <p class="eyebrow">${escapeHtml(eyebrow)}</p>
      <h1>${escapeHtml(title)}</h1>
      <p class="lede">${escapeHtml(desc)}</p>
    </header>`;
}

function applySearch() {
  if (state.section === "office") return;
  const q = state.query;
  document.querySelectorAll("[data-search-text], .action-card, .kanban-card, .research-card, .office-card, .data-table tbody tr, .numbered-list li, .standup-details, .priority-row").forEach((el) => {
    const text = (el.dataset.searchText || el.textContent || "").toLowerCase();
    el.classList.toggle("hidden", q && !text.includes(q));
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
    building: "🏢",
    sparkles: "✦",
  }[name] || "•";
}

function escapeHtml(v) {
  return String(v ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function escapeAttr(v) {
  return escapeHtml(v).replace(/`/g, "&#096;");
}
