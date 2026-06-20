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
RESPONSE_BODY_PLAN = ROOT / "docs/plans/2026-06-12-gnip-response-body-boundary.md"
VCS_DEPENDENCY_PLAN = ROOT / "docs/plans/2026-06-12-vcs-dependency-pinning.md"
DIAGNOSTIC_REDACTION_PLAN = ROOT / "docs/plans/2026-06-13-gnip-diagnostic-redaction.md"
POSTED_TIME_SUFFIX_PLAN = ROOT / "docs/plans/2026-06-13-gnip-posted-time-suffix.md"
RESPONSE_SHAPE_PLAN = ROOT / "docs/plans/2026-06-13-gnip-response-shape.md"
LOCATION_INDEPENDENT_MAKE_PLAN = ROOT / "docs/plans/2026-06-13-location-independent-make.md"
MAX_RESULTS_PLAN = ROOT / "docs/plans/2026-06-14-gnip-max-results-payload.md"
PYTHON_PREFLIGHT_PLAN = ROOT / "docs/plans/2026-06-16-python-verification-preflight.md"
FAILURE_EXIT_STATUS_PLAN = ROOT / "docs/plans/2026-06-16-gnip-failure-exit-status.md"


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
    "scripts/check-python3.sh",
    "docs/plans/2026-06-12-vcs-dependency-pinning.md",
    "step1.py",
    "step2.py",
    "gnip_search/gnip_search_api.py",
    "gnip_search/links.py",
    "gnip_search/pagination.py",
    "gnip_search/privacy.py",
    "gnip_search/response.py",
    "gnip_search/gnip_wrapper.py",
    "gnip_search/timeframe.py",
    "gnip_search/timestamps.py",
    "gnip_search/schema.py",
    "gnip_search/query.py",
    "gnip_search/tweets.py",
    "tests/test_timeframe.py",
    "tests/test_pagination.py",
    "tests/test_privacy.py",
    "tests/test_links.py",
    "tests/test_response.py",
    "tests/test_timestamps.py",
    "tests/test_schema.py",
    "tests/test_query.py",
    "tests/test_exit_status.py",
    "tests/test_api_runtime.py",
    "tests/test_samples.py",
    "tests/test_baseline_contract.py",
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
    "docs/plans/2026-06-12-gnip-response-body-boundary.md",
    "docs/plans/2026-06-13-gnip-diagnostic-redaction.md",
    "docs/plans/2026-06-13-gnip-posted-time-suffix.md",
    "docs/plans/2026-06-13-gnip-response-shape.md",
    "docs/plans/2026-06-14-gnip-max-results-payload.md",
    "docs/plans/2026-06-16-python-verification-preflight.md",
    "docs/plans/2026-06-16-gnip-failure-exit-status.md",
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
response_source = read("gnip_search/response.py")
response_tests = read("tests/test_response.py")
privacy_source = read("gnip_search/privacy.py")
privacy_tests = read("tests/test_privacy.py")
timestamps_source = read("gnip_search/timestamps.py")
timestamps_tests = read("tests/test_timestamps.py")
schema_source = read("gnip_search/schema.py")
schema_tests = read("tests/test_schema.py")
query_source = read("gnip_search/query.py")
query_tests = read("tests/test_query.py")
exit_status_tests = read("tests/test_exit_status.py")
api_runtime_tests = read("tests/test_api_runtime.py")
sample_tests = read("tests/test_samples.py")
wrapper_source = read("gnip_search/gnip_wrapper.py")
step1_source = read("step1.py")
step2_source = read("step2.py")
readme = read("README.md")
vision = read("VISION.md")
changes = read("CHANGES.md")
security = read("SECURITY.md")
agents = read("AGENTS.md")
python_preflight = read("scripts/check-python3.sh")
gitignore = read(".gitignore")
plan = PLAN.read_text() if PLAN.exists() else ""

require("git://" not in requirements, "requirements must not use unauthenticated git:// transport")
expected_requirements = [
    "-e git+https://github.com/DrSkippy/Simple-n-grams.git@bbfd782614b39e2d0a1bc01fc6a75cc5df235e3e#egg=Simple-n-grams",
    "-e git+https://github.com/twitterdev/twitter-python-ads-sdk.git@a3dd5819341e77aa469d0b4b3399f0bcd028c80c#egg=twitter-ads",
]
require(requirements.splitlines() == expected_requirements,
        "requirements must keep exactly the reviewed immutable HTTPS VCS dependencies")
require(all(re.search(r"\.git@[0-9a-f]{40}#egg=", line) for line in expected_requirements),
        "VCS dependencies must use full commit SHAs")
require(".PHONY: build check lint test" in makefile
        and "lint test build: check" in makefile
        and 'ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))' in makefile
        and "PYTHON ?= python3" in makefile
        and 'PYTHON="$(PYTHON)" "$(ROOT)/scripts/check-python3.sh"' in makefile
        and '"$(PYTHON)" "$(ROOT)/scripts/check-baseline.py"' in makefile,
        "Makefile must expose configurable, preflighted gate targets")
require('PYTHON=${PYTHON:-python3}' in python_preflight
        and 'command -v "$PYTHON"' in python_preflight
        and 'sys.version_info[0]' in python_preflight
        and 'Python command not found' in python_preflight
        and 'Python 3 is required' in python_preflight,
        "Python preflight must reject missing and non-Python-3 commands")

require("exec(" not in api_source, "GNIP API parser must not execute API-supplied strings")
require('if __name__ == "__main__":' not in api_source and
        'GnipSearchAPI("USER"' not in api_source,
        "GNIP library module must not execute or print live demo queries")
require("def build_rule_payload(" in query_source and
        "def validated_query(" in query_source and
        "MAX_QUERY_CHARS = 2048" in query_source and
        "MAX_QUERY_BYTES = MAX_QUERY_CHARS * 4" in query_source and
        'payload["maxResults"] = request_page_size(max_results, paged=paged)' in query_source and
        "return min(value, MAX_RESULTS_PER_PAGE)" in query_source and
        "if not counts:" in query_source,
        "GNIP query payloads must validate and bound activity page sizes")
require("from .query import build_rule_payload" in api_source and
        "self.rule_payload = build_rule_payload(" in api_source and
        "paged=self.paged" in api_source and
        'counts=use_case.startswith("time")' in api_source,
        "GNIP API requests must use the bounded query-payload helper")
require("test_builds_activity_payload_with_requested_page_size" in query_tests and
        "test_caps_single_requests_at_provider_page_limit" in query_tests and
        "test_paged_searches_force_provider_page_limit" in query_tests and
        "test_count_payload_omits_activity_page_size" in query_tests and
        "test_rejects_blank_non_string_control_or_oversized_queries" in query_tests and
        "test_rejects_invalid_page_sizes" in query_tests,
        "GNIP query-payload tests must cover inclusion, bounds, counts, and invalid values")
require("def response_results(payload):" in schema_source and
        "def decode_response_payload(payload):" in schema_source and
        "isinstance(payload, dict)" in schema_source and
        "isinstance(results, list)" in schema_source and
        "not isinstance(result, dict)" in schema_source,
        "GNIP response schema must require an object with list results")
require("from .schema import ResponseShapeError, decode_response_payload, response_results" in api_source and
        "tmp_response = decode_response_payload(doc)" in api_source and
        "results = response_results(tmp_response)" in api_source and
        "acs.extend(results)" in api_source and
        "for item in results:" in api_source and
        'tmp_response["results"]' not in api_source,
        "GNIP page parsing and file output must use validated results")
require("test_rejects_non_object_pages" in schema_tests and
        "test_rejects_non_list_results" in schema_tests and
        "test_defaults_missing_results_to_empty_list" in schema_tests and
        "test_rejects_non_object_result_items" in schema_tests and
        "test_deep_or_malformed_json_fails_with_a_controlled_shape_error" in schema_tests,
        "GNIP response-shape tests must cover malformed and missing containers")
require("remove_millisecond_utc_suffix(rec[\"postedTime\"])" in api_source and
        '.strip(".000Z")' not in api_source and
        "from .timestamps import remove_millisecond_utc_suffix" in api_source and
        "from timestamps import remove_millisecond_utc_suffix" in api_source,
        "GNIP geo exports must use exact posted-time suffix removal")
require("UTC_TIMESTAMP_RE = re.compile(" in timestamps_source and
        "isinstance(value, string_types)" in timestamps_source and
        'datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")' in timestamps_source and
        "return timestamp" in timestamps_source,
        "GNIP posted-time helper must validate UTC timestamps before normalization")
require("test_preserves_seconds_ending_in_zero" in timestamps_tests and
        "test_removes_suffix_from_ordinary_seconds" in timestamps_tests and
        "test_leaves_values_without_exact_suffix_unchanged" in timestamps_tests and
        "test_accepts_fractional_utc_seconds_and_normalizes_to_whole_seconds" in timestamps_tests and
        "test_rejects_invalid_calendar_values_and_non_utc_offsets" in timestamps_tests and
        "test_rejects_non_string_or_empty_values" in timestamps_tests,
        "GNIP posted-time tests must cover exact removal and rejected values")
require("parse_link_values(link_str)" in api_source and "except LinkParseError:" in api_source and
        'self.freq.add("InvalidLinks")' in api_source,
        "GNIP link aggregation must reject and count invalid serialized fields")
require("print self.rule_payload" not in api_source and "print >>sys.stderr, self.rule_payload" not in api_source and 'format(str(self.rule_payload))' not in api_source and "print link_str" not in api_source,
        "GNIP processing must not log query payloads or extracted link fields")
require("def redacted_rule_payload(payload):" in privacy_source and 'for key in ("query", "next")' in privacy_source and "preview = dict(payload)" in privacy_source,
        "GNIP diagnostics must redact query text and pagination tokens without mutating request payloads")
require("json.dumps(redacted_rule_payload(self.rule_payload), sort_keys=True)" in api_source and "return repr(self.message)" in api_source and 'return repr("%s (%s, %s)"' not in api_source,
        "GNIP preview and exception diagnostics must not expose request or response payloads")
require('raise QueryError("GNIP query failed", self.rule_payload, tmp_response)' in api_source and 'tmp_response.get("error").get("message")' not in api_source,
        "GNIP provider errors must use a fixed printable message instead of response content")
require(api_source.count("sys.exit(1)") == 8 and api_source.count("sys.exit()") == 1,
        "GNIP validation and request failures must exit nonzero while query preview remains successful")
require("test_failures_exit_nonzero_and_query_preview_remains_successful" in exit_status_tests and
        "failure_markers = (" in exit_status_tests and
        'self.assertIn("sys.exit(1)", failure_block, marker)' in exit_status_tests and
        'self.assertNotIn("sys.exit(1)", preview_block)' in exit_status_tests and
        'self.assertEqual(8, source.count("sys.exit(1)"))' in exit_status_tests and
        'self.assertEqual(1, source.count("sys.exit()"))' in exit_status_tests,
        "GNIP exit-status behavior must have a dependency-free source contract")
require("test_redacts_query_and_pagination_token_without_mutating_input" in privacy_tests and "test_accepts_payload_without_sensitive_fields" in privacy_tests,
        "GNIP diagnostic redaction must have dependency-free behavior coverage")
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
require("PaginationGuard()" in api_source and "pagination_guard.accept" in api_source and "except PaginationError as e:" in api_source,
        "GNIP paged requests must validate provider next tokens before reuse")
require("DEFAULT_MAX_PAGES = 1000" in pagination_source and "MAX_TOKEN_BYTES = 4096" in pagination_source and "token in self.seen_tokens" in pagination_source and "self.page_count >= self.max_pages" in pagination_source,
        "GNIP pagination must detect token cycles and enforce the hard page ceiling")
require("test_rejects_repeated_tokens" in pagination_tests and "test_rejects_tokens_beyond_page_limit" in pagination_tests and "test_rejects_blank_and_non_string_tokens" in pagination_tests and "test_rejects_oversized_or_control_bearing_tokens" in pagination_tests,
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
require("stream=True" in api_source and "read_response_body(res)" in api_source and
        "res.text" not in api_source,
        "GNIP requests must stream response bodies through the bounded reader")
require("res.close()" in api_source and "finally:" in api_source and
        "s.close()" in api_source and "except Exception:" in api_source,
        "GNIP HTTP errors and request sessions must release network resources")
require("MAX_RESPONSE_BYTES = 16 * 1024 * 1024" in response_source and
        "RESPONSE_CHUNK_BYTES = 64 * 1024" in response_source and
        "response.iter_content(chunk_size=RESPONSE_CHUNK_BYTES)" in response_source and
        "total_bytes > MAX_RESPONSE_BYTES" in response_source and
        "response.close()" in response_source,
        "GNIP response bodies must remain chunked, byte-bounded, and close-guaranteed")
for test_contract in [
        "test_accepts_exact_limit_and_ignores_empty_chunks",
        "test_rejects_payload_over_limit_and_closes_response",
        "test_closes_response_when_stream_iteration_fails",
        "test_close_failure_does_not_mask_stream_failure",
]:
    require(test_contract in response_tests,
            "GNIP response body tests must include %s" % test_contract)
require("except requests.exceptions.Timeout:" in api_source and
        api_source.index("requests.exceptions.Timeout") < api_source.index("requests.exceptions.ConnectionError"),
        "GNIP request timeouts must fail with a clear message before result parsing")
require("test_timeout_diagnostic_is_redacted_and_cleanup_cannot_mask_exit" in api_runtime_tests and
        "test_query_errors_do_not_retain_provider_payloads" in api_runtime_tests,
        "GNIP runtime tests must cover redacted failures and sensitive payload retention")
require("test_full_archive_search_fetches_at_most_once" in sample_tests and
        "test_csv_output_is_not_truncated_when_fetch_fails" in sample_tests,
        "GNIP samples must cover request deduplication and output preservation")
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
    require("def main(" in source and 'if __name__ == "__main__":' in source,
            "%s must keep live sample work behind a main guard" % script_name)
    main_index = source.find("def main(")
    guard_index = source.find('if __name__ == "__main__":')
    require(main_index != -1 and guard_index != -1 and main_index < guard_index,
            "%s must define main before the __main__ guard" % script_name)
    for token in ["FullArchiveSearch(", "tweets.get_data()"]:
        token_index = source.find(token)
        require(token_index > main_index and token_index < guard_index,
                "%s must not run GNIP sample calls at import time" % script_name)

open_index = step2_source.find("tempfile.mkstemp(")
require(open_index > step2_source.find("def main(") and open_index < step2_source.find('if __name__ == "__main__":'),
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
require("validate ISO-8601 UTC posted times" in read("README.md") and
        "validates ISO-8601 UTC posted times" in read("SECURITY.md") and
        "validate ISO-8601 UTC posted times" in read("VISION.md") and
        "Validate GNIP posted times as ISO-8601 UTC" in read("AGENTS.md") and
        "Validated and normalized GNIP UTC posted times" in changes,
        "Project guidance must document strict GNIP posted-time validation")
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
response_body_plan = RESPONSE_BODY_PLAN.read_text() if RESPONSE_BODY_PLAN.exists() else ""
response_body_statuses = re.findall(r"^status: .+$", response_body_plan, flags=re.MULTILINE)
response_body_sections = response_body_plan.split("## Verification Completed\n", 1)
response_body_verification = response_body_sections[1] if len(response_body_sections) == 2 else ""
response_body_required_evidence = (
    "All four Make gates",
    "all 17 tests passed in both interpreter paths",
    "push run `27393392384`",
    "pull-request run `27393397945`",
    "push run `27393412678`",
    "CodeQL run `27402321656`",
    "Mutations removing `stream=True`",
)
require(response_body_statuses == ["status: completed"] and
        all(item in response_body_verification for item in response_body_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", response_body_verification, re.IGNORECASE) is None,
        "GNIP response body plan must record completed status and actual verification")
vcs_dependency_plan = VCS_DEPENDENCY_PLAN.read_text() if VCS_DEPENDENCY_PLAN.exists() else ""
require("status: completed" in vcs_dependency_plan and
        "upstream `master` commit" in vcs_dependency_plan and
        "Python 2 and Python 3 offline gates passed" in vcs_dependency_plan and
        "hostile mutations were rejected" in vcs_dependency_plan,
        "VCS dependency pinning plan must record completed verification")
diagnostic_redaction_plan = DIAGNOSTIC_REDACTION_PLAN.read_text() if DIAGNOSTIC_REDACTION_PLAN.exists() else ""
diagnostic_redaction_statuses = re.findall(
        r"^status: .+$", diagnostic_redaction_plan, flags=re.MULTILINE)
diagnostic_redaction_sections = diagnostic_redaction_plan.split(
        "## Verification Completed\n", 1)
diagnostic_redaction_verification = (
        diagnostic_redaction_sections[1] if len(diagnostic_redaction_sections) == 2 else "")
diagnostic_redaction_required_evidence = (
        "All 19 tests passed on Python 3 and Python 2",
        "all four Make gates passed",
        "raw preview mutation failed",
        "no-result payload mutation failed",
        "exception payload mutation failed",
        "provider error-message mutation failed",
        "redaction helper removal mutation failed",
        "redaction test removal mutation failed",
        "hosted pull-request and CodeQL snapshot",
)
require(diagnostic_redaction_statuses == ["status: completed"] and
        all(item in diagnostic_redaction_verification for item in diagnostic_redaction_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", diagnostic_redaction_verification, re.IGNORECASE) is None,
        "GNIP diagnostic redaction plan must record completed status and actual verification")
posted_time_suffix_plan = POSTED_TIME_SUFFIX_PLAN.read_text() if POSTED_TIME_SUFFIX_PLAN.exists() else ""
posted_time_suffix_statuses = re.findall(
        r"^status: .+$", posted_time_suffix_plan, flags=re.MULTILINE)
posted_time_suffix_sections = posted_time_suffix_plan.split(
        "## Verification Completed\n", 1)
posted_time_suffix_verification = (
        posted_time_suffix_sections[1] if len(posted_time_suffix_sections) == 2 else "")
posted_time_suffix_required_evidence = (
        "All 23 tests passed on Python 3 and Python 2",
        "All four Make gates passed",
        "character-set stripping mutation failed",
        "exact suffix guard mutation failed",
        "timestamp test removal mutation failed",
        "hosted push, pull-request, and CodeQL snapshot",
)
require(posted_time_suffix_statuses == ["status: completed"] and
        all(item in posted_time_suffix_verification for item in posted_time_suffix_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", posted_time_suffix_verification, re.IGNORECASE) is None,
        "GNIP posted-time suffix plan must record completed status and actual verification")
response_shape_plan = RESPONSE_SHAPE_PLAN.read_text() if RESPONSE_SHAPE_PLAN.exists() else ""
response_shape_statuses = re.findall(
        r"^status: .+$", response_shape_plan, flags=re.MULTILINE)
response_shape_sections = response_shape_plan.split(
        "## Verification Completed\n", 1)
response_shape_verification = (
        response_shape_sections[1] if len(response_shape_sections) == 2 else "")
response_shape_required_evidence = (
        "All 27 tests passed on Python 3 and Python 2",
        "All four Make gates passed",
        "object guard mutation failed",
        "results-list guard mutation failed",
        "direct results iteration mutation failed",
        "hosted push, pull-request, and code-scanning snapshot",
)
require(response_shape_statuses == ["status: completed"] and
        all(item in response_shape_verification for item in response_shape_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", response_shape_verification, re.IGNORECASE) is None,
        "GNIP response-shape plan must record completed status and actual verification")
location_independent_make_plan = (
        LOCATION_INDEPENDENT_MAKE_PLAN.read_text()
        if LOCATION_INDEPENDENT_MAKE_PLAN.exists() else "")
location_independent_make_statuses = re.findall(
        r"^status: .+$", location_independent_make_plan, flags=re.MULTILINE)
location_independent_make_sections = location_independent_make_plan.split(
        "## Verification Completed\n", 1)
location_independent_make_verification = (
        location_independent_make_sections[1]
        if len(location_independent_make_sections) == 2 else "")
location_independent_make_required_evidence = (
        "All 27 tests passed on Python 3 and Python 2",
        "All four Make gates",
        "from /tmp",
        "root-derivation mutation failed",
        "checker-command mutation failed",
        "plan-status mutation failed",
        "plan-evidence mutation failed",
        "documentation mutation failed",
)
require(location_independent_make_statuses == ["status: completed"] and
        all(item in location_independent_make_verification
            for item in location_independent_make_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b",
                  location_independent_make_verification,
                  re.IGNORECASE) is None,
        "Location-independent Make plan must record completed status and actual verification")
require("absolute Makefile path" in readme and
        "Made GNIP verification independent" in changes,
        "Project guidance must document location-independent Make verification")
max_results_plan = MAX_RESULTS_PLAN.read_text() if MAX_RESULTS_PLAN.exists() else ""
max_results_statuses = re.findall(
        r"^status: .+$", max_results_plan, flags=re.MULTILINE)
max_results_sections = max_results_plan.split("## Verification Completed\n", 1)
max_results_verification = (
        max_results_sections[1] if len(max_results_sections) == 2 else "")
max_results_required_evidence = (
        "Seven focused query-payload tests passed on Python 3 and Python 2",
        "All 34 tests passed on Python 3 and Python 2",
        "each of `make lint`,",
        "The absolute Makefile path passed from `/tmp`",
        "Six isolated mutations were rejected",
        "generated-artifact inventory",
        "credential-pattern scanning passed",
)
require(max_results_statuses == ["status: completed"] and
        all(item in max_results_verification
            for item in max_results_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b",
                  max_results_verification,
                  re.IGNORECASE) is None,
        "GNIP max-results plan must record completed status and actual verification")
require("GNIP response pages must decode to objects with list results" in readme and
        "GNIP response objects and results containers should be type-checked" in security and
        "Require GNIP response objects and list results" in vision and
        "Validated GNIP response objects and list results" in changes and
        "Validate GNIP response objects and list results" in agents,
        "Project guidance must document GNIP response-shape validation")
require("validated `maxResults` page size capped at" in readme and
        "Activity queries send a validated `maxResults`" in vision and
        "Restored activity-query `maxResults`" in changes and
        "Activity query page sizes are validated and capped at 500" in security and
        "gnip_search.query.build_rule_payload" in agents,
        "Project guidance must document bounded GNIP activity page sizes")
python_preflight_guidance = (
    "Offline verification uses one explicit, fail-fast Python 3 command."
)
require(all(python_preflight_guidance in re.sub(r"\s+", " ", text)
            for text in (readme, agents, vision, changes)),
        "Project guidance must document the offline Python preflight boundary")
python_preflight_plan = (
        PYTHON_PREFLIGHT_PLAN.read_text() if PYTHON_PREFLIGHT_PLAN.exists() else "")
python_preflight_statuses = re.findall(
        r"^status: .+$", python_preflight_plan, flags=re.MULTILINE)
python_preflight_sections = python_preflight_plan.split(
        "## Verification Completed\n", 1)
python_preflight_verification = (
        python_preflight_sections[1]
        if len(python_preflight_sections) == 2 else "")
python_preflight_required_evidence = (
        "All 34 tests passed",
        "All four Make gates passed",
        "absolute Makefile path passed from `/tmp`",
        "explicit Python override passed",
        "missing-command case failed with the intended diagnostic",
        "non-Python-3 case failed with the intended diagnostic",
        "Nine isolated mutations were rejected",
        "generated-artifact inventory was empty",
        "credential-pattern scan passed",
)
require(python_preflight_statuses == ["status: completed"] and
        all(item in python_preflight_verification
            for item in python_preflight_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b",
                  python_preflight_verification,
                  re.IGNORECASE) is None,
        "Python verification preflight plan must record completed status and actual verification")
require("immutable 40-character commits" in read("README.md") and
        "immutable VCS commits" in read("SECURITY.md") and
        "Pin legacy VCS dependencies" in read("VISION.md") and
        "Pinned the Twitter Ads SDK VCS dependency" in read("CHANGES.md"),
        "Project guidance must document immutable VCS dependency pins")
require("GNIP validation and request failures exit with a nonzero status" in readme and
        "GNIP validation and request failures exit with a nonzero status" in security and
        "GNIP validation and request failures exit with a nonzero status" in vision and
        "GNIP validation and request failures exit with a nonzero status" in agents and
        "GNIP validation and request failures now exit with a nonzero status" in changes,
        "Project guidance must document GNIP failure exit status")
failure_exit_status_plan = (
        FAILURE_EXIT_STATUS_PLAN.read_text()
        if FAILURE_EXIT_STATUS_PLAN.exists() else "")
failure_exit_status_statuses = re.findall(
        r"^status: .+$", failure_exit_status_plan, flags=re.MULTILINE)
failure_exit_status_sections = failure_exit_status_plan.split(
        "## Verification Completed\n", 1)
failure_exit_status_verification = (
        failure_exit_status_sections[1]
        if len(failure_exit_status_sections) == 2 else "")
failure_exit_status_required_evidence = (
        "focused exit-status test passed on Python 3 and Python 2",
        "complete suite passed on Python 3 and Python 2",
        "All four Make gates passed",
        "external-directory Make gate passed",
        "successful-failure-exit mutation failed",
        "nonzero-preview-exit mutation failed",
        "focused-test contract mutation failed",
        "plan-status mutation failed",
        "plan-evidence mutation failed",
)
require(failure_exit_status_statuses == ["status: completed"] and
        all(item in failure_exit_status_verification
            for item in failure_exit_status_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run|not yet)\b",
                  failure_exit_status_verification,
                  re.IGNORECASE) is None,
        "GNIP failure-exit-status plan must record completed status and actual verification")

env = dict(os.environ)
env["PYTHONDONTWRITEBYTECODE"] = "1"
python3_test_command = [
    sys.executable, "-m", "unittest", "discover", "-s", "tests"
]
require(python3_test_command[0] == sys.executable,
        "Python 3 tests must run through the selected checker interpreter")
py_files = [str(path.relative_to(ROOT)) for path in sorted(ROOT.glob("*.py"))]
py_files += [str(path.relative_to(ROOT)) for path in sorted((ROOT / "gnip_search").glob("*.py"))]
py_files += [str(path.relative_to(ROOT)) for path in sorted((ROOT / "tests").glob("*.py"))]
for filename in py_files:
    compile((ROOT / filename).read_bytes(), filename, "exec")
subprocess.check_call(python3_test_command, cwd=str(ROOT), env=env)
require(not python_artifacts(),
        "Python 3 characterization tests must not generate bytecode artifacts")

python2 = shutil.which("python2")
if python2:
    python2_identity = subprocess.check_output([
        python2,
        "-c",
        (
            "import platform, sys\n"
            "sys.stdout.write('%s\\t%s\\t%s' % "
            "(sys.version_info[0], platform.python_implementation(), "
            "platform.python_version()))\n"
        ),
    ], cwd=str(ROOT)).decode("ascii", "replace").split("\t")
    require(len(python2_identity) == 3 and python2_identity[0] == "2",
            "python2 command must identify itself as a Python 2 interpreter")
    print("check-baseline: Python 2 syntax compiler: %s (%s %s)" % (
        python2, python2_identity[1], python2_identity[2]))
    syntax_check = (
        "import sys\n"
        "for filename in sys.argv[1:]:\n"
        "    compile(open(filename, 'rb').read(), filename, 'exec')\n"
    )
    subprocess.check_call([python2, "-c", syntax_check] + py_files, cwd=str(ROOT))
    require(not python_artifacts(),
            "baseline checks must not generate Python bytecode artifacts")
else:
    print("check-baseline: python2 not found; skipped Python 2 syntax compilation")

print("GNIP light demo baseline checks passed.")
