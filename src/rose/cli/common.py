import argparse
import os
from pathlib import Path

import yaml

from rose.core.config import load_config
from rose.integrations.commands import ExternalCommand


def parser(prog: str, description: str) -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog=prog, description=description)
    result.add_argument("--config", required=True)
    result.add_argument("--dry-run", action="store_true")
    result.add_argument("--set", action="append", default=[])
    return result


def parse_values(args: argparse.Namespace) -> tuple[dict, dict[str, str]]:
    config_path = Path(args.config).expanduser().resolve()
    config = load_config(config_path)
    overrides: dict[str, str] = {}
    for item in args.set:
        if "=" not in item:
            raise ValueError(f"--set expects key=value, got {item!r}")
        key, value = item.split("=", 1)
        overrides[key] = value
        target = config
        parts = key.split(".")
        for part in parts[:-1]:
            target = target.setdefault(part, {})
        target[parts[-1]] = yaml.safe_load(value)
    env = {f"ROSE_CONFIG_{key.upper().replace('.', '_')}": value for key, value in overrides.items()}
    env.update(_legacy_env(config))
    env.update({key.upper(): value for key, value in overrides.items() if key.isidentifier()})
    env["ROSE_CONFIG_PATH"] = str(config_path)
    env["ROSE_PLATFORM"] = str(config.get("platform", ""))
    env["ROSE_POLICY_NAME"] = str(config.get("policy", {}).get("name", "IP"))
    return config, env


def _legacy_env(config: dict) -> dict[str, str]:
    data = config.get("data", {})
    action = config.get("action", {})
    policy = config.get("policy", {})
    map_config = config.get("map", {})
    window = map_config.get("window", {})
    environment = config.get("environment", {})
    values = {
        "RAW_DEMO_H5": data.get("raw_demo_h5"),
        "RAW_DEMO_JSON": data.get("raw_demo_json"),
        "PREPROCESSED_ROOT_DIR": data.get("prepared_dir"),
        "ACTION_DIM": action.get("dim"),
        "OBS_HORIZON": policy.get("obs_horizon"),
        "ACT_HORIZON": policy.get("action_horizon"),
        "PRED_HORIZON": policy.get("horizon"),
        "MAS_SHORT_WINDOW_HORIZON": window.get("short_horizon"),
        "MAS_LONG_BACKWARD_LENGTH": window.get("long_backward"),
        "MAS_LONG_FORWARD_LENGTH": window.get("long_forward"),
        "CONTROL_MODE": environment.get("control_mode"),
        "OBS_MODE": environment.get("obs_mode"),
    }
    if map_config.get("mask_types"):
        values["MASK_TYPE_LIST"] = str(map_config["mask_types"])
    if map_config.get("mask_ratios"):
        values["MASK_RATIO_LIST"] = str(map_config["mask_ratios"])
    return {key: str(value) for key, value in values.items() if value is not None}


def verify_policy(config: dict) -> None:
    if config.get("project", {}).get("name") != "rose":
        raise ValueError("project.name must be rose")
    if config.get("map", {}).get("interface") != "MAP":
        raise ValueError("map.interface must be MAP")
    if config.get("policy", {}).get("name") != "IP":
        raise ValueError("policy.name must be IP")


def run_command(command: ExternalCommand, env: dict[str, str], dry_run: bool) -> int:
    from rose.runtimes.launcher import launch

    return launch(command, env, dry_run)
