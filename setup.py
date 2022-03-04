"""
Set up the PyPi Package
"""

from setuptools import setup

setup(
    name="turbo_stream",
    packages=[
        "turbo_stream",
        "turbo_stream.google_analyitcs",
        "turbo_stream.google_search_console",
    ],
    install_requires=[
        "boto3==1.21.12",
        "google_api_python_client==2.39.0",
        "oauth2client==4.1.3",
        "pandas==1.4.1",
        "python_dateutil==2.8.2",
        "PyYAML==6.0",
        "setuptools==60.5.0",
        "oauthlib==3.2.0",
        "pyarrow==6.0.1",
    ],
    extras_require={},
    description="A module for down-streaming data from a selection of vendors.",
    version="0.0.5",
    url="https://github.com/DirksCGM/turbo-stream.git",
    author="DirkSCGM",
    author_email="dirkscgm@gmail.com",
    keywords=["pip", "google_analytics", "google_search_console"],
)
