# -*- encoding:utf-8 -*-

# args to only use checks that raise an 'M' prefixed error
extra_args = ['--select', 'M']


def test_with_test_id_mark(flake8dir):
    flake8dir.make_example_py("""
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_without_test_id_mark(flake8dir):
    flake8dir.make_example_py("""
def test_happy_path():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == ['./example.py:1:1: M501 test definition not marked with test_id']
