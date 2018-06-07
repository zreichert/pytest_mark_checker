.PHONY: clean clean-test clean-pyc clean-build clean-venv check-venv help install-editable
.DEFAULT_GOAL := help

SHELL := /bin/bash
export VIRTUALENVWRAPPER_PYTHON := /usr/bin/python

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

check-venv: ## verify that the user is running in a Python virtual environment
	@if [ -z "$(VIRTUALENVWRAPPER_SCRIPT)" ]; then echo 'Python virtualenvwrapper not installed!' && exit 1; fi
	@if [ -z "$(VIRTUAL_ENV)" ]; then echo 'Not running within a virtual environment!' && exit 1; fi

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage, artifacts and wipe virtualenv

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache/

clean-venv: uninstall check-venv ## remove all packages from current virtual environment
	@source virtualenvwrapper.sh && wipeenv || echo "Skipping wipe of environment"

lint: ## check style with flake8
	flake8 flake8_pytest_mark setup.py tests --ignore M

test: ## run tests quickly with the default Python
	py.test

test-all: ## run tests on every Python version with tox
	tox

install: clean build uninstall ## install the package to the active Python's site-packages
	pip install dist/*.whl

install-editable: ## install the package in editable mode
	if pip list -e | grep 'flake8-pytest-mark'; then echo 'Editable package already installed'; else pip install -e .; fi

install-dev-requirements: ## install the requirements for development
	pip install -r requirements_dev.txt

develop: clean install-dev-requirements install-editable ## install necessary packages to setup a dev environment

build: ## build a wheel
	python setup.py bdist_wheel

publish: ## publish package to PyPI
	twine upload dist/*.whl

bump-major: ## bumps the version of by major
	bumpversion major

bump-minor: ## bumps the version of by minor
	bumpversion minor

bump-patch: ## bumps the version of by patch
	bumpversion patch

uninstall: ## remove this package
	pip uninstall flake8-pytest-mark -y || echo 'flake8-pytest-mark not installed'

release-major: install-dev-requirements lint install test clean-build bump-major build publish ## package and upload a major release
	echo 'Successfully released!'
	echo 'Please push the newly created tag and commit to GitHub.'

release-minor: install-dev-requirements lint install test clean-build bump-minor build publish ## package and upload a minor release
	echo 'Successfully released!'
	echo 'Please push the newly created tag and commit to GitHub.'

release-patch: install-dev-requirements lint install test clean-build bump-patch build publish ## package and upload a patch release
	echo 'Successfully released!'
	echo 'Please push the newly created tag and commit to GitHub.'
