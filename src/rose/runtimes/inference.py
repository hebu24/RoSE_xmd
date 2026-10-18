from rose.integrations.commands import build_infer_command
from rose.runtimes.launcher import launch


def infer(config: dict, dry_run: bool = False) -> int:
    return launch(build_infer_command(config["platform"]), dry_run=dry_run)
