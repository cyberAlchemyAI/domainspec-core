(() => {
  const routes = window.__GQ_ROUTES || {};
  const stitchScreenPrefix = window.__GQ_STITCH_PREFIX || "";

  const pathFor = (key) => {
    const screen = routes[String(key || "").trim().toLowerCase()];
    return screen ? stitchScreenPrefix + encodeURIComponent(screen) + "/code.html" : "";
  };
  const labelFor = (text) => String(text || "").replace(/\s+/g, " ").trim().toLowerCase();
  const routeKeys = Object.keys(routes).sort((a, b) => b.length - a.length);
  const routeKeyFor = (text) => {
    const label = labelFor(text);
    if (routes[label]) return label;
    return routeKeys.find((key) => label.includes(key)) || "";
  };

  const style = document.createElement("style");
  style.textContent = [
    "[data-gq-live='true']{cursor:pointer!important}",
    ".gq-live-toast{position:fixed;right:16px;bottom:16px;z-index:99999;background:#07111f;color:#eef4ff;border:1px solid #d8e3fb;padding:10px 12px;font:12px ui-monospace,SFMono-Regular,Menlo,monospace;box-shadow:0 12px 40px rgba(0,0,0,.45);max-width:360px}",
    ".gq-live-badge{position:fixed;left:16px;bottom:16px;z-index:99999;background:#0b1c30;color:#b7c8e1;border:1px solid #38485d;padding:7px 9px;font:11px ui-monospace,SFMono-Regular,Menlo,monospace;text-transform:uppercase;letter-spacing:.04em;pointer-events:none}",
    ".gq-identity-indicator{position:fixed;left:16px;bottom:48px;z-index:99999;background:#101d2f;color:#eef4ff;border:1px solid #38485d;padding:7px 9px;font:11px ui-monospace,SFMono-Regular,Menlo,monospace;text-transform:uppercase;letter-spacing:.04em;pointer-events:none}",
    "a[role='button'][data-gq-live='true']{position:relative!important;z-index:80!important}",
    "footer{pointer-events:none!important}",
    "footer [data-gq-route],footer [data-gq-selectable='true']{pointer-events:auto!important}",
    ".gq-bookmarked{outline:1px solid #22c55e!important;color:#22c55e!important}",
    ".gq-filter-active{background:#ffffff!important;color:#101827!important;border-color:#ffffff!important}",
    ".gq-filter-muted{opacity:.42!important}",
    "[data-gq-route],[data-gq-selectable='true']{cursor:pointer!important}"
  ].join("\n");
  document.head.appendChild(style);

  let toastTimer = null;
  let openClawStatusCache = null;
  function toast(message) {
    let node = document.querySelector(".gq-live-toast");
    if (!node) {
      node = document.createElement("div");
      node.className = "gq-live-toast";
      document.body.appendChild(node);
    }
    node.textContent = message;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => node.remove(), 2200);
  }

  function setCommandPanel(state, message) {
    const panel = document.getElementById("commandResultPanel") || document.querySelector("[aria-live='polite']");
    if (!panel) return;
    panel.dataset.gqCommandState = state;
    panel.style.borderColor = state === "accepted" ? "#7A8C70" : state === "rejected" ? "#9C3C28" : "#B89745";
    const textNode = panel.querySelector("[class*='font-data-mono']") || panel;
    textNode.textContent = message;
  }

  function appendTerminal(message) {
    const log = document.querySelector("[role='log'] .font-data-mono, [role='log'], pre, .terminal");
    if (!log) return;
    const line = document.createElement("div");
    line.textContent = "> " + message;
    log.appendChild(line);
    log.scrollTop = log.scrollHeight;
  }

  async function openClawAction(action, label) {
    if (action === "status" && openClawStatusCache) {
      const message = "OPENCLAW_OK: " + openClawStatusCache;
      setCommandPanel("accepted", message);
      appendTerminal("openclaw status cached");
      toast(message);
      return { ok: true, action, version: openClawStatusCache, cached: true };
    }
    setCommandPanel("pending", "OPENCLAW_RUNNING: " + label);
    appendTerminal("openclaw " + action + " requested");
    try {
      const response = await fetch("/api/openclaw/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action, label })
      });
      const result = await response.json();
      const ok = response.ok && result.ok !== false;
      const message = ok
        ? "OPENCLAW_OK: " + (result.output_text || result.version || result.model || action)
        : "OPENCLAW_REJECTED: " + (result.reason || result.error || "unknown");
      setCommandPanel(ok ? "accepted" : "rejected", message);
      appendTerminal(message);
      toast(message);
      if (ok && action === "status") openClawStatusCache = result.version || result.output_text || "status ready";
      return result;
    } catch (error) {
      const message = "OPENCLAW_ERROR: " + error.message;
      setCommandPanel("rejected", message);
      appendTerminal(message);
      toast(message);
      return { ok: false, reason: error.message };
    }
  }

  async function commandEnvelope(commandType, payload, label) {
    setCommandPanel("pending", "COMMAND_RUNNING: " + label);
    try {
      const response = await fetch("/api/commands", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command_type: commandType, payload })
      });
      const result = await response.json();
      const accepted = response.ok && result.status === "accepted";
      const message = accepted
        ? "COMMAND_" + result.command_result + ": " + label
        : "COMMAND_REJECTED: " + (result.reason || label);
      setCommandPanel(accepted ? "accepted" : "rejected", message);
      appendTerminal(message);
      toast(message);
      return result;
    } catch (error) {
      const message = "COMMAND_ERROR: " + error.message;
      setCommandPanel("rejected", message);
      appendTerminal(message);
      toast(message);
      return { status: "rejected", reason: error.message };
    }
  }

  async function runScoutRescan(buttonLabel) {
    const input = Array.from(document.querySelectorAll("input"))
      .find((node) => /ONE-SHOT DISCOVERY/i.test(node.placeholder || ""));
    const query = input?.value || "";
    const payload = {
      cycle_id: "cyc_09F82A",
      query,
      context: {
        org_slug: "fit_farms_llc",
        cic: "Food Systems",
        clc: "Research & Evidence",
      },
    };
    const result = await commandEnvelope("SCOUT_DISCOVERY_REQUESTED", payload, buttonLabel || "Scout discovery");
    if (result && result.status === "accepted") {
      if (typeof renderLiveScoutPanel === "function") {
        renderLiveScoutPanel();
      } else {
        window.location.reload();
      }
    }
  }

  function navigate(key) {
    const path = pathFor(key);
    if (!path) {
      toast("No linked screen for " + key);
      return;
    }
    window.location.assign(path);
  }

  document.addEventListener("click", (event) => {
    const target = event.target.closest("a,button");
    if (!target) return;
    const text = target.textContent || target.getAttribute("aria-label") || "";
    if (/rescan/i.test(text)) {
      event.preventDefault();
      runScoutRescan(text.trim());
    }
  });

  function candidateText(node) {
    return [
      node.getAttribute?.("data-gq-route") || "",
      node.getAttribute?.("aria-label") || "",
      node.getAttribute?.("title") || "",
      node.textContent || ""
    ].join(" ");
  }

  function markRouteTarget(node, key, path) {
    if (!node || node.dataset.gqLive === "true") return;
    node.dataset.gqLive = "true";
    node.dataset.gqRoute = key;
    node.title = node.title || "Open " + labelFor(node.textContent || key);
    if (node.tagName === "A") {
      node.href = path;
      return;
    }
    node.setAttribute("role", "link");
    if (!node.hasAttribute("tabindex")) node.tabIndex = 0;
  }

  function wireNavLinks() {
    document.querySelectorAll("a").forEach((link) => {
      const key = routeKeyFor(candidateText(link));
      const path = pathFor(key);
      if (!path) return;
      markRouteTarget(link, key, path);

      link.classList.remove("bg-surface-container-highest", "text-primary", "border-r-2", "border-l-2", "border-primary");

      const isActive = window.location.pathname === path || (window.location.pathname === "/" && key === "home");
      if (isActive) {
        link.classList.add("bg-surface-container-highest", "text-primary", "border-l-2", "border-primary");
        link.classList.remove("text-on-surface-variant", "hover:bg-surface-container-high");
      } else {
        link.classList.add("text-on-surface-variant", "hover:bg-surface-container-high");
      }
    });
  }

  function wireRouteTargets() {
    document.querySelectorAll("li[class*='cursor-pointer'], [class*='cursor-pointer'], [role='button']").forEach((node) => {
      const text = labelFor(node.textContent);
      if (node.classList.contains("material-symbols-outlined") && /^[a-z0-9_]+$/.test(text)) return;
      const key = routeKeyFor(candidateText(node));
      const path = pathFor(key);
      if (!path) return;
      markRouteTarget(node, key, path);
    });
  }

  function wireDelegatedRouting() {
    document.addEventListener("click", (event) => {
      const target = event.target.closest("a[data-gq-live='true'], [data-gq-route]");
      if (!target) return;
      const key = target.dataset.gqRoute || routeKeyFor(candidateText(target));
      const path = pathFor(key);
      if (!path) return;
      event.preventDefault();
      event.stopPropagation();
      window.location.assign(path);
    }, true);
    document.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      const target = event.target.closest?.("[data-gq-route]");
      if (!target) return;
      event.preventDefault();
      navigate(target.dataset.gqRoute);
    }, true);
  }

  function opportunityCards() {
    return Array.from(document.querySelectorAll("main div")).filter((node) => {
      const text = node.textContent || "";
      return /OPP-ID:/.test(text) && node.querySelector("h3");
    });
  }

  function wireSearch() {
    const input = Array.from(document.querySelectorAll("input")).find((node) => /query/i.test(node.placeholder || ""));
    if (!input) return;
    input.addEventListener("input", () => {
      const term = input.value.trim().toLowerCase();
      let shown = 0;
      opportunityCards().forEach((card) => {
        const match = !term || card.textContent.toLowerCase().includes(term);
        card.style.display = match ? "" : "none";
        if (match) shown += 1;
      });
      if (term) toast("Filtered opportunities: " + shown);
    });
  }

  function wireButtons() {
    document.querySelectorAll("button").forEach((button) => {
      const label = labelFor(button.textContent);
      const icon = labelFor(button.querySelector(".material-symbols-outlined")?.textContent);
      const key = routeKeyFor(candidateText(button));
      const path = pathFor(key);
      button.removeAttribute("onclick");

      if (path) {
        const link = document.createElement("a");
        link.href = path;
        link.className = button.className;
        link.innerHTML = button.innerHTML;
        link.dataset.gqLive = "true";
        link.setAttribute("role", "button");
        link.setAttribute("aria-label", button.textContent.trim().replace(/\s+/g, " "));
        button.replaceWith(link);
        return;
      }

      if (label.includes("initialize openclaw") || label.includes("openclaw")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => openClawAction("gateway_smoke", button.textContent.trim() || "OpenClaw"));
        return;
      }

      if (label.includes("open eligibility")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => navigate("eligibility"));
        return;
      }

      if (label.includes("refresh sam.gov connection")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => navigate("refresh sam.gov connection"));
        return;
      }

      if (label.includes("view full audit log")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => navigate("view full audit log"));
        return;
      }

      if (label.includes("executive override")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => navigate("executive override"));
        return;
      }

      if (label.includes("review requirement")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => navigate("intake"));
        return;
      }

      if (label.includes("new today") || label.includes("high fit") || label.includes("deadline risk")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => {
          document.querySelectorAll("button").forEach((candidate) => candidate.classList.remove("gq-filter-active"));
          button.classList.add("gq-filter-active");
          const mode = button.textContent.trim();
          opportunityCards().forEach((card) => {
            const text = card.textContent.toLowerCase();
            const show = label.includes("new today")
              || (label.includes("high fit") && /9[0-9]% fit|98% fit|92% fit/.test(text))
              || (label.includes("deadline risk") && /5 days|14 days/.test(text));
            card.classList.toggle("gq-filter-muted", !show);
          });
          toast("Filter applied: " + mode);
        });
        return;
      }

      if (icon === "bookmark" || label === "bookmark") {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => {
          button.classList.toggle("gq-bookmarked");
          toast(button.classList.contains("gq-bookmarked") ? "Opportunity saved locally" : "Opportunity unsaved");
        });
        return;
      }

      if (label.includes("stage data")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => openClawAction("gateway_smoke", button.textContent.trim() || "Stage Data"));
        return;
      }

      if (icon === "sync" || label.includes("sync")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => openClawAction("status", button.textContent.trim() || "OpenClaw status"));
        return;
      }

      if (label.includes("scribe")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => commandEnvelope("SCRIBE_RUN_REQUESTED", { cycle_id: "cyc_09F82A", section_id: "sec_project_narrative" }, button.textContent.trim() || "Scribe command"));
        return;
      }

      if (label.includes("judge")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => commandEnvelope("JUDGE_PANEL_RUN_REQUESTED", { cycle_id: "cyc_09F82A" }, button.textContent.trim() || "Judge command"));
        return;
      }

      if (label.includes("red team")) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => commandEnvelope("RED_TEAM_PROBE_RUN_REQUESTED", { cycle_id: "cyc_09F82A" }, button.textContent.trim() || "Red Team command"));
        return;
      }

      if (!button.disabled) {
        button.dataset.gqLive = "true";
        button.addEventListener("click", () => openClawAction("status", button.textContent.trim() || icon || "button action"));
      }
    });
  }

  function wireSort() {
    document.querySelectorAll("select").forEach((select) => {
      select.addEventListener("change", () => toast("Sort changed: " + select.value));
    });
  }

  function hideRetiredCardRoutes() {
    document.querySelectorAll("a, li, [class*='cursor-pointer']").forEach((node) => {
      const label = labelFor(node.textContent);
      if (label.includes("cards") || label.includes("card matrix")) {
        node.style.display = "none";
        node.removeAttribute("href");
        node.removeAttribute("data-gq-live");
        node.removeAttribute("data-gq-route");
        node.removeAttribute("tabindex");
      }
    });
  }

  function addBadge() {
    const badge = document.createElement("div");
    badge.className = "gq-live-badge";
    badge.textContent = "Local Stitch viewer active";
    document.body.appendChild(badge);
  }

  function addIdentityIndicator() {
    const indicator = document.createElement("div");
    indicator.className = "gq-identity-indicator";
    indicator.textContent = "Lens: Food Systems / Research";
    document.body.appendChild(indicator);
  }

  hideRetiredCardRoutes();
  wireNavLinks();
  wireButtons();
  wireRouteTargets();
  wireDelegatedRouting();
  wireSearch();
  wireSort();
  hideRetiredCardRoutes();
  addIdentityIndicator();
  addBadge();
  renderLiveScoutPanel();

  function scoutEscape(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  function scoutCurrency(n) {
    const num = Number(n) || 0;
    if (!num) return "—";
    return "$" + num.toLocaleString();
  }

  function renderScoutOpp(opp) {
    const titleUrl = opp.url || "#";
    const conf = (opp.confidence == null || opp.confidence === "") ? "—" : opp.confidence;
    return [
      '<li style="padding:10px 12px;border:1px solid #2a2a2a;border-radius:4px;margin-bottom:6px;background:#0f0f0f;color:#eef4ff;">',
      '<div style="display:flex;justify-content:space-between;gap:12px;">',
      '<div style="flex:1;min-width:0;">',
      '<a href="' + scoutEscape(titleUrl) + '" target="_blank" rel="noopener" style="font-weight:600;color:#ffeb99;text-decoration:none;">',
      scoutEscape(opp.program || "Untitled"),
      "</a>",
      '<div style="font-size:11px;color:#b7c8e1;margin-top:2px;">',
      scoutEscape(opp.agency || ""), " · ",
      scoutEscape(opp.deadline || "no deadline"), " · ",
      scoutEscape(opp.urgency || ""),
      "</div>",
      '<div style="font-size:12px;color:#dcdcdc;margin-top:6px;line-height:1.4;">',
      scoutEscape(opp.rationale || opp.summary || ""),
      "</div>",
      "</div>",
      '<div style="font-size:11px;color:#9aa6b8;text-align:right;white-space:nowrap;">',
      "conf: " + scoutEscape(conf),
      opp.amount ? "<br>" + scoutCurrency(opp.amount) : "",
      "</div>",
      "</div>",
      "</li>",
    ].join("");
  }

  function renderScoutTier(label, items, color, collapsed) {
    if (!items.length) return "";
    const openAttr = collapsed ? "" : " open";
    return [
      "<details" + openAttr + ' style="margin-bottom:14px;">',
      '<summary style="cursor:pointer;font-weight:700;font-size:13px;color:' + color + ';margin-bottom:8px;letter-spacing:.05em;">',
      label + " (" + items.length + ")",
      "</summary>",
      '<ul style="list-style:none;padding:0;margin:8px 0;">',
      items.map(renderScoutOpp).join(""),
      "</ul>",
      "</details>",
    ].join("");
  }

  async function renderLiveScoutPanel() {
    let projection;
    try {
      const resp = await fetch("/api/projections/current");
      if (!resp.ok) return;
      projection = await resp.json();
    } catch (err) {
      console.warn("[gq-live-scout] fetch failed:", err);
      return;
    }

    const scout = projection && projection.scout;
    if (!scout || scout.source !== "scout.discovery.completed") return;

    const opps = Array.isArray(scout.opportunities) ? scout.opportunities : [];
    if (!opps.length) return;

    const byTier = { must_read: [], maybe: [], declined: [] };
    for (const opp of opps) {
      const t = opp.tier || (opp.confidence >= 80 ? "must_read" : "maybe");
      (byTier[t] || byTier.maybe).push(opp);
    }

    const meta = scout.meta || {};
    const totals = scout.totals || {};
    const generatedAt = scout.generated_at
      ? new Date(scout.generated_at).toLocaleString()
      : "just now";

    const existing = document.getElementById("gq-live-scout-panel");
    if (existing) existing.remove();

    const panel = document.createElement("section");
    panel.id = "gq-live-scout-panel";
    panel.style.cssText = [
      "background:#070b14",
      "border:2px solid #ffeb99",
      "border-radius:8px",
      "padding:20px 22px",
      "margin:72px 16px 16px 16px",
      "font-family:system-ui,-apple-system,sans-serif",
      "color:#eef4ff",
      "box-shadow:0 8px 30px rgba(0,0,0,.5)",
      "position:relative",
      "z-index:50",
    ].join(";");

    const metaLine = [
      meta.model || "?",
      meta.family || "",
      (meta.elapsed_seconds != null ? meta.elapsed_seconds + "s" : ""),
      (meta.candidates_reviewed || opps.length) + " candidates",
      meta.validation_passed === true
        ? "✓ validation passed"
        : "⚠ validation: " + ((meta.validation_errors || []).join("; ") || "n/a"),
    ].filter(Boolean).map(scoutEscape).join(" · ");

    const totalsLine = [
      "<span><strong>" + (totals.signals || 0) + "</strong> signals</span>",
      "<span><strong>" + (totals.tracked || 0) + "</strong> tracked</span>",
      "<span><strong>" + (totals.new_today || 0) + "</strong> new (7d)</span>",
    ].join("&nbsp;&nbsp;&nbsp;");

    panel.innerHTML = [
      '<header style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;gap:16px;flex-wrap:wrap;">',
      '<h2 style="margin:0;font-size:20px;font-weight:700;color:#ffeb99;letter-spacing:.02em;">LIVE SCOUT SCAN</h2>',
      '<div style="display:flex;align-items:center;gap:12px;">',
      '<span style="font-size:11px;color:#9aa6b8;">' + scoutEscape(generatedAt) + "</span>",
      '<button id="gq-live-scout-rescan" type="button" style="background:#ffeb99;color:#070b14;border:none;padding:6px 14px;border-radius:4px;font-weight:700;font-size:12px;letter-spacing:.05em;cursor:pointer;">RESCAN</button>',
      "</div>",
      "</header>",
      '<div style="font-size:11px;color:#9aa6b8;margin-bottom:12px;">' + metaLine + "</div>",
      '<div style="font-size:12px;color:#b7c8e1;margin-bottom:16px;">' + totalsLine + "</div>",
      renderScoutTier("MUST READ", byTier.must_read, "#4ade80", false),
      renderScoutTier("MAYBE", byTier.maybe, "#ffeb99", false),
      renderScoutTier("DECLINED", byTier.declined, "#f87171", true),
      '<div style="font-size:10px;color:#5a6678;margin-top:8px;text-align:right;">dev path — pipeline/cli/tilth_scout_ui.py</div>',
    ].join("");

    const rescanBtn = panel.querySelector("#gq-live-scout-rescan");
    if (rescanBtn) {
      rescanBtn.addEventListener("click", () => {
        rescanBtn.disabled = true;
        rescanBtn.textContent = "SCANNING…";
        rescanBtn.style.opacity = "0.6";
        runScoutRescan("Live panel rescan");
      });
    }

    document.body.insertBefore(panel, document.body.firstChild);
  }
})();
