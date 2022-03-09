"""
Set up the PyPi Package
"""

# read the contents of your README file
from pathlib import Path

from setuptools import setup, find_packages

# Package meta-data.
NAME = "turbo_stream"
DESCRIPTION = "A module for down-streaming data from a selection of vendors."
URL = "https://github.com/DirksCGM/turbo-stream.git"
EMAIL = "dirkscgm{at}gmail.com"
AUTHOR = "DirksCGM"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.6"

with open("requirements.txt") as f:
    REQUIRED = f.read().splitlines()

setup(
    name=NAME,
    packages=find_packages(include=["turbo_stream", "turbo_stream.*"]),
    install_requires=REQUIRED,
    extras_require={},
    description=DESCRIPTION,
    version=VERSION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    keywords=["pip", "google_analytics", "google_search_console"],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
