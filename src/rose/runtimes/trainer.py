from rose.integrations.commands import build_train_command
from rose.runtimes.launcher import launch


def train(config: dict, dry_run: bool = False) -> int:
    return launch(build_train_command(config["platform"]), dry_run=dry_run)
