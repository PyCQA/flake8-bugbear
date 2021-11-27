# Copyright (C) 2016-2021 Łukasz Langa

import ast
import os
import re
import sys

from setuptools import setup

assert sys.version_info >= (3, 6, 0), "bugbear requires Python 3.6+"


current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "README.rst"), encoding="utf8") as ld_file:
    long_description = ld_file.read()


_version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")


with open(os.path.join(current_dir, "bugbear.py"), "r") as f:
    version = _version_re.search(f.read()).group("version")
    version = str(ast.literal_eval(version))


setup(
    name="flake8-bugbear",
    version=version,
    description=(
        "A plugin for flake8 finding likely bugs and design problems "
        "in your program. Contains warnings that don't belong in "
        "pyflakes and pycodestyle."
    ),
    long_description=long_description,
    keywords="flake8 bugbear bugs pyflakes pylint linter qa",
    author="Łukasz Langa",
    author_email="lukasz@langa.pl",
    url="https://github.com/PyCQA/flake8-bugbear",
    license="MIT",
    py_modules=["bugbear"],
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=["flake8 >= 3.0.0", "attrs>=19.2.0"],
    test_suite="tests.test_bugbear",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={"flake8.extension": ["B = bugbear:BugBearChecker"]},
    extras_require={
        "dev": ["coverage", "hypothesis", "hypothesmith>=0.2", "pre-commit"]
    },
    project_urls={"Change Log": "https://github.com/PyCQA/flake8-bugbear#change-log"},
)
