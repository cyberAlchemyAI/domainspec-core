/* ============================================================
   Tilth Demo v0 — frontend
   - Hash routing across the seven screens
   - Home org cards populated from /api/orgs
   - Scout Activity drawer with live SSE streaming
   - Pipeline table re-renders from /api/orgs/{slug}/scout_results
   ============================================================ */

(function () {
  const screens = document.querySelectorAll('section.screen');
  const navItems = document.querySelectorAll('.nav-item[data-route]');

  function setActive(route) {
    let matched = false;
    screens.forEach((s) => {
      const isMatch = s.dataset.screen === route;
      s.classList.toggle('hidden', !isMatch);
      if (isMatch) matched = true;
    });
    navItems.forEach((n) => { n.classList.toggle('active', n.dataset.route === route); });
    if (!matched) {
      document.querySelector('section.screen[data-screen="home"]')?.classList.remove('hidden');
      document.querySelector('.nav-item[data-route="home"]')?.classList.add('active');
    }
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  function routeFromHash() {
    const h = (location.hash || '#/home').replace(/^#\/?/, '');
    return h.split('/')[0] || 'home';
  }

  window.addEventListener('hashchange', () => setActive(routeFromHash()));
  setActive(routeFromHash());

  function escapeHtml(s) {
    return String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]));
  }

  // ============================================================
  // Home — load org cards from /api/orgs
  // ============================================================
  async function loadOrgCards() {
    const grid = document.getElementById('orgCards');
    if (!grid) return;
    try {
      const r = await fetch('/api/orgs');
      const orgs = await r.json();
      grid.innerHTML = orgs.map(orgCardHtml).join('');
      grid.querySelectorAll('.org-card').forEach((card) => {
        card.addEventListener('click', () => { location.hash = '#/vault'; });
      });
    } catch (err) {
      grid.innerHTML = `<div class="card"><p class="text-muted">Could not load orgs: ${escapeHtml(String(err))}</p></div>`;
    }
  }

  function orgCardHtml(o) {
    const initials = (o.name || '?').split(/\s+/).map((w) => w[0]).slice(0, 2).join('').toUpperCase();
    const liveBadge = o.is_live ? '<span class="live-dot">Live · on-disk</span>' : '<span class="demo-tag">Demo fixture</span>';
    return `
      <article class="org-card ${o.is_live ? 'live' : ''}">
        <div class="org-card-head">
          <div class="org-icon">${escapeHtml(initials)}</div>
          <div class="org-card-name">
            <h3>${escapeHtml(o.name || '')}</h3>
            <div class="org-cic">${escapeHtml(o.cic || '')}</div>
          </div>
        </div>
        <p class="org-tagline">${escapeHtml(o.tagline || '')}</p>
        <div class="org-stats">
          <div class="org-stat"><span class="v">${escapeHtml(o.prior_grants?.total_awards_last_5yr || '—')}</span><span class="l">5-yr awards</span></div>
          <div class="org-stat"><span class="v">${o.prior_grants?.success_rate_pct ?? '—'}%</span><span class="l">success</span></div>
          <div class="org-stat"><span class="v">${o.active_opportunities_count ?? 0}</span><span class="l">active opps</span></div>
          <div class="org-stat"><span class="v">${o.document_inventory_count ?? 0}</span><span class="l">documents</span></div>
        </div>
        <div class="org-card-footer">${liveBadge}<span class="card-link">Open workspace →</span></div>
      </article>
    `;
  }
  loadOrgCards();

  // ============================================================
  // Sidebar collapse
  // ============================================================
  document.getElementById('sidebarCollapse')?.addEventListener('click', () => {
    document.getElementById('sidebar')?.classList.toggle('collapsed');
  });

  // ============================================================
  // Scout Activity drawer
  // ============================================================
  const drawer = document.getElementById('scoutDrawer');
  const scrim = document.getElementById('drawerScrim');
  const closeBtn = document.getElementById('scoutDrawerClose');
  const dismissBtn = document.getElementById('scoutDismissBtn');
  const refreshBtn = document.getElementById('scoutRefreshBtn');
  const statusDot = document.querySelector('#scoutStatus .status-dot');
  const statusLabel = document.getElementById('scoutStatusLabel');
  const cmdPre = document.getElementById('scoutCmd');
  const sessionEl = document.getElementById('scoutSession');
  const log = document.getElementById('scoutLog');
  const logCount = document.getElementById('scoutLogCount');
  const resultSection = document.getElementById('scoutResultSection');
  const resultBody = document.getElementById('scoutResultBody');
  const resultMeta = document.getElementById('scoutResultMeta');

  let logEvents = 0;

  function openDrawer() {
    drawer?.classList.add('open');
    drawer?.setAttribute('aria-hidden', 'false');
    scrim?.classList.add('open');
  }
  function closeDrawer() {
    drawer?.classList.remove('open');
    drawer?.setAttribute('aria-hidden', 'true');
    scrim?.classList.remove('open');
  }
  closeBtn?.addEventListener('click', closeDrawer);
  dismissBtn?.addEventListener('click', closeDrawer);
  scrim?.addEventListener('click', closeDrawer);

  function setStatus(state, label) {
    if (!statusDot) return;
    statusDot.classList.remove('pending', 'running', 'done', 'error');
    statusDot.classList.add(state);
    if (statusLabel) statusLabel.textContent = label;
  }

  function resetDrawer() {
    setStatus('pending', 'Preparing dispatch...');
    if (cmdPre) cmdPre.textContent = 'awaiting dispatch...';
    if (sessionEl) sessionEl.textContent = '—';
    if (log) log.innerHTML = '';
    logEvents = 0;
    if (logCount) logCount.textContent = '0 events';
    if (resultSection) resultSection.hidden = true;
    if (resultBody) resultBody.textContent = '';
    if (resultMeta) resultMeta.innerHTML = '';
    if (refreshBtn) refreshBtn.disabled = true;
  }

  function appendLog(kind, text) {
    if (!log) return;
    logEvents += 1;
    if (logCount) logCount.textContent = `${logEvents} event${logEvents === 1 ? '' : 's'}`;
    const div = document.createElement('div');
    div.className = `log-line kind-${kind}`;
    div.textContent = text;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
  }

  // ============================================================
  // Scout run — fires through /api/agents/scout/run
  // ============================================================
  const SCOUT_PROMPT = [
    "Run a verified Scout discovery pass for the FIT Farms client. Read",
    "orgs/fit_farms/PROJECT_CONTEXT.md to ground org context, then surface",
    "current funding opportunities across the three FIT Farms sector axes:",
    "food_systems, education, and research.",
    "",
    "Use live federal channels (Grants.gov, SAM.gov, USASpending) and curated",
    "state/foundation channels in parallel per Scout discipline. Verify each",
    "candidate against a live synopsis before elevating to CRITICAL fit. Cap",
    "output at 20 verified rows.",
    "",
    "Write two output artifacts to orgs/fit_farms/grants/ (create the folder",
    "if it does not exist):",
    "",
    "  1. scout_pass.json — a JSON array of opportunity rows. Each row must",
    "     include these keys: funder, program, status (Open|Rolling|",
    "     Anticipated|Closed), deadline, ask_range, eligibility, fit_score",
    "     (0-100 integer), verification (VERIFIED_LIVE|RECENT_CACHED|",
    "     FROM_TRAINING_ONLY), dimension (food_systems|education|research|",
    "     cross-cutting), url.",
    "",
    "  2. Funders_Master.xlsx — the same rows as a spreadsheet. (If xlsx",
    "     generation is not available in this turn, write a placeholder",
    "     CSV at Funders_Master.csv instead.)",
    "",
    "End your reply with a single-line summary of how many verified rows",
    "were written and which sector axis was strongest.",
  ].join("\n");

  async function runScout() {
    resetDrawer();
    openDrawer();
    setStatus('running', 'Dispatching Scout via OpenClaw...');
    appendLog('info', `[ui] firing Scout against FIT Farms — three-axis pass`);

    try {
      const resp = await fetch('/api/agents/scout/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: SCOUT_PROMPT }),
      });
      if (!resp.ok || !resp.body) {
        const errText = await resp.text().catch(() => '');
        appendLog('error', `[ui] dispatch HTTP ${resp.status} — ${errText}`);
        setStatus('error', `Dispatch failed (HTTP ${resp.status})`);
        return;
      }

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buf = '';
      let okExit = false;

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        // Parse SSE blocks separated by \n\n
        let idx;
        while ((idx = buf.indexOf('\n\n')) >= 0) {
          const raw = buf.slice(0, idx);
          buf = buf.slice(idx + 2);
          const event = parseSseBlock(raw);
          if (!event) continue;
          handleScoutEvent(event);
          if (event.event === 'done') okExit = !!event.data.ok;
        }
      }

      if (okExit) {
        setStatus('done', 'Scout run complete.');
        if (refreshBtn) refreshBtn.disabled = false;
      } else {
        setStatus('error', 'Scout exited with non-zero code.');
      }
    } catch (err) {
      console.error(err);
      appendLog('error', `[ui] network error: ${String(err)}`);
      setStatus('error', `Network error: ${String(err)}`);
    }
  }

  function parseSseBlock(raw) {
    const lines = raw.split('\n');
    let event = null;
    const dataLines = [];
    for (const line of lines) {
      if (line.startsWith('event:')) event = line.slice(6).trim();
      else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim());
    }
    if (!event) return null;
    let data = {};
    try { data = JSON.parse(dataLines.join('\n')); } catch { data = { _raw: dataLines.join('\n') }; }
    return { event, data };
  }

  function handleScoutEvent(evt) {
    const { event, data } = evt;
    if (event === 'start') {
      if (data.session_id && sessionEl) sessionEl.textContent = data.session_id;
      if (data.cmd && cmdPre) cmdPre.textContent = data.cmd;
      if (data.session_id) appendLog('session', `[session] ${data.session_id}`);
      setStatus('running', 'Scout running — waiting on agent...');
    } else if (event === 'stdout') {
      const t = (data.text || '').replace(/\n$/, '');
      if (t) appendLog('stdout', t);
    } else if (event === 'result') {
      const text = (data.text || '').trim();
      if (text && resultSection && resultBody) {
        resultSection.hidden = false;
        resultBody.textContent = text;
      }
      if (data.meta && resultMeta) {
        const meta = data.meta || {};
        const agentMeta = meta.agentMeta || {};
        const parts = [];
        if (agentMeta.model) parts.push(`model: ${agentMeta.model}`);
        if (agentMeta.provider) parts.push(`provider: ${agentMeta.provider}`);
        if (meta.durationMs) parts.push(`${(meta.durationMs / 1000).toFixed(1)}s`);
        if (agentMeta.usage?.total) parts.push(`${agentMeta.usage.total.toLocaleString()} tokens`);
        resultMeta.innerHTML = parts.map((p) => `<span>${escapeHtml(p)}</span>`).join('');
      }
      appendLog('done', `[result] received agent reply`);
    } else if (event === 'error') {
      appendLog('error', `[error] ${data.text || 'unknown'}`);
    } else if (event === 'done') {
      appendLog('done', `[done] exit=${data.exit_code ?? '?'} ok=${data.ok ? 'true' : 'false'}`);
    }
  }

  document.getElementById('runScoutBtn')?.addEventListener('click', runScout);

  // ============================================================
  // Refresh Pipeline button — re-render table from scout_results
  // ============================================================
  async function refreshPipelineFromDisk() {
    try {
      const r = await fetch('/api/orgs/fit_farms/scout_results');
      const data = await r.json();
      const rows = data.rows || [];
      if (!rows.length) {
        appendLog('info', '[refresh] no scout_pass.json yet on disk (Scout may not have written it).');
        return;
      }
      const tbody = document.getElementById('pipelineRows');
      if (!tbody) return;
      tbody.innerHTML = rows.map(renderPipelineRow).join('');
      tbody.querySelectorAll('tr').forEach((tr, i) => {
        setTimeout(() => tr.classList.add('row-arrived'), i * 60);
      });
      appendLog('done', `[refresh] rendered ${rows.length} rows from scout_pass.json`);
    } catch (err) {
      appendLog('error', `[refresh] ${String(err)}`);
    }
  }
  refreshBtn?.addEventListener('click', refreshPipelineFromDisk);

  function renderPipelineRow(row, i) {
    const num = i + 1;
    const status = (row.status || '').toLowerCase();
    let statusPill = `<span class="pill">${escapeHtml(row.status || '—')}</span>`;
    if (status.includes('open')) statusPill = `<span class="pill pill-ok">${escapeHtml(row.status)}</span>`;
    else if (status.includes('roll')) statusPill = `<span class="pill pill-warn">${escapeHtml(row.status)}</span>`;
    else if (status.includes('antic')) statusPill = `<span class="pill">${escapeHtml(row.status)}</span>`;
    else if (status.includes('closed')) statusPill = `<span class="pill pill-bad">${escapeHtml(row.status)}</span>`;

    const elig = (row.eligibility || '').toLowerCase();
    let eligPill = `<span class="pill">${escapeHtml(row.eligibility || '—')}</span>`;
    if (elig.includes('elig')) eligPill = `<span class="pill pill-ok">${escapeHtml(row.eligibility)}</span>`;
    else if (elig.includes('likely')) eligPill = `<span class="pill pill-warn">${escapeHtml(row.eligibility)}</span>`;
    else if (elig.includes('pending')) eligPill = `<span class="pill pill-warn">${escapeHtml(row.eligibility)}</span>`;

    const fit = typeof row.fit_score === 'number' ? row.fit_score : '—';
    const verif = row.verification ? String(row.verification).toLowerCase().replace(/_/g, ' ') : '—';

    return `
      <tr>
        <td>${num}</td>
        <td>${escapeHtml(row.funder || '')}</td>
        <td>${escapeHtml(row.program || '')}</td>
        <td>${statusPill}</td>
        <td>${escapeHtml(row.deadline || '—')}</td>
        <td>${escapeHtml(row.ask_range || '—')}</td>
        <td>${eligPill}</td>
        <td class="num"><strong>${fit}</strong></td>
        <td class="muted">${escapeHtml(verif)}</td>
      </tr>
    `;
  }

  // ============================================================
  // File-event SSE — animate rows when files land on disk
  // ============================================================
  function subscribeFileEvents(slug) {
    if (!window.EventSource) return null;
    const es = new EventSource(`/api/events/files/${encodeURIComponent(slug)}`);
    es.addEventListener('file', (e) => {
      let evt;
      try { evt = JSON.parse(e.data); } catch { return; }
      console.log('[file]', evt);
      appendLog('info', `[disk] ${evt.type} ${evt.path}`);
      // If scout_pass.json just landed, auto-refresh pipeline after a beat.
      if (typeof evt.path === 'string' && evt.path.endsWith('scout_pass.json') && evt.type === 'created') {
        setTimeout(refreshPipelineFromDisk, 600);
      }
    });
    es.onerror = () => { /* browser auto-reconnects */ };
    return es;
  }
  subscribeFileEvents('fit_farms');

})();
