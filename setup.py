# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import codecs
import re

from setuptools import setup


def get_version(filename):
    with codecs.open(filename, 'r', 'utf-8') as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)


version = get_version('pytest_mark_checker.py')

with codecs.open('README.rst', 'r', 'utf-8') as readme_file:
    readme = readme_file.read()

with codecs.open('HISTORY.rst', 'r', 'utf-8') as history_file:
    history = history_file.read()

setup(
    name='pytest-mark-checker',
    version=version,
    description="A flake8 plugin that helps check the presence of a PyTest mark",
    long_description=readme + '\n\n' + history,
    author="Zach Reichert",
    author_email='zach.reichert@rackspace.com',
    url='https://github.com/zreichert/test-mark-checker',
    entry_points={
        'flake8.extension': [
            'M = pytest_mark_checker:MarkChecker',
        ],
    },
    py_modules=['pytest_mark_checker'],
    include_package_data=True,
    install_requires=[
        'flake8!=3.2.0',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    license="ISCL",
    zip_safe=False,
    keywords='pytest-mark-checker',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
