from typing import Any

from rose.envs.base import ExternalEnvAdapter


class FrankaEnvironment(ExternalEnvAdapter):
    def __init__(self, env: Any):
        super().__init__(env)
