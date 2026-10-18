from collections.abc import Iterable, Mapping
from typing import Any, Protocol

from rose.core.types import MAPWindow, Observation, ProgressEstimate, Trajectory


class DatasetAdapter(Protocol):
    def load(self, split: str) -> Iterable[Trajectory]: ...


class EnvironmentAdapter(Protocol):
    def reset(self, seed: int | None = None) -> Observation: ...

    def step(self, action: Any) -> tuple[Observation, float, bool, Mapping[str, Any]]: ...

    def close(self) -> None: ...


class ProgressEstimator(Protocol):
    def estimate(self, observation: Observation) -> ProgressEstimate: ...


class PolicyBackend(Protocol):
    def predict(self, observation: Observation, window: MAPWindow) -> Any: ...
