import sys
from argparse import Namespace

from countries_info.src.countries_info_service import get_random_countries_info
from countries_info.src.random_data_client import RandomDataClient
from countries_info.src.rest_countries_client import RestCountriesClient

NUM_COUNTRIES_MIN = 5
NUM_COUNTRIES_MAX = 20


def create_random_countries_info_report(
    arguments: Namespace,
) -> None:
    report = get_random_countries_info(
        arguments.num_countries,
        RandomDataClient(),
        RestCountriesClient(),
    )

    for country_name, country_info in report:
        if country_info:
            print(country_name)
            print(f"\tCapital: {', '.join(country_info.capital)}")
            print(f"\tLanguages: {', '.join(country_info.languages)}")
            print(f"\tPopulation: {country_info.population}\n")
        else:
            print(f"{country_name} - No information found!\n")


def validate_arguments(args: Namespace) -> None:
    if not (NUM_COUNTRIES_MIN <= args.num_countries <= NUM_COUNTRIES_MAX):
        print(
            f"num_countries must be between {NUM_COUNTRIES_MIN} and {NUM_COUNTRIES_MAX}"
        )
        sys.exit(1)
