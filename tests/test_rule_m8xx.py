# -*- coding: utf-8 -*-

# args to only use checks that raise an 'M' prefixed error
extra_args = ['--select', 'M']

config = """
[flake8]
pytest_mark1 = name=test_id

"""


def test_with_duplicate_marks(flake8dir):
    flake8dir.make_setup_cfg(config)
    flake8dir.make_example_py("""
@pytest.mark.test_id('there are two of me')
@pytest.mark.test_id('there are two of me')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == ['./example.py:1:1: M801 @pytest.mark.test_id may only be called once for a given test']


def test_allow_duplicate_marks_with_configuration(flake8dir):
    c = """
[flake8]
pytest_mark1 = name=test_id,allow_duplicate=true
    """
    flake8dir.make_setup_cfg(c)
    flake8dir.make_example_py("""
@pytest.mark.test_id('there are two of me')
@pytest.mark.test_id('there are two of me')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_with_duplicate_marks_config(flake8dir):
    c = """
[flake8]
pytest_mark1 = name=test_id,allow_duplicate=nope
    """
    flake8dir.make_setup_cfg(c)
    flake8dir.make_example_py("""
@pytest.mark.test_id('there are two of me')
@pytest.mark.test_id('there are two of me')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == ['./example.py:1:1: M801 @pytest.mark.test_id may only be called once for a given test']
