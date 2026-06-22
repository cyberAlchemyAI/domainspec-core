const state = {
  activities: [],
  profile: null,
  tracks: [],
};

const $ = (selector) => document.querySelector(selector);

function getCookie(name) {
  const prefix = `${name}=`;
  return document.cookie
    .split(";")
    .map((part) => part.trim())
    .find((part) => part.startsWith(prefix))
    ?.slice(prefix.length);
}

function fmtDistance(meters) {
  if (!Number.isFinite(Number(meters))) return "unknown distance";
  return `${(Number(meters) / 1000).toFixed(2)} km`;
}

function fmtTime(seconds) {
  const total = Number(seconds);
  if (!Number.isFinite(total)) return "unknown time";
  const minutes = Math.floor(total / 60);
  const secs = total % 60;
  return `${minutes}:${String(secs).padStart(2, "0")}`;
}

function pace(activity) {
  const meters = Number(activity.distance || 0);
  const seconds = Number(activity.moving_time || 0);
  if (!meters || !seconds) return "pace unavailable";
  return `${(seconds / 60 / (meters / 1000)).toFixed(2)} min/km`;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;",
  })[char]);
}

function safeHttpUrl(value) {
  try {
    const url = new URL(String(value ?? ""));
    return ["http:", "https:"].includes(url.protocol) ? url.toString() : "";
  } catch {
    return "";
  }
}

async function getJson(url) {
  const response = await fetch(url);
  const payload = await response.json();
  if (!response.ok)
    throw new Error(payload.message || payload.error || "Request failed");
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
  if (!response.ok)
    throw new Error(payload.message || payload.error || "Request failed");
  return payload;
}

async function loadStatus() {
  const status = await getJson("/api/status");
  const copy = $("#connection-copy");
  const connect = $("#connect");
  const logout = $("#logout");
  const profileLink = $("#profile-link");
  const card = $("#athlete-card");

  if (!status.configured) {
    copy.textContent = `Strava is not configured. Add .env credentials. Callback: ${status.redirect_uri}`;
    connect.classList.add("hidden");
    logout.classList.add("hidden");
    return status;
  }

  connect.classList.toggle("hidden", status.connected);
  logout.classList.toggle("hidden", !status.authenticated);
  profileLink.classList.toggle("hidden", !status.authenticated);

  if (!status.connected) {
    copy.textContent =
      "Connect Strava to load recent activities for pilot validation.";
    card.classList.add("hidden");
    return status;
  }

  const athlete = status.athlete || {};
  copy.textContent = `Connected with scope: ${athlete.scope || status.scope}`;
  card.classList.remove("hidden");
  const imageUrl = safeHttpUrl(athlete.profile);
  const stravaUrl = safeHttpUrl(athlete.strava_profile_url);
  card.innerHTML = `
    ${imageUrl ? `<img src="${escapeHtml(imageUrl)}" alt="" />` : ""}
    <div>
      <strong>${escapeHtml(athlete.firstname || "Connected")} ${escapeHtml(athlete.lastname || "")}</strong>
      ${stravaUrl ? `<p><a data-od-id="profile.strava-link" href="${escapeHtml(stravaUrl)}" rel="noreferrer" target="_blank">Open public Strava profile</a></p>` : ""}
    </div>
  `;
  return status;
}

async function loadProfile() {
  const copy = $("#profile-copy");
  const card = $("#profile-card");
  try {
    const data = await getJson("/api/profile");
    const profile = data.profile;
    state.profile = profile;
    const strava = profile.strava || {};
    const account = strava.account || {};
    const stravaUrl = safeHttpUrl(strava.profile_url);
    copy.textContent = `${profile.display_name || profile.principal_id}`;
    card.innerHTML = `
      <article class="profile-item">
        <p class="tag">Runner</p>
        <h3>${escapeHtml(profile.display_name || profile.principal_id)}</h3>
        <p>${escapeHtml(profile.principal_id)}</p>
      </article>
      <article class="profile-item">
        <p class="tag">${strava.connected ? "Strava connected" : "Strava disconnected"}</p>
        <h3>${escapeHtml(account.provider || "strava")}</h3>
        <p>${escapeHtml(account.scope || "scope unavailable")}</p>
        ${stravaUrl ? `<a data-od-id="profile.strava-link" href="${escapeHtml(stravaUrl)}" rel="noreferrer" target="_blank">Open public Strava profile</a>` : ""}
      </article>
      <article class="profile-item">
        <p class="tag">Privacy</p>
        <h3>Server-owned session</h3>
        <p>Tokens stay server-side and never render in this page. Activity summaries stay redacted.</p>
      </article>
      <article class="profile-item">
        <p class="tag">Validation</p>
        <h3>Taquaral pending</h3>
        <p>Consent and route geometry remain separate checks.</p>
      </article>
    `;
  } catch (error) {
    state.profile = null;
    copy.textContent = isAuthRequired(error.message)
      ? "Connect Strava to create a runner profile."
      : error.message;
    card.innerHTML = "";
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

async function loadTracks() {
  const data = await getJson("/api/tracks");
  state.tracks = data.tracks || [];
  $("#tracks").innerHTML = state.tracks
    .map(
      (track) => `
        <article class="track" data-pilot="${track.pilot}">
          <p class="tag">${track.pilot}</p>
          <h3>${track.name}</h3>
          <p>${track.description}</p>
          <p><strong>Controller metric:</strong> ${track.controller_metric}</p>
        </article>
      `,
    )
    .join("");
}

async function loadActivities() {
  const container = $("#activities");
  const copy = $("#activity-copy");
  container.innerHTML = "<p>Loading recent activities...</p>";
  try {
    const data = await getJson("/api/activities?per_page=12");
    if (data.receipt) {
      copy.textContent =
        `${data.receipt.summary_count || 0} summaries imported. Route geometry and scoring are explicitly separate from this preview.`;
    }
    state.activities = (data.activities || []).filter((activity) =>
      ["Run", "TrailRun", "VirtualRun"].includes(
        activity.sport_type || activity.type,
      ),
    );
    renderActivities();
  } catch (error) {
    copy.textContent = "Connect Strava before importing redacted activity summaries.";
    container.innerHTML = `<p>${error.message === "not_connected" || isAuthRequired(error.message) ? "Connect Strava first." : error.message}</p>`;
  }
}

function renderActivities() {
  const container = $("#activities");
  const template = $("#activity-template");
  container.innerHTML = "";

  if (!state.activities.length) {
    container.innerHTML = "<p>No recent runs found from Strava.</p>";
    return;
  }

  for (const activity of state.activities) {
    const node = template.content.cloneNode(true);
    node.querySelector("[data-name]").textContent =
      activity.name || `Activity ${activity.id}`;
    node.querySelector("[data-meta]").textContent =
      `${fmtDistance(activity.distance)} - ${fmtTime(activity.moving_time)} - ${pace(activity)}`;

    const select = node.querySelector("[data-track]");
    for (const track of state.tracks) {
      const option = document.createElement("option");
      option.value = track.id;
      option.textContent = track.name;
      select.appendChild(option);
    }

    node.querySelector("[data-submit]").addEventListener("click", async () => {
      await submitActivity(activity, select.value);
    });

    container.appendChild(node);
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
  const data = await getJson("/api/submissions");
  const submissions = data.submissions || [];
  if (!submissions.length) {
    container.innerHTML = "<p>No submissions yet.</p>";
    return;
  }
  container.innerHTML = submissions
    .slice()
    .reverse()
    .map(
      (item) => `
        <article class="submission">
          <p class="tag">${item.status} - ${item.authority}</p>
          <h3>${item.activity_name || item.activity_id}</h3>
          <p>${item.athlete_name || item.athlete_id} submitted to ${item.track_id}</p>
          <p>${fmtDistance(item.distance)} - ${fmtTime(item.moving_time)}</p>
        </article>
      `,
    )
    .join("");
}

async function boot() {
  $("#refresh").addEventListener("click", loadActivities);
  $("#logout").addEventListener("click", async () => {
    await postJson("/api/auth/logout", {});
    window.location.href = "/";
  });
  await loadStatus();
  await loadProfile();
  await loadTracks();
  await loadActivities();
  await loadSubmissions();
}

boot().catch((error) => {
  $("#connection-copy").textContent = error.message;
});
