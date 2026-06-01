// Cloudflare Pages Function — handles POST /api/submit from the interest form.
//
// Three delivery paths run in sequence; any one of them succeeding counts as success
// and the submission is preserved. If all three fail, the client falls back to mailto.
//
//   1. Console log         (always — visible in Cloudflare Pages Functions logs)
//   2. KV namespace        (if `SUBMISSIONS` binding is set on the Pages project)
//   3. Email via Resend    (if `RESEND_API_KEY` env var is set on the Pages project)
//
// Configure on Cloudflare:
//   Pages → Settings → Environment variables → add RESEND_API_KEY (production)
//   Pages → Settings → Functions → KV namespace bindings → bind `SUBMISSIONS` (optional)
//
// Resend signup: https://resend.com (free tier = 3,000 emails/month, no card)
// After signup: verify yourgoldenquill.com domain, drop the API key into Pages env.

export async function onRequestPost(context) {
  const { request, env } = context;
  let payload;

  try {
    const fd = await request.formData();
    payload = normalize(fd);
  } catch (e) {
    return json({ ok: false, error: "bad_form" }, 400);
  }

  // Honeypot — silently accept and discard bot submissions
  if (payload.company_url) {
    return json({ ok: true, discarded: true });
  }

  // Required fields
  if (!payload.name || !payload.email || !payload.organization) {
    return json({ ok: false, error: "missing_required" }, 400);
  }

  // 1. Always log (Pages → Functions → Logs)
  console.log("INTEREST_SUBMISSION", JSON.stringify(payload));

  // 2. KV write (optional — bind a namespace named SUBMISSIONS)
  if (env.SUBMISSIONS) {
    try {
      const key = `${payload.received_at}_${payload.email}`;
      await env.SUBMISSIONS.put(key, JSON.stringify(payload), {
        metadata: { email: payload.email, organization: payload.organization }
      });
    } catch (err) {
      console.error("KV_WRITE_FAILED", String(err));
    }
  }

  // 3. Email via Resend (optional — set RESEND_API_KEY env var)
  if (env.RESEND_API_KEY) {
    try {
      const subject = `Golden Quill interest — ${payload.organization}`;
      const body = formatEmailBody(payload);
      const res = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${env.RESEND_API_KEY}`
        },
        body: JSON.stringify({
          from: "Golden Quill <noreply@yourgoldenquill.com>",
          to: ["tilth@yourgoldenquill.com"],
          reply_to: payload.email,
          subject,
          text: body
        })
      });
      if (!res.ok) {
        const errText = await res.text();
        console.error("RESEND_FAILED", res.status, errText);
      }
    } catch (err) {
      console.error("RESEND_EXCEPTION", String(err));
    }
  }

  return json({ ok: true });
}

// --- helpers ---

function normalize(fd) {
  const get = (k) => (fd.get(k) || "").toString().trim();
  return {
    received_at: new Date().toISOString(),
    name: get("name"),
    email: get("email"),
    organization: get("organization"),
    role: get("role"),
    scale: get("scale"),
    timeline: get("timeline"),
    notes: get("notes"),
    market: fd.getAll("market").map(String),
    company_url: get("company_url"),
    user_agent: fd.get("user_agent") || ""
  };
}

function formatEmailBody(p) {
  const lines = [
    `Received: ${p.received_at}`,
    ``,
    `Name:         ${p.name}`,
    `Email:        ${p.email}`,
    `Organization: ${p.organization}`,
  ];
  if (p.market && p.market.length) lines.push(`Markets:      ${p.market.join(", ")}`);
  if (p.role) lines.push(`Role:         ${p.role}`);
  if (p.scale) lines.push(`Scale:        ${p.scale}`);
  if (p.timeline) lines.push(`Timeline:     ${p.timeline}`);
  if (p.notes) {
    lines.push(``, `Notes:`, p.notes);
  }
  return lines.join("\n");
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" }
  });
}

// Reject GET / other methods
export const onRequest = ({ request }) => {
  if (request.method === "POST") return onRequestPost.apply(null, arguments);
  return new Response("Method not allowed", { status: 405 });
};
