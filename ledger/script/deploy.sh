#!/usr/bin/env bash
# Deploy an empty StockLedger and record verified deployment metadata.
#
#   ledger/script/deploy.sh <published-network-dir> [network]
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
CONFIRMATIONS=${CONFIRMATIONS:-5}
if [ -z "$PUBLISHED_NETWORK_DIR" ]; then
  echo "usage: ledger/script/deploy.sh <published-network-dir> [network]" >&2
  exit 1
fi
if [ -z "${ACCOUNT:-}" ] || [ -z "${STOCK_NAME:-}" ] || [ -z "${CONTROLLER:-}" ]; then
  echo "ACCOUNT, STOCK_NAME, and CONTROLLER must be configured" >&2
  exit 1
fi
CHAIN_ID=$(cd "$LEDGER_DIR" && cast chain-id --rpc-url "$NETWORK")
RUN="$LEDGER_DIR/broadcast/Deploy.s.sol/$CHAIN_ID/run-latest.json"
if [ "${CONFIRM_DEPLOY:-}" != YES ]; then
  echo "refusing deployment without CONFIRM_DEPLOY=YES" >&2
  exit 1
fi
if [ "$CHAIN_ID" -eq 8453 ] && [ "${CONFIRM_MAINNET_DEPLOY:-}" != YES ]; then
  echo "refusing Base mainnet deployment without CONFIRM_MAINNET_DEPLOY=YES" >&2
  exit 1
fi
if [[ "$PUBLISHED_NETWORK_DIR" != /* ]]; then
  PUBLISHED_NETWORK_DIR="$REPO_ROOT/$PUBLISHED_NETWORK_DIR"
fi
DEPLOYMENT_PATH="$PUBLISHED_NETWORK_DIR/deployment.json"
if [ -e "$DEPLOYMENT_PATH" ]; then
  echo "refusing to replace deployment metadata: $DEPLOYMENT_PATH" >&2
  exit 1
fi
if [ -e "$RUN" ]; then
  echo "refusing to deploy while prior broadcast evidence exists: $RUN" >&2
  echo "inspect and recover that deployment before attempting another" >&2
  exit 1
fi
if [ -n "$(git -C "$REPO_ROOT" status --porcelain --untracked-files=no)" ]; then
  echo "refusing deployment from a dirty tracked worktree; commit and review first" >&2
  exit 1
fi
SOURCE_COMMIT=$(git -C "$REPO_ROOT" rev-parse HEAD)

mkdir -p "$PUBLISHED_NETWORK_DIR/batches"
(
  cd "$LEDGER_DIR"
  forge script script/Deploy.s.sol:Deploy \
    --rpc-url "$NETWORK" \
    --account "$ACCOUNT" \
    --broadcast
)

(
  cd "$LEDGER_DIR"
  TX_HASH=$(jq -r '.receipts[-1].transactionHash' "$RUN")
  ADDRESS=$(jq -r '.transactions[] | select(.contractName == "StockLedger") | .contractAddress' "$RUN" | tail -1)
  if [ -z "$ADDRESS" ] || [ "$ADDRESS" = null ]; then
    echo "could not determine deployed StockLedger address" >&2
    exit 1
  fi
  RECEIPT=$(cast receipt "$TX_HASH" --rpc-url "$NETWORK" --confirmations "$CONFIRMATIONS" --json)
  if [ "$(jq -r '.status' <<<"$RECEIPT")" != "0x1" ]; then
    echo "deployment transaction failed" >&2
    exit 1
  fi
  BLOCK=$(cast to-dec "$(jq -r '.blockNumber' <<<"$RECEIPT")")
  BLOCK_HASH=$(jq -r '.blockHash' <<<"$RECEIPT")
  DEPLOYER=$(jq -r '.from' <<<"$RECEIPT")
  TIMESTAMP=$(cast to-dec "$(cast block "$BLOCK" --rpc-url "$NETWORK" --field timestamp)")
  ONCHAIN_NAME=$(cast call "$ADDRESS" 'stockName()(string)' --rpc-url "$NETWORK" | sed -e 's/^"//' -e 's/"$//')
  ONCHAIN_CONTROLLER=$(cast call "$ADDRESS" 'controller()(address)' --rpc-url "$NETWORK")
  ONCHAIN_COUNT=$(cast to-dec "$(cast call "$ADDRESS" 'eventCount()(uint256)' --rpc-url "$NETWORK")")
  ONCHAIN_HEAD=$(cast call "$ADDRESS" 'head()(bytes32)' --rpc-url "$NETWORK")
  RUNTIME_CODE_HASH=$(cast keccak "$(cast code "$ADDRESS" --rpc-url "$NETWORK")")
  if [ "$ONCHAIN_NAME" != "$STOCK_NAME" ] || [ "$(printf '%s' "$ONCHAIN_CONTROLLER" | tr '[:upper:]' '[:lower:]')" != "$(printf '%s' "$CONTROLLER" | tr '[:upper:]' '[:lower:]')" ]; then
    echo "deployed contract configuration mismatch" >&2
    exit 1
  fi
  if [ "$ONCHAIN_COUNT" -ne 0 ] || [ "$ONCHAIN_HEAD" != "0x0000000000000000000000000000000000000000000000000000000000000000" ]; then
    echo "new ledger is not empty" >&2
    exit 1
  fi
  jq -n \
    --argjson chainId "$CHAIN_ID" \
    --arg network "$NETWORK" \
    --arg address "$ADDRESS" \
    --arg stockName "$STOCK_NAME" \
    --arg controller "$ONCHAIN_CONTROLLER" \
    --arg deployer "$DEPLOYER" \
    --arg transactionHash "$TX_HASH" \
    --argjson deploymentBlock "$BLOCK" \
    --arg blockHash "$BLOCK_HASH" \
    --argjson deployedAt "$TIMESTAMP" \
    --arg sourceCommit "$SOURCE_COMMIT" \
    --arg runtimeCodeHash "$RUNTIME_CODE_HASH" \
    '{format:"personal-stock-ledger-deployment",format_version:1,chain_id:$chainId,network:$network,stock_contract:$address,stock_name:$stockName,controller:$controller,deployer:$deployer,transaction_hash:$transactionHash,deployment_block:$deploymentBlock,block_hash:$blockHash,deployed_at_unix:$deployedAt,source_commit:$sourceCommit,runtime_code_hash:$runtimeCodeHash}' \
    > "$DEPLOYMENT_PATH"
)

"$SCRIPT_DIR/sync.sh" "$PUBLISHED_NETWORK_DIR" "$NETWORK"
if python3 "$SCRIPT_DIR/verify_source.py" "$DEPLOYMENT_PATH"; then
  :
else
  echo "warning: deployment is recorded and verified locally, but source verification failed" >&2
fi
echo "deployment: $DEPLOYMENT_PATH"
