"""Citation-verify gate — fail-closed on hallucinated citations, soft-fail on
transient network errors.

Why two failure modes
---------------------
LLM-authored citations fail in two distinct ways:

1. Hallucination: the source does not exist. DOI doesn't resolve; URL returns
   404 or 410. This is a fail-closed condition — Scribe may not cite this
   source, ever.

2. Network transient: the source exists but we couldn't reach it this attempt.
   DNS glitch; rate-limited (429); 5xx; auth required (401/403) — a paywalled
   journal is still a real source. On exhausted retries we flag for operator
   review, not fail-closed.

Tagging downstream:
    VERIFIED                 → Scribe may cite
    UNVERIFIED-HALLUCINATION → Logician blocks draft if this is cited
    UNVERIFIED-NETWORK       → flagged for operator approval; not auto-blocked
    UNVERIFIED-MALFORMED     → bad input; neither source nor network

Integration
-----------
Called by Researcher after producing an evidence pack. Logician's draft-gate
refuses to release any draft citing an UNVERIFIED-HALLUCINATION source.

Usage
-----
    from pipeline.logician.gates.citation_verify import verify_pack, verify_one
    result = verify_pack(Path("pipeline/research/packs/grant_abc/"))
    for cite in result.citations:
        print(cite.status, cite.reason)

Board-review fixes (2026-04-14, cross-family code review)
---------------------------------------------------------
- BUG: 401/403 were previously classified HALLUCINATION. Now NETWORK — a
  paywalled or auth-gated resource is a real resource, not a fabrication.
  Operator can still reject it on content grounds.
- SECURITY (SSRF): resolved URL effective is checked; loopback / RFC1918 /
  link-local addresses reject with MALFORMED (prevents citation-pack from
  probing internal services).
- SECURITY: url_or_doi length capped at 2048 chars.
- BUG: all file I/O uses encoding="utf-8".
- RACE: verification_log.json is written via tmp + os.replace (atomic).
- BRITTLE: http_code stored as int (-1 on transport failure) with separate
  transport_failed flag; removes string/int mixing.
- AMBIGUOUS: --json flag separates machine output from human text.

Board-review rev 3 fixes (2026-04-14, 3-seat rerun, board HEALTHY)
------------------------------------------------------------------
- SECURITY (command injection, Red Team): curl argv now includes `--`
  before the URL so a leading `@` in the URL can't be interpreted as
  a curl file-read directive.
- SECURITY (SSRF via hostname, Red Team/Editor): _host_is_private now
  resolves hostnames (getaddrinfo) and rejects if ANY resolved address
  is private/loopback/reserved. DNS-rebind fallback is documented.
- BUG (Editor): DOI normalized to lowercase + trailing slash stripped
  before resolver URL is built (case-sensitive resolvers / double-slash
  redirect chains would previously burn retry budget).
- SECURITY (Editor): effective_url now has query string stripped before
  being persisted to verification_log.json — prevents ?token=... leaks
  into shared audit log.
"""
from __future__ import annotations

import argparse
import dataclasses
import ipaddress
import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, urlunparse

# --- Configuration ---------------------------------------------------------

RETRY_ATTEMPTS = 3
BACKOFF_SECONDS = [1.0, 2.0, 4.0]  # len must be >= RETRY_ATTEMPTS - 1
REQUEST_TIMEOUT = 10  # seconds per attempt
USER_AGENT = "GoldenQuill-citation-verify/1.0"
MAX_URL_LEN = 2048

DOI_RESOLVER = "https://doi.org/"
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/[\-._;()/:A-Z0-9]+$", re.IGNORECASE)

STATUS_VERIFIED = "VERIFIED"
STATUS_HALLUC = "UNVERIFIED-HALLUCINATION"
STATUS_NETWORK = "UNVERIFIED-NETWORK"
STATUS_MALFORMED = "UNVERIFIED-MALFORMED"

# HTTP codes that are "not found / gone" and therefore HALLUCINATION candidates
# (conclusive absence, not a permission problem):
HALLUCINATION_CODES = {404, 410}
# HTTP codes that are auth-gated; source exists but we can't confirm content:
AUTH_CODES = {401, 403}


# --- Types -----------------------------------------------------------------

@dataclasses.dataclass
class Citation:
    title: str
    source: str
    year: str
    url_or_doi: str
    author: str = ""
    # Populated by verify:
    status: str = ""
    reason: str = ""
    http_code: int = 0          # 0 = not attempted, -1 = transport failure
    transport_failed: bool = False
    attempts: int = 0
    effective_url: str = ""

    def is_verified(self) -> bool:
        return self.status == STATUS_VERIFIED

    def is_hallucination(self) -> bool:
        return self.status == STATUS_HALLUC


@dataclasses.dataclass
class PackResult:
    pack_path: str
    citations: list[Citation]

    @property
    def hallucinated(self) -> list[Citation]:
        return [c for c in self.citations if c.is_hallucination()]

    @property
    def network_unverified(self) -> list[Citation]:
        return [c for c in self.citations if c.status == STATUS_NETWORK]

    @property
    def verified(self) -> list[Citation]:
        return [c for c in self.citations if c.is_verified()]

    def scribe_may_proceed(self) -> bool:
        """Fail-closed on hallucinations only. Network-unverified flagged,
        not blocked."""
        return len(self.hallucinated) == 0


# --- SSRF protection -------------------------------------------------------

def _ip_is_private(addr: ipaddress._BaseAddress) -> bool:
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
        or addr.is_unspecified
    )


def _host_is_private(host: str) -> bool:
    """True if host is loopback / RFC1918 / link-local / reserved.

    Prior behaviour treated DNS names as safe (can't resolve reliably, many
    journals use normal DNS). Red Team flagged this as an SSRF bypass —
    `private.example.internal` resolving to 10.0.0.1 defeats the check.
    Now: parse IPs directly, and for DNS names attempt getaddrinfo and
    reject if ANY resolved address is private. Resolution failure → treat
    as safe (we can't probe what we can't resolve) rather than reject,
    because many legitimate DOIs have short-lived DNS hiccups and we
    already cap total URL count via MAX_URL_LEN and per-request timeout.

    Note: this is NOT DNS-rebind proof — an attacker could return a public
    IP at check time and a private IP at fetch time. Mitigated by: (a)
    post-fetch url_effective check in verify_one catches any redirect
    that resolved to an unsafe host; (b) citation input is operator-
    authored, not attacker-controlled.
    """
    if not host:
        return True
    host = host.strip("[]")
    # Special hostnames that must not be probed:
    if host.lower() in {"localhost", "localhost.localdomain", "ip6-localhost"}:
        return True
    # Literal IP?
    try:
        return _ip_is_private(ipaddress.ip_address(host))
    except ValueError:
        pass
    # DNS name — resolve and check each address.
    try:
        infos = socket.getaddrinfo(host, None)
    except (socket.gaierror, socket.herror, UnicodeError, OSError):
        return False  # can't resolve → can't probe → leave for curl to fail
    for info in infos:
        sockaddr = info[4]
        ip_str = sockaddr[0]
        try:
            if _ip_is_private(ipaddress.ip_address(ip_str)):
                return True
        except ValueError:
            continue
    return False


def _url_is_safe(url: str) -> tuple[bool, str]:
    """Returns (is_safe, reason_if_unsafe)."""
    if len(url) > MAX_URL_LEN:
        return False, f"url length {len(url)} > {MAX_URL_LEN}"
    try:
        parsed = urlparse(url)
    except Exception as e:
        return False, f"urlparse failed: {e}"
    if parsed.scheme.lower() not in {"http", "https"}:
        return False, f"scheme not http(s): {parsed.scheme!r}"
    if not parsed.netloc:
        return False, "missing netloc"
    host = parsed.hostname or ""
    if _host_is_private(host):
        return False, f"host {host!r} is private/loopback/reserved"
    return True, ""


# --- HTTP helper -----------------------------------------------------------

def _curl_head(url: str, timeout: int = REQUEST_TIMEOUT) -> tuple[int, str, str]:
    """Returns (http_code_int, err_str, effective_url).
    http_code == -1 on transport failure.

    Security note: `--` separator before the URL prevents curl from
    interpreting a URL that starts with `@` as a file-read directive
    (`@file` would read args from file). Since citations can in theory
    come from LLM output, treat URL as potentially adversarial.
    """
    try:
        proc = subprocess.run(
            [
                "curl", "-sSI", "-L",
                "--max-redirs", "10",
                "--max-time", str(timeout),
                "--user-agent", USER_AGENT,
                "-o", "/dev/null",
                "-w", "%{http_code}\n%{url_effective}",
                "--", url,
            ],
            capture_output=True, text=True, timeout=timeout + 5,
        )
        if proc.returncode != 0:
            return -1, proc.stderr.strip()[:200] or f"curl exit {proc.returncode}", ""
        out = proc.stdout.strip()
        if "\n" in out:
            code_s, _, eff = out.partition("\n")
        else:
            code_s, eff = out, ""
        try:
            return int(code_s), "", eff.strip()
        except ValueError:
            return -1, f"non-numeric http_code={code_s!r}", eff.strip()
    except subprocess.TimeoutExpired:
        return -1, "curl timeout", ""
    except FileNotFoundError:
        return -1, "curl not installed", ""
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}", ""


def _with_retry(url: str) -> tuple[int, str, int, str]:
    """Returns (http_code, err_str, attempts, effective_url)."""
    last_err = ""
    last_code = -1
    last_eff = ""
    attempts_made = 0
    for i in range(RETRY_ATTEMPTS):
        if i > 0:
            delay = BACKOFF_SECONDS[min(i - 1, len(BACKOFF_SECONDS) - 1)]
            time.sleep(delay)
        attempts_made = i + 1
        code, err, eff = _curl_head(url)
        last_code = code
        last_err = err
        last_eff = eff
        if code == -1:
            continue  # transport → retry
        if code >= 500 or code == 429:
            continue  # server error / rate limit → retry
        return code, "", attempts_made, eff  # conclusive
    return last_code, last_err, attempts_made, last_eff


# --- Verification ----------------------------------------------------------

def _normalize_doi(raw: str) -> str:
    """DOIs are case-insensitive per the spec — lowercase + strip trailing
    slash to avoid double-slash redirect chains at doi.org and case-
    sensitive mis-lookups at downstream resolvers."""
    return raw.lower().rstrip("/")


def _normalize_target(raw: str) -> tuple[str, str]:
    """Returns (target_url, malformed_reason).
    If malformed, target_url is empty."""
    raw = (raw or "").strip()
    if not raw:
        return "", "empty"
    if len(raw) > MAX_URL_LEN:
        return "", f"url_or_doi length {len(raw)} > {MAX_URL_LEN}"
    if DOI_PATTERN.match(raw):
        return DOI_RESOLVER + _normalize_doi(raw), ""
    low = raw.lower()
    if low.startswith("doi:"):
        doi = raw[4:].strip()
        if DOI_PATTERN.match(doi):
            return DOI_RESOLVER + _normalize_doi(doi), ""
        return "", f"malformed DOI: {raw!r}"
    if low.startswith(("http://", "https://")):
        return raw, ""
    return "", f"not a DOI nor http(s) URL: {raw!r}"


def _strip_query(url: str) -> str:
    """Return URL with query string and fragment removed. Used when
    persisting effective_url to logs so tokens in ?key=... don't leak."""
    if not url:
        return url
    try:
        p = urlparse(url)
        return urlunparse((p.scheme, p.netloc, p.path, "", "", ""))
    except Exception:
        return url


def verify_one(c: Citation) -> Citation:
    """Verify a single citation. Mutates and returns c."""
    if not c.title or not c.source or not c.year or not c.url_or_doi:
        c.status = STATUS_MALFORMED
        c.reason = "missing required fields (title/source/year/url_or_doi)"
        c.http_code = 0
        return c

    target, why = _normalize_target(c.url_or_doi)
    if not target:
        c.status = STATUS_MALFORMED
        c.reason = why
        c.http_code = 0
        return c

    safe, why = _url_is_safe(target)
    if not safe:
        c.status = STATUS_MALFORMED
        c.reason = f"rejected before fetch: {why}"
        c.http_code = 0
        return c

    code, err, attempts, eff = _with_retry(target)
    c.attempts = attempts
    c.http_code = code
    c.transport_failed = (code == -1)
    # Strip query/fragment before persisting — prevents ?token=... leak
    # into verification_log.json. The SSRF post-check below uses `eff`
    # (including query) to classify, then we store the sanitized form.
    c.effective_url = _strip_query(eff)

    # Post-redirect SSRF check: if curl followed redirects to a private host,
    # reject as MALFORMED (treat as "cannot be used as a citation").
    if eff:
        safe_after, why_after = _url_is_safe(eff)
        if not safe_after:
            c.status = STATUS_MALFORMED
            c.reason = f"redirect led to unsafe target: {why_after}"
            return c

    if 200 <= code < 400:
        c.status = STATUS_VERIFIED
        c.reason = f"HTTP {code} via {attempts} attempt(s)"
        return c

    # HALLUCINATION only if the server conclusively says "not here".
    if code in HALLUCINATION_CODES:
        c.status = STATUS_HALLUC
        c.reason = f"HTTP {code} — target reports not found"
        return c

    # Auth-gated: source exists, we can't see content → flag for operator.
    if code in AUTH_CODES:
        c.status = STATUS_NETWORK
        c.reason = f"HTTP {code} — auth-gated; operator to confirm source"
        return c

    # Other 4xx (e.g. 400, 405, 451): ambiguous. Mark NETWORK so operator
    # reviews — don't auto-fail scribe on these.
    if 400 <= code < 500:
        c.status = STATUS_NETWORK
        c.reason = f"HTTP {code} after {attempts} attempt(s) — ambiguous"
        return c

    # 5xx / 429 exhausted, or transport failure.
    c.status = STATUS_NETWORK
    c.reason = f"unresolved after {attempts} attempt(s): {err or f'HTTP {code}'}"
    return c


def _atomic_write_json(path: Path, payload: dict) -> None:
    """Write json to path via tmp file and os.replace (atomic, crash-safe)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def verify_pack(pack_path: Path) -> PackResult:
    """Verify every citation in `<pack_path>/sources.json`. Writes
    `<pack_path>/verification_log.json` atomically."""
    sources_file = pack_path / "sources.json"
    if not sources_file.exists():
        raise FileNotFoundError(f"no sources.json in {pack_path}")

    raw = json.loads(sources_file.read_text(encoding="utf-8"))
    cite_dicts = raw["citations"] if isinstance(raw, dict) and "citations" in raw else raw

    citations: list[Citation] = []
    for cd in cite_dicts:
        c = Citation(
            title=cd.get("title", ""),
            source=cd.get("source", ""),
            year=str(cd.get("year", "")),
            url_or_doi=cd.get("url_or_doi") or cd.get("url") or cd.get("doi", ""),
            author=cd.get("author", ""),
        )
        verify_one(c)
        citations.append(c)

    result = PackResult(pack_path=str(pack_path), citations=citations)
    _atomic_write_json(pack_path / "verification_log.json", {
        "pack_path": result.pack_path,
        "scribe_may_proceed": result.scribe_may_proceed(),
        "counts": {
            "verified": len(result.verified),
            "hallucinated": len(result.hallucinated),
            "network_unverified": len(result.network_unverified),
        },
        "citations": [dataclasses.asdict(c) for c in citations],
    })
    return result


# --- CLI -------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Verify an evidence-pack sources.json. Fail-closed on hallucinations."
    )
    ap.add_argument("pack_path", type=Path, help="evidence pack directory")
    ap.add_argument("--json", action="store_true",
                    help="emit only JSON summary to stdout (human text suppressed)")
    args = ap.parse_args(argv)

    result = verify_pack(args.pack_path)
    summary = {
        "pack_path": result.pack_path,
        "verified": len(result.verified),
        "hallucinated": len(result.hallucinated),
        "network_unverified": len(result.network_unverified),
        "scribe_may_proceed": result.scribe_may_proceed(),
    }
    if args.json:
        sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    else:
        print(f"[citation_verify] {args.pack_path}", file=sys.stderr)
        print(f"  verified:            {summary['verified']}", file=sys.stderr)
        print(f"  hallucinated:        {summary['hallucinated']}", file=sys.stderr)
        print(f"  network_unverified:  {summary['network_unverified']}", file=sys.stderr)
        print(f"  scribe_may_proceed:  {summary['scribe_may_proceed']}", file=sys.stderr)
        sys.stdout.write(json.dumps(summary) + "\n")
    return 0 if result.scribe_may_proceed() else 1


if __name__ == "__main__":
    sys.exit(main())
