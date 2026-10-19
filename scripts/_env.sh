#!/usr/bin/env bash
set -eu
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
if [ -x "$ROOT_DIR/.venv/bin/python" ]; then
  export PATH="$ROOT_DIR/.venv/bin:$PATH"
fi
export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
export ROSE_MANISKILL_ROOT="${ROSE_MANISKILL_ROOT:-/home/hebu/code/mam/ManiSkill}"
export ROSE_MASKED_ACTION_ROOT="${ROSE_MASKED_ACTION_ROOT:-/home/hebu/code/mam/Masked-Action-Model}"
export ROSE_LEROBOT_ROOT="${ROSE_LEROBOT_ROOT:-/home/hebu/code/mam/lerobot_mam}"
