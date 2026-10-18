import numpy as np

from rose.data.masks import MaskSpec, build_mask
from rose.progress.window import build_map_window


def test_keypoint_3d_mask_preserves_only_pose_position():
    actions = np.arange(35, dtype=np.float32).reshape(5, 7)
    values, mask = build_mask(actions, MaskSpec("keypoint_3d", retain_ratio=0.4, seed=1))
    assert mask.shape == actions.shape
    assert mask[:, 3:].sum() == 0
    assert np.array_equal(values[mask], actions[mask])
    assert np.all(values[~mask] == 0.0)


def test_map_window_uses_progress_and_boundary_validity():
    values = np.arange(28, dtype=np.float32).reshape(4, 7)
    mask = np.ones_like(values, dtype=bool)
    progress = np.linspace(0.0, 1.0, 4)
    window = build_map_window(values, mask, progress, 0.0, backward=2, forward=2)
    assert window.center_index == 0
    assert window.values.shape == (4, 7)
    assert window.valid.tolist() == [False, False, True, True]
