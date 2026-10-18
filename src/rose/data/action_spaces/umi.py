import numpy as np


def _finite(value, shape_tail: tuple[int, ...], name: str) -> np.ndarray:
    array = np.asarray(value, dtype=np.float64)
    if array.shape[-len(shape_tail) :] != shape_tail or not np.isfinite(array).all():
        raise ValueError(f"{name} must end with shape {shape_tail} and be finite")
    return array


def quaternion_to_matrix(quaternion: np.ndarray) -> np.ndarray:
    q = _finite(quaternion, (4,), "quaternion")
    norm = np.linalg.norm(q, axis=-1, keepdims=True)
    if np.any(norm < 1e-8):
        raise ValueError("quaternion contains a zero value")
    w, x, y, z = np.moveaxis(q / norm, -1, 0)
    matrix = np.empty(q.shape[:-1] + (3, 3), dtype=np.float64)
    matrix[..., 0, 0] = 1.0 - 2.0 * (y * y + z * z)
    matrix[..., 0, 1] = 2.0 * (x * y - z * w)
    matrix[..., 0, 2] = 2.0 * (x * z + y * w)
    matrix[..., 1, 0] = 2.0 * (x * y + z * w)
    matrix[..., 1, 1] = 1.0 - 2.0 * (x * x + z * z)
    matrix[..., 1, 2] = 2.0 * (y * z - x * w)
    matrix[..., 2, 0] = 2.0 * (x * z - y * w)
    matrix[..., 2, 1] = 2.0 * (y * z + x * w)
    matrix[..., 2, 2] = 1.0 - 2.0 * (x * x + y * y)
    return matrix


def intrinsic_xyz_to_matrix(euler: np.ndarray) -> np.ndarray:
    value = _finite(euler, (3,), "intrinsic_xyz")
    rx, ry, rz = np.moveaxis(value, -1, 0)
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    matrix = np.empty(value.shape[:-1] + (3, 3), dtype=np.float64)
    matrix[..., 0, 0] = cy * cz
    matrix[..., 0, 1] = -cy * sz
    matrix[..., 0, 2] = sy
    matrix[..., 1, 0] = sx * sy * cz + cx * sz
    matrix[..., 1, 1] = -sx * sy * sz + cx * cz
    matrix[..., 1, 2] = -sx * cy
    matrix[..., 2, 0] = -cx * sy * cz + sx * sz
    matrix[..., 2, 1] = cx * sy * sz + sx * cz
    matrix[..., 2, 2] = cx * cy
    return matrix


def matrix_to_rotation_6d(matrix: np.ndarray) -> np.ndarray:
    value = _finite(matrix, (3, 3), "rotation_matrix")
    return value[..., :2, :].reshape(value.shape[:-2] + (6,))


def rotation_6d_to_matrix(rotation: np.ndarray) -> np.ndarray:
    value = _finite(rotation, (6,), "rotation_6d")
    first, second = value[..., :3], value[..., 3:]
    norm_first = np.linalg.norm(first, axis=-1, keepdims=True)
    if np.any(norm_first < 1e-6):
        raise ValueError("rotation_6d contains a degenerate first row")
    first = first / norm_first
    second = second - np.sum(first * second, axis=-1, keepdims=True) * first
    norm_second = np.linalg.norm(second, axis=-1, keepdims=True)
    if np.any(norm_second < 1e-6):
        raise ValueError("rotation_6d rows are collinear")
    second = second / norm_second
    third = np.cross(first, second)
    return np.stack((first, second, third), axis=-2)


def absolute_to_relative_umi(action: np.ndarray, anchor: np.ndarray) -> np.ndarray:
    value = _finite(action, (7,), "absolute_action")
    base = _finite(anchor, (7,), "anchor_pose")
    base_rotation = quaternion_to_matrix(base[..., 3:])
    target_rotation = intrinsic_xyz_to_matrix(value[..., 3:6])
    position = np.einsum("...ji,...j->...i", base_rotation, value[..., :3] - base[..., :3])
    rotation = np.einsum("...ji,...jk->...ik", base_rotation, target_rotation)
    return np.concatenate((position, matrix_to_rotation_6d(rotation), value[..., 6:7]), axis=-1).astype(np.float32)


def relative_umi_to_absolute(action: np.ndarray, anchor: np.ndarray) -> np.ndarray:
    value = _finite(action, (10,), "relative_umi_action")
    base = _finite(anchor, (7,), "anchor_pose")
    base_rotation = quaternion_to_matrix(base[..., 3:])
    relative_rotation = rotation_6d_to_matrix(value[..., 3:9])
    position = base[..., :3] + np.einsum("...ij,...j->...i", base_rotation, value[..., :3])
    rotation = np.einsum("...ij,...jk->...ik", base_rotation, relative_rotation)
    return np.concatenate((position, matrix_to_intrinsic_xyz(rotation), value[..., 9:10]), axis=-1).astype(np.float32)


def matrix_to_intrinsic_xyz(matrix: np.ndarray) -> np.ndarray:
    value = _finite(matrix, (3, 3), "rotation_matrix")
    ry = np.arcsin(np.clip(value[..., 0, 2], -1.0, 1.0))
    regular = np.abs(np.cos(ry)) > 1e-7
    rx = np.where(regular, np.arctan2(-value[..., 1, 2], value[..., 2, 2]), np.arctan2(value[..., 2, 1], value[..., 1, 1]))
    rz = np.where(regular, np.arctan2(-value[..., 0, 1], value[..., 0, 0]), 0.0)
    return np.stack((rx, ry, rz), axis=-1).astype(np.float32)


def expand_map_mask_to_umi(mask: np.ndarray) -> np.ndarray:
    source = np.asarray(mask) > 0.5
    if source.shape[-1] != 7:
        raise ValueError("MAP mask must have seven action dimensions")
    position = source[..., :3]
    rotation = source[..., 3:6]
    if np.any(np.any(position, axis=-1) != np.all(position, axis=-1)):
        raise ValueError("UMI requires complete position groups")
    if np.any(np.any(rotation, axis=-1) != np.all(rotation, axis=-1)):
        raise ValueError("UMI requires complete rotation groups")
    result = np.zeros(source.shape[:-1] + (10,), dtype=np.float32)
    result[..., :3] = np.all(position, axis=-1)[..., None]
    result[..., 3:9] = np.all(rotation, axis=-1)[..., None]
    result[..., 9] = source[..., 6]
    return result
