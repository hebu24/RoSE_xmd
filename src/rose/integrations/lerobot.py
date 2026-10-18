from pathlib import Path

from rose.integrations.imports import import_from_root


def load_dataset_class(root: str | Path):
    return import_from_root(Path(root) / "src", "lerobot.datasets.lerobot_dataset").LeRobotDataset


def load_policy_class(root: str | Path):
    return import_from_root(Path(root) / "src", "lerobot.policies.mam.modeling_mam").MamPolicy
