#!/usr/bin/env bash
set -euo pipefail

api_file="gnip_search/gnip_search_api.py"

if ! rg -q "ast.literal_eval" "$api_file"; then
  echo "GNIP link parsing must use literal_eval" >&2
  exit 1
fi

if ! rg -q "parse_link_list" "$api_file"; then
  echo "GNIP link parsing helper is missing" >&2
  exit 1
fi

if rg -n "\\b(exec|eval)\\s*\\(" "$api_file"; then
  echo "GNIP source must not execute parsed API fields" >&2
  exit 1
fi

echo "GNIP link parsing avoids code execution"
