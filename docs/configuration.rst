=============
Configuration
=============

Location
========
The flake8-pytest-mark plug-in loads its configuration options from the same source as standard flake8 configuration.  Flake8 supports storing its configuration in the following places:

Your top-level user directory In your project in one of ``setup.cfg``, ``tox.ini``, or ``.flake8``.  For more information on configuration locations see:

Flake8_configuration_

Configuration
=============
You may configure up to 50 pytest-marks to be validated.  Flake8-pytest-mark will only validate marks that accept a single string as an argument ``@pytest.mark.test_id('I_am_a_string')``.  IF you would like to match the value of a marks string you may supply one of the following parameters.


+-----------------+----------------------------------------------+----------------------------------------------------------------+
| Param Name      + Valid Argument                               + Explanation                                                    +
+=================+==============================================+================================================================+
| value_match     + uuid                                         + Will validate the the supplied string is a valid UUID          |
+-----------------+----------------------------------------------+----------------------------------------------------------------+
| value_regex     + any valid regex that does not contain spaces | Will validate that the supplied string is a match to the regex |
+-----------------+----------------------------------------------+----------------------------------------------------------------+
| allow_duplicate + false (default), true                        | Allows a mark to decorate a test more than once                |
+-----------------+----------------------------------------------+----------------------------------------------------------------+

Examples:
=========
All examples assume running against the following test file.


**example.py** : An example pytest::

    @pytest.mark.test_type('functional')
    def test_multiple_marks():
        pass

**.flake8** : A simple configuration, validate the presence of two separate pytest-marks::

    [flake8]
    pytest_mark1 = name=test_id
    pytest_mark2 = name=test_name

**Shell Output** : validate the presence of two separate pytest-marks::

    ./example.py:1:1: M501 test definition not marked with test_id
    ./example.py:1:1: M502 test definition not marked with test_name

**.flake8** : Validation Configuration, validate the presence and contents of two pytest-marks::

    [flake8]
    pytest_mark1 = name=test_id
                   value_match=uuid
    pytest_mark2 = name=test_type
                   value_regex=(integration)|(unit)

**Shell Output** : Validating one mark not present & one mark value does not match::

    ./example.py:1:1: M501 test definition not marked with test_id
    ./example.py:6:1: M602 the mark value 'functional' does not match the configuration specified by pytest_mark2, Configured regex: '(integration)|(unit)'

.. _Flake8_configuration: http://flake8.pycqa.org/en/latest/user/configuration.html