#!/usr/bin/env python

from setuptools import setup, find_packages

from setuputils import find_version


setup(
    name='xpdb',
    version=find_version('xpdb/__init__.py'),
    description='hacking the module pdb',
    author='x r',
    packages=find_packages(),
    py_modules=['setuputils'],
    entry_points={
        'console_scripts': [
            'xpdb = xpdb.script:main',
        ],
    }
)
