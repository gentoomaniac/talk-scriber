#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import os

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'talk-scriber'
DESCRIPTION = ''
URL = 'https://github.com/gentoomaniac/talk-scriber'
EMAIL = 'marco.siebecke@trustly.com'
AUTHOR = 'Marco Siebecke'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None
LICENSE = 'MIT'
EXCLUDE_FROM_PACKAGES = []
PACKAGE_DATA = []
REQUIRED = [
    'click', 'youtube_transcript_api'
]

EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    package_data={'': PACKAGE_DATA},
    license=LICENSE,
    entry_points={
        'console_scripts': [
            'talk-scriber = talk_scriber.main:cli',
        ],
    },
)
