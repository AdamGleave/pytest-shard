from setuptools import setup
import os

import pytest_shard


def read(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r") as f:
        return f.read()


setup(
    name="pytest-shard",
    version=pytest_shard.__version__,
    packages=["pytest_shard"],
    license="MIT",
    url="https://github.com/AdamGleave/pytest-shard",
    install_requires=["pytest"],
    long_description=read("README.md"),
    python_requires=">=3.6",
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["pytest-shard = pytest_shard.pytest_shard"]},
    classifiers=[
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
