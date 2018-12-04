# -*- coding: utf-8 -*-

# args to only use checks that raise an 'M' prefixed error
extra_args = ['--select', 'M']

config = r"""
[flake8]
pytest_mark1 = name=jira,value_regex=[a-zA-Z]*-\d*,allow_multiple_args=true

"""


def test_with_valid_test_id_marks(flake8dir):
    flake8dir.make_setup_cfg(config)
    flake8dir.make_example_py("""
@pytest.mark.jira('ASC-123', 'ASC-124', 'ASC-125')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_with_invalid_test_id_mark(flake8dir):
    flake8dir.make_setup_cfg(config)
    flake8dir.make_example_py("""
@pytest.mark.jira('ASC-123', 'not_good', 'ASC-125')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == ["./example.py:1:1: M601 the mark values '['not_good']' do not match the configuration specified by pytest_mark1, Configured regex: '[a-zA-Z]*-\\d*'"]  # noqa


def test_with_multiple_invalid_test_id_mark(flake8dir):
    flake8dir.make_setup_cfg(config)
    flake8dir.make_example_py("""
@pytest.mark.jira('bad', 'not_good', 'really bad')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == ["./example.py:1:1: M601 the mark values '['bad', 'not_good', 'really bad']' do not match the configuration specified by pytest_mark1, Configured regex: '[a-zA-Z]*-\\d*'"]  # noqa


def test_mark_with_ast_call(flake8dir):
    config = r"""
[flake8]
pytest_mark1 = name=jira,value_regex=[a-zA-Z]*-\d*,allow_multiple_args=true
pytest_mark3 = name=test_case_with_steps
    """
    flake8dir.make_setup_cfg(config)
    flake8dir.make_example_py("""
@pytest.mark.jira("JIRA-123")
@pytest.mark.test_case_with_steps()
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_mark_with_ast_attr(flake8dir):
    config = r"""
[flake8]
pytest_mark1 = name=jira,value_regex=[a-zA-Z]*-\d*,allow_multiple_args=true
pytest_mark3 = name=test_case_with_steps
    """
    flake8dir.make_setup_cfg(config)
    flake8dir.make_example_py("""
@pytest.mark.jira("JIRA-123")
@pytest.mark.test_case_with_steps
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


# This test gets tricky now that we're checking for for the existence of a
# value anytime we have a regex (test_mark_with_regex_and_no_arg).
# For this test, since non-string args get dropped, we won't see any values
# even though we see a validator. As a result, we'll get an additional failure
# for the lack of argument along with the the non-string error.
def test_values_that_are_not_strings(flake8dir):
    flake8dir.make_setup_cfg(config)
    flake8dir.make_example_py("""
@pytest.mark.jira(['ASC-123', 'ASC-124', 'ASC-125'])
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    err1 = "./example.py:1:1: M601 the mark values '['']' do " + \
           "not match the configuration specified by pytest_mark1, " + \
           "Validation supplied, but values absent."
    err2 = u'./example.py:1:1: M701 mark values must be strings'
    expected_results = [err1, err2]
    assert result.out_lines == expected_results


def test_multiple_values_that_are_not_strings(flake8dir):
    flake8dir.make_setup_cfg(config)
    flake8dir.make_example_py("""
@pytest.mark.jira('ASC-432', ['ASC-123', 'ASC-124'], 'RE-234')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == [u'./example.py:1:1: M701 mark values must be strings']


def test_mark_with_regex_and_no_arg(flake8dir):
    config = r"""
[flake8]
pytest_mark1 = name=jira,value_regex=[a-zA-Z]*-\d*,allow_multiple_args=true
    """
    flake8dir.make_setup_cfg(config)
    flake8dir.make_example_py("""
@pytest.mark.jira()
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    expected_result = "./example.py:1:1: M601 the mark values '['']' do " + \
                      "not match the configuration specified by pytest_mark1, " + \
                      "Validation supplied, but values absent."
    assert result.out_lines == [expected_result]
