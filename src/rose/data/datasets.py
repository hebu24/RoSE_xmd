from collections.abc import Iterable, Iterator

import numpy as np

from rose.core.types import MAPWindow, Trajectory
from rose.data.masks import MaskSpec, build_mask
from rose.progress.window import build_map_window, build_progress


def iter_masked_trajectories(
    trajectories: Iterable[Trajectory],
    spec: MaskSpec,
) -> Iterator[Trajectory]:
    for trajectory in trajectories:
        actions = np.asarray(trajectory.actions, dtype=np.float32)
        masked, mask = build_mask(actions, spec, action_dim=actions.shape[-1])
        yield Trajectory(
            actions=masked,
            observations=trajectory.observations,
            progress=trajectory.progress,
            metadata={**trajectory.metadata, "action_mask": mask},
        )


def make_window(
    trajectory: Trajectory,
    current_progress: float,
    backward: int,
    forward: int,
) -> MAPWindow:
    actions = np.asarray(trajectory.actions, dtype=np.float32)
    mask = np.asarray(trajectory.metadata.get("action_mask", np.ones_like(actions, dtype=bool)))
    progress = build_progress(len(actions)) if trajectory.progress is None else trajectory.progress
    return build_map_window(actions, mask, progress, current_progress, backward, forward)
