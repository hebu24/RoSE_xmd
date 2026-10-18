from typing import Any

from rose.envs.base import ExternalEnvAdapter


class LiberoEnvironment(ExternalEnvAdapter):
    @classmethod
    def make(cls, **kwargs: Any):
        try:
            from lerobot.envs.libero import LiberoEnv
        except ImportError as exc:
            raise ImportError("LIBERO environment requires the LeRobot integration on PYTHONPATH") from exc
        return cls(LiberoEnv(**kwargs))
