# -*- encoding:utf-8 -*-

import pytest
from pytest_mark_checker import MarkChecker

pytest_plugins = ['helpers_namespace']


@pytest.helpers.register
def assert_lines(expected, observed):
    e = [str(string) for string in expected]
    o = [str(string) for string in observed]
    e.sort()
    o.sort()
    assert e == o


@pytest.yield_fixture(autouse=True)
def run_around_tests():
    MarkChecker.pytest_marks = dict.fromkeys(["pytest_mark{}".format(x) for x in range(1, 50)], {})
    yield
