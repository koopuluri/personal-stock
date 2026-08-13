#!/usr/bin/env bash
# Validate a source event batch before compilation or publication.
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
LEDGER_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(cd -- "$LEDGER_DIR/.." && pwd)

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "usage: ledger/script/check.sh <event-batch.json> [verified-journal.json]" >&2
  exit 1
fi

requested_path=$1
batch_path=$requested_path
if [[ "$batch_path" != /* && ! -f "$batch_path" && -f "$REPO_ROOT/$batch_path" ]]; then
  batch_path="$REPO_ROOT/$batch_path"
fi

if [ ! -s "$batch_path" ]; then
  echo "batch does not exist or is empty: $requested_path" >&2
  exit 1
fi
if ! iconv -f UTF-8 -t UTF-8 "$batch_path" >/dev/null 2>&1; then
  echo "batch is not valid UTF-8" >&2
  exit 1
fi
if [ "$(head -c 3 "$batch_path" | od -An -tx1 | tr -d ' \n')" = "efbbbf" ]; then
  echo "batch starts with a UTF-8 BOM" >&2
  exit 1
fi
if LC_ALL=C grep -qU $'\r' "$batch_path"; then
  echo "batch contains CR characters; use LF line endings" >&2
  exit 1
fi
if LC_ALL=C grep -nE '[[:blank:]]+$' "$batch_path" >/dev/null; then
  echo "batch contains trailing whitespace" >&2
  exit 1
fi
if [ "$(tail -c 1 "$batch_path" | od -An -tx1 | tr -d ' \n')" != "0a" ]; then
  echo "batch must end with one newline" >&2
  exit 1
fi

if [ "$#" -eq 2 ]; then
  journal_path=$2
  if [[ "$journal_path" != /* && ! -f "$journal_path" && -f "$REPO_ROOT/$journal_path" ]]; then
    journal_path="$REPO_ROOT/$journal_path"
  fi
  python3 "$SCRIPT_DIR/ledger_events.py" "$batch_path" --journal "$journal_path"
else
  python3 "$SCRIPT_DIR/ledger_events.py" "$batch_path"
fi
