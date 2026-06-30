const state = {
  activities: [],
  evidenceCandidates: [],
  profile: null,
  status: null,
  suggestedTracks: [],
};

const EVIDENCE_CONSENT_TEXT =
  "Autorizo o TROQAR a guardar somente o resumo redigido desta atividade como candidata de evidencia para a rota sugerida.";

const $ = (selector, root = document) => root.querySelector(selector);

function getCookie(name) {
  const prefix = `${name}=`;
  return document.cookie
    .split(";")
    .map((part) => part.trim())
    .find((part) => part.startsWith(prefix))
    ?.slice(prefix.length);
}

function clear(node) {
  node.replaceChildren();
}

function setHidden(node, hidden) {
  node.classList.toggle("hidden", hidden);
}

function el(tag, options = {}, children = []) {
  const node = document.createElement(tag);
  if (options.className) node.className = options.className;
  if (options.text !== undefined) node.textContent = String(options.text);
  if (options.odId) node.dataset.odId = options.odId;
  if (options.attrs) {
    for (const [name, value] of Object.entries(options.attrs)) {
      if (value !== undefined && value !== null && value !== "") {
        node.setAttribute(name, String(value));
      }
    }
  }
  for (const child of children) node.append(child);
  return node;
}

function message(text, options = {}) {
  return el("p", {
    className: `state-message${options.error ? " error" : ""}`,
    odId: options.odId,
    text,
  });
}

function fmtDistance(meters) {
  if (!Number.isFinite(Number(meters))) return "distancia indisponivel";
  return `${(Number(meters) / 1000).toFixed(2)} km`;
}

function fmtTime(seconds) {
  const total = Number(seconds);
  if (!Number.isFinite(total)) return "tempo indisponivel";
  const minutes = Math.floor(total / 60);
  const secs = total % 60;
  return `${minutes}:${String(secs).padStart(2, "0")}`;
}

function pace(activity) {
  const meters = Number(activity.distance || 0);
  const seconds = Number(activity.moving_time || 0);
  if (!meters || !seconds) return "ritmo indisponivel";
  return `${(seconds / 60 / (meters / 1000)).toFixed(2)} min/km`;
}

function safeHttpUrl(value) {
  try {
    const url = new URL(String(value ?? ""));
    return ["http:", "https:"].includes(url.protocol) ? url.toString() : "";
  } catch {
    return "";
  }
}

function isAuthRequired(message) {
  return [
    "Session cookie is required",
    "Missing bearer token",
    "auth_required",
    "invalid_session",
  ].includes(String(message));
}

function uiErrorMessage(message) {
  const raw = String(message ?? "");
  if (isAuthRequired(raw) || raw === "not_connected") return "Conecte o Strava para continuar.";
  if (raw === "csrf_required") return "Atualize a pagina e tente novamente.";
  if (raw === "invalid_activity") return "Este treino nao pode ser enviado para a pista selecionada.";
  if (raw === "invalid_suggested_track") return "Preencha nome, lugar, cidade e uma distancia positiva quando informada.";
  if (raw === "consent_required") return "Confirme o consentimento antes de enviar a candidata.";
  if (raw === "suggested_track_not_found") return "Esta rota sugerida nao esta mais disponivel.";
  if (raw === "track_geometry_missing") return "Geometria da rota ainda nao foi confirmada para esta evidencia.";
  if (raw === "access_denied") return "Nao foi possivel conectar com Strava. Tente de novo quando quiser.";
  if (raw === "invalid_state") return "A sessao de login do Strava expirou. Comece de novo.";
  return raw || "Nao foi possivel concluir. Tente de novo.";
}

async function getJson(url) {
  const response = await fetch(url);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || payload.message || "Request failed");
  }
  return payload;
}

async function postJson(url, body) {
  const csrf = getCookie("bw_csrf");
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(csrf ? { "X-CSRF-Token": csrf } : {}),
    },
    body: JSON.stringify(body),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || payload.message || "Request failed");
  }
  return payload;
}

function renderQueryNotices() {
  const params = new URLSearchParams(window.location.search);
  const callback = $("#callback-status");
  const error = $("#auth-error");
  const errorCopy = $("#auth-error-copy");
  const connected = params.get("connected");
  const authError = params.get("auth_error");

  setHidden(callback, true);
  setHidden(error, true);
  callback.textContent = "";
  errorCopy.textContent = "";

  if (connected === "1") {
    callback.textContent = "Strava conectado. Perfil publico e resumos seguros estao prontos.";
    setHidden(callback, false);
  }

  if (authError) {
    errorCopy.textContent = uiErrorMessage(authError);
    setHidden(error, false);
  }
}

function renderShell(status) {
  const anonymous = !(status.authenticated && status.connected);
  setHidden($("#auth-login"), !anonymous);
  setHidden($("#runner-home"), anonymous);
  setHidden($("#connect"), !anonymous || !status.configured);
  setHidden($("#connect-top"), true);
  setHidden($("#logout"), anonymous);
  setHidden($("#profile-link"), anonymous);

  if (!status.configured) {
    $("#connection-copy").textContent = `Strava ainda nao esta configurado. Callback: ${status.redirect_uri}`;
  } else if (anonymous) {
    $("#connection-copy").textContent = "Login unico do MVP: Strava. Sem senha, sem outro provedor.";
  }
}

function renderAthlete(status) {
  const copy = $("#connected-copy");
  const card = $("#athlete-card");
  const athlete = status.athlete || {};
  const imageUrl = safeHttpUrl(athlete.profile);
  const stravaUrl = safeHttpUrl(athlete.strava_profile_url);

  copy.textContent = `Conectado com escopo: ${athlete.scope || status.scope || "activity:read"}.`;
  clear(card);

  if (imageUrl) {
    card.append(el("img", { attrs: { src: imageUrl, alt: "" } }));
  }
  const details = el("div");
  details.append(el("strong", { text: `${athlete.firstname || "Corredor conectado"} ${athlete.lastname || ""}`.trim() }));
  if (stravaUrl) {
    details.append(
      el("p", {}, [
        el("a", {
          odId: "profile.strava-link",
          text: "Open public Strava profile",
          attrs: { href: stravaUrl, rel: "noreferrer", target: "_blank" },
        }),
      ]),
    );
  }
  card.append(details);
  setHidden(card, false);
}

async function loadStatus() {
  const status = await getJson("/api/status");
  state.status = status;
  renderShell(status);
  if (status.authenticated && status.connected) renderAthlete(status);
  return status;
}

function profileItem(tag, title, copy, link, options = {}) {
  const article = el("article", { className: "profile-item", odId: options.odId });
  article.append(el("p", { className: "tag", text: tag }));
  article.append(el("h3", { text: title }));
  article.append(el("p", { text: copy }));
  if (link) article.append(link);
  return article;
}

async function loadProfile() {
  const copy = $("#profile-copy");
  const title = $("#profile-title");
  const card = $("#profile-card");
  clear(card);
  try {
    const data = await getJson("/api/profile");
    const profile = data.profile;
    state.profile = profile;
    const strava = profile.strava || {};
    const account = strava.account || {};
    const stravaUrl = safeHttpUrl(strava.profile_url);
    const displayName = profile.display_name || profile.principal_id || "Corredor";
    title.textContent = displayName;
    copy.textContent = "Credenciais ficam no servidor e nunca aparecem nesta pagina. Os treinos chegam como resumos seguros.";
    const profileLink = stravaUrl
      ? el("a", {
          odId: "profile.strava-link",
          text: "Open public Strava profile",
          attrs: { href: stravaUrl, rel: "noreferrer", target: "_blank" },
        })
      : null;
    card.append(
      profileItem("Corredor", displayName, profile.principal_id || "principal indisponivel"),
      profileItem(strava.connected ? "Strava conectado" : "Strava desconectado", account.provider || "strava", account.scope || "escopo indisponivel", profileLink),
      profileItem("Privacidade", "Sessao no servidor", "Credenciais do provedor e dados privados ficam fora do navegador.", null, { odId: "profile.privacy-card" }),
      profileItem("Validacao", "Autoridade de preview", "Geometria da rota e pontuacao seguem como checagens separadas ate existir evidencia do backend."),
    );
  } catch (error) {
    state.profile = null;
    copy.textContent = uiErrorMessage(error.message);
    card.append(message(uiErrorMessage(error.message), { error: !isAuthRequired(error.message) }));
  }
}

function suggestedTrackStatus(track) {
  const labels = {
    needs_evidence: "Precisa de evidencia",
    evidence_submitted: "Evidencia enviada",
    operator_review: "Em analise",
    source_backed: "Fonte confirmada",
    retired: "Retirada",
  };
  return labels[track.status] || "Precisa de evidencia";
}

function renderSuggestedTracks() {
  const container = $("#suggested-tracks");
  clear(container);
  if (!state.suggestedTracks.length) {
    container.append(message("Nenhuma rota sugerida ainda."));
    return;
  }
  for (const track of state.suggestedTracks) {
    const article = el("article", {
      className: "track",
      attrs: { "data-status": track.status || "needs_evidence" },
    });
    article.append(el("p", { className: "tag", text: track.place_label || track.city || "rota" }));
    article.append(el("h3", { text: track.name || track.id }));
    article.append(el("p", { text: track.public_note || "Aguardando uma candidata de atividade real." }));
    article.append(el("span", {
      className: `status-chip ${track.status === "source_backed" ? "" : "pending"}`,
      odId: "track.geometry-status",
      text: suggestedTrackStatus(track),
    }));
    article.append(el("p", {
      text: `${fmtDistance(track.distance_hint_meters)} - geometria: ${track.geometry_authority || "needs_evidence"}`,
    }));
    const help = el("button", {
      className: "button ghost",
      odId: "suggested-track.help.cta",
      text: "Tenho essa corrida",
      attrs: { type: "button" },
    });
    help.addEventListener("click", () => $("#activities")?.scrollIntoView({ behavior: "smooth", block: "start" }));
    article.append(help);
    container.append(article);
  }
}

async function loadSuggestedTracks() {
  const data = await getJson("/api/suggested-tracks");
  state.suggestedTracks = data.suggested_tracks || [];
  $("#suggested-track-copy").textContent =
    `${state.suggestedTracks.length} rotas sugeridas. Promocao por fonte e piloto seguem fora deste preview.`;
  renderSuggestedTracks();
}

async function createSuggestedTrack(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const error = $("#suggest-form-error");
  const button = form.querySelector("button[type='submit']");
  setHidden(error, true);
  error.textContent = "";
  button.disabled = true;
  try {
    const distance = $("#suggest-distance").value.trim();
    await postJson("/api/suggested-tracks", {
      name: $("#suggest-name").value,
      place_label: $("#suggest-place").value,
      city: $("#suggest-city").value,
      distance_hint_meters: distance ? Number(distance) : null,
      public_note: $("#suggest-note").value,
    });
    form.reset();
    $("#suggest-city").value = "Campinas";
    await loadSuggestedTracks();
    renderActivities();
    await loadSubmissions();
  } catch (createError) {
    error.textContent = uiErrorMessage(createError.message);
    setHidden(error, false);
  } finally {
    button.disabled = false;
  }
}

async function loadActivities() {
  const container = $("#activities");
  const copy = $("#activity-copy");
  clear(container);
  container.append(message("Carregando treinos recentes...", { odId: "activity.loading" }));
  try {
    const data = await getJson("/api/activities?per_page=12");
    if (data.receipt) {
      copy.textContent =
        `${data.receipt.summary_count || 0} resumos importados. Geometria da rota e pontuacao seguem separadas deste preview.`;
    }
    state.activities = (data.activities || []).filter((activity) =>
      ["Run", "TrailRun", "VirtualRun"].includes(activity.sport_type || activity.type),
    );
    renderActivities();
  } catch (error) {
    copy.textContent = "Conecte o Strava antes de importar resumos seguros dos treinos.";
    clear(container);
    container.append(message(uiErrorMessage(error.message), { error: true, odId: "activity.error" }));
  }
}

function renderActivities() {
  const container = $("#activities");
  clear(container);

  if (!state.activities.length) {
    container.append(message("Nenhuma corrida recente encontrada no Strava.", { odId: "activity.empty" }));
    return;
  }

  for (const activity of state.activities) {
    const article = el("article", { className: "activity" });
    const summary = el("div");
    summary.append(el("h3", { text: activity.name || `Activity ${activity.id}` }));
    summary.append(
      el("p", {
        className: "activity-meta",
        text: `${fmtDistance(activity.distance)} - ${fmtTime(activity.moving_time)} - ${pace(activity)}`,
      }),
    );

    const select = el("select", { attrs: { "aria-label": "Rota sugerida" } });
    for (const track of state.suggestedTracks) {
      select.append(el("option", { text: track.name || track.id, attrs: { value: track.id } }));
    }

    const actions = el("div");
    const button = el("button", {
      className: "button",
      odId: "evidence.submit.cta",
      text: "Enviar candidata",
      attrs: { type: "button", disabled: state.suggestedTracks.length ? null : "disabled" },
    });
    const error = el("p", { className: "submit-error hidden", odId: "evidence.submit.error" });
    button.addEventListener("click", async () => {
      setHidden(error, true);
      error.textContent = "";
      button.disabled = true;
      try {
        await submitActivity(activity, select.value);
      } catch (submitError) {
        error.textContent = uiErrorMessage(submitError.message);
        setHidden(error, false);
      } finally {
        button.disabled = false;
      }
    });
    actions.append(button, error);
    article.append(summary, select, actions);
    container.append(article);
  }
}

async function submitActivity(activity, trackId) {
  await postJson(`/api/suggested-tracks/${encodeURIComponent(trackId)}/evidence-candidates`, {
    activity_id: activity.id,
    consent_acknowledged: true,
    consent_text: EVIDENCE_CONSENT_TEXT,
  });
  await loadSuggestedTracks();
  await loadSubmissions();
}

async function loadSubmissions() {
  const container = $("#submissions");
  clear(container);
  if (!state.suggestedTracks.length) {
    container.append(message("Nenhuma rota sugerida para receber candidatas."));
    return;
  }
  const detailResults = await Promise.all(
    state.suggestedTracks.map((track) =>
      getJson(`/api/suggested-tracks/${encodeURIComponent(track.id)}`),
    ),
  );
  const candidates = detailResults.flatMap((detail) =>
    (detail.my_evidence_candidates || []).map((candidate) => ({
      ...candidate,
      suggested_track: detail.suggested_track,
    })),
  );
  state.evidenceCandidates = candidates;
  if (!candidates.length) {
    container.append(message("Nenhuma candidata enviada ainda."));
    return;
  }
  for (const item of candidates) {
    const summary = item.redacted_summary || {};
    const track = item.suggested_track || {};
    const article = el("article", { className: "submission" });
    article.append(el("span", {
      className: "status-chip preview",
      odId: "evidence.status-chip",
      text: `${item.status === "submitted" ? "enviado" : item.status || "enviado"} - candidato`,
    }));
    article.append(el("h3", { text: summary.name || item.provider_activity_id || "Atividade" }));
    article.append(el("p", { text: `Candidata para ${track.name || item.suggested_track_id}` }));
    article.append(el("p", { text: `${fmtDistance(summary.distance)} - ${fmtTime(summary.moving_time)}` }));
    container.append(article);
  }
}

async function renderConnected() {
  await loadProfile();
  await loadSuggestedTracks();
  await loadActivities();
  await loadSubmissions();
}

async function boot() {
  renderQueryNotices();
  $("#refresh").addEventListener("click", loadActivities);
  $("#suggest-track-form").addEventListener("submit", createSuggestedTrack);
  $("#logout").addEventListener("click", async () => {
    await postJson("/api/auth/logout", {});
    window.location.href = "/";
  });
  const status = await loadStatus();
  if (status.authenticated && status.connected) {
    await renderConnected();
  }
}

boot().catch((error) => {
  const copy = $("#connection-copy");
  if (copy) copy.textContent = uiErrorMessage(error.message);
});
