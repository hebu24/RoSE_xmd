from dataclasses import dataclass
import numpy as np


ACTION_DIM = 7
MASKED_VALUE = 0.0
CANONICAL_MASK_TYPES = {
    "none",
    "full",
    "keypoint_2d",
    "keypoint_3d",
    "flow_2d",
    "flow_3d",
    "keypose",
    "orientation",
    "gripper",
    "random",
    "mix0",
    "single_keypose",
    "temporal_hole",
    "autoregressive_prefix",
}
MASK_TYPE_ALIASES = {
    "2D_trajectory": "flow_2d",
    "local_planner": "temporal_hole",
    "points": "keypoint_2d",
    "3D_points": "keypoint_3d",
    "pose_motion_planning": "keypose",
    "random_mask": "random",
    "pose_AnyGrasp": "single_keypose",
    "auto_regressive": "autoregressive_prefix",
}


@dataclass(frozen=True)
class MaskSpec:
    mask_type: str
    retain_ratio: float = 1.0
    seed: int = 0
    masked_value: float = MASKED_VALUE

    def canonical_type(self) -> str:
        return canonical_mask_type(self.mask_type)


def canonical_mask_type(mask_type: str) -> str:
    value = MASK_TYPE_ALIASES.get(str(mask_type), str(mask_type))
    if value not in CANONICAL_MASK_TYPES:
        raise ValueError(f"unsupported MAP mask type: {mask_type}")
    return value


def _selected_rows(length: int, ratio: float, rng: np.random.Generator) -> np.ndarray:
    count = int(length * ratio)
    indices = np.arange(length, dtype=np.int64)
    rng.shuffle(indices)
    return indices[:count]


def _segment(length: int, ratio: float, rng: np.random.Generator) -> slice:
    count = max(1, int(length * ratio))
    start = int(rng.integers(0, length - count + 1))
    return slice(start, start + count)


def build_mask(
    actions: np.ndarray,
    spec: MaskSpec,
    action_dim: int = ACTION_DIM,
    rng: np.random.Generator | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(actions, dtype=np.float32)
    if action_dim not in (6, 7):
        raise ValueError("MAP masking expects 6 or 7 Cartesian dimensions; convert other representations first")
    if values.ndim != 2 or values.shape[1] != action_dim or not np.isfinite(values).all():
        raise ValueError(f"actions must have shape (T, {action_dim})")
    mask_type = spec.canonical_type()
    if mask_type not in {"none", "full", "mix0", "single_keypose", "autoregressive_prefix"}:
        if not 0.0 <= float(spec.retain_ratio) <= 1.0:
            raise ValueError("retain_ratio must be in [0, 1]")
    if mask_type == "gripper" and action_dim != 7:
        raise ValueError("gripper masks require a gripper dimension")
    mask = np.zeros(values.shape, dtype=bool)
    rng = np.random.default_rng(spec.seed) if rng is None else rng
    if mask_type == "none":
        return np.full_like(values, spec.masked_value), mask
    if mask_type == "full":
        mask[...] = True
    elif len(values) == 0:
        pass
    elif mask_type == "keypoint_2d":
        mask[_selected_rows(len(values), spec.retain_ratio, rng), :2] = True
    elif mask_type == "keypoint_3d":
        mask[_selected_rows(len(values), spec.retain_ratio, rng), :3] = True
    elif mask_type == "flow_2d":
        if spec.retain_ratio > 0:
            mask[_segment(len(values), spec.retain_ratio, rng), :2] = True
    elif mask_type == "flow_3d":
        if spec.retain_ratio > 0:
            mask[_segment(len(values), spec.retain_ratio, rng), :3] = True
    elif mask_type == "keypose":
        mask[_selected_rows(len(values), spec.retain_ratio, rng), :] = True
    elif mask_type == "orientation":
        mask[_selected_rows(len(values), spec.retain_ratio, rng), 3:6] = True
    elif mask_type == "gripper":
        mask[_selected_rows(len(values), spec.retain_ratio, rng), 6] = True
    elif mask_type == "random":
        indices = _selected_rows(values.size, spec.retain_ratio, rng)
        mask.reshape(-1)[indices] = True
    elif mask_type == "mix0":
        if len(values) < 4:
            raise ValueError("mix0 requires at least four reference locations")
        indices = np.arange(len(values))
        rng.shuffle(indices)
        mask[:, :2] = True
        mask[indices[0], :] = True
        mask[indices[1:4], :3] = True
    elif mask_type == "single_keypose":
        indices = np.arange(len(values))
        rng.shuffle(indices)
        mask[indices[0], :] = True
    elif mask_type == "temporal_hole":
        mask[...] = True
        if spec.retain_ratio > 0:
            mask[_segment(len(values), spec.retain_ratio, rng), :] = False
    elif mask_type == "autoregressive_prefix":
        row = int(rng.integers(0, len(values)))
        column = int(rng.integers(0, action_dim))
        mask[:row, :] = True
        mask[row, :column] = True
    masked = np.full_like(values, spec.masked_value)
    masked[mask] = values[mask]
    return masked, mask


def compose_masks(
    actions: np.ndarray,
    specs: list[MaskSpec],
    action_dim: int = ACTION_DIM,
) -> tuple[np.ndarray, np.ndarray]:
    if not specs:
        return build_mask(actions, MaskSpec("none"), action_dim)
    values = np.asarray(actions, dtype=np.float32)
    merged = np.zeros(values.shape, dtype=bool)
    for spec in specs:
        _, current = build_mask(values, spec, action_dim)
        merged |= current
    masked = np.full_like(values, MASKED_VALUE)
    masked[merged] = values[merged]
    return masked, merged
