# Append-only Stock Ledger

This directory implements the official onchain history for one personal stock. The
contract publishes an immutable journal of compact events. It does not store a full
state document or execute agreement economics onchain.

The governing [Personal Stock agreement](https://github.com/onrootnet/personal-stock)
is released separately. An adoption identifies exact agreement bytes by release
version and SHA-256. An `AGREEMENT_CONFIGURATION` event copies the small set of
executable values the reducer needs, so replay never fetches an agreement at runtime.

## The model

```text
StockLedger logs
  -> verify sequence and hash chain
  -> activate global schema by SCHEMA events
  -> decode subsequent events under that schema
  -> resolve supplements, revisions, voids, and insertions
  -> replay effective chronological history
  -> current state
```

The raw onchain journal is authoritative. The repository commits a complete verified
mirror for readability and reproducibility. Each active `published/<network>/`
directory contains deployment metadata, raw journal, effective history, replayed
state, and exact batches/previews/receipts. These files are regenerated from chain
and never outrank it.

## Contract envelope and hash

`src/StockLedger.sol` stores `stockName`, controller state, `eventCount`, and `head`.
Every payload is emitted in `EventAppended`. The event hash is:

```text
keccak256(abi.encode(
  keccak256("personal-stock-ledger/event/v2"),
  chain_id,
  ledger_address,
  sequence,
  event_type,
  effective_at,
  keccak256(payload),
  previous_head
))
```

Chain ID and contract address prevent cross-ledger replay. Expected count/head checks
prevent stale writers. A batch is atomic and limited to 100 events. Controller
transfer is two-step. There is no delete, pause, payload replacement, or upgrade
method.

## One global schema

Schema `1.0.0` is the exact [`schema.md`](schema.md) file. Its SHA-256 is placed in
the first `SCHEMA` event, which must be raw sequence 1. `FORMATION` must be sequence 2.

There are no schema suffixes in event names and no per-event schema field. A later
`SCHEMA` event activates a new decoder for subsequent raw sequences only. Old bytes
retain their original interpretation. Supplements and replacement/inserted events
are decoded under the schema active when the overlay is appended, which permits
retroactive enrichment without rewriting history.

The fixed `SCHEMA` bootstrap payload is always:

```json
{"version":"1.0.0","content_hash":"0x...SHA-256..."}
```

The initial implementation rejects an unsupported schema activation until its
validator, resolver, reducer, documentation, and tests exist.

## Timestamps

Source JSON always uses San Francisco local civil time with the correct explicit
offset, such as `2026-08-12T21:00:00-07:00`. Tooling checks it against
`America/Los_Angeles` daylight-saving rules and converts it to Unix seconds for the
contract. Public mirrors convert Unix seconds back to the same readable form. Block
time remains the distinct publication time.

## Source batch and public mirror

A source batch contains only proposed events plus the exact current chain position:

```json
{
  "format": "personal-stock-ledger-batch",
  "format_version": 1,
  "chain_id": 84532,
  "stock_contract": "0x1111111111111111111111111111111111111111",
  "expected_event_count": 0,
  "expected_head": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "events": [
    {
      "event_type": "SCHEMA",
      "effective_at": "2026-08-12T22:00:00-07:00",
      "data": {"version": "1.0.0", "content_hash": "0x..."}
    },
    {
      "event_type": "FORMATION",
      "effective_at": "2026-08-12T22:00:01-07:00",
      "data": {
        "owner_shareholder_id": "holder_000000",
        "owner_display_name": "Karthik Uppuluri",
        "owner_handle": "@koopuluri"
      }
    }
  ]
}
```

After deployment, sync before drafting or publishing:

```sh
ledger/script/sync.sh published/base-sepolia base_sepolia

python3 ledger/script/new_batch.py \
  published/base-sepolia/journal.json next.batch.json

ledger/script/check.sh \
  next.batch.json published/base-sepolia/journal.json

python3 ledger/script/preview_batch.py \
  published/base-sepolia/journal.json next.batch.json
```

The synchronizer fetches logs from the verified deployment block, checks sequence,
payload canonicalization, hash continuity, final count/head, deployment bytecode and
controller, then regenerates:

```text
published/base-sepolia/
  deployment.json
  journal.json
  effective.json
  state.json
  batches/
```

`journal.json` is the complete raw history. `effective.json` resolves overlays and
annotates the schema active at each source sequence. `state.json` is disposable replay
output. Git history versions these mirrors; the ledger has no release number.

## Validation and tests

```sh
forge build --root ledger
forge test --root ledger --offline -vv
python3 -m unittest discover -s ledger/test -p 'test_*.py'
```

The reducer currently supports the types in [`schema.md`](schema.md). Agreement
amendment/proposal schemas must be implemented and tested before a real amendment.
When a new agreement changes only some executable settings, one
`AGREEMENT_CONFIGURATION` event supplies the changed field or coherent group; omitted
values carry forward.

## Deploy

Create an encrypted Foundry account once and keep private key material out of the
repository, environment, command line, and logs:

```sh
cast wallet import <name> --interactive
cast wallet list
```

Deploy an empty rehearsal contract first:

```sh
CONFIRM_DEPLOY=YES ledger/script/deploy.sh \
  published/base-sepolia base_sepolia
```

Deploying only establishes the address needed for authoritative adoption. It does not
form the stock, adopt an agreement, commence the portfolio, or issue shares. The
script refuses dirty tracked worktrees, existing deployment metadata, and ambiguous
prior broadcast evidence; it verifies the mined contract and records the source
commit. Source verification is submitted to Sourcify when available.

Base mainnet requires a second explicit rail:

```sh
CONFIRM_DEPLOY=YES CONFIRM_MAINNET_DEPLOY=YES \
  ledger/script/deploy.sh published/base base
```

## Formation batch

The currently planned initial batch has six independent events in one atomic append:

1. `SCHEMA`;
2. `FORMATION`;
3. owner's `AGREEMENT_ADOPTION`;
4. complete `AGREEMENT_CONFIGURATION`;
5. `PORTFOLIO_COMMENCEMENT`; and
6. owner's opening `SHARE_ISSUANCE`.

Opening asset/item events are inserted before commencement only if real opening facts
exist. The owner's signed adoption must identify the authoritative mainnet chain ID,
deployed contract address, agreement version/hash, and signing time. A Base Sepolia
rehearsal uses conspicuously fictitious identity/signature facts and has no legal
effect.

## Publish

```sh
CONFIRM_PUBLISH=YES ledger/script/publish.sh \
  next.batch.json published/base-sepolia base_sepolia
```

The script synchronizes the live journal, validates the proposed batch against the
complete history and active schema, canonicalizes payloads, predicts every event hash
and the full state diff, appends atomically, verifies the mined count/head and logs,
then preserves the batch, preview, receipt, and regenerated views.

Base mainnet publication additionally requires `CONFIRM_MAINNET_PUBLISH=YES`.
Publication is irreversible. Before signing, review the network, controller, contract,
source commit, exact payloads/timestamps, agreement version/hash, opening calculation,
predicted hashes, and state diff.

## Reader rules

A reader must verify contiguous sequences, every hash link, final count/head,
canonical payloads, schema activation by raw sequence, overlay supersession, and full
domain replay. If a correction affects an old logical sequence, invalidate any cached
checkpoint at or before that sequence and replay forward.
