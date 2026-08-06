Both feedback gaps are `ready`. The repair provides digest-bound, machine-expandable manifests without repository mutation or runtime claims.

## AKV-FB-001 — `ready`

Official live source: [Anime.js documentation](https://animejs.com/documentation/).

Observed snapshot:

```json
{
  "observed_at": "2026-08-03T16:36:51.838Z",
  "seed_url": "https://animejs.com/documentation/",
  "seed_raw_sha256": "6f9912f716849789b9468b4916e88398f0028775e8b054c5d4604ef1afb78f28",
  "route_count": 418,
  "successful_rows": 418,
  "failed_rows": 0,
  "raw_page_set_sha256": "63125e931350f5dbf8552a289ac80d687bb1867e7c94c1e2d6e33904f16befcd",
  "semantic_jsonl_sha256": "681f004e04a91ab1a3462e882edff24d09454297f34a41863e81df06e20066fb"
}
```

Every route returned HTTP 200 after redirect normalization to a trailing-slash canonical path.

### Lossless extraction contract

The official `/documentation/` HTML is the route-set artifact. Discover routes with:

```regex
href="(\/documentation(?:\/[^"?# ]*)?)"
```

Exclude `/documentation`, deduplicate, and sort lexicographically. For each path, request `https://animejs.com<path>/` with redirects enabled.

Extract only from:

```css
article#docs-info
```

For every route emit this ordered JSON object:

```json
{
  "canonical_path": "<final redirected URL pathname>",
  "title": "<decoded title text>",
  "h1": "<decoded article#docs-info h1 text>",
  "heading_selectors": ["#<id>", "..."],
  "headings": ["<article h1-h6 text>", "..."],
  "topic_kind": "<classification below>",
  "parameters": "present|absent",
  "returns": "present|absent",
  "related_topics": {
    "disposition": "present|absent",
    "targets": [
      {"path": "<normalized documentation path with trailing slash>", "label": "<decoded anchor text>"}
    ]
  },
  "examples": "present-source-only|absent",
  "version_notes": {
    "disposition": "present|absent",
    "notes": ["<.docs-breadcrumb-version text>"]
  },
  "badges": {"js": false, "waapi": false, "new": false},
  "status": "semantic-observed",
  "http_status": 200,
  "raw_sha256": "<SHA-256 of response HTML bytes>"
}
```

Normalization and disposition rules:

- Decode tags/whitespace plus `&nbsp;`, `&amp;`, `&#39;`, `&apos;`, and `&quot;`.
- `heading_selectors`: ordered IDs of `article#docs-info h1` through `h6`.
- `parameters=present` iff an article heading normalizes case-insensitively to `Parameters`, `Parameter`, or `Accepts`.
- `returns=present` iff an article heading normalizes to `Return` or `Returns`.
- `related_topics.targets`: all distinct internal `/documentation/...` anchors in the article except the current canonical path, preserving first occurrence.
- `examples=present-source-only` iff the article contains `section.code-preview`. It is not execution evidence.
- `version_notes`: ordered `.docs-breadcrumb-version` text, generally `Since <version>`.
- Badges are article-local: literal `(JS)`, `(WAAPI)`, or `NEW` in the H1.
- Topic-kind precedence: top-level family; callback; method; property; parameter-or-setting; recipe; pitfall-guide; target-kind; keyframe-guide; easing-topic; otherwise guide-or-api-topic.
- Sort rows by `canonical_path`.
- Serialize each object with `JSON.stringify(row) + "\n"`.
- `semantic_jsonl_sha256` is SHA-256 of the concatenated rows.
- `raw_page_set_sha256` is SHA-256 of sorted `canonical_path + "\t" + raw_sha256 + "\n"` records.

Snapshot dispositions:

```json
{
  "parameters": {"present": 260, "absent": 158},
  "returns": {"present": 123, "absent": 295},
  "related_topics": {"present": 418, "absent": 0},
  "examples": {"present-source-only": 353, "absent": 65},
  "version_notes": {"present": 388, "absent": 30}
}
```

Representative exact row:

```json
{
  "canonical_path": "/documentation/animation/tween-parameters/duration/",
  "title": "duration | Tween parameters | Animation | Documentation | Anime.js | JavaScript Animation Engine",
  "h1": "duration",
  "heading_selectors": ["#accepts", "#default"],
  "headings": ["duration", "Accepts", "Default"],
  "topic_kind": "parameter-or-setting",
  "parameters": "present",
  "returns": "absent",
  "related_topics": {
    "disposition": "present",
    "targets": [
      {"path": "/documentation/animation/", "label": "Animation"},
      {"path": "/documentation/animation/tween-parameters/", "label": "Tween parameters"},
      {"path": "/documentation/animation/tween-value-types/function-based/", "label": "Function based value"},
      {"path": "/documentation/animation/tween-parameters/delay/", "label": "delay"},
      {"path": "/documentation/animation/tween-parameters/ease/", "label": "ease"}
    ]
  },
  "examples": "present-source-only",
  "version_notes": {"disposition": "present", "notes": ["Since 1.0.0"]},
  "badges": {"js": false, "waapi": false, "new": false},
  "status": "semantic-observed",
  "http_status": 200,
  "raw_sha256": "81383b6835e550ddd35e7e9c2d6b6d83862e0bc057a61c2fe8273aff701d4a0b"
}
```

Residue: no official sitemap, robots manifest, or repository-owned documentation-generation input was found at the obvious official endpoints. The digest binds this crawl but does not make the mutable website immutable. Re-crawls must compare both digests and retain changed rows as versioned observations.

The HTML references site CSS/JS assets with `?v=4.4.1`; that is a cache/version marker, not proof that documentation semantics are package v4.4.1.

## AKV-FB-002 — `ready`

Official immutable anchors: [v4.5.0 commit](https://github.com/juliangarnier/anime/tree/2c9cf8ea00329f6768c7d7902252ed977d75ce42), [v4.5.0 release](https://github.com/juliangarnier/anime/releases/tag/v4.5.0).

```json
{
  "version": "4.5.0",
  "commit_sha": "2c9cf8ea00329f6768c7d7902252ed977d75ce42",
  "commit_tree_sha1": "1511dce2d3e54de4c9c9cbfdb1d1dff2248d2c98",
  "tree_api": "https://api.github.com/repos/juliangarnier/anime/git/trees/1511dce2d3e54de4c9c9cbfdb1d1dff2248d2c98?recursive=1",
  "tree_truncated": false,
  "manifest_rows": 348,
  "manifest_jsonl_sha256": "f4026dec178de523262aca34dcddc5e419681b3494f37f496d9da8553d3ebcc0",
  "counts": {
    "source": 70,
    "type": 70,
    "test": 125,
    "example": 81,
    "package_documentation": 2
  }
}
```

### Machine expansion contract

Read the immutable recursive Git tree and retain blobs matching:

```text
README.md
package.json
src/**
dist/modules/**/*.d.ts
tests/**
examples/**
```

Sort by `path`. Emit:

```json
{
  "path": "<repository path>",
  "blob_sha1": "<Git blob identity>",
  "size": 0,
  "kind": "source|type|test|example|package-documentation",
  "structured_pointer": "git:2c9cf8ea00329f6768c7d7902252ed977d75ce42:<path>",
  "evidence_status": "source-observed|type-present|test-present-not-executed|example-source-present-not-executed"
}
```

Serialize as ordered JSONL. The resulting digest must equal `f4026dec...3ebcc0`.

Package-documentation anchors:

```json
[
  {
    "path": "README.md",
    "blob_sha1": "11e8d61143d56f82c5940267d990425bc6de5482",
    "size": 5192
  },
  {
    "path": "package.json",
    "blob_sha1": "7ebe3997b3620aeb7757c1d24b568d461ceb967d",
    "size": 8344
  }
]
```

### Documentation-family joins

| Documentation family | Package/module source |
|---|---|
| Getting started | `README.md`; `package.json#exports` |
| Timer | `animejs/timer`; `src/timer/`; `dist/modules/timer/` |
| Animation | `animejs/animation`; `src/animation/`; shared `src/core/`; matching declarations |
| Timeline | `animejs/timeline`; `src/timeline/`; matching declarations |
| Animatable | `animejs/animatable`; `src/animatable/`; matching declarations |
| Draggable | `animejs/draggable`; `src/draggable/`; matching declarations |
| Layout | `animejs/layout`; `src/layout/`; matching declarations |
| Scope | `animejs/scope`; `src/scope/`; matching declarations |
| Events | `animejs/events`; `src/events/`; matching declarations |
| SVG | `animejs/svg`; `src/svg/`; matching declarations |
| Text | `animejs/text`; `src/text/`; matching declarations |
| Utilities | `animejs/utils`; `src/utils/`; matching declarations |
| Easings | `animejs/easings` and its six published easing subpaths; `src/easings/` |
| WAAPI | `animejs/waapi`; `src/waapi/`; matching declarations |
| Engine | `animejs/engine`; `src/engine/`; matching declarations |
| Adapters | `animejs/adapters`; side-effect `animejs/adapters/three`; `src/adapters/` |

Root `src/index.js` re-exports every principal module and namespace except adapters; adapters remain explicit package subpaths. Structured symbol pointers may therefore use `path#export:<symbol>` after following `export *` edges from each module `index.js`.

Source-level observed direct exports include:

- SVG: `morphTo`, `createDrawable`, `createMotionPath`.
- Adapters: `registerAdapter`.
- Three.js adapter: `threeAdapter`, `getInstances`, `commitChanges`, plus side-effect resolver registrations.
- Root namespaces: `easings`, `utils`, `svg`, `text`; root also exports `globals`.

### Explicit residues

- `getting-started` has repository package/README evidence but no same-named source, test, or example directory.
- No directly named repository example was found for Timer, Engine, or WAAPI. Documentation code previews remain separate `present-source-only` examples.
- Tests and examples whose filenames do not identify one family must remain `shared-or-unmatched`; do not infer ownership from plausible behavior.
- Unmatched support material consists of 29 blobs: example assets/configuration and additive/canvas examples; test assets/configuration/runners plus generic build, leak, Node, seconds, and types suites.
- Test and example presence does not establish execution, passing behavior, performance, accessibility, or production readiness.
- The official [v3-to-v4 migration guide](https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4) is mutable wiki evidence and is not part of the pinned commit tree.

## Proposed continuation receipt

```json
{
  "action_id": "spawn-0001",
  "dispatch_id": "2026-08-03-animejs-agent-knowledge-vault-route",
  "run_id": "animejs-vault-run-001",
  "wave_id": "explorers",
  "step_id": "s1",
  "role": "official-source-explorer",
  "capability_ref": "research",
  "status": "pass",
  "artifacts": [
    {
      "ref": "urn:animejs-doc-semantic-manifest:sha256:681f004e04a91ab1a3462e882edff24d09454297f34a41863e81df06e20066fb",
      "state": "returned-not-written",
      "rows": 418
    },
    {
      "ref": "urn:animejs-v4.5.0-source-manifest:sha256:f4026dec178de523262aca34dcddc5e419681b3494f37f496d9da8553d3ebcc0",
      "state": "returned-not-written",
      "rows": 348
    }
  ],
  "validation": {
    "feedback_traversal": "1/1",
    "AKV-FB-001": "ready",
    "AKV-FB-002": "ready",
    "documentation_rows": "418/418",
    "documentation_fetch_failures": 0,
    "repository_tree_truncated": false,
    "test_execution": "not-performed",
    "example_execution": "not-performed",
    "workspace_mutation_during_feedback": "none",
    "git_mutation": "none"
  },
  "blockers": [],
  "started_at": "2026-08-03T16:28:00Z",
  "finished_at": "2026-08-03T16:37:00Z"
}
```

Hygiene residue from the earlier traversal: `/tmp/animejs-doc-urls` was created during the initial diagnostic, outside the repository, and a host safety guard rejected its attempted removal. This feedback traversal made no filesystem writes; the parent should account for that temporary-file residue when normalizing the overall action receipt.
