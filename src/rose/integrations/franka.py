from pathlib import Path

from rose.integrations.imports import import_from_root


def load_training_module(root: str | Path):
    return import_from_root(root, "franka_train.train_mam_franka")


def load_umi_training_module(root: str | Path):
    return import_from_root(root, "franka_train.train_mam_franka_umi")


def load_inference_module(root: str | Path):
    return import_from_root(root, "scripts.tools.descfly_infer_mam")
