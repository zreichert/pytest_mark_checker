# -*- coding: utf-8 -*-

# ======================================================================================================================
# imports
# ======================================================================================================================
import pytest

# ======================================================================================================================
# Globals
# ======================================================================================================================
# args to only use checks that raise an 'M' prefixed error
extra_args = ['--select', 'M']


# ======================================================================================================================
# Tests
# ======================================================================================================================
def test_duplicate_value_in_same_file(flake8dir, mocker):
    """Verify that rule3xx violations are reported when the same value is repeated for marks declared to be unqiue
    within a single file.
    """

    # Setup
    flake8dir.make_setup_cfg("""
        [flake8]
        pytest_mark1 = name=test,allow_duplicate=true,enforce_unique_value=true
    """)
    flake8dir.make_example_py("""
        @pytest.mark.test('Unique!')
        def test_unique():
            pass

        @pytest.mark.test('Unique!')
        def test_not_unique():
            pass
    """)

    # Mock
    mocker.patch.dict('flake8_pytest_mark.rules._unique_value_collision_map', {})   # Need to ensure cache cleared.

    # Expectations
    exp_out_lines = ["./example.py:5:1: M301 @pytest.mark.test value is not unique! "
                     "The 'Unique!' mark value already specified for the 'test_unique' test at line '1' found in the "
                     "'./example.py' file!"]

    # Test
    result = flake8dir.run_flake8(extra_args)
    # noinspection PyUnresolvedReferences
    pytest.helpers.assert_lines(exp_out_lines, result.out_lines)


def test_duplicate_value_in_same_mark(flake8dir, mocker):
    """Verify that rule3xx violations are reported when the same value is repeated for marks declared to be unqiue
    within a multi-argument mark.
    """

    # Setup
    flake8dir.make_setup_cfg("""
        [flake8]
        pytest_mark1 = name=test,allow_duplicate=true,allow_multiple_args=true,enforce_unique_value=true
    """)
    flake8dir.make_example_py("""
        @pytest.mark.test('Unique!', 'Unique!')
        def test_not_so_unique():
            pass
    """)

    # Mock
    mocker.patch.dict('flake8_pytest_mark.rules._unique_value_collision_map', {})   # Need to ensure cache cleared.

    # Expectations
    exp_out_lines = ["./example.py:1:1: M301 @pytest.mark.test value is not unique! "
                     "The 'Unique!' mark value already specified for the 'test_not_so_unique' test at line '1' "
                     "found in the './example.py' file!"]

    # Test
    result = flake8dir.run_flake8(extra_args)
    # noinspection PyUnresolvedReferences
    pytest.helpers.assert_lines(exp_out_lines, result.out_lines)


# noinspection PyUnresolvedReferences
def test_duplicate_value_in_different_files(flake8dir, mocker):
    """Verify that rule3xx violations are reported when the same value is repeated for marks declared to be unqiue
    across different files.
    """

    # Setup
    flake8dir.make_setup_cfg("""
        [flake8]
        pytest_mark1 = name=test,enforce_unique_value=true
    """)
    flake8dir.make_py_files(
        example1="""
            @pytest.mark.test('Unique!')
            def test_unique():
                pass
        """,
        example2="""
            @pytest.mark.test('Unique!')
            def test_not_so_unique():
                pass
        """)

    # Mock
    mocker.patch.dict('flake8_pytest_mark.rules._unique_value_collision_map', {})   # Need to ensure cache cleared.

    # Expectations
    exp_out_lines = ["./example2.py:1:1: M301 @pytest.mark.test value is not unique! "
                     "The 'Unique!' mark value already specified for the 'test_unique' test at line '1' "
                     "found in the './example1.py' file!"]
    exp_out_lines_reverse = ["./example1.py:1:1: M301 @pytest.mark.test value is not unique! "
                             "The 'Unique!' mark value already specified for the 'test_not_so_unique' test at line '1' "
                             "found in the './example2.py' file!"]

    # Test
    result = flake8dir.run_flake8(extra_args)

    # Given that certain Linux distros will have Python walk directories in non-deterministic fashion the failure
    # might happen in reverse order.
    try:
        pytest.helpers.assert_lines(exp_out_lines, result.out_lines)
    except AssertionError:
        pytest.helpers.assert_lines(exp_out_lines_reverse, result.out_lines)


# noinspection PyUnresolvedReferences
def test_duplicate_values_for_multiple_rules(flake8dir, mocker):
    """Verify that rule3xx violations are reported when the same value is repeated for marks declared to be unqiue
    across different files with multiple rules.
    """

    # Setup
    flake8dir.make_setup_cfg("""
        [flake8]
        pytest_mark1 = name=test1,enforce_unique_value=true
        pytest_mark2 = name=test2,enforce_unique_value=true
    """)
    flake8dir.make_py_files(
        example1="""
            @pytest.mark.test1('Unique!')
            @pytest.mark.test2('Also quite unique!')
            def test_unique1():
                pass
            @pytest.mark.test1('Very Unique!')
            @pytest.mark.test2('Also unique!')
            def test_unique2():
                pass
        """,
        example2="""
            @pytest.mark.test1('Unique!')
            @pytest.mark.test2('Also very unique!')
            def test_unique3():
                pass
            @pytest.mark.test1('So Unique!')
            @pytest.mark.test2('Also unique!')
            def test_unique4():
                pass
        """)

    # Mock
    mocker.patch.dict('flake8_pytest_mark.rules._unique_value_collision_map', {})   # Need to ensure cache cleared.

    # Expectations
    exp_out_lines = ["./example2.py:1:1: M301 @pytest.mark.test1 value is not unique! "
                     "The 'Unique!' mark value already specified for the 'test_unique1' test at line '1' "
                     "found in the './example1.py' file!",
                     "./example2.py:5:1: M302 @pytest.mark.test2 value is not unique! "
                     "The 'Also unique!' mark value already specified for the 'test_unique2' test at line '5' "
                     "found in the './example1.py' file!"]
    exp_out_lines_reverse = ["./example1.py:1:1: M301 @pytest.mark.test1 value is not unique! "
                             "The 'Unique!' mark value already specified for the 'test_unique3' test at line '1' "
                             "found in the './example2.py' file!",
                             "./example1.py:5:1: M302 @pytest.mark.test2 value is not unique! "
                             "The 'Also unique!' mark value already specified for the 'test_unique4' test at line '5' "
                             "found in the './example2.py' file!"]

    # Test
    result = flake8dir.run_flake8(extra_args)

    # Given that certain Linux distros will have Python walk directories in non-deterministic fashion the failure
    # might happen in reverse order.
    try:
        pytest.helpers.assert_lines(exp_out_lines, result.out_lines)
    except AssertionError:
        pytest.helpers.assert_lines(exp_out_lines_reverse, result.out_lines)


def test_all_unique_values(flake8dir, mocker):
    """Verify that rule 3xx will report no violations if enabled and all marks are unique."""

    # Setup
    flake8dir.make_setup_cfg("""
        [flake8]
        pytest_mark1 = name=test1,enforce_unique_value=true
        pytest_mark2 = name=test2,enforce_unique_value=true
    """)
    flake8dir.make_py_files(
        example1="""
            @pytest.mark.test1('Unique!')
            @pytest.mark.test2('Also unique!')
            def test_unique1():
                pass
            @pytest.mark.test1('Very Unique!')
            @pytest.mark.test2('Also quite unique!')
            def test_unique2():
                pass
        """,
        example2="""
            @pytest.mark.test1('Even more Unique!')
            @pytest.mark.test2('Also much more unique!')
            def test_unique3():
                pass
            @pytest.mark.test1('So Unique!')
            @pytest.mark.test2('Much unique wow!')
            def test_unique4():
                pass
        """)

    # Mock
    mocker.patch.dict('flake8_pytest_mark.rules._unique_value_collision_map', {})   # Need to ensure cache cleared.

    # Expectations
    exp_out_lines = []

    # Test
    result = flake8dir.run_flake8(extra_args)
    # noinspection PyUnresolvedReferences
    pytest.helpers.assert_lines(exp_out_lines, result.out_lines)


def test_duplicate_values_with_rule_disabled(flake8dir, mocker):
    """Verify that repeated values do not report violations when rule3xx is disabled."""

    # Setup
    flake8dir.make_setup_cfg("""
        [flake8]
        pytest_mark1 = name=test
    """)
    flake8dir.make_py_files(
        example1="""
            @pytest.mark.test('Unique!')
            def test_unique():
                pass
        """,
        example2="""
            @pytest.mark.test('Unique!')
            def test_not_so_unique():
                pass
        """)

    # Mock
    mocker.patch.dict('flake8_pytest_mark.rules._unique_value_collision_map', {})   # Need to ensure cache cleared.

    # Expectations
    exp_out_lines = []

    # Test
    result = flake8dir.run_flake8(extra_args)
    # noinspection PyUnresolvedReferences
    pytest.helpers.assert_lines(exp_out_lines, result.out_lines)
