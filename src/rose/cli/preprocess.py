
import argparse

from rose.cli.common import parse_values, parser, run_command, verify_policy
from rose.integrations.commands import build_preprocess_command


def main() -> None:
    args = parser("rose-preprocess", "Prepare a platform dataset for ROSE.").parse_args()
    config, env = parse_values(args)
    verify_policy(config)
    command = build_preprocess_command(config["platform"])
    raise SystemExit(run_command(command, env, args.dry_run))


if __name__ == "__main__":
    main()
