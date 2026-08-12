#!/usr/bin/env bash
# Validate, compile, and atomically append an event batch to StockLedger.
#
#   ledger/script/publish.sh <event-batch.json> <ledger-address> [network]
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
LEDGER_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(cd -- "$LEDGER_DIR/.." && pwd)

if [ -f "$LEDGER_DIR/.env" ]; then
  set -a
  . "$LEDGER_DIR/.env"
  set +a
fi

BATCH_PATH="${1:-${BATCH_PATH:-}}"
LEDGER_ADDRESS="${2:-${LEDGER_ADDRESS:-}}"
NETWORK="${3:-${NETWORK:-base_sepolia}}"

if [ -z "$BATCH_PATH" ] || [ -z "$LEDGER_ADDRESS" ]; then
  echo "usage: ledger/script/publish.sh <event-batch.json> <ledger-address> [network]" >&2
  exit 1
fi
if [ -z "${ACCOUNT:-}" ]; then
  echo "ACCOUNT is not set (Foundry keystore account name)" >&2
  exit 1
fi
if [[ "$BATCH_PATH" != /* ]]; then
  BATCH_PATH="$REPO_ROOT/$BATCH_PATH"
fi

PUBLISHED_DIR="${PUBLISHED_DIR:-$REPO_ROOT/published/events}"
if [[ "$PUBLISHED_DIR" != /* ]]; then
  PUBLISHED_DIR="$REPO_ROOT/$PUBLISHED_DIR"
fi

"$SCRIPT_DIR/check.sh" "$BATCH_PATH"

mkdir -p "$LEDGER_DIR/cache"
COMPILED_BATCH_PATH=$(mktemp "$LEDGER_DIR/cache/compiled-batch.XXXXXX.json")
LOG=$(mktemp)
trap 'rm -f "$COMPILED_BATCH_PATH" "$LOG"' EXIT
python3 "$SCRIPT_DIR/ledger_events.py" "$BATCH_PATH" --compile "$COMPILED_BATCH_PATH"

echo
(
  cd "$LEDGER_DIR"
  LEDGER_ADDRESS="$LEDGER_ADDRESS" COMPILED_BATCH_PATH="$COMPILED_BATCH_PATH" \
    forge script script/Append.s.sol:Append \
      --rpc-url "$NETWORK" --account "$ACCOUNT" --broadcast
) | tee "$LOG"

CHAIN_ID=$(cast chain-id --rpc-url "$NETWORK")
RUN="$LEDGER_DIR/broadcast/Append.s.sol/$CHAIN_ID/run-latest.json"
TX_HASH=$(jq -r '.receipts[-1].transactionHash' "$RUN")
BLOCK=$(cast to-dec "$(jq -r '.receipts[-1].blockNumber' "$RUN")")
GAS_USED=$(cast to-dec "$(jq -r '.receipts[-1].gasUsed' "$RUN")")
BLOCK_TIMESTAMP=$(cast to-dec "$(cast block "$BLOCK" --rpc-url "$NETWORK" --field timestamp)")

EXPECTED_COUNT=$(jq -r '.expected_event_count' "$BATCH_PATH")
BATCH_SIZE=$(jq -r '.events | length' "$BATCH_PATH")
FIRST_SEQUENCE=$((EXPECTED_COUNT + 1))
LAST_SEQUENCE=$((EXPECTED_COUNT + BATCH_SIZE))
LEDGER_COUNT=$(cast to-dec "$(cast call "$LEDGER_ADDRESS" 'eventCount()(uint256)' --rpc-url "$NETWORK")")
LEDGER_HEAD=$(cast call "$LEDGER_ADDRESS" 'head()(bytes32)' --rpc-url "$NETWORK")

if [ "$LEDGER_COUNT" -ne "$LAST_SEQUENCE" ]; then
  echo "post-publish event count mismatch" >&2
  exit 1
fi

mkdir -p "$PUBLISHED_DIR"
SNAP="$PUBLISHED_DIR/events-$(printf '%06d' "$FIRST_SEQUENCE")-$(printf '%06d' "$LAST_SEQUENCE")"
cp "$BATCH_PATH" "$SNAP.batch.json"
jq -n \
  --argjson firstSequence "$FIRST_SEQUENCE" \
  --argjson lastSequence "$LAST_SEQUENCE" \
  --arg head "$LEDGER_HEAD" \
  --arg txHash "$TX_HASH" \
  --argjson blockNumber "$BLOCK" \
  --argjson timestamp "$BLOCK_TIMESTAMP" \
  --arg address "$LEDGER_ADDRESS" \
  --argjson chainId "$CHAIN_ID" \
  --argjson gasUsed "$GAS_USED" \
  '{firstSequence:$firstSequence,lastSequence:$lastSequence,head:$head,txHash:$txHash,blockNumber:$blockNumber,timestamp:$timestamp,address:$address,chainId:$chainId,gasUsed:$gasUsed}' \
  > "$SNAP.receipt.json"

rm -f "$COMPILED_BATCH_PATH" "$LOG"
trap - EXIT

echo
echo "appended events $FIRST_SEQUENCE-$LAST_SEQUENCE"
echo "head: $LEDGER_HEAD"
echo "snapshot: $SNAP.batch.json"
echo "receipt:  $SNAP.receipt.json"
