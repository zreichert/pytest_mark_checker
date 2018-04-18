# -*- encoding:utf-8 -*-
import pytest

# args to only use checks that raise an 'M' prefixed error
extra_args = ['--select', 'M']


def test_no_configuration(flake8dir):
    flake8dir.make_example_py("""
def test_there_is_no_configuration():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    expected = ['./example.py:0:1: M401 no configuration found for pytest-mark-checker, please provide configured marks in a flake8 config']  # noqa: E501
    observed = result.out_lines
    pytest.helpers.assert_lines(expected, observed)
