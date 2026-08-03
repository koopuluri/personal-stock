# Onchain Publishing System

This directory contains the smart contract, tests, validation, deployment, and
publishing tools used to publish the two primary documents to Base. All commands below
are run from the repository root.

**The chain is canonical.** Files in the repository are drafts until they are
published. If a draft disagrees with the contract, the contract is right.

Two documents, two contract instances of the same minimal `Document` contract:

| Document       | Contract | Base mainnet | Base Sepolia |
| -------------- | -------- | ------------ | ------------ |
| `documents/stock.md`     | label `stock`     | _not deployed_ | `<sepolia-stock>` |
| `documents/agreement.md` | label `agreement` | _not deployed_ | `<sepolia-agreement>` |

## Reading the current document

Basescan → the contract address → **Contract → Read Contract → `content`**. One click,
no tooling. That is what storing the full text onchain buys, and why the contracts must
be verified.

Also on that tab: `version` (how many publishes so far), `latestHash` (keccak256 of the
current bytes, the value referenced in signed documents), `label`, `owner`.

### Reading past versions

Storage holds only the latest version; every version ever published is in the logs.

```sh
cast logs --rpc-url base \
  --from-block <deploy-block> \
  --address <doc-address> \
  'Published(uint256 indexed,bytes32,string)'
```

Add `--topic-1 $(cast to-uint256 3)` to fetch one specific version. Decode a log's data
back into readable text with:

```sh
cast abi-decode 'x()(bytes32,string)' <data> --output
```

The transaction list on Basescan is the version history. Nothing is ever rewritten.

## Publishing is permanent

> **Publishing is irreversible.** There is no edit, no delete, no takedown, no
> upgrade path. Anything you publish is public forever, and the transaction proving you
> published it is public forever. A mistake is corrected by publishing the next version
> — the wrong version stays visible and stays part of the history. Content hashes are
> cited in signed legal documents; changing bytes after the fact is not an option that
> exists. Read the diff before you run the script.

## Canonicalization

Published bytes must be reproducible, because the hash of those bytes is what a
shareholder signs against. Both markdown files must be:

- UTF-8, no BOM
- LF line endings only, never CRLF
- exactly one trailing newline
- no trailing whitespace on any line
- no unresolved or malformed `0x...` address/hash references
- no date-shaped values containing `X` placeholders

`.gitattributes` forces LF on checkout. `onchain/script/check.sh` verifies these rules
and exits non-zero on failure; `onchain/script/publish.sh` runs it first and refuses to
publish if it fails. Nothing in the publish path normalizes content — the bytes on disk
are the bytes that go onchain. Never reformat these files casually: an invisible
whitespace change is a different document with a different hash.

```sh
onchain/script/check.sh                         # both documents
onchain/script/check.sh documents/stock.md      # one
```

## Setup

```sh
cp onchain/env.example onchain/.env  # fill in RPC URLs, BASESCAN_API_KEY, ACCOUNT
forge build --root onchain
forge test --root onchain -vv
```

### Signing key

Signing uses a Foundry **encrypted keystore account**, never a private key in a file or
an environment variable. Create one once:

```sh
cast wallet import <name> --interactive     # paste the key, set a password
cast wallet list
cast wallet address --account <name>
```

Every command below takes `--account <name>` and prompts for that password. Set
`ACCOUNT=<name>` in `onchain/.env` so `onchain/script/publish.sh` picks it up. The
keystore lives in `~/.foundry/keystores/`, outside this repo.

## Deploying

Sepolia first, always. Verification is not optional — without it Basescan cannot show
the "Read Contract" tab, and the document becomes unreadable to anyone without tooling.

```sh
source onchain/.env

# 1. Base Sepolia
forge script onchain/script/Deploy.s.sol:Deploy \
  --root onchain \
  --rpc-url base_sepolia --account "$ACCOUNT" --broadcast --verify

# 2. Base mainnet — only when Sepolia has been exercised end to end
forge script onchain/script/Deploy.s.sol:Deploy \
  --root onchain \
  --rpc-url base --account "$ACCOUNT" --broadcast --verify
```

The script deploys both instances and prints both addresses. Record them in the table
above. If verification fails or was skipped, verify after the fact:

```sh
forge verify-contract <address> onchain/src/Document.sol:Document \
  --root onchain --chain base --constructor-args $(cast abi-encode 'c(string)' 'stock')
```

Confirm the Read Contract tab loads before publishing anything.

## Publishing an update

```sh
# 1. Edit the draft.
$EDITOR documents/stock.md

# 2. Check the bytes. Read the diff — this is the last reversible moment.
onchain/script/check.sh documents/stock.md
git diff documents/stock.md

# 3. Publish.
onchain/script/publish.sh documents/stock.md <doc-address> base_sepolia   # or: base
```

`publish.sh` runs `check.sh`, runs the forge script (which prints the content hash and
byte length *before* sending), broadcasts the transaction, and then writes the record:

```
documents/published/stock-v3.md      the exact bytes that were published
documents/published/stock-v3.json    { version, contentHash, txHash, blockNumber, timestamp, address, chainId, gasUsed }
```

`documents/published/` is a record of what was sent. Never edit it. Set
`PUBLISHED_DIR` to somewhere else for throwaway testnet publishes you do not want in
the record.

Verify the result independently:

```sh
cast call <doc-address> 'latestHash()(bytes32)' --rpc-url base
cast keccak "$(cat documents/stock.md)"     # note: strips the trailing newline, see below
```

Reading the raw file bytes is what matters, so prefer comparing against the hash the
publish script printed, or:

```sh
python3 -c "import sys;print(sys.stdin.buffer.read().hex())" < documents/stock.md | xargs cast keccak
```

## Contract

`onchain/src/Document.sol` — under 50 lines, deployed twice. `label`, `owner`, `version`,
`content`, `latestHash`; `publish(string)` and `transferOwnership(address)`, both
owner-only. No proxy, no upgradeability, no pausing. Empty content reverts.

Storing content costs meaningfully more gas than emitting an event alone — roughly
20k gas per 32 bytes of new storage. A 5 KB document costs on the order of 3.6M gas.
That is a deliberate trade: the one-click read is worth it. See
`test_GasForFiveKilobyteDocument` for the current number.

```sh
forge test --root onchain -vv
```
