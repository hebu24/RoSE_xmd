from pathlib import Path
from collections import defaultdict

import numpy as np

from rose.core.types import Trajectory


class LiberoDatasetAdapter:
    platform = "libero"

    def __init__(self, root: str | Path, repo_id: str | None = None):
        self.root = Path(root)
        self.repo_id = repo_id or self.root.name

    def load(self, split: str = "train") -> list[Trajectory]:
        del split
        try:
            from lerobot.datasets.lerobot_dataset import LeRobotDataset
        except ImportError as exc:
            raise ImportError("LIBERO loading requires the LeRobot integration on PYTHONPATH") from exc
        dataset = LeRobotDataset(self.repo_id, root=self.root, download_videos=False)
        grouped: dict[int, list[np.ndarray]] = defaultdict(list)
        for index in range(len(dataset)):
            item = dataset.get_raw_item(index)
            episode = int(item.get("episode_index", 0))
            action = item.get("action")
            if action is None:
                raise KeyError("LIBERO LeRobot dataset must contain an action field")
            grouped[episode].append(np.asarray(action, dtype=np.float32))
        return [
            Trajectory(actions=np.stack(actions), metadata={"episode_id": episode})
            for episode, actions in sorted(grouped.items())
        ]
