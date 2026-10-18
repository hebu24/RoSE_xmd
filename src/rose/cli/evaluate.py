
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="rose-eval")
    parser.add_argument("--config", required=True)
    parser.parse_known_args()
    raise NotImplementedError("Evaluation CLI will be implemented after framework review.")


if __name__ == "__main__":
    main()
