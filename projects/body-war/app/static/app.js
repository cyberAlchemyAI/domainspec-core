const state = {
  activities: [],
  profile: null,
  status: null,
  tracks: [],
};

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

function trackStatus(track) {
  if (track.pilot === "body-war") return "Geometria pendente";
  return "Metrica de controle";
}

async function loadTracks() {
  const data = await getJson("/api/tracks");
  state.tracks = data.tracks || [];
  const container = $("#tracks");
  clear(container);
  if (!state.tracks.length) {
    container.append(message("Nenhuma pista piloto configurada."));
    return;
  }
  for (const track of state.tracks) {
    const article = el("article", {
      className: "track",
      attrs: { "data-pilot": track.pilot || "unknown" },
    });
    article.append(el("p", { className: "tag", text: track.pilot || "pilot" }));
    article.append(el("h3", { text: track.name || track.id }));
    article.append(el("p", { text: track.description || "Sem descricao disponivel." }));
    article.append(el("span", { className: "status-chip pending", odId: "track.geometry-status", text: trackStatus(track) }));
    article.append(el("p", { text: `Metrica de controle: ${track.controller_metric || "nao selecionada"}` }));
    container.append(article);
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

    const select = el("select", { attrs: { "aria-label": "Pista piloto" } });
    for (const track of state.tracks) {
      select.append(el("option", { text: track.name || track.id, attrs: { value: track.id } }));
    }

    const actions = el("div");
    const button = el("button", {
      className: "button",
      odId: "evidence.submit.cta",
      text: "Enviar preview",
      attrs: { type: "button" },
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
  await postJson("/api/submissions", {
    track_id: trackId,
    activity_id: activity.id,
    activity_name: activity.name,
    moving_time: activity.moving_time,
    distance: activity.distance,
    average_speed: activity.average_speed,
  });
  await loadSubmissions();
}

async function loadSubmissions() {
  const container = $("#submissions");
  clear(container);
  const data = await getJson("/api/submissions");
  const submissions = data.submissions || [];
  if (!submissions.length) {
    container.append(message("Nenhuma evidencia de preview enviada ainda."));
    return;
  }
  for (const item of submissions.slice().reverse()) {
    const article = el("article", { className: "submission" });
    article.append(el("span", {
      className: "status-chip preview",
      odId: "evidence.status-chip",
      text: `${item.status === "submitted" ? "enviado" : item.status || "enviado"} - ${item.authority || "preview"}`,
    }));
    article.append(el("h3", { text: item.activity_name || item.activity_id || "Atividade" }));
    article.append(el("p", { text: `${item.athlete_name || item.athlete_id || "Corredor"} enviou para ${item.track_id || "pista"}` }));
    article.append(el("p", { text: `${fmtDistance(item.distance)} - ${fmtTime(item.moving_time)}` }));
    container.append(article);
  }
}

async function renderConnected() {
  await loadProfile();
  await loadTracks();
  await loadActivities();
  await loadSubmissions();
}

async function boot() {
  renderQueryNotices();
  $("#refresh").addEventListener("click", loadActivities);
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
