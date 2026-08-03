#!/usr/bin/env bash
# Validates the canonical form of the markdown documents.
#
# Published bytes must be stable and reproducible: the content hash is referenced in
# signed legal documents, so an invisible whitespace change is a different document.
#
# Rules: UTF-8, no BOM. LF line endings only. Exactly one trailing newline.
# No trailing whitespace on any line. No unresolved address/hash or date placeholders.
#
# Usage: onchain/script/check.sh [file ...]
# Defaults to documents/stock.md and documents/agreement.md in the repository root.

set -u

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ONCHAIN_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(cd -- "$ONCHAIN_DIR/.." && pwd)

FILES=("$@")
if [ ${#FILES[@]} -eq 0 ]; then
  FILES=("$REPO_ROOT/documents/stock.md" "$REPO_ROOT/documents/agreement.md")
fi

fail=0

err() {
  echo "  FAIL: $1"
  fail=1
}

for requested_path in "${FILES[@]}"; do
  f="$requested_path"
  if [[ "$f" != /* && ! -f "$f" && -f "$REPO_ROOT/$f" ]]; then
    f="$REPO_ROOT/$f"
  fi

  echo "checking $requested_path"

  if [ ! -f "$f" ]; then
    err "file does not exist"
    continue
  fi

  if [ ! -s "$f" ]; then
    err "file is empty"
    continue
  fi

  # UTF-8, no BOM
  if ! iconv -f UTF-8 -t UTF-8 "$f" >/dev/null 2>&1; then
    err "not valid UTF-8"
  fi
  if [ "$(head -c 3 "$f" | od -An -tx1 | tr -d ' \n')" = "efbbbf" ]; then
    err "starts with a UTF-8 BOM"
  fi

  # LF only
  if LC_ALL=C grep -qU $'\r' "$f"; then
    err "contains CR (expected LF line endings only); offending lines:"
    LC_ALL=C grep -nU $'\r' "$f" | cut -d: -f1 | sed 's/^/        line /'
  fi

  # No trailing whitespace
  if LC_ALL=C grep -nE '[[:blank:]]+$' "$f" >/dev/null; then
    err "trailing whitespace on:"
    LC_ALL=C grep -nE '[[:blank:]]+$' "$f" | cut -d: -f1 | sed 's/^/        line /'
  fi

  # Exactly one trailing newline
  last_two=$(tail -c 2 "$f" | od -An -tx1 | tr -d ' \n')
  case "$last_two" in
    *0a0a) err "more than one trailing newline" ;;
    *0a)   ;;
    *)     err "missing trailing newline" ;;
  esac

  # Every 0x-prefixed reference in these documents is an Ethereum address or a
  # bytes32 hash. Reject placeholders and truncated/malformed values.
  hex_refs=$(LC_ALL=C grep -nEo '0x[[:alnum:]_]+' "$f" || true)
  invalid_hex_refs=""
  if [ -n "$hex_refs" ]; then
    while IFS=: read -r line ref; do
      if [[ ! "$ref" =~ ^0x([[:xdigit:]]{40}|[[:xdigit:]]{64})$ ]]; then
        invalid_hex_refs+="${line}: ${ref}"$'\n'
      fi
    done <<< "$hex_refs"
  fi
  if [ -n "$invalid_hex_refs" ]; then
    err "unresolved or malformed address/hash references:"
    printf '%s' "$invalid_hex_refs" | sed 's/^/        line /'
  fi

  # Reject date-shaped values containing X placeholders in any component.
  placeholder_dates=$(
    LC_ALL=C grep -nEi '[0-9x]{4}-[0-9x]{2}-[0-9x]{2}' "$f" \
      | grep -i 'x' \
      || true
  )
  if [ -n "$placeholder_dates" ]; then
    err "unresolved date placeholders:"
    printf '%s\n' "$placeholder_dates" | sed 's/^/        line /'
  fi

  # The stock document contains a metadata object followed by the event array.
  # Validate both as strict JSON and reject duplicate keys and event IDs.
  case "$f" in
    stock.md|*/stock.md)
      if ! python3 "$SCRIPT_DIR/validate_stock_json.py" "$f" >/dev/null 2>&1; then
        err "stock metadata or ledger JSON is invalid"
      fi
      ;;
  esac
done

if [ "$fail" -ne 0 ]; then
  echo
  echo "canonicalization check FAILED — do not publish"
  exit 1
fi

echo
echo "canonicalization check passed"
