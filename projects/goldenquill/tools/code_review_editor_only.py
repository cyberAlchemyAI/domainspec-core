#!/usr/bin/env python3
"""Re-run Editor seat only — deepseek-r1-distill-llama-70b was decommissioned.
Falls back to llama-3.3-70b-versatile and appends to CODE_REVIEW_2026-04-14.md.
"""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path

# Portable: derive workspace root from this file's location.
# Override via QUILL_WORKSPACE env var if needed.
_WORKSPACE = Path(os.environ.get("QUILL_WORKSPACE") or Path(__file__).resolve().parent.parent)

FILES = [
    _WORKSPACE / "logician/gates/topology_gate.py",
    _WORKSPACE / "logician/gates/citation_verify.py",
    _WORKSPACE / "tools/dedup_skills.py",
]
ENV_PATH = Path.home() / ".openclaw" / ".env"
# Output filename includes today's date so re-runs don't collide.
OUT_PATH = _WORKSPACE / f"CODE_REVIEW_EDITOR_{time.strftime('%Y-%m-%d')}.md"

env = {}
for line in ENV_PATH.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line: continue
    k, _, v = line.partition("=")
    env[k.strip()] = v.strip().strip('"').strip("'")
GROQ_KEY = env.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

bundle = []
for p in FILES:
    bundle.append(f"===== FILE: {p.name} =====\n{p.read_text()}\n===== END: {p.name} =====\n\n")
CODE_BUNDLE = "".join(bundle)

SYSTEM = (
    "You are the Editor seat. Review these three files for clarity, "
    "maintainability, and whether an operator (Josh, non-coder) could read "
    "the CLI output and act on it. Are error messages actionable? Do function "
    "names describe what they do? Are docstrings accurate vs aspirational? "
    "Is any logic obscure enough it will bite us in 6 months?"
)
USER = (
    "An Anthropic model authored these three files for the Golden Quill "
    "migration. They are load-bearing. Return 5-10 findings per file. Each "
    "in remediation-shape: WHICH file + line/function, WHAT, WHY, HOW. "
    "Categorize: BRITTLE / RATIONALIZATION / GAP / ORDERING / AMBIGUOUS / BUG / SECURITY. "
    "Be direct. Probe.\n\n"
    "===== CODE BUNDLE BEGINS =====\n\n"
    f"{CODE_BUNDLE}\n===== CODE BUNDLE ENDS =====\n\n"
    "End with one paragraph: what would make you pause before running these in production?"
)

MODEL = "llama-3.3-70b-versatile"
body = json.dumps({
    "model": MODEL,
    "messages": [{"role":"system","content":SYSTEM},{"role":"user","content":USER}],
    "temperature": 0.3, "max_tokens": 6144,
})
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    f.write(body); body_path = f.name
t0 = time.time()
proc = subprocess.run([
    "curl","-sS","-X","POST","https://api.groq.com/openai/v1/chat/completions",
    "-H", f"Authorization: Bearer {GROQ_KEY}",
    "-H", "Content-Type: application/json",
    "-H", "User-Agent: openclaw-code-review/1.0",
    "--data-binary", f"@{body_path}",
    "--max-time", "240",
    "-w", "\n__HTTPCODE__%{http_code}",
], capture_output=True, text=True, timeout=260)
elapsed = time.time() - t0
os.unlink(body_path)

out = proc.stdout or ""
body_out, _, code_out = out.rpartition("__HTTPCODE__")
http_code = code_out.strip()
if http_code != "200":
    print(f"FAIL HTTP {http_code}: {body_out[:500]}", file=sys.stderr); sys.exit(1)

data = json.loads(body_out)
content = data["choices"][0]["message"]["content"]
usage = data.get("usage", {})
meta = (f"\n\n_[probe meta: {MODEL} | prompt_tokens={usage.get('prompt_tokens','?')} | "
        f"completion_tokens={usage.get('completion_tokens','?')} | elapsed={elapsed:.1f}s]_")

# Replace the failed Editor block in the existing file
text = OUT_PATH.read_text()
marker = "## Editor — `deepseek-r1-distill-llama-70b`"
if marker not in text:
    print("ERROR: Editor marker not found; appending instead", file=sys.stderr)
    text += f"\n\n## Editor — `{MODEL}` (fallback; deepseek was decommissioned)\n\n{content}{meta}\n\n---\n\n"
else:
    # Replace block between marker and next "---\n\n## " or end
    start = text.index(marker)
    # find end of block: next line starting with "---" followed by "## " OR the end
    rest = text[start:]
    # find "\n---\n" followed by "\n## " (new section)
    end_rel = None
    idx = 0
    while True:
        j = rest.find("\n---\n", idx)
        if j < 0: break
        # check what follows
        after = rest[j+5:j+200]
        if after.lstrip().startswith("## "):
            end_rel = j + 5
            break
        idx = j + 5
    if end_rel is None:
        end_rel = len(rest)
    new_block = (f"## Editor — `{MODEL}` (fallback; deepseek-r1-distill-llama-70b was decommissioned)\n\n"
                 f"{content}{meta}\n\n---\n\n")
    text = text[:start] + new_block + text[start+end_rel:]

OUT_PATH.write_text(text)
print(f"OK: {len(content):,} chars, elapsed {elapsed:.1f}s")
