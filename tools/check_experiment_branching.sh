#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

allow_skip_branch_policy_check="${ALLOW_EXPERIMENT_BRANCH_POLICY:-0}"
if [[ "$allow_skip_branch_policy_check" == "1" ]]; then
  echo "[info] experiment branch policy check explicitly disabled (ALLOW_EXPERIMENT_BRANCH_POLICY=1)"
  exit 0
fi

current_branch="$(git branch --show-current || true)"
if [[ -z "$current_branch" ]]; then
  current_branch="${GITHUB_HEAD_REF:-${GITHUB_REF_NAME:-}}"
fi

base_ref=""
if git show-ref --verify --quiet refs/remotes/origin/main; then
  base_ref="origin/main"
elif git show-ref --verify --quiet refs/remotes/origin/master; then
  base_ref="origin/master"
elif git rev-parse --verify --quiet HEAD~1 >/dev/null; then
  base_ref="HEAD~1"
fi

if [[ -z "$base_ref" ]]; then
  echo "[warning] unable to infer comparison base for experiment branch policy check; skipping"
  exit 0
fi

mapfile -t changed_files < <(git diff --name-only "$base_ref"...HEAD)

if [[ "${#changed_files[@]}" -eq 0 ]]; then
  echo "[info] no git diff entries detected for experiment branch policy check"
  exit 0
fi

declare -a experiment_refs=()
for file in "${changed_files[@]}"; do
  if [[ "$file" =~ ^research/projects/([^/]+)/experiments/([^/]+)/ ]]; then
    experiment_refs+=("${BASH_REMATCH[1]}/${BASH_REMATCH[2]}")
  fi
done

if [[ "${#experiment_refs[@]}" -eq 0 ]]; then
  echo "[info] no experiment bundle changes detected; experiment branch policy not applicable"
  exit 0
fi

mapfile -t unique_refs < <(printf '%s\n' "${experiment_refs[@]}" | sort -u)
if [[ "${#unique_refs[@]}" -ne 1 ]]; then
  echo "[violation] experiment changes span multiple bundles on one branch:"
  printf '  - %s\n' "${unique_refs[@]}"
  echo "[hint] keep each branch scoped to one experiment bundle"
  exit 1
fi

if [[ -z "$current_branch" ]]; then
  echo "[warning] current branch name is unavailable; unable to enforce experiment branch naming"
  exit 0
fi

expected_branch="experiment/${unique_refs[0]}"
if [[ "$current_branch" != "$expected_branch" && "$current_branch" != "$expected_branch/"* ]]; then
  echo "[violation] experiment bundle '${unique_refs[0]}' must use branch '$expected_branch' (or '$expected_branch/<suffix>')"
  echo "[info] current branch: $current_branch"
  exit 1
fi

echo "[ok] experiment branch policy satisfied ($current_branch)"
