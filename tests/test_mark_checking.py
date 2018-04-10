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


def test_functions_that_are_not_tests(flake8dir):
    flake8dir.make_example_py("""
def not_a_test():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_different_mark(flake8dir):
    flake8dir.make_example_py("""
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
@pytest.mark.foo('bar')
def test_mark_we_dont_care_about():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_a_skipped_test(flake8dir):
    flake8dir.make_example_py("""
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
@pytest.mark.skip(reason='Need implementation')
def test_a_test_we_will_skip():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_a_mark_with_parametrize(flake8dir):
    flake8dir.make_example_py("""
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
@pytest.mark.parametrize(("n", "expected"), [
    (1, 2),
    pytest.mark.bar((1, 3)),
    (2, 3),
])
def test_a_parametrized_mark():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_try_first(flake8dir):
    flake8dir.make_example_py("""
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
@pytest.mark.tryfirst
def test_a_try_first_mark():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_xfail(flake8dir):
    flake8dir.make_example_py("""
@pytest.mark.xfail(True, reason=None, run=True, raises=None, strict=False)
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
def test_a_xfail_mark():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_usefixtures(flake8dir):
    flake8dir.make_example_py("""
@pytest.mark.usefixtures(fixturename1, fixturename2)
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
def test_a_usefixture_mark():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_dont_validate_one_of_many(flake8dir):
    flake8dir.make_example_py("""
@pytest.mark.foo
@pytest.mark.skip(reason='Need implementation')
@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
@pytest.mark.parametrize(("n", "expected"), [
    (1, 2),
    pytest.mark.bar((1, 3)),
    (2, 3),
])
def test_a_parametrized_mark():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == []


def test_do_validate_one_of_many(flake8dir):
    flake8dir.make_example_py("""
@pytest.mark.foo
@pytest.mark.skip(reason='Need implementation')
@pytest.mark.parametrize(("n", "expected"), [
    (1, 2),
    pytest.mark.bar((1, 3)),
    (2, 3),
])
def test_a_parametrized_mark():
    pass
    """)
    result = flake8dir.run_flake8(extra_args)
    assert result.out_lines == ['./example.py:1:1: M501 test definition not marked with test_id']
