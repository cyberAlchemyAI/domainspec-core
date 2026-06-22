import type { CookieMap } from "./types.js";

export function parseCookieHeader(header: string | undefined): CookieMap {
  const cookies: CookieMap = {};
  if (!header) return cookies;

  for (const pair of header.split(";")) {
    const [rawName, ...rawValue] = pair.trim().split("=");
    const name = rawName?.trim();
    if (!name) continue;
    cookies[name] = decodeURIComponent(rawValue.join("="));
  }

  return cookies;
}

export type CookieOptions = {
  httpOnly?: boolean;
  secure?: boolean;
  sameSite?: "Lax" | "Strict" | "None";
  path?: string;
  maxAgeSeconds?: number;
};

export function cookieHeader(
  name: string,
  value: string,
  options: CookieOptions = {},
): string {
  const parts = [`${name}=${encodeURIComponent(value)}`];
  if (options.httpOnly) parts.push("HttpOnly");
  if (options.secure) parts.push("Secure");
  parts.push(`SameSite=${options.sameSite ?? "Lax"}`);
  parts.push(`Path=${options.path ?? "/"}`);
  if (options.maxAgeSeconds !== undefined) {
    parts.push(`Max-Age=${options.maxAgeSeconds}`);
  }
  return parts.join("; ");
}

export function clearCookieHeader(name: string): string {
  return cookieHeader(name, "", {
    httpOnly: true,
    sameSite: "Lax",
    path: "/",
    maxAgeSeconds: 0,
  });
}
