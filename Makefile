.PHONY: build check lint test

override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3

lint test build: check

check:
	@PYTHON="$(PYTHON)" "$(ROOT)/scripts/check-python3.sh"
	@"$(PYTHON)" "$(ROOT)/scripts/check-baseline.py"
