import numpy as np

from rose.data.action_spaces.umi import (
    _finite,
    intrinsic_xyz_to_matrix,
    matrix_to_rotation_6d,
    rotation_6d_to_matrix,
)


def matrix_to_intrinsic_xyz(matrix: np.ndarray) -> np.ndarray:
    value = _finite(matrix, (3, 3), "rotation_matrix")
    ry = np.arcsin(np.clip(value[..., 0, 2], -1.0, 1.0))
    regular = np.abs(np.cos(ry)) > 1e-7
    rx = np.where(regular, np.arctan2(-value[..., 1, 2], value[..., 2, 2]), np.arctan2(value[..., 2, 1], value[..., 1, 1]))
    rz = np.where(regular, np.arctan2(-value[..., 0, 1], value[..., 0, 0]), 0.0)
    return np.stack((rx, ry, rz), axis=-1).astype(np.float32)


def absolute_euler_to_abs6d(action: np.ndarray) -> np.ndarray:
    value = _finite(action, (7,), "absolute_euler_action")
    rotation = intrinsic_xyz_to_matrix(value[..., 3:6])
    return np.concatenate((value[..., :3], matrix_to_rotation_6d(rotation), value[..., 6:7]), axis=-1).astype(np.float32)


def absolute_abs6d_to_euler(action: np.ndarray) -> np.ndarray:
    value = _finite(action, (10,), "absolute_abs6d_action")
    rotation = rotation_6d_to_matrix(value[..., 3:9])
    return np.concatenate((value[..., :3], matrix_to_intrinsic_xyz(rotation), value[..., 9:10]), axis=-1).astype(np.float32)


def expand_map_mask_to_abs6d(mask: np.ndarray) -> np.ndarray:
    source = np.asarray(mask) > 0.5
    if source.shape[-1] != 7:
        raise ValueError("MAP mask must have seven action dimensions")
    position = source[..., :3]
    rotation = source[..., 3:6]
    if np.any(np.any(position, axis=-1) != np.all(position, axis=-1)):
        raise ValueError("ABS6D requires complete position groups")
    if np.any(np.any(rotation, axis=-1) != np.all(rotation, axis=-1)):
        raise ValueError("ABS6D requires complete rotation groups")
    result = np.zeros(source.shape[:-1] + (10,), dtype=np.float32)
    result[..., :3] = np.all(position, axis=-1)[..., None]
    result[..., 3:9] = np.all(rotation, axis=-1)[..., None]
    result[..., 9] = source[..., 6]
    return result
