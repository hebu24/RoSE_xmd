from pathlib import Path
from typing import Iterator

from rose.core.types import Trajectory


def _episode_sort_key(name: str) -> tuple[int, str]:
    prefix = name.removeprefix("traj_")
    return (int(prefix), name) if prefix.isdigit() else (2**63 - 1, name)


def iter_h5_trajectories(path: str | Path) -> Iterator[Trajectory]:
    import h5py

    with h5py.File(path, "r") as handle:
        names = sorted((name for name in handle if name.startswith("traj_")), key=_episode_sort_key)
        for name in names:
            group = handle[name]
            if "actions" not in group:
                continue
            actions = group["actions"][...]
            metadata = {"episode_id": name}
            if "success" in group:
                metadata["success"] = group["success"][...]
            yield Trajectory(actions=actions, metadata=metadata)


class H5DatasetAdapter:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self, split: str = "train") -> Iterator[Trajectory]:
        del split
        return iter_h5_trajectories(self.path)
