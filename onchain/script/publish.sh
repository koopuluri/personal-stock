#!/usr/bin/env bash
# Publish a document onchain and record exactly what was sent.
#
#   onchain/script/publish.sh <file> <doc-address> [network]
#
#   network defaults to base_sepolia. ACCOUNT (foundry keystore account name) must be
#   set, in the environment or in onchain/.env.
#
# This is irreversible. Read what it prints before confirming.
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ONCHAIN_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(cd -- "$ONCHAIN_DIR/.." && pwd)

if [ -f "$ONCHAIN_DIR/.env" ]; then
  set -a; . "$ONCHAIN_DIR/.env"; set +a
fi

DOC_PATH="${1:-${DOC_PATH:-}}"
DOC_ADDRESS="${2:-${DOC_ADDRESS:-}}"
NETWORK="${3:-${NETWORK:-base_sepolia}}"

if [ -z "$DOC_PATH" ] || [ -z "$DOC_ADDRESS" ]; then
  echo "usage: onchain/script/publish.sh <file> <doc-address> [network]" >&2
  exit 1
fi
if [ -z "${ACCOUNT:-}" ]; then
  echo "ACCOUNT is not set (foundry keystore account name, see onchain/env.example)" >&2
  exit 1
fi

if [[ "$DOC_PATH" != /* ]]; then
  DOC_PATH="$REPO_ROOT/$DOC_PATH"
fi

PUBLISHED_DIR="${PUBLISHED_DIR:-$REPO_ROOT/documents/published}"
if [[ "$PUBLISHED_DIR" != /* ]]; then
  PUBLISHED_DIR="$REPO_ROOT/$PUBLISHED_DIR"
fi

# 1. Canonicalization gate. Never publish bytes that fail this.
"$SCRIPT_DIR/check.sh" "$DOC_PATH"

# 2. Publish.
echo
LOG=$(mktemp)
trap 'rm -f "$LOG"' EXIT
(
  cd "$ONCHAIN_DIR"
  DOC_PATH="$DOC_PATH" DOC_ADDRESS="$DOC_ADDRESS" \
    forge script script/Publish.s.sol:Publish \
    --rpc-url "$NETWORK" --account "$ACCOUNT" --broadcast
) | tee "$LOG"

VERSION=$(grep 'PUBLISHED_VERSION=' "$LOG" | tail -1 | awk '{print $NF}')
HASH=$(grep 'PUBLISHED_HASH   =' "$LOG" | tail -1 | awk '{print $NF}')

# 3. Pull the receipt out of the broadcast log.
CHAIN_ID=$(cast chain-id --rpc-url "$NETWORK")
RUN="$ONCHAIN_DIR/broadcast/Publish.s.sol/$CHAIN_ID/run-latest.json"
TX_HASH=$(jq -r '.receipts[-1].transactionHash' "$RUN")
BLOCK=$(cast to-dec "$(jq -r '.receipts[-1].blockNumber' "$RUN")")
GAS_USED=$(cast to-dec "$(jq -r '.receipts[-1].gasUsed' "$RUN")")
TIMESTAMP=$(cast block "$BLOCK" --rpc-url "$NETWORK" --field timestamp)

LABEL=$(cast call "$DOC_ADDRESS" "label()(string)" --rpc-url "$NETWORK" | tr -d '"')

# 4. Snapshot the exact bytes plus the metadata that proves where they went.
mkdir -p "$PUBLISHED_DIR"
SNAP="$PUBLISHED_DIR/$LABEL-v$VERSION"
cp "$DOC_PATH" "$SNAP.md"
jq -n \
  --argjson version "$VERSION" \
  --arg contentHash "$HASH" \
  --arg txHash "$TX_HASH" \
  --argjson blockNumber "$BLOCK" \
  --argjson timestamp "$TIMESTAMP" \
  --arg address "$DOC_ADDRESS" \
  --argjson chainId "$CHAIN_ID" \
  --argjson gasUsed "$GAS_USED" \
  '{version:$version, contentHash:$contentHash, txHash:$txHash, blockNumber:$blockNumber, timestamp:$timestamp, address:$address, chainId:$chainId, gasUsed:$gasUsed}' \
  > "$SNAP.json"

rm -f "$LOG"
trap - EXIT

echo
echo "published $LABEL v$VERSION  gas $GAS_USED"
echo "snapshot: $SNAP.md"
echo "          $SNAP.json"
echo
echo "Snapshots are records of what was sent. Do not edit them."
