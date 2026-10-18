
import argparse

from rose.cli.common import parse_values, parser, run_command, verify_policy
from rose.integrations.commands import build_train_command


def main() -> None:
    args = parser("rose-train", "Train the ROSE IP policy.").parse_args()
    config, env = parse_values(args)
    verify_policy(config)
    command = build_train_command(config["platform"])
    raise SystemExit(run_command(command, env, args.dry_run))


if __name__ == "__main__":
    main()
