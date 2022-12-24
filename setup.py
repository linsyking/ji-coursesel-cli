#!/usr/bin/env python3

from setuptools import setup

setup(
    entry_points={
        'console_scripts': ['ji-coursesel=courseselcli.command_line:main'],
    }
)
