#!/usr/bin/env bash
set -eu
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
exec python -m rose.cli.infer --config "$ROOT_DIR/configs/real/franka.yaml" "$@"
