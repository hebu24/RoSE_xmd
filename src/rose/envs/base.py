from collections.abc import Mapping
from typing import Any

from rose.core.types import Observation


def _observation(value: Any) -> Observation:
    if isinstance(value, Observation):
        return value
    if isinstance(value, Mapping):
        state = value.get("state", value.get("agent_pos"))
        images = {str(key): item for key, item in value.items() if "image" in str(key)}
        return Observation(images=images, state=state)
    return Observation(state=value)


class ExternalEnvAdapter:
    def __init__(self, env: Any):
        self.env = env

    def reset(self, seed: int | None = None) -> Observation:
        result = self.env.reset(seed=seed) if seed is not None else self.env.reset()
        return _observation(result[0] if isinstance(result, tuple) else result)

    def step(self, action: Any):
        result = self.env.step(action)
        if len(result) == 5:
            observation, reward, terminated, truncated, info = result
            done = bool(terminated or truncated)
        else:
            observation, reward, done, info = result
        return _observation(observation), float(reward), done, info

    def close(self) -> None:
        self.env.close()
