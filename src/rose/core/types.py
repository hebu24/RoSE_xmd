from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class ActionSpec:
    dim: int = 7
    pose_dims: tuple[int, ...] = (0, 1, 2, 3, 4, 5)
    gripper_dim: int = 6


@dataclass
class Trajectory:
    actions: Any
    observations: Mapping[str, Any] = field(default_factory=dict)
    progress: Any | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MAPWindow:
    values: Any
    mask: Any
    progress: Any
    valid: Any
    start_index: int
    center_index: int


@dataclass
class Observation:
    images: Mapping[str, Any] = field(default_factory=dict)
    state: Any | None = None
    task: str | None = None


@dataclass
class ProgressEstimate:
    value: float
    confidence: float | None = None
