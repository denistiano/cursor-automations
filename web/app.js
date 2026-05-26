const DATA_URL = "data/site.json";
const REPO_URL = "https://github.com/denistiano/cursor-automations";

const state = {
  data: null,
  activeSection: "overview",
  query: "",
};

const app = document.querySelector("#app");
const tabs = document.querySelector("#tabs");
const searchInput = document.querySelector("#searchInput");

document.addEventListener("DOMContentLoaded", init);

async function init() {
  wireControls();

  try {
    const response = await fetch(DATA_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`Could not load ${DATA_URL}`);
    state.data = await response.json();
    renderShellData();
    setActiveSection(getSectionFromHash() || "overview");
  } catch (error) {
    renderError(error);
  }
}

function wireControls() {
  tabs.addEventListener("click", (event) => {
    const button = event.target.closest("[data-section]");
    if (!button) return;
    setActiveSection(button.dataset.section);
  });

  searchInput.addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    applySearch();
  });

  window.addEventListener("hashchange", () => {
    setActiveSection(getSectionFromHash() || "overview", { updateHash: false });
  });
}

function getSectionFromHash() {
  const value = window.location.hash.replace("#", "");
  return value || null;
}

function setActiveSection(section, options = {}) {
  state.activeSection = section;
  if (options.updateHash !== false) window.location.hash = section;

  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.toggle("is-active", tab.dataset.section === section);
  });

  renderSection();
}

function renderShellData() {
  const { data } = state;
  const generated = new Date(data.meta.generatedAt);
  document.querySelector("#generatedAt").textContent = `Generated ${generated.toLocaleString([], {
    dateStyle: "medium",
    timeStyle: "short",
  })}`;

  document.querySelector("#heroMetrics").innerHTML = [
    metric("Open tasks", data.todo.counts.open),
    metric("Standups", data.standups.entries.length),
    metric("Automations", data.automations.length),
    metric("Sources", data.meta.sources.length),
  ].join("");
}

function metric(label, value) {
  return `<div class="metric-card"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(label)}</span></div>`;
}

function renderSection() {
  if (!state.data) return;

  const renderers = {
    overview: renderOverview,
    tasks: renderTasks,
    standups: renderStandups,
    business: renderBusiness,
    research: renderResearch,
    automations: renderAutomations,
    social: renderSocial,
  };

  app.innerHTML = renderers[state.activeSection]?.() || renderOverview();
  applySearch();
}

function renderOverview() {
  const { readme, todo, standups, business, research, automations, social } = state.data;
  const latest = standups.latest;
  const blockers = latest?.blockers?.length ? latest.blockers : ["No blockers recorded in the latest standup."];

  return `
    ${sectionHeader("Overview", readme.description || "Single source of truth for this course business.")}
    <div class="grid">
      ${card(
        "Operating status",
        `
          <div class="chip-row">
            ${pill(`${todo.counts.open} open tasks`, "warn")}
            ${pill(`${todo.counts.done} done`, "good")}
          </div>
          ${renderTaskPreview(todo.groups.flatMap((group) => group.items).slice(0, 5))}
        `,
        readme.path
      )}
      ${card(
        "Latest standup",
        latest
          ? `
            <p class="eyebrow">${escapeHtml(latest.date)}</p>
            <h3>Today</h3>
            ${list(latest.today)}
            <h3>Blockers / decisions</h3>
            ${list(blockers)}
          `
          : "<p>No standups have been generated yet.</p>",
        latest?.path || "planning/standups/"
      )}
      ${card(
        "Automation coverage",
        `
          <p>${escapeHtml(automations.length)} automation prompts are documented.</p>
          <div class="chip-row">
            ${automations.map((automation) => pill(automation.settings.name || automation.title)).join("")}
          </div>
        `,
        "docs/automations/"
      )}
    </div>

    <div class="grid two">
      ${card(
        "Business signal",
        `
          <p><strong>Status:</strong> ${escapeHtml(business.plan.status || "Unknown")}</p>
          <p><strong>Last updated:</strong> ${escapeHtml(business.plan.lastUpdated || "Unknown")}</p>
          <div class="chip-row">
            ${business.approvedMessaging.allowedClaims.map((claim) => pill(claim, "good")).join("")}
          </div>
        `,
        business.plan.path
      )}
      ${card(
        "Research + social",
        `
          <p>${escapeHtml(research.competitors.watchlist.length)} competitor watchlist rows.</p>
          <p>${escapeHtml(social.counts.total)} social drafts, ${escapeHtml(social.counts.pending)} pending approval.</p>
          <div class="chip-row">
            ${pill("Markdown remains source of truth")}
            ${pill("JSON powers UI")}
          </div>
        `,
        research.competitors.path
      )}
    </div>
    ${renderSources()}
  `;
}

function renderTasks() {
  const { todo } = state.data;
  return `
    ${sectionHeader("Tasks", "Grouped directly from planning/TODO.md so the dashboard follows PM automation output.")}
    <div class="grid two">
      ${todo.groups
        .map((group) =>
          card(
            group.title,
            group.items.length
              ? group.items.map(renderTaskRow).join("")
              : "<p>No checklist items in this group yet.</p>",
            todo.path
          )
        )
        .join("")}
    </div>
  `;
}

function renderStandups() {
  const { standups } = state.data;
  return `
    ${sectionHeader("Standups", "Daily PM records with Done, Today, Blockers, and Agent next actions.")}
    <div class="timeline">
      ${
        standups.entries.length
          ? standups.entries
              .map(
                (entry) => `
                  <article class="card timeline-item" data-search-text="${searchText(entry)}">
                    <div>
                      <div class="timeline-date">${escapeHtml(entry.date)}</div>
                      ${sourceLink(entry.path)}
                    </div>
                    <div class="grid two">
                      <div>
                        <h3>Done</h3>
                        ${list(entry.done)}
                      </div>
                      <div>
                        <h3>Today</h3>
                        ${list(entry.today)}
                      </div>
                      <div>
                        <h3>Blockers / decisions</h3>
                        ${list(entry.blockers)}
                      </div>
                      <div>
                        <h3>Agent next actions</h3>
                        ${list(entry.agentNextActions)}
                      </div>
                    </div>
                  </article>
                `
              )
              .join("")
          : card("No standups yet", "<p>Morning standup automation has not produced dated files yet.</p>", "planning/standups/")
      }
    </div>
  `;
}

function renderBusiness() {
  const { plan, approvedMessaging } = state.data.business;
  return `
    ${sectionHeader("Business", "Plan sections, messaging guardrails, pricing status, and claims rules.")}
    <div class="grid two">
      ${card(
        "Plan status",
        `
          <p><strong>Status:</strong> ${escapeHtml(plan.status || "Unknown")}</p>
          <p><strong>Last updated:</strong> ${escapeHtml(plan.lastUpdated || "Unknown")}</p>
          <div class="chip-row">${plan.sections.map((section) => pill(section.title)).join("")}</div>
        `,
        plan.path
      )}
      ${card(
        "Approved messaging",
        `
          <p><strong>Working title:</strong> ${escapeHtml(approvedMessaging.course["working-title"] || "TBD")}</p>
          <p><strong>One-liner:</strong> ${escapeHtml(approvedMessaging.course["one-liner"] || "TBD")}</p>
          <p><strong>Who it is for:</strong> ${escapeHtml(approvedMessaging.course["who-its-for"] || approvedMessaging.course["who-it-s-for"] || "TBD")}</p>
        `,
        approvedMessaging.path
      )}
    </div>
    <div class="grid">
      ${plan.sections
        .map((section) =>
          card(
            section.title,
            `
              ${section.bullets.length ? list(section.bullets.slice(0, 7)) : markdownBlock(section.content)}
              ${section.tables?.[0] ? table(section.tables[0]) : ""}
            `,
            plan.path
          )
        )
        .join("")}
    </div>
    <div class="grid two">
      ${card("Allowed claims", list(approvedMessaging.allowedClaims), approvedMessaging.path)}
      ${card("Claims not allowed", list(approvedMessaging.disallowedClaims), approvedMessaging.path)}
    </div>
  `;
}

function renderResearch() {
  const competitors = state.data.research.competitors;
  return `
    ${sectionHeader("Research", "Competitor watchlist and report inventory for the research automation.")}
    <div class="grid two">
      ${card(
        "Competitor watchlist",
        competitors.watchlist.length ? table(competitors.watchlist) : "<p>No competitors entered yet.</p>",
        competitors.path
      )}
      ${card(
        "Research triggers",
        `
          ${list(competitors.triggerHints)}
          <div class="chip-row">
            ${pill(`${competitors.reports.length} dated reports`)}
          </div>
        `,
        competitors.path
      )}
    </div>
    <div class="grid">
      ${
        competitors.reports.length
          ? competitors.reports
              .map((report) => card(report.title || report.path, "<p>Dated competitor research report.</p>", report.path))
              .join("")
          : card("No dated reports yet", "<p>Reports will appear after the research automation writes files.</p>", "research/competitors/")
      }
    </div>
  `;
}

function renderAutomations() {
  const { automations } = state.data;
  return `
    ${sectionHeader("Automations", "Copy-paste prompt inventory with triggers, tools, checklist, and prompt previews.")}
    <div class="grid two">
      ${automations
        .map((automation) =>
          card(
            automation.settings.name || automation.title,
            `
              <div class="automation-topline">
                ${pill(automation.settings.trigger || "Trigger TBD", "warn")}
                ${pill(automation.settings.repo || "Repo TBD")}
              </div>
              <p><strong>Tools:</strong> ${escapeHtml(automation.settings.tools || "TBD")}</p>
              <h3>Denis checklist</h3>
              ${list(automation.checklist)}
              <pre>${escapeHtml(automation.promptPreview)}</pre>
            `,
            automation.path
          )
        )
        .join("")}
    </div>
  `;
}

function renderSocial() {
  const { social } = state.data;
  return `
    ${sectionHeader("Social", "Draft inventory with approval status from frontmatter.")}
    <div class="grid">
      ${card(
        "Draft status",
        `
          <div class="chip-row">
            ${pill(`${social.counts.total} total`)}
            ${pill(`${social.counts.pending} pending`, "warn")}
            ${pill(`${social.counts.approved} approved`, "good")}
          </div>
          <p>Publishing stays gated by <code>approved: true</code> in markdown frontmatter.</p>
        `,
        social.templatePath || "content/social/"
      )}
      ${
        social.drafts.length
          ? social.drafts
              .map((draft) =>
                card(
                  draft.title || draft.path,
                  `
                    <div class="chip-row">
                      ${pill(draft.platform)}
                      ${pill(draft.approved ? "approved" : "pending", draft.approved ? "good" : "warn")}
                    </div>
                    <p><strong>Scheduled:</strong> ${escapeHtml(draft.scheduledAt || "Not scheduled")}</p>
                    <p><strong>Post ID:</strong> ${escapeHtml(draft.postId || "None")}</p>
                  `,
                  draft.path
                )
              )
              .join("")
          : card("No social drafts yet", "<p>Drafts will appear under content/social/YYYY-MM-DD/.</p>", social.templatePath || "content/social/")
      }
    </div>
  `;
}

function sectionHeader(title, description) {
  return `
    <section class="section-heading">
      <div>
        <p class="eyebrow">${escapeHtml(state.activeSection)}</p>
        <h2>${escapeHtml(title)}</h2>
        <p>${escapeHtml(description)}</p>
      </div>
    </section>
  `;
}

function card(title, body, sourcePath = "") {
  return `
    <article class="card" data-search-text="${escapeAttr(`${title} ${stripTags(body)} ${sourcePath}`)}">
      <div>
        <h3>${escapeHtml(title)}</h3>
        ${body}
      </div>
      ${sourcePath ? `<footer class="card-footer">${sourceLink(sourcePath)}</footer>` : ""}
    </article>
  `;
}

function renderTaskPreview(items) {
  return items.length ? items.map(renderTaskRow).join("") : "<p>No tasks found.</p>";
}

function renderTaskRow(item) {
  return `
    <div class="task-row">
      <span class="checkbox" aria-hidden="true">${item.done ? "x" : ""}</span>
      <span class="task-text ${item.done ? "done" : ""}">${escapeHtml(item.text)}</span>
    </div>
  `;
}

function list(items) {
  const safeItems = (items || []).filter(Boolean);
  if (!safeItems.length) return "<p class=\"meta\">Nothing recorded yet.</p>";
  return `<ul>${safeItems.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function table(rows) {
  if (!rows?.length) return "";
  const columns = Object.keys(rows[0]);
  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>${columns.map((column) => `<th>${escapeHtml(titleCase(column))}</th>`).join("")}</tr>
        </thead>
        <tbody>
          ${rows
            .map((row) => `<tr>${columns.map((column) => `<td>${escapeHtml(row[column] || "")}</td>`).join("")}</tr>`)
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

function markdownBlock(content) {
  const text = (content || "").split("\n").filter(Boolean).slice(0, 8).join("\n");
  if (!text) return "<p class=\"meta\">No content yet.</p>";
  return `<p>${escapeHtml(text).replace(/\n/g, "<br />")}</p>`;
}

function renderSources() {
  const sources = state.data.meta.sources.slice(0, 18);
  return card(
    "Data sources",
    `
      <p>The dashboard is generated from ${escapeHtml(state.data.meta.sources.length)} repo files.</p>
      <div class="source-list">
        ${sources.map((source) => sourceLink(source)).join("")}
      </div>
    `,
    "web/data/site.json"
  );
}

function sourceLink(path) {
  const href = `${REPO_URL}/blob/master/${path}`;
  return `<a class="card-source" href="${escapeAttr(href)}" target="_blank" rel="noreferrer">${escapeHtml(path)}</a>`;
}

function pill(label, variant = "") {
  return `<span class="pill ${escapeAttr(variant)}">${escapeHtml(label || "TBD")}</span>`;
}

function applySearch() {
  const query = state.query;
  const cards = app.querySelectorAll("[data-search-text]");
  let visible = 0;

  cards.forEach((cardElement) => {
    const text = cardElement.dataset.searchText.toLowerCase();
    const matches = !query || text.includes(query);
    cardElement.classList.toggle("hidden-by-search", !matches);
    if (matches) visible += 1;
  });

  const oldEmpty = app.querySelector(".empty-state");
  if (oldEmpty) oldEmpty.remove();

  if (query && cards.length > 0 && visible === 0) {
    app.appendChild(document.querySelector("#emptyStateTemplate").content.cloneNode(true));
  }
}

function renderError(error) {
  app.innerHTML = `
    <section class="empty-state">
      <p class="eyebrow">Data unavailable</p>
      <h2>Could not load the dashboard JSON.</h2>
      <p>${escapeHtml(error.message)}</p>
      <p class="meta">Run <code>node scripts/build-site-data.js</code> and serve the web directory over HTTP.</p>
    </section>
  `;
}

function titleCase(value) {
  return value.replace(/-/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function stripTags(value) {
  return value.replace(/<[^>]*>/g, " ");
}

function searchText(value) {
  return escapeAttr(JSON.stringify(value));
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
  return escapeHtml(value).replace(/`/g, "&#096;");
}
