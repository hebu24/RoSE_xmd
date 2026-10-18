
import argparse

from rose.cli.common import parse_values, parser, run_command, verify_policy
from rose.integrations.commands import build_infer_command


def main() -> None:
    args = parser("rose-infer", "Run ROSE IP inference.").parse_args()
    config, env = parse_values(args)
    verify_policy(config)
    command = build_infer_command(config["platform"])
    raise SystemExit(run_command(command, env, args.dry_run))


if __name__ == "__main__":
    main()
