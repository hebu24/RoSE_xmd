from enum import Enum


class ActionRepresentation(str, Enum):
    MAP = "map_7d"
    RELATIVE_CARTESIAN = "relative_cartesian_7d"
    UMI = "umi_10d"
    ABS6D = "absolute_6d_10d"


def validate_representation(values, representation: ActionRepresentation) -> None:
    expected = {
        ActionRepresentation.MAP: 7,
        ActionRepresentation.RELATIVE_CARTESIAN: 7,
        ActionRepresentation.UMI: 10,
        ActionRepresentation.ABS6D: 10,
    }[representation]
    if values.shape[-1] != expected:
        raise ValueError(f"{representation.value} expects action dimension {expected}")


def to_map(values, representation: ActionRepresentation, anchor=None):
    import numpy as np

    array = np.asarray(values, dtype=np.float32)
    validate_representation(array, representation)
    if representation is ActionRepresentation.MAP:
        return array
    if anchor is None:
        raise ValueError(f"{representation.value} conversion requires an anchor pose")
    if representation is ActionRepresentation.RELATIVE_CARTESIAN:
        if np.asarray(anchor).shape[-1] != 7:
            raise ValueError("relative Cartesian conversion requires a 7D anchor pose")
        result = array.copy()
        result[..., :3] += np.asarray(anchor)[..., :3]
        result[..., 3:6] += np.asarray(anchor)[..., 3:6]
        return result
    raise NotImplementedError(f"conversion from {representation.value} is platform-specific")
