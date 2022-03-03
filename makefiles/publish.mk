SHELL := /bin/bash

update-version:
	$(eval VERSION := $(shell grep version= setup.py | grep -Eo '[0-9]+([.][0-9]+)([.][0-9]+)?'))
	$(eval NEW_VERSION := $(REF:refs/tags/v%=%))
	sed -i "s#version='${VERSION}'#version='$(NEW_VERSION)'#g" setup.py
	sed -i "s#${VERSION}.zip#$(NEW_VERSION).zip#g" setup.py
