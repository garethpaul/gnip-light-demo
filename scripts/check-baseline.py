#!/usr/bin/env python3

from pathlib import Path
import os
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-gnip-baseline.md"
TIMEOUT_PLAN = ROOT / "docs/plans/2026-06-09-gnip-timeout-validation.md"
BYTECODE_PLAN = ROOT / "docs/plans/2026-06-09-python-bytecode-artifact-guard.md"
ENDPOINT_PARTS_PLAN = ROOT / "docs/plans/2026-06-09-gnip-endpoint-url-parts.md"
ENTRYPOINT_PLAN = ROOT / "docs/plans/2026-06-09-gnip-sample-entrypoints.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
EXPORT_PREFIX_PLAN = ROOT / "docs/plans/2026-06-09-gnip-export-prefix-sanitizer.md"
TIMEOUT_EXCEPTION_PLAN = ROOT / "docs/plans/2026-06-09-gnip-timeout-exception-handling.md"
DATE_FORMAT_PLAN = ROOT / "docs/plans/2026-06-09-gnip-date-format-validation.md"
DATE_VALUE_PLAN = ROOT / "docs/plans/2026-06-09-gnip-date-value-validation.md"
CI_PLAN = ROOT / "docs/plans/2026-06-10-python3-timeframe-ci.md"
PAGINATION_PLAN = ROOT / "docs/plans/2026-06-10-gnip-pagination-boundary.md"
LINK_LITERAL_PLAN = ROOT / "docs/plans/2026-06-12-gnip-link-literal-boundary.md"


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
    "gnip_search/links.py",
    "gnip_search/pagination.py",
    "gnip_search/gnip_wrapper.py",
    "gnip_search/timeframe.py",
    "gnip_search/tweets.py",
    "tests/test_timeframe.py",
    "tests/test_pagination.py",
    "tests/test_links.py",
    "docs/plans/2026-06-08-gnip-baseline.md",
    "docs/plans/2026-06-09-gnip-endpoint-validation.md",
    "docs/plans/2026-06-09-gnip-endpoint-url-parts.md",
    "docs/plans/2026-06-09-gnip-timeout-validation.md",
    "docs/plans/2026-06-09-python-bytecode-artifact-guard.md",
    "docs/plans/2026-06-09-gnip-sample-entrypoints.md",
    "docs/plans/2026-06-09-make-gate-aliases.md",
    "docs/plans/2026-06-09-gnip-export-prefix-sanitizer.md",
    "docs/plans/2026-06-09-gnip-timeout-exception-handling.md",
    "docs/plans/2026-06-09-gnip-date-format-validation.md",
    "docs/plans/2026-06-09-gnip-date-value-validation.md",
    "docs/plans/2026-06-10-python3-timeframe-ci.md",
    "docs/plans/2026-06-10-gnip-pagination-boundary.md",
    "docs/plans/2026-06-12-gnip-link-literal-boundary.md",
    ".github/workflows/check.yml",
]

for required_file in required_files:
    read(required_file)

requirements = read("requirements.txt")
makefile = read("Makefile")
api_source = read("gnip_search/gnip_search_api.py")
links_source = read("gnip_search/links.py")
links_tests = read("tests/test_links.py")
pagination_source = read("gnip_search/pagination.py")
pagination_tests = read("tests/test_pagination.py")
wrapper_source = read("gnip_search/gnip_wrapper.py")
step1_source = read("step1.py")
step2_source = read("step2.py")
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
require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
        "Makefile must expose lint, test, build, and check gate targets")

require("exec(" not in api_source, "GNIP API parser must not execute API-supplied strings")
require("parse_link_values(link_str)" in api_source and "except LinkParseError:" in api_source and
        'self.freq.add("InvalidLinks")' in api_source,
        "GNIP link aggregation must reject and count invalid serialized fields")
require("print self.rule_payload" not in api_source and "print link_str" not in api_source,
        "GNIP processing must not log query payloads or extracted link fields")
require("ast.literal_eval(serialized)" in links_source and
        "isinstance(parsed, (list, tuple, set))" in links_source and
        "MAX_SERIALIZED_LINK_CHARS = 65536" in links_source and
        "MAX_LINK_VALUES = 1000" in links_source and
        "MAX_LINK_CHARS = 4096" in links_source and
        "GNIP link values exceed the accepted boundaries" in links_source,
        "GNIP link parsing must use literal evaluation with strict shape validation")
require("eval(" not in links_source.replace("literal_eval(", "") and "exec(" not in links_source,
        "GNIP link parser must not execute serialized fields")
for test_contract in [
        "test_accepts_string_and_collection_literals",
        "test_rejects_code_expressions",
        "test_rejects_malformed_or_blank_input",
        "test_rejects_scalar_and_mapping_literals",
        "test_rejects_empty_or_mixed_collections",
        "test_rejects_oversized_serialized_input",
        "test_rejects_too_many_or_oversized_link_values",
]:
    require(test_contract in links_tests,
            "GNIP link parser tests must include %s" % test_contract)
require("PaginationGuard()" in api_source and "pagination_guard.accept" in api_source and "except PaginationError, e:" in api_source,
        "GNIP paged requests must validate provider next tokens before reuse")
require("DEFAULT_MAX_PAGES = 1000" in pagination_source and "token in self.seen_tokens" in pagination_source and "self.page_count >= self.max_pages" in pagination_source,
        "GNIP pagination must detect token cycles and enforce the hard page ceiling")
require("test_rejects_repeated_tokens" in pagination_tests and "test_rejects_tokens_beyond_page_limit" in pagination_tests and "test_rejects_blank_and_non_string_tokens" in pagination_tests,
        "GNIP pagination boundary tests must cover cycles, page limits, and malformed tokens")
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
require("except requests.exceptions.Timeout, e:" in api_source and
        api_source.index("requests.exceptions.Timeout") < api_source.index("requests.exceptions.ConnectionError"),
        "GNIP request timeouts must fail with a clear message before result parsing")
require("def safe_file_name_prefix" in api_source and r"[^A-Za-z0-9._-]+" in api_source,
        "GNIP output file prefixes must use a conservative filename character set")
require("prefix.strip('._')" in api_source and 'prefix or "query"' in api_source,
        "GNIP output file prefixes must avoid empty, dot, or underscore-only names")
require("self.file_name_prefix = self.safe_file_name_prefix(f)" in api_source,
        "GNIP output file prefix generation must use the sanitizer")
require('DATE_RE = re.compile(r"^([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})$")' in api_source,
        "GNIP date parsing must use an anchored YYYY-MM-DD HH:MM regex",
        )
require("dt = DATE_RE.match(value)" in api_source,
        "GNIP date parsing must match the full start and end strings",
        )
require("return ''.join(dt.groups())" in api_source,
        "GNIP date parsing must build API dates from captured components",
        )
require('re.compile("([0-9]{4}).' not in api_source,
        "GNIP date parsing must not accept arbitrary delimiters",
        )
require('INPUT_DATE_FMT = "%Y-%m-%d %H:%M"' in api_source and "def api_date_filter" in api_source,
        "GNIP date parsing must keep a strict API date validation helper")
require("datetime.datetime.strptime(value, INPUT_DATE_FMT)" in api_source and "Invalid %s-date value" in api_source,
        "GNIP date parsing must reject impossible calendar date values")
require('self.fromDate = api_date_filter(start, "start")' in api_source and 'self.toDate = api_date_filter(end, "end")' in api_source,
        "GNIP start and end filters must use the strict API date validation helper")

for env_name in ["GNIP_USER_NAME", "GNIP_PASSWORD"]:
    require(f"required_environment('{env_name}')" in wrapper_source,
            f"{env_name} must use fail-fast environment validation")
require("GNIPConfigurationError" in wrapper_source and "Missing required environment variable" in wrapper_source,
        "wrapper must raise a clear configuration error for missing credentials")
require("required_https_endpoint('GNIP_SEARCH_ENDPOINT')" in wrapper_source and "urlparse.urlsplit" in wrapper_source and "parsed.netloc" in wrapper_source,
        "GNIP_SEARCH_ENDPOINT must use fail-fast HTTPS endpoint validation")
require("parsed.username" in wrapper_source and "parsed.password" in wrapper_source and "parsed.query" in wrapper_source and "parsed.fragment" in wrapper_source,
        "GNIP_SEARCH_ENDPOINT must reject embedded credentials, query strings, and fragments")
require('GnipSearchAPI("USER"' not in wrapper_source and 'GnipSearchAPI("PASSWORD"' not in wrapper_source,
        "wrapper must not pass literal demo credentials to GnipSearchAPI")

require("*.pyc" in gitignore and "__pycache__/" in gitignore and ".env" in gitignore,
        "local Python artifacts and env files must stay ignored")
require(not python_artifacts(),
        "generated Python bytecode artifacts must be removed from the working tree")
require("*.csv" in gitignore and "bliebers.csv" in gitignore,
        "sample CSV exports must stay ignored")

for script_name, source in [("step1.py", step1_source), ("step2.py", step2_source)]:
    require("def main():" in source and 'if __name__ == "__main__":' in source,
            "%s must keep live sample work behind a main guard" % script_name)
    main_index = source.find("def main():")
    guard_index = source.find('if __name__ == "__main__":')
    require(main_index != -1 and guard_index != -1 and main_index < guard_index,
            "%s must define main before the __main__ guard" % script_name)
    for token in ["FullArchiveSearch(", "tweets.get_data()"]:
        token_index = source.find(token)
        require(token_index > main_index and token_index < guard_index,
                "%s must not run GNIP sample calls at import time" % script_name)

open_index = step2_source.find("with open('bliebers.csv', 'wb')")
require(open_index > step2_source.find("def main():") and open_index < step2_source.find('if __name__ == "__main__":'),
        "step2.py must not write the sample CSV at import time")

require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "GNIP_USER_NAME" in readme and "HTTPS URL with a host" in readme,
        "README must document baseline checks and credential environment variables")
require("no embedded credentials, query string, or fragment" in readme,
        "README must document the GNIP endpoint URL-parts guard")
require("Python bytecode artifacts" in readme,
        "README must document the bytecode artifact guard")
require("Importing the sample scripts does not trigger live GNIP requests" in readme,
        "README must document the sample entrypoint guard")
require("output filename prefixes" in readme and "conservative filename" in readme and "character set" in readme,
        "README must document GNIP output filename prefix sanitization")
require("GNIP request timeout exceptions" in readme and "clear error" in readme,
        "README must document GNIP request timeout exception handling")
require("GNIP date filters" in readme and "YYYY-MM-DD HH:MM" in readme,
        "README must document strict GNIP date filter validation")
require("impossible calendar values" in readme,
        "README must document GNIP date value validation")
require("InvalidLinks" in readme and "without code execution" in readme,
        "README must document safe GNIP link literal handling")
require("64 KiB" in readme and "1,000 values" in readme,
        "README must document GNIP link parser resource bounds")
require("does not log query payloads or extracted link values" in readme,
        "README must document GNIP query and link log privacy")
require("make lint" in vision and "make test" in vision and "make build" in vision and "literal_eval" in vision and "git://" in vision and "GNIP_SEARCH_ENDPOINT" in vision,
        "VISION must describe the current safety baseline")
require("no embedded credentials, query string, or fragment" in vision,
        "VISION must describe the GNIP endpoint URL-parts guard")
require("bytecode artifacts" in vision,
        "VISION must describe the bytecode artifact guard")
require("entry points keep live GNIP calls and CSV writes behind main guards" in vision,
        "VISION must describe the sample entrypoint guard")
require("output filename prefixes" in vision and "conservative filename" in vision and "character set" in vision,
        "VISION must describe GNIP output filename prefix sanitization")
require("GNIP request timeout exceptions" in vision and "clear error" in vision,
        "VISION must describe GNIP request timeout exception handling")
require("GNIP date filters" in vision and "YYYY-MM-DD HH:MM" in vision,
        "VISION must describe strict GNIP date filter validation")
require("impossible calendar values" in vision,
        "VISION must describe GNIP date value validation")
require("GNIP link aggregation" in vision and "without executing" in vision,
        "VISION must describe safe GNIP link literal handling")
require("Query payloads and extracted link values are not logged" in vision,
        "VISION must describe GNIP query and link log privacy")
require("make lint" in changes and "make test" in changes and "make build" in changes and "literal_eval" in changes and "HTTPS" in changes,
        "CHANGES must record parser and dependency transport hardening")
require("embedded credentials, query strings, or fragments" in changes,
        "CHANGES must record the GNIP endpoint URL-parts guard")
require("bytecode artifacts" in changes,
        "CHANGES must record the bytecode artifact guard")
require("sample scripts behind main guards" in changes,
        "CHANGES must record the sample entrypoint guard")
require("output filename prefixes" in changes,
        "CHANGES must record the output filename prefix sanitizer")
require("GNIP request timeout exceptions" in changes,
        "CHANGES must record GNIP request timeout exception handling")
require("GNIP date filters" in changes,
        "CHANGES must record GNIP date filter validation")
require("impossible calendar values" in changes,
        "CHANGES must record GNIP date value validation")
require("GNIP link literal parser" in changes and "InvalidLinks" in changes,
        "CHANGES must record GNIP link literal validation")
require("Removed unconditional query-payload and link-value debug output" in changes,
        "CHANGES must record GNIP query and link log privacy")
require("status: completed" in plan, "baseline plan must be marked completed")
endpoint_plan = (ROOT / "docs/plans/2026-06-09-gnip-endpoint-validation.md").read_text()
require("status: completed" in endpoint_plan, "endpoint validation plan must be marked completed")
timeout_plan = TIMEOUT_PLAN.read_text() if TIMEOUT_PLAN.exists() else ""
require("status: completed" in timeout_plan, "request timeout validation plan must be marked completed")
bytecode_plan = BYTECODE_PLAN.read_text() if BYTECODE_PLAN.exists() else ""
require("status: completed" in bytecode_plan, "bytecode artifact guard plan must be marked completed")
endpoint_parts_plan = ENDPOINT_PARTS_PLAN.read_text() if ENDPOINT_PARTS_PLAN.exists() else ""
require("status: completed" in endpoint_parts_plan, "endpoint URL-parts validation plan must be marked completed")
entrypoint_plan = ENTRYPOINT_PLAN.read_text() if ENTRYPOINT_PLAN.exists() else ""
require("status: completed" in entrypoint_plan, "sample entrypoint plan must be marked completed")
require("make check" in entrypoint_plan, "sample entrypoint plan must record make check verification")
make_gates_plan = MAKE_GATES_PLAN.read_text() if MAKE_GATES_PLAN.exists() else ""
require("status: completed" in make_gates_plan, "Make gate alias plan must be marked completed")
export_prefix_plan = EXPORT_PREFIX_PLAN.read_text() if EXPORT_PREFIX_PLAN.exists() else ""
require("status: completed" in export_prefix_plan, "GNIP export prefix sanitizer plan must be marked completed")
timeout_exception_plan = TIMEOUT_EXCEPTION_PLAN.read_text() if TIMEOUT_EXCEPTION_PLAN.exists() else ""
require("status: completed" in timeout_exception_plan, "GNIP timeout exception handling plan must be marked completed")
date_format_plan = DATE_FORMAT_PLAN.read_text() if DATE_FORMAT_PLAN.exists() else ""
require("status: completed" in date_format_plan, "GNIP date format validation plan must be marked completed")
date_value_plan = DATE_VALUE_PLAN.read_text() if DATE_VALUE_PLAN.exists() else ""
require("status: completed" in date_value_plan, "GNIP date value validation plan must be marked completed")

workflow = read(".github/workflows/check.yml")
workflow_lines = workflow.splitlines()
require(workflow_lines.count("permissions:") == 1 and
        workflow_lines.count("  contents: read") == 1 and
        not re.search(r"^[ \t]+permissions:", workflow, re.MULTILINE) and
        not re.search(r"^[ \t]+[^#][^:]*:[ \t]*write(?:[ \t]*#.*)?$", workflow, re.MULTILINE) and
        "write-all" not in workflow,
        "GitHub Actions must keep one top-level read-only permissions block")
require(workflow.count("uses: actions/checkout@") == 1 and
        "uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3" in workflow and
        workflow_lines.count("          persist-credentials: false") == 1,
        "GitHub Actions must keep one pinned, credential-free checkout step")
require(workflow.count("uses: actions/setup-python@") == 1 and
        "uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6.2.0" in workflow and
        workflow_lines.count("        run: make check") == 1 and
        "cancel-in-progress: true" in workflow and
        "runs-on: ubuntu-24.04" in workflow and "timeout-minutes: 10" in workflow and
        'python-version: ["3.10", "3.12", "3.14"]' in workflow,
        "GitHub Actions must keep the pinned offline Python matrix contract")
ci_plan = CI_PLAN.read_text() if CI_PLAN.exists() else ""
require("status: completed" in ci_plan and "make check" in ci_plan,
        "Python 3 timeframe CI plan must be completed and record verification")
pagination_plan = PAGINATION_PLAN.read_text() if PAGINATION_PLAN.exists() else ""
require("status: completed" in pagination_plan and "Mutations disabling cycle detection or the page ceiling must fail" in pagination_plan,
        "GNIP pagination boundary plan must record completed mutation verification")
link_literal_plan = LINK_LITERAL_PLAN.read_text() if LINK_LITERAL_PLAN.exists() else ""
require("status: completed" in link_literal_plan and
        "Mutations restoring direct literal iteration" in link_literal_plan and
        "removing resource limits" in link_literal_plan and
        "logging query/link values" in link_literal_plan,
        "GNIP link literal plan must record completed mutation verification")

env = dict(os.environ)
env["PYTHONDONTWRITEBYTECODE"] = "1"
subprocess.check_call([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=str(ROOT), env=env)
require(not python_artifacts(),
        "Python 3 characterization tests must not generate bytecode artifacts")

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
    python2_env = dict(os.environ)
    python2_env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.check_call([python2, "-m", "unittest", "discover", "-s", "tests"], cwd=str(ROOT), env=python2_env)
    require(not python_artifacts(),
            "baseline checks must not generate Python bytecode artifacts")
else:
    print("check-baseline: python2 not found; skipped Python 2 syntax compilation and unit tests")

print("GNIP light demo baseline checks passed.")
