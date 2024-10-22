#!/usr/bin/env python3

from setuptools import setup, find_packages
setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["static/*.txt"]},
)
