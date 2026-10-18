import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExternalRoots:
    maniskill: Path | None
    masked_action: Path | None
    lerobot: Path | None

    @property
    def all(self) -> tuple[Path, ...]:
        return tuple(path for path in (self.maniskill, self.masked_action, self.lerobot) if path is not None)


def resolve_roots() -> ExternalRoots:
    defaults = {
        "ROSE_MANISKILL_ROOT": "/home/hebu/code/mam/ManiSkill",
        "ROSE_MASKED_ACTION_ROOT": "/home/hebu/code/mam/Masked-Action-Model",
        "ROSE_LEROBOT_ROOT": "/home/hebu/code/mam/lerobot_mam",
    }

    def resolve(name: str) -> Path | None:
        value = os.environ.get(name, defaults[name])
        path = Path(value).expanduser()
        return path if path.exists() else None

    return ExternalRoots(
        maniskill=resolve("ROSE_MANISKILL_ROOT"),
        masked_action=resolve("ROSE_MASKED_ACTION_ROOT"),
        lerobot=resolve("ROSE_LEROBOT_ROOT"),
    )


def require_root(path: Path | None, name: str) -> Path:
    if path is None:
        raise RuntimeError(f"missing external source path: {name}")
    if not path.exists():
        raise FileNotFoundError(path)
    return path
