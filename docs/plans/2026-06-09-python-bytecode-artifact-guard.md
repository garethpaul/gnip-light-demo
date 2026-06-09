# Python Bytecode Artifact Guard

status: completed

## Context

The legacy GNIP sample is checked with Python 3 static checks and optional
Python 2 syntax/unit verification. Those checks should not leave `*.pyc` files
or `__pycache__` directories in the working tree, and generated artifacts should
not be accepted as part of the repository baseline.

## Completed Scope

- Added a baseline helper that detects generated Python bytecode artifacts.
- Required the working tree to be free of `*.pyc` files and `__pycache__`
  directories before baseline checks pass.
- Replaced Python 2 `py_compile` file writes with in-memory compilation.
- Ran Python 2 unit discovery with `PYTHONDONTWRITEBYTECODE=1`.
- Documented the artifact guard in README, VISION, and CHANGES.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
