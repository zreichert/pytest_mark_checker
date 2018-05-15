# -*- coding: utf-8 -*-

import pytest

# args to only use checks that raise an 'M' prefixed error
extra_args = ['--select', 'M']

uuid_config = """
[flake8]
pytest_mark1 = name=test_id
               value_match=uuid
"""

regex_config = """
[flake8]
pytest_mark1 = name=test_id
               value_regex=^this_is_a_regex
"""

complex_config = """
[flake8]
pytest_mark1 = name=test_id
               value_regex=^this_is_a_regex
pytest_mark2 = name=test_other_id
               value_match=uuid
"""

conflicting_match = """
[flake8]
pytest_mark1 = name=test_id
               value_regex=^this_is_a_regex
               value_match=uuid
"""


def test_with_valid_uuid(flake8dir):
    flake8dir.make_setup_cfg(uuid_config)
    flake8dir.make_example_py("""
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_without_valid_uuid(flake8dir):
    flake8dir.make_setup_cfg(uuid_config)
    flake8dir.make_example_py("""
@pytest.mark.test_id('this is a bad value')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    expected = ["./example.py:1:1: M601 the mark values '['this is a bad value']' do not match the configuration specified by pytest_mark1, badly formed hexadecimal UUID string"]  # noqa: E501
    observed = result.out_lines
    pytest.helpers.assert_lines(expected, observed)


def test_regex_match(flake8dir):
    flake8dir.make_setup_cfg(regex_config)
    flake8dir.make_example_py("""
@pytest.mark.test_id('this_is_a_regex')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    observed = result.out_lines
    expected = []
    pytest.helpers.assert_lines(expected, observed)


def test_regex_does_not_match(flake8dir):
    flake8dir.make_setup_cfg(regex_config)
    flake8dir.make_example_py("""
@pytest.mark.test_id('this_should_fail')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    observed = result.out_lines
    expected = [r"./example.py:1:1: M601 the mark values '['this_should_fail']' do not match the configuration specified by pytest_mark1, Configured regex: '^this_is_a_regex'"]  # noqa: E501
    pytest.helpers.assert_lines(expected, observed)


def test_multiple_match_regex_and_uuid(flake8dir):
    flake8dir.make_setup_cfg(complex_config)
    flake8dir.make_example_py("""
@pytest.mark.test_other_id('cdd82eab-4284-11e8-bf5c-6c96cfdf5101')
@pytest.mark.test_id('this_should_fail')
def test_i_will_fail():
    pass

@pytest.mark.test_id('this_is_a_regex')
@pytest.mark.test_other_id('babe2863-4284-11e8-9eca-6c96cfdf5101fail')
def test_i_will_fail_too():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    observed = result.out_lines
    expected = [r"./example.py:1:1: M601 the mark values '['this_should_fail']' do not match the configuration specified by pytest_mark1, Configured regex: '^this_is_a_regex'",  # noqa: E501
                r"./example.py:6:1: M602 the mark values '['babe2863-4284-11e8-9eca-6c96cfdf5101fail']' do not match the configuration specified by pytest_mark2, badly formed hexadecimal UUID string"]  # noqa: E501
    pytest.helpers.assert_lines(expected, observed)


def test_mark_ignored_if_regex_supplied(flake8dir):
    flake8dir.make_setup_cfg(conflicting_match)
    flake8dir.make_example_py("""
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
def test_i_will_fail():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    observed = result.out_lines
    expected = [r"./example.py:1:1: M601 the mark values '['b360c12d-0d47-4cfc-9f9e-5d86c315b1e4']' do not match the configuration specified by pytest_mark1, Configured regex: '^this_is_a_regex'"]  # noqa: E501
    pytest.helpers.assert_lines(expected, observed)
