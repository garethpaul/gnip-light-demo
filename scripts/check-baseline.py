#!/usr/bin/env python3

from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-gnip-baseline.md"


def fail(message):
    print(f"check-baseline: {message}", file=sys.stderr)
    sys.exit(1)


def read(path):
    full_path = ROOT / path
    if not full_path.is_file():
        fail(f"missing required file: {path}")
    return full_path.read_text()


def require(condition, message):
    if not condition:
        fail(message)


required_files = [
    ".gitignore",
    "CHANGES.md",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "requirements.txt",
    "step1.py",
    "step2.py",
    "gnip_search/gnip_search_api.py",
    "gnip_search/gnip_wrapper.py",
    "gnip_search/timeframe.py",
    "gnip_search/tweets.py",
    "tests/test_timeframe.py",
    "docs/plans/2026-06-08-gnip-baseline.md",
]

for required_file in required_files:
    read(required_file)

requirements = read("requirements.txt")
api_source = read("gnip_search/gnip_search_api.py")
wrapper_source = read("gnip_search/gnip_wrapper.py")
readme = read("README.md")
vision = read("VISION.md")
changes = read("CHANGES.md")
gitignore = read(".gitignore")
plan = PLAN.read_text() if PLAN.exists() else ""

require("git://" not in requirements, "requirements must not use unauthenticated git:// transport")
require("git+https://github.com/DrSkippy/Simple-n-grams.git@bbfd782614b39e2d0a1bc01fc6a75cc5df235e3e" in requirements,
        "Simple-n-grams dependency must keep its pinned HTTPS VCS URL")
require("git+https://github.com/twitterdev/twitter-python-ads-sdk.git" in requirements,
        "Twitter ads SDK dependency must use HTTPS VCS URL")

require("exec(" not in api_source, "GNIP API parser must not execute API-supplied strings")
require("ast.literal_eval" in api_source, "GNIP link parsing must use ast.literal_eval")
require("requests.Session()" in api_source and "s.auth = (self.user, self.password)" in api_source,
        "GNIP requests must keep credentials on the requests session auth field")

for env_name in ["GNIP_USER_NAME", "GNIP_PASSWORD", "GNIP_SEARCH_ENDPOINT"]:
    require(env_name in wrapper_source, f"{env_name} must be read from the environment")
require('GnipSearchAPI("USER"' not in wrapper_source and 'GnipSearchAPI("PASSWORD"' not in wrapper_source,
        "wrapper must not pass literal demo credentials to GnipSearchAPI")

require("*.pyc" in gitignore and "__pycache__/" in gitignore and ".env" in gitignore,
        "local Python artifacts and env files must stay ignored")
require("*.csv" in gitignore and "bliebers.csv" in gitignore,
        "sample CSV exports must stay ignored")

require("make check" in readme and "GNIP_USER_NAME" in readme,
        "README must document baseline checks and credential environment variables")
require("literal_eval" in vision and "git://" in vision,
        "VISION must describe the current safety baseline")
require("literal_eval" in changes and "HTTPS" in changes,
        "CHANGES must record parser and dependency transport hardening")
require("status: completed" in plan, "baseline plan must be marked completed")

python2 = shutil.which("python2")
if python2:
    py_files = [str(path.relative_to(ROOT)) for path in sorted(ROOT.glob("*.py"))]
    py_files += [str(path.relative_to(ROOT)) for path in sorted((ROOT / "gnip_search").glob("*.py"))]
    py_files += [str(path.relative_to(ROOT)) for path in sorted((ROOT / "tests").glob("*.py"))]
    subprocess.check_call([python2, "-m", "py_compile"] + py_files, cwd=str(ROOT))
    subprocess.check_call([python2, "-m", "unittest", "discover", "-s", "tests"], cwd=str(ROOT))
else:
    print("check-baseline: python2 not found; skipped Python 2 syntax compilation and unit tests")

print("GNIP light demo baseline checks passed.")
