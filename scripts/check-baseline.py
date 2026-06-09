#!/usr/bin/env python3

from pathlib import Path
import os
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-gnip-baseline.md"
TIMEOUT_PLAN = ROOT / "docs/plans/2026-06-09-gnip-timeout-validation.md"
BYTECODE_PLAN = ROOT / "docs/plans/2026-06-09-python-bytecode-artifact-guard.md"


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


def python_artifacts():
    artifacts = [path for path in ROOT.rglob("*.pyc")]
    artifacts += [path for path in ROOT.rglob("__pycache__") if path.is_dir()]
    return sorted(str(path.relative_to(ROOT)) for path in artifacts)


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
    "docs/plans/2026-06-09-gnip-endpoint-validation.md",
    "docs/plans/2026-06-09-gnip-timeout-validation.md",
    "docs/plans/2026-06-09-python-bytecode-artifact-guard.md",
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
require("REQUEST_TIMEOUT" in api_source and "timeout=REQUEST_TIMEOUT" in api_source,
        "GNIP requests must use an explicit timeout")
require("def request_timeout()" in api_source and 'os.environ.get("GNIP_REQUEST_TIMEOUT", "30").strip()' in api_source,
        "GNIP request timeout must be parsed through a validation helper")
require("timeout <= 0" in api_source and "GNIP_REQUEST_TIMEOUT must be a positive integer" in api_source,
        "GNIP request timeout must reject non-positive or non-integer values")
require("REQUEST_TIMEOUT = request_timeout()" in api_source,
        "GNIP request timeout constant must use the validation helper")
require("res.raise_for_status()" in api_source,
        "GNIP requests must fail on HTTP error responses")

for env_name in ["GNIP_USER_NAME", "GNIP_PASSWORD"]:
    require(f"required_environment('{env_name}')" in wrapper_source,
            f"{env_name} must use fail-fast environment validation")
require("GNIPConfigurationError" in wrapper_source and "Missing required environment variable" in wrapper_source,
        "wrapper must raise a clear configuration error for missing credentials")
require("required_https_endpoint('GNIP_SEARCH_ENDPOINT')" in wrapper_source and "urlparse.urlsplit" in wrapper_source and "parsed.netloc" in wrapper_source,
        "GNIP_SEARCH_ENDPOINT must use fail-fast HTTPS endpoint validation")
require('GnipSearchAPI("USER"' not in wrapper_source and 'GnipSearchAPI("PASSWORD"' not in wrapper_source,
        "wrapper must not pass literal demo credentials to GnipSearchAPI")

require("*.pyc" in gitignore and "__pycache__/" in gitignore and ".env" in gitignore,
        "local Python artifacts and env files must stay ignored")
require(not python_artifacts(),
        "generated Python bytecode artifacts must be removed from the working tree")
require("*.csv" in gitignore and "bliebers.csv" in gitignore,
        "sample CSV exports must stay ignored")

require("make check" in readme and "GNIP_USER_NAME" in readme and "HTTPS URL with a host" in readme,
        "README must document baseline checks and credential environment variables")
require("Python bytecode artifacts" in readme,
        "README must document the bytecode artifact guard")
require("literal_eval" in vision and "git://" in vision and "GNIP_SEARCH_ENDPOINT" in vision,
        "VISION must describe the current safety baseline")
require("bytecode artifacts" in vision,
        "VISION must describe the bytecode artifact guard")
require("literal_eval" in changes and "HTTPS" in changes,
        "CHANGES must record parser and dependency transport hardening")
require("bytecode artifacts" in changes,
        "CHANGES must record the bytecode artifact guard")
require("status: completed" in plan, "baseline plan must be marked completed")
endpoint_plan = (ROOT / "docs/plans/2026-06-09-gnip-endpoint-validation.md").read_text()
require("status: completed" in endpoint_plan, "endpoint validation plan must be marked completed")
timeout_plan = TIMEOUT_PLAN.read_text() if TIMEOUT_PLAN.exists() else ""
require("status: completed" in timeout_plan, "request timeout validation plan must be marked completed")
bytecode_plan = BYTECODE_PLAN.read_text() if BYTECODE_PLAN.exists() else ""
require("status: completed" in bytecode_plan, "bytecode artifact guard plan must be marked completed")

python2 = shutil.which("python2")
if python2:
    py_files = [str(path.relative_to(ROOT)) for path in sorted(ROOT.glob("*.py"))]
    py_files += [str(path.relative_to(ROOT)) for path in sorted((ROOT / "gnip_search").glob("*.py"))]
    py_files += [str(path.relative_to(ROOT)) for path in sorted((ROOT / "tests").glob("*.py"))]
    syntax_check = (
        "import sys\n"
        "for filename in sys.argv[1:]:\n"
        "    compile(open(filename, 'rb').read(), filename, 'exec')\n"
    )
    subprocess.check_call([python2, "-c", syntax_check] + py_files, cwd=str(ROOT))
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.check_call([python2, "-m", "unittest", "discover", "-s", "tests"], cwd=str(ROOT), env=env)
    require(not python_artifacts(),
            "baseline checks must not generate Python bytecode artifacts")
else:
    print("check-baseline: python2 not found; skipped Python 2 syntax compilation and unit tests")

print("GNIP light demo baseline checks passed.")
