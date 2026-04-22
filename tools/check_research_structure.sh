#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

allow_compatibility="${ALLOW_RESEARCH_COMPATIBILITY:-0}"

projects=(domainspec meta-meta mars)
required_files=(
  "PROJECT.yaml"
  "claims/CLAIMS.md"
  "deps/DEPENDENCIES.yaml"
  "registry/ARTIFACT-INDEX.md"
  "registry/TRACEABILITY-MATRIX.md"
  "telemetry/SIGNAL-SCHEMA.md"
)

legacy_compat_paths=(
  "research/experiments"
  "research/EXPERIMENTS-META.md"
  "research/EXPERIMENT-BOUNDARIES.md"
  "research/INVENTORY-READINESS-GATE.md"
  "research/MARS-AGENT-ROLLOUT.md"
  "research/MARS-EVIDENCE-STATUS.md"
  "research/MARS-PIPELINE.md"
  "research/MARS-PROTOCOL-CHECKLIST.md"
  "research/MULTI-SOURCE-CONTEXT-PATTERN.md"
  "research/projects/domainspec/EXPERIMENTS.md"
  "research/projects/domainspec/domainspec-paper.md"
  "research/projects/domainspec/research-ideas.md"
  "research/projects/meta-meta/EXPERIMENTS-META.md"
  "research/projects/mars/INVENTORY-READINESS-GATE.md"
  "research/projects/mars/MARS-AGENT-ROLLOUT.md"
  "research/projects/mars/MARS-EVIDENCE-STATUS.md"
  "research/projects/mars/MARS-PIPELINE.md"
  "research/projects/mars/MARS-PROTOCOL-CHECKLIST.md"
  "research/projects/mars/MULTI-SOURCE-CONTEXT-PATTERN.md"
)

violations=0

echo "== Research Structure Check =="

for project in "${projects[@]}"; do
  base="research/projects/$project"
  echo
  echo "[project] $project"

  if [[ ! -d "$base" ]]; then
    echo "[violation] missing project directory: $base"
    ((violations+=1))
    continue
  fi

  for rel in "${required_files[@]}"; do
    if [[ ! -f "$base/$rel" ]]; then
      echo "[violation] missing required file: $base/$rel"
      ((violations+=1))
    fi
  done

  deps_file="$base/deps/DEPENDENCIES.yaml"
  if [[ -f "$deps_file" ]]; then
    for key in dependency_id type provider_project provider_artifact provider_version_or_commit consumer_project consumer_purpose validation_gate fallback_plan; do
      if ! grep -q "$key:" "$deps_file"; then
        echo "[violation] dependency manifest missing key '$key' in $deps_file"
        ((violations+=1))
      fi
    done
  fi

  if [[ ! -d "$base/exports" ]]; then
    echo "[violation] missing exports directory: $base/exports"
    ((violations+=1))
  fi

done

if [[ "$allow_compatibility" != "1" ]]; then
  for path in "${legacy_compat_paths[@]}"; do
    if [[ -e "$path" || -L "$path" ]]; then
      echo "[violation] compatibility alias present without explicit request: $path"
      ((violations+=1))
    fi
  done

  if find research -type l | grep -q .; then
    echo
    echo "[violation] symbolic links found under research/ (compatibility handling is disabled by default)"
    find research -type l
    ((violations+=1))
  fi
else
  echo
  echo "[info] compatibility handling explicitly enabled (ALLOW_RESEARCH_COMPATIBILITY=1)"
fi

if find research -xtype l | grep -q .; then
  echo
  echo "[violation] broken symbolic links found under research/"
  find research -xtype l
  ((violations+=1))
fi

if [[ "$violations" -gt 0 ]]; then
  echo
  echo "[result] FAIL ($violations violations found)"
  exit 1
fi

echo

echo "[result] PASS (research project structure is valid)"
