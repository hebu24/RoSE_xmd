
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="rose-train")
    parser.add_argument("--config", required=True)
    parser.parse_known_args()
    raise NotImplementedError("Training CLI will be implemented after framework review.")


if __name__ == "__main__":
    main()
