from typing import Any

from rose.envs.base import ExternalEnvAdapter


class ManiSkillEnvironment(ExternalEnvAdapter):
    @classmethod
    def make(cls, env_id: str, **kwargs: Any):
        import gymnasium as gym

        return cls(gym.make(env_id, **kwargs))
