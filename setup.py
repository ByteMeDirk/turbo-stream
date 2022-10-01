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
EMAIL = "dirkscgm@gmail.com"
AUTHOR = "DirksCGM"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.8"

setup(
    name=NAME,
    packages=find_packages(include=["turbo_stream", "turbo_stream.*"]),
    install_requires=[
        "boto3~=1.21.16",
        "google_api_python_client==2.63.0",
        "oauth2client==4.1.3",
        "pandas~=1.4.1",
        "python_dateutil==2.8.2",
        "PyYAML==6.0",
        "setuptools~=60.9.3",
        "oauthlib==3.2.0",
        "pyarrow==7.0.0",
        "coverage==6.3.2",
        "pylint==2.12.2",
        "pytest==7.0.1",
        "pyOpenSSL",
        "botocore~=1.24.16",
        "moto~=3.0.7",
    ],
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
