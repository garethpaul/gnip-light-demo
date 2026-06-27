.PHONY: build check lint test

override empty :=
override space := $(empty) $(empty)
override makefile_space := __GNIP_MAKEFILE_SPACE__
override encoded_makefile_list := $(patsubst $(makefile_space)%,%,$(subst $(space),$(makefile_space),$(MAKEFILE_LIST)))
override ROOT := $(subst $(makefile_space),$(space),$(abspath $(dir $(lastword $(encoded_makefile_list)))))
PYTHON ?= python3

lint test build: check

check:
	@PYTHON="$(PYTHON)" "$(ROOT)/scripts/check-python3.sh"
	@"$(PYTHON)" "$(ROOT)/scripts/check-baseline.py"
