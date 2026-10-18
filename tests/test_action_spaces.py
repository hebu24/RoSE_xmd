import numpy as np

from rose.data.action_spaces.abs6d import absolute_abs6d_to_euler, absolute_euler_to_abs6d
from rose.data.action_spaces.umi import absolute_to_relative_umi, relative_umi_to_absolute


def test_abs6d_round_trip():
    action = np.array([[0.2, -0.1, 0.4, 0.1, -0.2, 0.3, 0.7]], dtype=np.float32)
    converted = absolute_euler_to_abs6d(action)
    restored = absolute_abs6d_to_euler(converted)
    assert np.allclose(restored, action, atol=1e-5)


def test_umi_identity_anchor_round_trip():
    action = np.array([[0.2, -0.1, 0.4, 0.1, -0.2, 0.3, 0.7]], dtype=np.float32)
    anchor = np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], dtype=np.float32)
    relative = absolute_to_relative_umi(action, anchor)
    restored = relative_umi_to_absolute(relative, anchor)
    assert np.allclose(restored, action, atol=1e-5)
