#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Installation of the tritondse module."""

import sys
from setuptools import setup, find_packages


with open("README.md") as f:
    README = f.read()


setup(
    name="tritondse",
    version="0.1.7",
    description="A library of Dynamic Symbolic Exploration based the Triton library",
    packages=find_packages(),
    long_description=README,
    long_description_content_type='text/markdown',
    url="https://github.com/quarkslab/tritondse",
    project_urls={
        "Documentation": "https://quarkslab.github.io/tritondse/",
        "Bug Tracker": "https://github.com/quarkslab/tritondse/issues",
        "Source": "https://github.com/quarkslab/tritondse"
    },
    setup_requires=[],
    install_requires=[
        "triton-library",
        "lief",
        "pyQBDI",
        "cle",
        "quokka-project",
        "enum_tools"
    ],
    tests_require=[],
    license="AGPL-3.0",
    author="Quarkslab",
    classifiers=[
        'Topic :: Security',
        'Environment :: Console',
        'Operating System :: OS Independent',
    ],
    test_suite="",
    scripts=[]
)
