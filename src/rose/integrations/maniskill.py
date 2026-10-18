from pathlib import Path

from rose.integrations.imports import import_from_root


def load_training_module(root: str | Path):
    return import_from_root(root, "examples.baselines.diffusion_policy_debug.train_mam")


def load_evaluation_module(root: str | Path):
    return import_from_root(root, "examples.baselines.diffusion_policy_debug.evaluate.evaluate_mam")
