from pathlib import Path

from rose.integrations.imports import import_from_root


def load_dataset_class(root: str | Path):
    module = import_from_root(Path(root) / "src", "lerobot.datasets.lerobot_dataset")
    return module.LeRobotDataset


def load_mam_policy(root: str | Path):
    module = import_from_root(Path(root) / "src", "lerobot.policies.mam.modeling_mam")
    return module.MamPolicy
