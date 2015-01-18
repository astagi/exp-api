#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

extra_kwargs = {}
if sys.version_info >= (3,):
    extra_kwargs['setup_requires'] = ['setuptools']

setup(name="taiga",
    packages=find_packages(),
    include_package_data=True,
    version="0.1.0",
    description="Taiga python API",
    license="MIT",
    author="Nephila",
    author_email="stagi.andrea@gmail.com",
    url="",
    keywords= "taiga kanban wrapper api",
    zip_safe = False,
    **extra_kwargs)