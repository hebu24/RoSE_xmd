import numpy as np

from rose.data.transforms import ActionRepresentation, to_map


def test_relative_cartesian_to_map_uses_anchor():
    value = np.array([[1, 2, 3, 0.1, 0.2, 0.3, 1]], dtype=np.float32)
    anchor = np.array([10, 20, 30, 0.4, 0.5, 0.6, 0], dtype=np.float32)
    result = to_map(value, ActionRepresentation.RELATIVE_CARTESIAN, anchor)
    assert np.allclose(result[0, :6], [11, 22, 33, 0.5, 0.7, 0.9])
