#!/usr/bin/env bash
# Fetch and verify the complete onchain journal, then regenerate public views.
#
#   ledger/script/sync.sh <published-network-dir> [network]
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
LEDGER_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(cd -- "$LEDGER_DIR/.." && pwd)

if [ -f "$LEDGER_DIR/.env" ]; then
  set -a
  . "$LEDGER_DIR/.env"
  set +a
fi

PUBLISHED_NETWORK_DIR=${1:-}
NETWORK=${2:-${NETWORK:-base_sepolia}}
if [ -z "$PUBLISHED_NETWORK_DIR" ]; then
  echo "usage: ledger/script/sync.sh <published-network-dir> [network]" >&2
  exit 1
fi
if [[ "$PUBLISHED_NETWORK_DIR" != /* ]]; then
  PUBLISHED_NETWORK_DIR="$REPO_ROOT/$PUBLISHED_NETWORK_DIR"
fi
DEPLOYMENT_PATH="$PUBLISHED_NETWORK_DIR/deployment.json"
if [ ! -s "$DEPLOYMENT_PATH" ]; then
  echo "deployment metadata does not exist: $DEPLOYMENT_PATH" >&2
  exit 1
fi

(
  cd "$LEDGER_DIR"
  python3 "$SCRIPT_DIR/sync_ledger.py" "$DEPLOYMENT_PATH" --rpc-url "$NETWORK"
)
