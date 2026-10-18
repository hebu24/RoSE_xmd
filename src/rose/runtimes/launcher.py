import os
import subprocess
from collections.abc import Mapping, Sequence

from rose.integrations.commands import ExternalCommand


def launch(command: ExternalCommand, extra_env: Mapping[str, str] | None = None, dry_run: bool = False) -> int:
    env = os.environ.copy()
    env.update(command.env)
    if extra_env:
        env.update({str(key): str(value) for key, value in extra_env.items()})
    if dry_run:
        print(" ".join(command.argv))
        return 0
    return subprocess.run(command.argv, cwd=command.cwd, env=env, check=False).returncode


def append_args(command: ExternalCommand, args: Sequence[str]) -> ExternalCommand:
    return ExternalCommand(command.argv + tuple(args), command.cwd, dict(command.env))
