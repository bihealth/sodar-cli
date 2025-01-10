"""Test the main function."""

import pytest

from sodar_cli.__main__ import main


def test_no_args():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main([])
    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 1
