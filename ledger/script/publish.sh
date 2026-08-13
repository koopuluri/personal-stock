#!/usr/bin/env bash
# Verify the full journal, preview, and atomically append a reviewed event batch.
#
#   CONFIRM_PUBLISH=YES ledger/script/publish.sh <batch.json> <published-network-dir> [network]
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
LEDGER_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(cd -- "$LEDGER_DIR/.." && pwd)

if [ -f "$LEDGER_DIR/.env" ]; then
  set -a
  . "$LEDGER_DIR/.env"
  set +a
fi

BATCH_PATH=${1:-}
PUBLISHED_NETWORK_DIR=${2:-}
NETWORK=${3:-${NETWORK:-base_sepolia}}
CONFIRMATIONS=${CONFIRMATIONS:-5}
if [ -z "$BATCH_PATH" ] || [ -z "$PUBLISHED_NETWORK_DIR" ]; then
  echo "usage: ledger/script/publish.sh <batch.json> <published-network-dir> [network]" >&2
  exit 1
fi
if [ -z "${ACCOUNT:-}" ]; then
  echo "ACCOUNT is not set (Foundry keystore account name)" >&2
  exit 1
fi
if [[ "$BATCH_PATH" != /* ]]; then
  BATCH_PATH="$REPO_ROOT/$BATCH_PATH"
fi
if [[ "$PUBLISHED_NETWORK_DIR" != /* ]]; then
  PUBLISHED_NETWORK_DIR="$REPO_ROOT/$PUBLISHED_NETWORK_DIR"
fi
DEPLOYMENT_PATH="$PUBLISHED_NETWORK_DIR/deployment.json"
JOURNAL_PATH="$PUBLISHED_NETWORK_DIR/journal.json"
DEPLOYMENT_REPO_PATH=${DEPLOYMENT_PATH#"$REPO_ROOT"/}
JOURNAL_REPO_PATH=${JOURNAL_PATH#"$REPO_ROOT"/}
if [ ! -s "$DEPLOYMENT_PATH" ]; then
  echo "deployment metadata does not exist: $DEPLOYMENT_PATH" >&2
  exit 1
fi
LEDGER_ADDRESS=$(jq -r '.stock_contract' "$DEPLOYMENT_PATH")

"$SCRIPT_DIR/sync.sh" "$PUBLISHED_NETWORK_DIR" "$NETWORK"
if ! git -C "$REPO_ROOT" ls-files --error-unmatch "$DEPLOYMENT_REPO_PATH" "$JOURNAL_REPO_PATH" >/dev/null 2>&1; then
  echo "commit the deployment and verified journal before publishing events" >&2
  exit 1
fi
if [ -n "$(git -C "$REPO_ROOT" status --porcelain --untracked-files=no)" ]; then
  echo "refusing publication from a dirty tracked worktree; commit and review first" >&2
  exit 1
fi
"$SCRIPT_DIR/check.sh" "$BATCH_PATH"

mkdir -p "$LEDGER_DIR/cache"
COMPILED_BATCH_PATH=$(mktemp "$LEDGER_DIR/cache/compiled-batch.XXXXXX.json")
PREVIEW_PATH=$(mktemp "$LEDGER_DIR/cache/preview.XXXXXX.json")
PREDICTED_HASHES=$(mktemp)
OBSERVED_HASHES=$(mktemp)
trap 'rm -f "$COMPILED_BATCH_PATH" "$PREVIEW_PATH" "$PREDICTED_HASHES" "$OBSERVED_HASHES"' EXIT

cast_in_ledger() {
  (cd "$LEDGER_DIR" && cast "$@")
}

python3 "$SCRIPT_DIR/ledger_events.py" "$BATCH_PATH" --compile "$COMPILED_BATCH_PATH"
python3 "$SCRIPT_DIR/preview_batch.py" "$JOURNAL_PATH" "$BATCH_PATH" --output "$PREVIEW_PATH"

FIRST_SEQUENCE=$(( $(jq -r '.before.event_count' "$PREVIEW_PATH") + 1 ))
LAST_SEQUENCE=$(jq -r '.after.event_count' "$PREVIEW_PATH")
PREDICTED_HEAD=$(jq -r '.after.head' "$PREVIEW_PATH")
mkdir -p "$PUBLISHED_NETWORK_DIR/batches"
SNAP="$PUBLISHED_NETWORK_DIR/batches/events-$(printf '%06d' "$FIRST_SEQUENCE")-$(printf '%06d' "$LAST_SEQUENCE")"
if [ -e "$SNAP.batch.json" ] || [ -e "$SNAP.receipt.json" ] || [ -e "$SNAP.preview.json" ]; then
  echo "refusing to replace an existing published batch snapshot" >&2
  exit 1
fi

echo
echo "reviewed append preview"
jq '{chain_id,stock_contract,before:{event_count:.before.event_count,head:.before.head},proposed_events:[.proposed_events[]|{sequence,event_type,schema_version,effective_at,event_hash,data}],after:{event_count:.after.event_count,head:.after.head},state_changes}' "$PREVIEW_PATH"
echo
if [ "${CONFIRM_PUBLISH:-}" != YES ]; then
  echo "refusing irreversible publication without CONFIRM_PUBLISH=YES" >&2
  exit 1
fi
if [ "$(jq -r '.chain_id' "$DEPLOYMENT_PATH")" -eq 8453 ] && [ "${CONFIRM_MAINNET_PUBLISH:-}" != YES ]; then
  echo "refusing Base mainnet publication without CONFIRM_MAINNET_PUBLISH=YES" >&2
  exit 1
fi

(
  cd "$LEDGER_DIR"
  LEDGER_ADDRESS="$LEDGER_ADDRESS" COMPILED_BATCH_PATH="$COMPILED_BATCH_PATH" \
    forge script script/Append.s.sol:Append \
      --rpc-url "$NETWORK" --account "$ACCOUNT" --broadcast
)

CHAIN_ID=$(cast_in_ledger chain-id --rpc-url "$NETWORK")
RUN="$LEDGER_DIR/broadcast/Append.s.sol/$CHAIN_ID/run-latest.json"
TX_HASH=$(jq -r '.receipts[-1].transactionHash' "$RUN")
RECEIPT=$(cast_in_ledger receipt "$TX_HASH" --rpc-url "$NETWORK" --confirmations "$CONFIRMATIONS" --json)
if [ "$(jq -r '.status' <<<"$RECEIPT")" != "0x1" ]; then
  echo "append transaction failed" >&2
  exit 1
fi
BLOCK=$(cast to-dec "$(jq -r '.receipts[-1].blockNumber' "$RUN")")
GAS_USED=$(cast to-dec "$(jq -r '.receipts[-1].gasUsed' "$RUN")")
BLOCK_TIMESTAMP=$(cast to-dec "$(cast_in_ledger block "$BLOCK" --rpc-url "$NETWORK" --field timestamp)")
SOURCE_COMMIT=$(git -C "$REPO_ROOT" rev-parse HEAD)

LEDGER_COUNT=$(cast to-dec "$(cast_in_ledger call "$LEDGER_ADDRESS" 'eventCount()(uint256)' --rpc-url "$NETWORK")")
LEDGER_HEAD=$(cast_in_ledger call "$LEDGER_ADDRESS" 'head()(bytes32)' --rpc-url "$NETWORK")
if [ "$LEDGER_COUNT" -ne "$LAST_SEQUENCE" ] || [ "${LEDGER_HEAD,,}" != "${PREDICTED_HEAD,,}" ]; then
  echo "post-publish contract state does not match preview" >&2
  exit 1
fi

cp "$BATCH_PATH" "$SNAP.batch.json"
cp "$PREVIEW_PATH" "$SNAP.preview.json"
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
  --arg sourceCommit "$SOURCE_COMMIT" \
  '{first_sequence:$firstSequence,last_sequence:$lastSequence,head:$head,transaction_hash:$txHash,block_number:$blockNumber,published_at_unix:$timestamp,stock_contract:$address,chain_id:$chainId,gas_used:$gasUsed,source_commit:$sourceCommit}' \
  > "$SNAP.receipt.json"

"$SCRIPT_DIR/sync.sh" "$PUBLISHED_NETWORK_DIR" "$NETWORK"
jq -r '.proposed_events[].event_hash' "$SNAP.preview.json" > "$PREDICTED_HASHES"
jq -r --argjson first "$FIRST_SEQUENCE" --argjson last "$LAST_SEQUENCE" '.events[] | select(.sequence >= $first and .sequence <= $last) | .event_hash' "$JOURNAL_PATH" > "$OBSERVED_HASHES"
if ! cmp -s "$PREDICTED_HASHES" "$OBSERVED_HASHES"; then
  echo "published log hashes do not match the reviewed preview" >&2
  exit 1
fi

rm -f "$COMPILED_BATCH_PATH" "$PREVIEW_PATH" "$PREDICTED_HASHES" "$OBSERVED_HASHES"
trap - EXIT

echo
echo "appended and verified events $FIRST_SEQUENCE-$LAST_SEQUENCE"
echo "head: $LEDGER_HEAD"
echo "batch:   $SNAP.batch.json"
echo "preview: $SNAP.preview.json"
echo "receipt: $SNAP.receipt.json"
