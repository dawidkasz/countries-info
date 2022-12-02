from argparse import Namespace

import pytest

from countries_info.src.cli import (NUM_COUNTRIES_MAX, NUM_COUNTRIES_MIN,
                                    validate_arguments)


def test_validate_arguments_valid():
    args = Namespace(num_countries=(NUM_COUNTRIES_MIN + NUM_COUNTRIES_MAX) // 2)

    assert validate_arguments(args) is None


def test_validate_arguments_too_small():
    args = Namespace(num_countries=NUM_COUNTRIES_MIN - 1)

    with pytest.raises(SystemExit):
        assert validate_arguments(args)


def test_validate_arguments_too_big():
    args = Namespace(num_countries=NUM_COUNTRIES_MAX + 1)

    with pytest.raises(SystemExit):
        assert validate_arguments(args)
