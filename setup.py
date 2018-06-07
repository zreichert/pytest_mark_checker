#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='flake8-pytest-mark',
    version='0.4.0',
    description='A flake8 plugin that helps check the presence of a PyTest mark',
    long_description=readme + '\n\n' + history,
    author='rpc-automation',
    author_email='rpc-automation@rackspace.com',
    url='https://github.com/rcbops/flake8-pytest-mark',
    entry_points={
        'flake8.extension': [
            'M = flake8_pytest_mark:MarkChecker',
        ],
    },
    packages=['flake8_pytest_mark'],
    include_package_data=True,
    install_requires=[
        'flake8>=3.5.0',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    license='Apache Software License 2.0',
    zip_safe=False,
    keywords='flake8 flake8-pytest-mark',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
