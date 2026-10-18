import numpy as np


def split_indices(length: int, validation_ratio: float = 0.1, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    if length < 1 or not 0.0 <= validation_ratio < 1.0:
        raise ValueError("length must be positive and validation_ratio must be in [0, 1)")
    indices = np.arange(length)
    np.random.default_rng(seed).shuffle(indices)
    count = int(length * validation_ratio)
    return indices[count:], indices[:count]
