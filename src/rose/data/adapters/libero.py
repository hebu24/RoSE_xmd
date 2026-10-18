from pathlib import Path

from rose.core.types import Trajectory


class LiberoDatasetAdapter:
    platform = "libero"

    def __init__(self, root: str | Path):
        self.root = Path(root)

    def load(self, split: str = "train") -> list[Trajectory]:
        del split
        raise NotImplementedError("LIBERO loading requires the LeRobot integration.")
