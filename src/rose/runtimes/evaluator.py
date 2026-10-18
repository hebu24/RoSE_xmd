from rose.integrations.commands import build_eval_command
from rose.runtimes.launcher import launch


def evaluate(config: dict, dry_run: bool = False) -> int:
    return launch(build_eval_command(config["platform"]), dry_run=dry_run)
