=======================
Developer Documentation
=======================

``flake8-pytest-mark`` implements the following patterns:

- `Command Pattern`_
    The command pattern allows us to create new rules encapsulated as simple functions that operate on a single line
    of a Python file at a time.


Creating a New Rule
-------------------

New rules must be added to the ``flake8_pytest_mark.rules`` module using the following signature style::

    def rule_m#xx(pos1, pos2, **kwargs):
        # code

The implementer is responsible for deciding which data elements should be fed into arguments. The ``**kwargs`` at the
end of the signature is **required** for the rule to be called correctly. The ``**kwargs`` argument allows for rules
to implement any number of positional arguments while allowing to be called from a generic caller in the ``MarkChecker``
main class.

.. _Command Pattern: https://sourcemaking.com/design_patterns/command
