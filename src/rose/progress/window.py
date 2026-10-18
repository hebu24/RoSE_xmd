import numpy as np

from rose.core.types import MAPWindow


def build_map_window(
    values: np.ndarray,
    mask: np.ndarray,
    progress: np.ndarray,
    current_progress: float,
    backward: int,
    forward: int,
) -> MAPWindow:
    values_array = np.asarray(values, dtype=np.float32)
    mask_array = np.asarray(mask, dtype=bool)
    progress_array = np.asarray(progress, dtype=np.float32).reshape(-1)
    if values_array.ndim != 2 or mask_array.shape != values_array.shape:
        raise ValueError("values and mask must have the same shape (T, D)")
    if progress_array.shape[0] != values_array.shape[0]:
        raise ValueError("progress length must match MAP length")
    if backward < 0 or forward <= 0:
        raise ValueError("backward must be non-negative and forward must be positive")
    if values_array.shape[0] == 0:
        raise ValueError("MAP cannot be empty")
    center = int(np.argmin(np.abs(progress_array - float(current_progress))))
    raw_indices = np.arange(center - backward, center + forward)
    indices = np.clip(raw_indices, 0, values_array.shape[0] - 1)
    valid = (raw_indices >= 0) & (raw_indices < values_array.shape[0])
    return MAPWindow(
        values=values_array[indices].copy(),
        mask=mask_array[indices].copy(),
        progress=progress_array[indices].copy(),
        valid=valid,
        start_index=int(raw_indices[0]),
        center_index=center,
    )


def build_progress(length: int) -> np.ndarray:
    if length <= 0:
        raise ValueError("length must be positive")
    return np.linspace(0.0, 1.0, length, dtype=np.float32)
