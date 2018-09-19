# -*- coding: utf-8 -*-

"""Tests for validating rules processing exclusions for test methods and functions. (Driven by the 'exclude_methods'
and 'exclude_functions' options.)
"""

# ======================================================================================================================
# Imports
# ======================================================================================================================
import pytest


# ======================================================================================================================
# Globals
# ======================================================================================================================
# args to only use checks that raise an 'M' prefixed error
extra_args = ['--select', 'M']


# ======================================================================================================================
# Test Suites
# ======================================================================================================================
class TestExcludeClasses(object):
    """Tests for validating the 'exclude_classes' option works as expected."""

    # Test suite variables
    config = """
[flake8]
pytest_mark1 = name=test,exclude_classes=true

"""

    def test_enable_exclude_classes_configuration(self, flake8dir):
        """Verify rules that explicitly enable the 'exclude_classes' configuration will ignore classes that are
        missing required marks.
        """

        # Setup
        flake8dir.make_setup_cfg(self.config)
        flake8dir.make_example_py("""
class TestDisabledConfiguration(object):
    pass
""")

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert [] == result.out_lines

    def test_enabled_with_class_containing_tests(self, flake8dir):
        """Verify rules that explicitly enable the 'exclude_classes' configuration will ignore classes that are
        missing required marks, but will still trigger violations on test functions contained within the class.
        """

        # Setup
        flake8dir.make_setup_cfg(self.config)
        flake8dir.make_example_py("""
class TestUnconfigured(object):
    def test_function(self):
        pass
    """)

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert ['./example.py:2:1: M501 test definition not marked with test'] == result.out_lines

    def test_unconfigured_with_class_containing_tests(self, flake8dir):
        """Verify rules that leave the 'exclude_classes' option unconfigured will trigger violations on test functions
        contained within the class as well as the class itself.
        """

        # Setup
        flake8dir.make_setup_cfg("""
[flake8]
pytest_mark1 = name=test

""")

        flake8dir.make_example_py("""
class TestUnconfigured(object):
    def test_function(self):
        pass
""")

        # Expectations
        exp_out_lines = ['./example.py:1:1: M501 test definition not marked with test',
                         './example.py:2:1: M501 test definition not marked with test']

        # Test
        result = flake8dir.run_flake8(extra_args)
        # noinspection PyUnresolvedReferences
        pytest.helpers.assert_lines(exp_out_lines, result.out_lines)


class TestExcludeFunctions(object):
    """Tests for validating the 'exclude_functions' option works as expected."""

    # Test suite variables
    config = """
[flake8]
pytest_mark1 = name=test,exclude_functions=true

"""

    def test_enable_exclude_functions_configuration(self, flake8dir):
        """Verify that a violation is not triggered on a function that is missing a required mark with the
        'exclude_functions' option set to 'true'.
        """

        # Setup
        flake8dir.make_setup_cfg(self.config)
        flake8dir.make_example_py("""
def test_exclude_function():
    pass
""")

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert [] == result.out_lines


class TestExcludeMethods(object):
    """Tests for validating the 'exclude_methods' option works as expected."""

    # Test suite variables
    config = """
[flake8]
pytest_mark1 = name=test,exclude_methods=true

"""

    def test_enable_exclude_methods_configuration(self, flake8dir):
        """Verify that a violation is not triggered on a method that is missing a required mark with the
        'exclude_methods' option set to 'true'.
        """

        # Setup
        flake8dir.make_setup_cfg(self.config)
        flake8dir.make_example_py("""
class TestExclusion(object):
    def test_exclude_method(self):
        pass
""")

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert ['./example.py:1:1: M501 test definition not marked with test'] == result.out_lines

    def test_exclude_method_with_class_properly_marked(self, flake8dir):
        """Verify that a violation is not triggered on a method that is missing a required mark with the
        'exclude_methods' option set to 'true'.
        """

        # Setup
        flake8dir.make_setup_cfg(self.config)
        flake8dir.make_example_py("""
@pytest.mark.test('Classy!')
class TestExclusion(object):
    def test_exclude_method(self):
        pass
""")

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert [] == result.out_lines

    def test_mangled_method_signature(self, flake8dir):
        """Verify that a violation is triggered on a method that is missing a required mark with the 'exclude_methods'
        option set to 'true' and the signature is mangled. (First element is not 'self')
        """

        # Setup
        flake8dir.make_setup_cfg(self.config)
        flake8dir.make_example_py("""
@pytest.mark.test('Classy!')
class TestExclusion(object):
    def test_exclude_method(me):
        pass
""")

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert ['./example.py:3:1: M501 test definition not marked with test'] == result.out_lines


class TestMixedExclusions(object):
    """Tests for validating that the various 'exclude_*' options can be combined in different fashions without
    causing surprising behavior.
    """

    example_tests = """
class TestClass(object):
    def test_method(self):
        pass

def test_function():
    pass
"""

    def test_no_exclusions_configured(self, flake8dir):
        """Verify that violations are triggered on all supported test definition types when no exclusions are configured
         and all test definitions are missing required marks.
        """

        # Setup
        flake8dir.make_setup_cfg("""
[flake8]
pytest_mark1 = name=test

""")
        flake8dir.make_example_py(self.example_tests)

        # Expectations
        exp_out_lines = ['./example.py:1:1: M501 test definition not marked with test',
                         './example.py:2:1: M501 test definition not marked with test',
                         './example.py:5:1: M501 test definition not marked with test']

        # Test
        result = flake8dir.run_flake8(extra_args)
        # noinspection PyUnresolvedReferences
        pytest.helpers.assert_lines(exp_out_lines, result.out_lines)

    def test_all_exclusions_configured(self, flake8dir):
        """Verify that no violations are triggered on all supported test definition types when all exclusions are
        configured and all test definitions are missing required marks.
        """

        # Setup
        flake8dir.make_setup_cfg("""
[flake8]
pytest_mark1 = name=test,
               exclude_classes=true,
               exclude_methods=true,
               exclude_functions=true

""")
        flake8dir.make_example_py(self.example_tests)

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert [] == result.out_lines

    def test_classes_and_methods_excluded(self, flake8dir):
        """Verify that only test function definition violations are triggered when 'exclude_classes' and
        'exclude_methods' are configured and all test definitions are missing required marks.
        """

        # Setup
        flake8dir.make_setup_cfg("""
[flake8]
pytest_mark1 = name=test,
               exclude_classes=true,
               exclude_methods=true,
               exclude_functions=false

""")
        flake8dir.make_example_py(self.example_tests)

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert ['./example.py:5:1: M501 test definition not marked with test'] == result.out_lines

    def test_classes_and_functions_excluded(self, flake8dir):
        """Verify that only test function definition violations are triggered when 'exclude_classes' and
        'exclude_functions' are configured and all test definitions are missing required marks.
        """

        # Setup
        flake8dir.make_setup_cfg("""
[flake8]
pytest_mark1 = name=test,
               exclude_classes=true,
               exclude_methods=false,
               exclude_functions=true

""")
        flake8dir.make_example_py(self.example_tests)

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert ['./example.py:2:1: M501 test definition not marked with test'] == result.out_lines

    def test_methods_and_functions_excluded(self, flake8dir):
        """Verify that only test function definition violations are triggered when 'exclude_methods' and
        'exclude_functions' are configured and all test definitions are missing required marks.
        """

        # Setup
        flake8dir.make_setup_cfg("""
[flake8]
pytest_mark1 = name=test,
               exclude_classes=false,
               exclude_methods=true,
               exclude_functions=true

""")
        flake8dir.make_example_py(self.example_tests)

        # Test
        result = flake8dir.run_flake8(extra_args)
        assert ['./example.py:1:1: M501 test definition not marked with test'] == result.out_lines
