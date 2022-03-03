SHELL := /bin/bash

COVERAGE_THRESHOLD ?= 90

test:
	pip install pytest mock pytest-mock coverage;
	coverage run -m pytest;
	coverage report --fail-under=${COVERAGE_THRESHOLD}
