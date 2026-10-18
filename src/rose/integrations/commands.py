import os
import sys
from dataclasses import dataclass
from pathlib import Path

from rose.integrations.paths import ExternalRoots, require_root, resolve_roots


@dataclass(frozen=True)
class ExternalCommand:
    argv: tuple[str, ...]
    cwd: Path
    env: dict[str, str]


def _python() -> str:
    return os.environ.get("ROSE_PYTHON", sys.executable)


def _script(path: Path) -> tuple[str, ...]:
    return ("bash", str(path))


def _roots(roots: ExternalRoots | None) -> ExternalRoots:
    return roots or resolve_roots()


def build_train_command(platform: str, roots: ExternalRoots | None = None) -> ExternalCommand:
    roots = _roots(roots)
    platform = platform.lower()
    if platform == "maniskill":
        root = require_root(roots.maniskill, "ROSE_MANISKILL_ROOT")
        script = root / "examples/baselines/diffusion_policy_debug/run_mam.sh"
    elif platform == "libero":
        root = require_root(roots.lerobot, "ROSE_LEROBOT_ROOT")
        return ExternalCommand(
            (_python(), "-m", "lerobot.scripts.lerobot_train_mam"),
            root,
            {"PYTHONPATH": f"{root / 'src'}:{os.environ.get('PYTHONPATH', '')}"},
        )
    elif platform == "franka":
        root = require_root(roots.masked_action, "ROSE_MASKED_ACTION_ROOT")
        script = root / "franka_train/run_train_mam_franka.sh"
    else:
        raise ValueError(f"unsupported ROSE platform: {platform}")
    if not script.is_file():
        raise FileNotFoundError(script)
    return ExternalCommand(_script(script), root, {})


def build_preprocess_command(platform: str, roots: ExternalRoots | None = None) -> ExternalCommand:
    roots = _roots(roots)
    platform = platform.lower()
    if platform == "maniskill":
        root = require_root(roots.maniskill, "ROSE_MANISKILL_ROOT")
        script = root / "examples/baselines/diffusion_policy_debug/data_preprocess/data_preprocess.py"
        return ExternalCommand((_python(), str(script)), root, {})
    if platform == "libero":
        root = require_root(roots.lerobot, "ROSE_LEROBOT_ROOT")
        return ExternalCommand(
            (_python(), "-m", "lerobot.scripts.lerobot_train_mam"),
            root,
            {"PYTHONPATH": f"{root / 'src'}:{os.environ.get('PYTHONPATH', '')}"},
        )
    if platform == "franka":
        root = require_root(roots.masked_action, "ROSE_MASKED_ACTION_ROOT")
        script = root / "franka_train/preprocess_franka_umi.py"
        if not script.is_file():
            raise FileNotFoundError(script)
        return ExternalCommand((_python(), str(script)), root, {})
    raise ValueError(f"unsupported ROSE platform: {platform}")


def build_eval_command(platform: str, roots: ExternalRoots | None = None) -> ExternalCommand:
    roots = _roots(roots)
    platform = platform.lower()
    if platform == "maniskill":
        root = require_root(roots.maniskill, "ROSE_MANISKILL_ROOT")
        script = root / "examples/baselines/diffusion_policy_debug/run_eval_inpaint.sh"
        return ExternalCommand(_script(script), root, {})
    if platform == "libero":
        root = require_root(roots.lerobot, "ROSE_LEROBOT_ROOT")
        return ExternalCommand(
            (_python(), "-m", "lerobot.scripts.lerobot_eval"),
            root,
            {"PYTHONPATH": f"{root / 'src'}:{os.environ.get('PYTHONPATH', '')}"},
        )
    if platform == "franka":
        root = require_root(roots.masked_action, "ROSE_MASKED_ACTION_ROOT")
        script = root / "franka_train/run_train_mam_franka.sh"
        return ExternalCommand(_script(script), root, {})
    raise ValueError(f"unsupported ROSE platform: {platform}")


def build_infer_command(platform: str, roots: ExternalRoots | None = None) -> ExternalCommand:
    roots = _roots(roots)
    if platform.lower() != "franka":
        raise ValueError("ROSE inference is currently implemented for franka")
    root_value = os.environ.get("ROSE_FRANKA_INFER_ROOT")
    if root_value:
        root = Path(root_value).expanduser().resolve()
    else:
        root = require_root(roots.masked_action, "ROSE_MASKED_ACTION_ROOT") / "mam-realworld-infer"
    script = root / "run_infer.sh"
    if not script.is_file():
        raise FileNotFoundError(script)
    return ExternalCommand(_script(script), root, {})
