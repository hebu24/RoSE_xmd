
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="rose-preprocess")
    parser.add_argument("--config", required=True)
    parser.parse_known_args()
    raise NotImplementedError("Preprocess CLI will be implemented after framework review.")


if __name__ == "__main__":
    main()
