==================
Flake8-pytest-mark
==================

.. image:: https://img.shields.io/travis/rcbops/flake8-pytest-mark.svg
        :target: https://travis-ci.org/rcbops/flake8-pytest-mark

Check and enforce the presence of a mark on a pytest test case.

Quick Start Guide
-----------------

1. Install ``flake8-pytest-mark`` from PyPI with pip::

    $ pip install flake8-pytest-mark

2. Configure a mark that you would like to validate::

    $ cd project_root/
    $ vi .flake8

.. code-block:: ini

    [flake8]
    pytest_mark1 = name=test_id
                   value_match=uuid

3. Run flake8::

    $ flake8 tests/

Gotchas
-------

1. It is highly recommended to use this plugin inside of a virtualenv
2. A configuration is required by this plugin, if none is found the plugin will throw a M401 validation error for every file

Violation Codes
---------------

All possible violation codes are documented in violation_codes_


Example Configurations
----------------------

More example configurations can be found in configuration_

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _CONTRIBUTING.rst: CONTRIBUTING.rst
.. _configuration: docs/configuration.rst
.. _violation_codes: docs/violation_codes.rst
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage