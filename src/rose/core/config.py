from pathlib import Path
from typing import Any

import yaml


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path).expanduser().resolve()
    with config_path.open() as handle:
        current = yaml.safe_load(handle) or {}
    merged: dict[str, Any] = {}
    for default in current.pop("defaults", []):
        default_path = (config_path.parent / default).with_suffix(".yaml")
        merged = _merge(merged, load_config(default_path))
    return _merge(merged, current)
