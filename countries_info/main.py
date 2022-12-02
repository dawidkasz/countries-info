from argparse import ArgumentParser

from src.cli import create_random_countries_info_report, validate_arguments


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("num_countries", type=int)

    args = parser.parse_args()
    validate_arguments(args)

    create_random_countries_info_report(args)


if __name__ == "__main__":
    main()
