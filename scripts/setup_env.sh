#!/usr/bin/env bash
set -euo pipefail

# Create a reproducible local environment for RoSE. External projects are
# installed only when they are present at the configured paths.
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export UV_CACHE_DIR="${UV_CACHE_DIR:-$ROOT_DIR/.uv-cache}"
VENV_DIR="${ROSE_VENV_DIR:-$ROOT_DIR/.venv}"
PROFILE="${ROSE_PROFILE:-all}"
PYTHON_REQUEST="${ROSE_PYTHON:-python3}"
INSTALL_EXTERNAL=1
RUN_CHECKS=1

usage() {
  cat <<'USAGE'
Usage: bash scripts/setup_env.sh [options]

Options:
  --profile NAME     core, sim, real, or all (default: all)
  --python VERSION   Python executable or version passed to uv (default: python3)
  --venv PATH        virtual environment path (default: .venv)
  --no-external      do not install detected ManiSkill/LeRobot repositories
  --no-check         skip dependency/import/test checks
  -h, --help         show this help

Examples:
  bash scripts/setup_env.sh
  bash scripts/setup_env.sh --profile sim
  bash scripts/setup_env.sh --profile core --no-external
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      [[ $# -ge 2 ]] || { echo "--profile needs a value" >&2; exit 2; }
      PROFILE="$2"; shift 2
      ;;
    --python)
      [[ $# -ge 2 ]] || { echo "--python needs a value" >&2; exit 2; }
      PYTHON_REQUEST="$2"; shift 2
      ;;
    --venv)
      [[ $# -ge 2 ]] || { echo "--venv needs a value" >&2; exit 2; }
      VENV_DIR="$2"; shift 2
      ;;
    --no-external) INSTALL_EXTERNAL=0; shift ;;
    --no-check) RUN_CHECKS=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$PROFILE" in
  core) EXTRAS="dev"; NEED_PYTHON_MINOR=10 ;;
  sim) EXTRAS="torch,maniskill,libero,dev"; NEED_PYTHON_MINOR=12 ;;
  real) EXTRAS="torch,franka,dev"; NEED_PYTHON_MINOR=10 ;;
  all) EXTRAS="torch,maniskill,libero,franka,dev"; NEED_PYTHON_MINOR=12 ;;
  *) echo "invalid profile: $PROFILE (expected core, sim, real, or all)" >&2; exit 2 ;;
esac

command -v uv >/dev/null 2>&1 || {
  echo "uv is required. Install it from https://docs.astral.sh/uv/" >&2
  exit 1
}

mkdir -p "$ROOT_DIR/data" "$ROOT_DIR/outputs"
PYTHON_BIN="$VENV_DIR/bin/python"
if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "[rose] creating virtual environment: $VENV_DIR"
  uv venv --python "$PYTHON_REQUEST" "$VENV_DIR"
else
  echo "[rose] reusing virtual environment: $VENV_DIR"
fi
[[ -x "$PYTHON_BIN" ]] || { echo "virtual environment Python not found: $PYTHON_BIN" >&2; exit 1; }

python_version=$($PYTHON_BIN -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
python_major=${python_version%%.*}
python_minor=${python_version#*.}
if (( python_major < 3 || (python_major == 3 && python_minor < NEED_PYTHON_MINOR) )); then
  echo "Python $python_version is too old for profile '$PROFILE'; need Python 3.$NEED_PYTHON_MINOR or newer." >&2
  exit 1
fi

echo "[rose] installing RoSE extras: $EXTRAS"
uv pip install --python "$PYTHON_BIN" \
  -e "$ROOT_DIR[$EXTRAS]"

install_external() {
  local label="$1" root="$2" spec="$3"
  if [[ ! -d "$root" ]]; then
    echo "[rose] $label not found at $root; skipping (set its ROSE_*_ROOT variable to enable it)"
    return 0
  fi
  if [[ ! -f "$root/pyproject.toml" && ! -f "$root/setup.py" ]]; then
    echo "[rose] $label has no pyproject.toml/setup.py at $root; keeping it source-only"
    return 0
  fi
  echo "[rose] installing $label from $root"
  uv pip install --python "$PYTHON_BIN" -e "$root$spec"
}

if (( INSTALL_EXTERNAL )); then
  case "$PROFILE" in
    sim|all)
      MANISKILL_ROOT="${ROSE_MANISKILL_ROOT:-$HOME/code/mam/ManiSkill}"
      LEROBOT_ROOT="${ROSE_LEROBOT_ROOT:-$HOME/code/mam/lerobot_mam}"
      install_external "ManiSkill" "$MANISKILL_ROOT" ""
      # The training extra includes dataset and accelerator dependencies used by
      # commands built in rose.integrations.commands.
      install_external "LeRobot" "$LEROBOT_ROOT" "[training]"
      ;;
    *)
      echo "[rose] skipping external simulator installs for profile '$PROFILE'"
      ;;
  esac
fi

if (( RUN_CHECKS )); then
  echo "[rose] running dependency check"
  uv pip check --python "$PYTHON_BIN"
  echo "[rose] checking imports and runtime metadata"
  "$PYTHON_BIN" - <<'PY'
import importlib.util
import sys

import numpy
import yaml
import rose

print(f"python={sys.version.split()[0]}")
print(f"numpy={numpy.__version__}")
print(f"pyyaml={yaml.__version__}")
print(f"rose={rose.__file__}")
if importlib.util.find_spec("torch"):
    import torch
    print(f"torch={torch.__version__} cuda_available={torch.cuda.is_available()}")
if importlib.util.find_spec("gymnasium"):
    import gymnasium
    print(f"gymnasium={gymnasium.__version__}")
PY
  echo "[rose] running tests"
  "$PYTHON_BIN" -m pytest -q
fi

cat <<EOF2

RoSE environment is ready.
Activate it with:
  source "$VENV_DIR/bin/activate"
Then use the existing scripts, for example:
  bash scripts/train_ip_maniskill.sh --dry-run
EOF2
