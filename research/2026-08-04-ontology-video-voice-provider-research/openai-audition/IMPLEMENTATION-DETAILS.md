# Implementation Detail Specs

These are execution contracts, not implemented code.

## Runtime posture

- Language/runtime: Node.js `v22.12.0`, ESM `.mjs`, built-in `fetch`, `crypto`, `fs`, and `node:test`.
- Dependency posture: no new package root and no provider SDK for L0/L1. The exact client identity is Node `v22.12.0` built-in fetch/Undici as observed by the later run.
- Runtime root: `openai-audition/runtime/`.
- Generated evidence root: `openai-audition/runs/`, excluded from Git by a package-local `.gitignore` created in L0.
- Network posture: injected transport; tests use a fake transport. Only the explicit `render` command can receive the real transport.
- Canonical JSON: recursively sorted keys, UTF-8, no insignificant whitespace, trailing newline only for stored documents; SHA-256 over the canonical bytes defined by the schema contract.

## Preflight algorithm

```text
load candidate JSON without environment access
validate schema and reject unknown fields
resolve every relative source path inside the package/repository boundary
hash exact source bytes and compare declared digests
count UTF-8 bytes, code points, words, and provider-route tokens with a pinned counter
assert exact excerpt digest and count are frozen and under the route limit
evaluate owner, account, disclosure, tool, model, voice, and route gates
project only allowlisted request body fields
scan persisted values and diagnostics for secret-shaped material
if any check fails: emit deterministic not_ready result and stop
otherwise: canonicalize manifest, request preview, and admission receipt
```

Preflight accepts an injected `transport_probe` only in tests so a causal negative fixture can prove zero network calls. It never reads `OPENAI_API_KEY`.

## Render algorithm

```text
re-run preflight and require admitted manifest digest
acquire per-manifest exclusive lock
for repetition in [1, 2]:
  allocate UUID run and O_EXCL temporary target before credential access
  read OPENAI_API_KEY only inside the request function
  POST exact request to fixed HTTPS origin and /v1/audio/speech
  reject redirects, SSE, non-binary success, non-success, or ambiguous completion
  stream bytes to unique temporary file; close and hash
  parse minimum WAV header fields without rewriting raw bytes
  atomically bind temp file and write redacted attempt receipt
  never retry automatically
release lock
emit TwoRendersCaptured only when both attempts and identical request digests validate
```

If transport completion is ambiguous, record a bounded failure and require a new explicit attempt ID. No operation deletes or overwrites the ambiguous evidence.

## Verification algorithm

1. Validate raw hashes, WAV container, duration, sample rate, bit depth, channels, and absence of truncation/clipping/non-speech artifacts using pinned tools.
2. Produce a mono 48 kHz, 24-bit WAV derivative normalized in two passes to `-16 LUFS-I` and true peak no higher than `-1 dBTP`; preserve commands, versions, logs, metrics, and parent hash.
3. Force-align for timing only; verify monotonic boundaries within audio duration.
4. Independently transcribe without supplying the reference text, or perform a token-by-token listening audit by an independent reviewer.
5. Compare normalized tokens to the frozen excerpt and escalate every addition, omission, substitution, reordering, low-confidence token, or disagreement.
6. Manually review the five required phrase groups. Wrong “Body War” pronunciation rejects the candidate.
7. Generate waveform-derived VTT only after acceptance; provider timing remains diagnostic.

The current machine has no discovered `ffmpeg`, `ffprobe`, or Whisper CLI. Tool choice/version and install authority are L2 blockers; implementation must not silently vendor or install them.

## Blinding and decision algorithm

- Use cryptographic UUID labels, never meaningful voice/provider labels.
- Deterministically generate balanced listener orders from a pinned randomization command after artifacts freeze; keep repetitions separated.
- Store the unblinding key outside listener-visible paths.
- Validate every sheet against the fixed rubric and calculate weighted points.
- Report median plus listener/repetition spread. Difference below 3 points is a tie; no automatic winner.
- Require named production operator and governing hashes for `approve|reject|defer`.

## Edge cases

- Unicode punctuation drift, newline normalization, or headings entering the spoken input.
- Model alias resolving differently from the dated snapshot.
- Selected voice unavailable for the selected model/account.
- Documentation changes between manifest preparation and render.
- Provider returns MP3/default despite requested WAV, redirects, streams SSE, or truncates bytes.
- Timeout after provider accepted the request but before local completion.
- Process crash between raw close and receipt binding.
- Two repetitions have different request bytes or metadata.
- Audio is lossless but not mono/24 kHz/16-bit minimum.
- Alignment looks clean while independent fidelity finds a word mismatch.
- Listener learns the voice identity or hears repetitions back-to-back.
- A passing score is mistaken for public-use or full-production authorization.
