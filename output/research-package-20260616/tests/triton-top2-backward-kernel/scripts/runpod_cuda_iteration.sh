#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Run one CUDA/Triton iteration on a remote RunPod-style SSH host.

Required:
  --host HOST                 Remote SSH host/IP, or set POD_HOST.

Optional:
  --port PORT                 SSH port, or set POD_PORT. Default: 22.
  --user USER                 SSH user, or set POD_USER. Default: root.
  --remote-dir DIR            Remote workspace. Default: /workspace.
  --python PYTHON             Remote Python command. Default: /usr/local/bin/python.
  --ssh-key PATH              SSH private key path, or set SSH_KEY.
  --bundle-name NAME          Archive name. Default uses UTC timestamp.
  --no-bootstrap              Skip scripts/free_cuda_runner_bootstrap.sh.
  --no-probe                  Skip scripts/cuda_runner_probe.py.
  --keep-remote               Do not remove existing remote project dir first.
  --help                      Show this help.

Examples:
  scripts/runpod_cuda_iteration.sh --host 1.2.3.4 --port 12345
  POD_HOST=1.2.3.4 POD_PORT=12345 scripts/runpod_cuda_iteration.sh
EOF
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd "$script_dir/.." && pwd)"
research_dir="$(cd "$project_dir/.." && pwd)"

pod_host="${POD_HOST:-}"
pod_port="${POD_PORT:-22}"
pod_user="${POD_USER:-root}"
remote_dir="${REMOTE_DIR:-/workspace}"
remote_python="${REMOTE_PYTHON:-/usr/local/bin/python}"
ssh_key="${SSH_KEY:-}"
bundle_name="${BUNDLE_NAME:-triton-top2-iteration-$(date -u +%Y%m%dT%H%M%SZ).tar.gz}"
run_bootstrap=1
run_probe=1
keep_remote=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      pod_host="${2:-}"
      shift 2
      ;;
    --port)
      pod_port="${2:-}"
      shift 2
      ;;
    --user)
      pod_user="${2:-}"
      shift 2
      ;;
    --remote-dir)
      remote_dir="${2:-}"
      shift 2
      ;;
    --python)
      remote_python="${2:-}"
      shift 2
      ;;
    --ssh-key)
      ssh_key="${2:-}"
      shift 2
      ;;
    --bundle-name)
      bundle_name="${2:-}"
      shift 2
      ;;
    --no-bootstrap)
      run_bootstrap=0
      shift
      ;;
    --no-probe)
      run_probe=0
      shift
      ;;
    --keep-remote)
      keep_remote=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$pod_host" ]]; then
  echo "BLOCK: set --host or POD_HOST." >&2
  usage >&2
  exit 2
fi

if [[ ! "$bundle_name" == *.tar.gz ]]; then
  echo "BLOCK: --bundle-name must end with .tar.gz" >&2
  exit 2
fi

bundle_dir="$project_dir/development/runner-bundles"
mkdir -p "$bundle_dir"
bundle_path="$bundle_dir/$bundle_name"
remote_project="$remote_dir/triton-top2-backward-kernel"
remote_bundle="$remote_dir/$bundle_name"

ssh_opts=(-p "$pod_port" -o ServerAliveInterval=30 -o ServerAliveCountMax=4)
scp_opts=(-P "$pod_port" -o ServerAliveInterval=30 -o ServerAliveCountMax=4)
if [[ -n "$ssh_key" ]]; then
  ssh_opts+=(-i "$ssh_key")
  scp_opts+=(-i "$ssh_key")
fi

echo "==> Building bundle: $bundle_path"
tar \
  --exclude='triton-top2-backward-kernel/.venv' \
  --exclude='triton-top2-backward-kernel/.pytest_cache' \
  --exclude='triton-top2-backward-kernel/development/runner-bundles' \
  --exclude='*/__pycache__' \
  --exclude='*.pyc' \
  -czf "$bundle_path" \
  -C "$research_dir" \
  triton-top2-backward-kernel

echo "==> Bundle size"
ls -lh "$bundle_path"
echo "==> Bundle sha256"
sha256sum "$bundle_path"

echo "==> Preparing remote workspace: ${pod_user}@${pod_host}:${remote_dir}"
ssh "${ssh_opts[@]}" "${pod_user}@${pod_host}" "mkdir -p '$remote_dir'"

echo "==> Uploading bundle"
scp "${scp_opts[@]}" "$bundle_path" "${pod_user}@${pod_host}:$remote_bundle"

remote_script="$(mktemp)"
cleanup() {
  rm -f "$remote_script"
}
trap cleanup EXIT

cat > "$remote_script" <<EOF
#!/usr/bin/env bash
set -euo pipefail

cd "$remote_dir"
if [[ "$keep_remote" != "1" ]]; then
  rm -rf "$remote_project"
fi
tar --no-same-owner -xzf "$remote_bundle"
cd "$remote_project"
remote_python_cmd="$remote_python"

echo "==> Remote Python"
command -v "\$remote_python_cmd" || true
"\$remote_python_cmd" --version

echo "==> NVIDIA state"
command -v nvidia-smi && nvidia-smi || true

if [[ "$run_bootstrap" == "1" ]]; then
  echo "==> Bootstrap"
  PYTHON="\$remote_python_cmd" bash scripts/free_cuda_runner_bootstrap.sh
  if [[ -f .cuda_runner_python ]]; then
    remote_python_cmd="\$(cat .cuda_runner_python)"
  fi
fi

if [[ "$run_probe" == "1" ]]; then
  echo "==> CUDA/Triton probe"
  "\$remote_python_cmd" scripts/cuda_runner_probe.py
fi

echo "==> Triton focused tests"
"\$remote_python_cmd" -m pytest tests/test_router_triton.py -q

echo "==> Full test suite"
"\$remote_python_cmd" -m pytest tests -q
EOF

echo "==> Running remote validation"
ssh "${ssh_opts[@]}" "${pod_user}@${pod_host}" "bash -s" < "$remote_script"

echo "PASS: remote CUDA/Triton iteration completed."
