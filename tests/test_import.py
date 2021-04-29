"""Test basic imports."""

import sodar_cli
from sodar_cli import __main__


def test_example():
    assert sodar_cli.__version__
    assert __main__
