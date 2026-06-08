const state = {
  activities: [],
  tracks: [],
};

const $ = (selector) => document.querySelector(selector);

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

async function getJson(url) {
  const response = await fetch(url);
  const payload = await response.json();
  if (!response.ok)
    throw new Error(payload.message || payload.error || "Request failed");
  return payload;
}

async function postJson(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
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
  const card = $("#athlete-card");

  if (!status.configured) {
    copy.textContent = `Strava is not configured. Add .env credentials. Callback: ${status.redirect_uri}`;
    connect.classList.add("hidden");
    return status;
  }

  connect.classList.remove("hidden");

  if (!status.connected) {
    copy.textContent =
      "Connect Strava to load recent activities for pilot validation.";
    card.classList.add("hidden");
    return status;
  }

  const athlete = status.athlete || {};
  copy.textContent = `Connected with scope: ${athlete.scope || status.scope}`;
  card.classList.remove("hidden");
  card.innerHTML = `
    ${athlete.profile ? `<img src="${athlete.profile}" alt="" />` : ""}
    <div>
      <strong>${athlete.firstname || "Connected"} ${athlete.lastname || ""}</strong>
      <p>Token expires at ${athlete.expires_at || "unknown"}</p>
    </div>
  `;
  return status;
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
  container.innerHTML = "<p>Loading recent activities...</p>";
  try {
    const data = await getJson("/api/activities?per_page=12");
    state.activities = (data.activities || []).filter((activity) =>
      ["Run", "TrailRun", "VirtualRun"].includes(
        activity.sport_type || activity.type,
      ),
    );
    renderActivities();
  } catch (error) {
    container.innerHTML = `<p>${error.message === "not_connected" ? "Connect Strava first." : error.message}</p>`;
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
      `${fmtDistance(activity.distance)} · ${fmtTime(activity.moving_time)} · ${pace(activity)}`;

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
          <p class="tag">${item.status} · ${item.authority}</p>
          <h3>${item.activity_name || item.activity_id}</h3>
          <p>${item.athlete_name || item.athlete_id} submitted to ${item.track_id}</p>
          <p>${fmtDistance(item.distance)} · ${fmtTime(item.moving_time)}</p>
        </article>
      `,
    )
    .join("");
}

async function boot() {
  $("#refresh").addEventListener("click", loadActivities);
  await loadStatus();
  await loadTracks();
  await loadActivities();
  await loadSubmissions();
}

boot().catch((error) => {
  $("#connection-copy").textContent = error.message;
});
