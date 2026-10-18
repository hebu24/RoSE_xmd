from dataclasses import dataclass

import numpy as np


@dataclass
class Normalizer:
    low: np.ndarray
    high: np.ndarray
    dimensions: tuple[int, ...]

    def __post_init__(self):
        self.low = np.asarray(self.low, dtype=np.float32)
        self.high = np.asarray(self.high, dtype=np.float32)
        self.dimensions = tuple(self.dimensions)
        if self.low.ndim != 1 or self.low.shape != self.high.shape:
            raise ValueError("normalization bounds must be matching vectors")
        if not np.isfinite(self.low).all() or not np.isfinite(self.high).all():
            raise ValueError("normalization bounds must be finite")
        if np.any(self.high < self.low):
            raise ValueError("upper bounds must not be below lower bounds")
        if len(set(self.dimensions)) != len(self.dimensions) or any(
            dim < 0 or dim >= len(self.low) for dim in self.dimensions
        ):
            raise ValueError("invalid normalization dimensions")

    def _array(self, values):
        array = np.asarray(values, dtype=np.float32)
        if array.ndim < 1 or array.shape[-1] != len(self.low):
            raise ValueError("input dimension does not match normalization bounds")
        if not np.isfinite(array).all():
            raise ValueError("normalization input must be finite")
        return array.copy()

    @classmethod
    def fit(
        cls,
        values: np.ndarray,
        dimensions: tuple[int, ...] | None = None,
        robust_margin: float = 0.0,
    ) -> "Normalizer":
        array = np.asarray(values, dtype=np.float32)
        if array.ndim < 2 or array.size == 0 or not np.isfinite(array).all():
            raise ValueError("values must be a non-empty finite array with at least two dimensions")
        dim = array.shape[-1]
        dims = tuple(range(dim)) if dimensions is None else tuple(dimensions)
        if not 0.0 <= robust_margin < 0.5:
            raise ValueError("robust_margin must be in [0, 0.5)")
        low = np.min(array, axis=tuple(range(array.ndim - 1)))
        high = np.max(array, axis=tuple(range(array.ndim - 1)))
        if robust_margin:
            low = np.quantile(array, robust_margin, axis=tuple(range(array.ndim - 1)))
            high = np.quantile(array, 1.0 - robust_margin, axis=tuple(range(array.ndim - 1)))
        return cls(low=np.asarray(low), high=np.asarray(high), dimensions=dims)

    def transform(self, values: np.ndarray) -> np.ndarray:
        array = self._array(values)
        denominator = self.high - self.low
        for dim in self.dimensions:
            if denominator[dim] <= 1e-6:
                array[..., dim] = 0.0
            else:
                clipped = np.clip(array[..., dim], self.low[dim], self.high[dim])
                array[..., dim] = 2.0 * (clipped - self.low[dim]) / denominator[dim] - 1.0
        return array

    def inverse(self, values: np.ndarray) -> np.ndarray:
        array = self._array(values)
        denominator = self.high - self.low
        for dim in self.dimensions:
            if denominator[dim] <= 1e-6:
                array[..., dim] = self.low[dim]
            else:
                array[..., dim] = 0.5 * (array[..., dim] + 1.0) * denominator[dim] + self.low[dim]
        return array
