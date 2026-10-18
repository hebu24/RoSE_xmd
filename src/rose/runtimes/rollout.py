from rose.integrations.commands import build_preprocess_command
from rose.runtimes.launcher import launch


def preprocess(config: dict, dry_run: bool = False) -> int:
    return launch(build_preprocess_command(config["platform"]), dry_run=dry_run)
