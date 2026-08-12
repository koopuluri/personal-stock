# Append-only Stock Ledger

This directory implements the onchain official history for one personal stock. The
chain stores an immutable journal of small events. It does **not** store or repeatedly
publish a complete state document.

The governing agreement is separate. Its exact source bytes live in a public source
repository and are identified in adoption and amendment events by version plus
`AGREEMENT_CONTENT_HASH`. There is no agreement contract.

## Model

```text
StockLedger logs
  -> verify sequence and hash chain
  -> decode each event by (event_type, schema_version)
  -> resolve supplements, revisions, voids, and insertions
  -> replay the effective chronological history
  -> current state and calculation trace
```

The raw journal is authoritative. A cap table, balance, obligation, or other current
value is a materialized view and can always be discarded and rebuilt.

The old state-document schema was useful as a catalogue of domain events, but its
publication layer does not fit this model:

- replaceable state snapshots, update types, and `previous_content_hash` are unnecessary;
- the contract's sequence and head hash supply ordering and continuity;
- schema versions belong to individual event types, not the whole historical ledger;
- the owner formerly stored in the document header belongs in `FORMATION`; and
- corrections and schema backfills are ordinary append-only ledger events.

The initial validator intentionally supports only formation and the seed-round domain
events, matching the current scope of [`schema.md`](schema.md), plus the four generic
overlay types below. Add later agreement events as new `(event_type, schema_version)`
decoders and reducer cases; the contract does not need to change.

## Contract

`src/StockLedger.sol` stores only:

- `stockName`;
- `controller` and `pendingController`;
- `eventCount`; and
- `head`, the hash of the latest event.

Every payload is emitted in `EventAppended`; historical payloads are not copied into
contract storage. This is appropriate because the intended consumer is an offchain
frontend. Other contracts cannot read historical logs, so a future onchain consumer
would require a separate state commitment or purpose-built state contract.

The event hash is:

```text
keccak256(abi.encode(
  keccak256("personal-stock-ledger/event/v1"),
  chain_id,
  ledger_address,
  sequence,
  event_type,
  schema_version,
  effective_at,
  keccak256(payload),
  previous_head
))
```

Including the chain and contract prevents a valid event from another stock or network
from being transplanted into this journal. `append` and `appendBatch` require the
publisher's expected count and head, so a stale publisher cannot accidentally append
against an unexpected history. A batch is atomic and limited to 100 events.

The controller should be a multisig or another account with a documented succession
and recovery process. Controller transfer is two-step. There is no deletion, pause,
payload replacement, contract upgrade, or controller method that changes the head
without appending an event.

## Event envelope

Every raw event has an immutable contract-assigned `sequence` and these supplied
fields:

```text
event_type       uppercase ASCII name, at most 32 bytes
schema_version   positive uint32, versioned independently per event type
effective_at     uint64 Unix time when the fact legally occurred or became effective
payload          canonical UTF-8 JSON bytes for that event schema
```

The transaction's block time is the recording/publication time. It is deliberately
different from `effective_at`. For correction overlays, the envelope time is when the
correction was recorded; an embedded replacement or insertion carries the historical
effective time of the corrected fact.

Source batches use an RFC 3339 UTC timestamp. `ledger_events.py` validates it and
converts it to Unix seconds. Payload objects are serialized with sorted keys and no
insignificant whitespace. Binary floating-point JSON values are prohibited; exact USD
amounts remain decimal strings.

## Retroactive changes

Old bytes are never reinterpreted or mutated. Four event types create the effective
view:

### `EVENT_SUPPLEMENT@1`

Adds a typed extension to an older logical event without changing its existing fields.
It is the normal mechanism for retroactively tracking newly introduced information.

```json
{
  "target_sequence": 12,
  "extension_type": "ISSUANCE_PROVENANCE",
  "extension_schema_version": 1,
  "extension_data": {
    "authorization_record": "private-record-17",
    "authorization_date": "2026-07-31"
  },
  "reason": "Backfilled from private records."
}
```

There is one active supplement for each `(target_sequence, extension_type)`. A later
one names the active supplement in `supersedes_sequence`.

### `EVENT_REVISION@1`

Completely replaces the effective body of an older event while preserving that
event's logical sequence and historical position. Use it when an existing field or the
event's meaning was wrong. Complete replacement avoids ambiguous JSON-patch behavior.
If correcting the effective time also changes chronological order, an optional
`after_sequence` moves the logical event to its corrected position. The resolver
rejects cycles and nonchronological effective histories.

### `EVENT_VOID@1`

Removes an event's effect from replay without removing it from the raw audit history.
Revisions and voids share one linear supersession chain per target.

### `EVENT_INSERTION@1`

Creates an omitted historical event immediately after an identified effective event.
The insertion event's own onchain sequence becomes the logical ID of the inserted
event. Insertions may be anchored after earlier insertions.

Resolution happens before domain replay. A correction does not undo a real payment or
transaction outside the ledger. Any resulting payment, repayment, or offset is a new
ordinary event.

## Source batch format

Publication accepts a small JSON file containing only the new events:

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
      "event_type": "FORMATION",
      "schema_version": 1,
      "effective_at": "2026-08-01T00:00:00Z",
      "data": {
        "owner_shareholder_id": "holder_000000",
        "owner_display_name": "Karthik Uppuluri",
        "owner_handle": "@koopuluri"
      }
    }
  ]
}
```

For the next batch, obtain the expected values directly from the contract:

```sh
cast call <ledger> 'eventCount()(uint256)' --rpc-url base_sepolia
cast call <ledger> 'head()(bytes32)' --rpc-url base_sepolia
```

The exact source batch and receipt are retained after publication, but they are mirrors
and operational evidence—not another authoritative ledger.

## Validation and replay

```sh
ledger/script/check.sh path/to/batch.json

# Compile the source form into the bytes consumed by Append.s.sol.
python3 ledger/script/ledger_events.py path/to/batch.json \
  --compile /tmp/compiled-batch.json

# A complete sequence-1 journal can also demonstrate overlay resolution and replay.
# Reader mode permits more than the contract's 100-event publication-batch limit.
python3 ledger/script/ledger_events.py complete-ledger.json --print-effective
python3 ledger/script/ledger_events.py complete-ledger.json --print-state
```

The current reducer covers `FORMATION`, `SHAREHOLDER_REGISTERED`,
`AGREEMENT_ADOPTION`, `SHARE_ISSUANCE`, `OWNER_TRANSFER`, and `BUYOUT`. Incremental
batches can structurally reference events already onchain, but complete semantic
validation requires fetching the preceding journal and replaying from sequence 1. A
production frontend and publishing service should always do that full replay before
display or publication.

## Setup and deployment

```sh
cp ledger/env.example ledger/.env
forge build --root ledger
forge test --root ledger -vv
python3 -m unittest discover -s ledger/test -p 'test_*.py'
```

Create an encrypted Foundry account once:

```sh
cast wallet import <name> --interactive
cast wallet list
```

Deploy to Base Sepolia first:

```sh
source ledger/.env
forge script ledger/script/Deploy.s.sol:Deploy \
  --root ledger \
  --rpc-url base_sepolia \
  --account "$ACCOUNT" \
  --broadcast \
  --verify
```

Only one contract is deployed. There is no `Document` contract and no agreement
contract.

## Publishing

```sh
ledger/script/publish.sh path/to/batch.json <ledger-address> base_sepolia
```

The script:

1. validates the source batch;
2. compiles every data object to canonical payload bytes;
3. verifies chain ID, contract address, expected count, and expected head;
4. appends the batch atomically;
5. verifies the resulting count and head; and
6. records the exact source batch and transaction receipt.

Publication is irreversible. Review the batch and its diff before signing.

## Frontend reads

Fetch `EventAppended` logs from the deployment block, ordered by block, transaction,
and log index. Verify:

1. sequences begin at 1 and are contiguous;
2. every event hash recomputes from the prior head;
3. the final sequence equals `eventCount()`;
4. the final hash equals `head()`;
5. each payload validates under its immutable `(event_type, schema_version)` decoder;
6. overlay supersession chains are linear and valid; and
7. the resolved domain history replays without violating agreement invariants.

The frontend may cache raw logs, resolved events, and replay checkpoints. Those caches
are disposable. If a revision affects sequence 12, invalidate the earliest checkpoint
at or before 12 and replay forward.
