# Append-only Stock Ledger

This directory implements the onchain official history for one personal stock. The
chain stores an immutable journal of small events. It does **not** store or repeatedly
publish a complete state document.

The governing [Personal Stock agreement](https://github.com/onrootnet/personal-stock)
is published separately by Rootnet. Its exact source bytes are identified in adoption
and amendment events by version plus `AGREEMENT_CONTENT_HASH`. There is no agreement
contract.

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

The repository nevertheless commits a complete verified mirror for readability and
auditability. Each `published/<network>/` directory contains deployment metadata, the
full raw journal reconstructed from logs, the resolved effective history, replayed
state, and every exact append batch with its preview and receipt. Generated views are
never edited by hand and never outrank the chain.

The old state-document schema was useful as a catalogue of domain events, but its
publication layer does not fit this model:

- replaceable state snapshots, update types, and `previous_content_hash` are unnecessary;
- the contract's sequence and head hash supply ordering and continuity;
- schema versions belong to individual event types, not the whole historical ledger;
- the owner formerly stored in the document header belongs in `FORMATION`; and
- corrections and schema backfills are ordinary append-only ledger events.

The initial validator supports formation, opening portfolio state, and the seed-round
domain events described in [`schema.md`](schema.md), plus the four generic overlay
types below. Add later agreement events as new `(event_type, schema_version)` decoders
and reducer cases; the contract does not need to change.

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

The exact source batch, pre-publication preview, and receipt are retained after
publication, but they are mirrors and operational evidence—not another authoritative
ledger.

## Complete public mirror

After deployment, synchronize the selected chain before drafting or publishing:

```sh
ledger/script/sync.sh published/base-sepolia base_sepolia
```

The synchronizer fetches `EventAppended` logs from the recorded deployment block and
verifies their order, canonical payload bytes, schema, `previous_head`, event hashes,
and final agreement with the contract's `eventCount()` and `head()`. It regenerates:

```text
published/base-sepolia/
  deployment.json
  journal.json
  effective.json
  state.json
  batches/
```

`journal.json` contains the complete raw onchain history and publication provenance.
`effective.json` resolves overlays. `state.json` is the current replay result. Git
history versions these files; the ledger itself has no separate release version.

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

Create the next local draft from the verified chain position:

```sh
python3 ledger/script/new_batch.py \
  published/base-sepolia/journal.json next.batch.json
```

Add one or more related events to `events`, then validate the complete candidate and
inspect predicted event hashes and state changes:

```sh
ledger/script/check.sh next.batch.json
python3 ledger/script/preview_batch.py \
  published/base-sepolia/journal.json next.batch.json
```

`next.batch.json` is ignored until publication. A batch is an atomic transaction
boundary, not a combined domain event: each element receives its own sequence and
hash. Use a batch whenever related facts, such as formation, should publish together.

The current reducer covers `FORMATION`, `SHAREHOLDER_REGISTERED`,
`AGREEMENT_ADOPTION`, `ASSET_REGISTERED`, `OPENING_PORTFOLIO_ITEM`,
`PORTFOLIO_COMMENCEMENT`, `SHARE_ISSUANCE`, `OWNER_TRANSFER`, and `BUYOUT`. Incremental
batches can structurally reference events already onchain, but complete semantic
validation requires fetching the preceding journal and replaying from sequence 1. A
production frontend and publishing service should always do that full replay before
display or publication.

`AGREEMENT_ADOPTION` records a person's first adoption; it is not an agreement-version
upgrade mechanism. A later version becomes governing only through the proposal,
delivery, approval, support-calculation, and effectiveness events required by §12.
Those event schemas and reducer transitions must be implemented and tested before the
first real amendment is proposed.

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

Deploy an empty ledger to Base Sepolia first:

```sh
CONFIRM_DEPLOY=YES ledger/script/deploy.sh \
  published/base-sepolia base_sepolia
```

Only one contract is deployed. There is no `Document` contract and no agreement
contract. Deployment records the address required by the owner's signed adoption but
does not form the stock, adopt the agreement, commence the portfolio, or issue shares.
The deployment script refuses to replace existing deployment metadata and submits the
exact source for public verification through Sourcify's v2 API. A verifier outage does not
discard the already-mined deployment or its locally verified metadata; retry source
verification with `ledger/script/verify_source.py <deployment.json>` if the script
reports a warning. If deployment is mined but a
later metadata step fails, do not blindly rerun: the script preserves and detects the
Foundry broadcast record so the first deployment can be recovered without creating a
second contract.

## Formation batch

After the empty contract exists, execute the owner's adoption using the deployed chain
ID and contract address. The reviewed formation batch then records, in order:

1. `FORMATION`;
2. the owner's `AGREEMENT_ADOPTION`;
3. one `ASSET_REGISTERED` for every opening in-scope asset;
4. chronological `OPENING_PORTFOLIO_ITEM` events needed to calculate the opening
   portfolio balance;
5. one `PORTFOLIO_COMMENCEMENT` declaring the replay-verified balance and CPI base;
6. opening `SHARE_ISSUANCE` events; and
7. any seed shareholder registrations, adoptions, and issuances that legally settle at
   formation.

Events with no corresponding real fact are omitted. If there are no opening assets or
historical opening items, the commencement records an item count of zero and an opening
balance of zero. Formation is normally one atomic batch, but every fact remains an
independent sequenced event. Base Sepolia rehearsals must use conspicuously fictitious
data and have no legal effect.

## Publishing

```sh
CONFIRM_PUBLISH=YES ledger/script/publish.sh \
  next.batch.json published/base-sepolia base_sepolia
```

The script:

1. synchronizes and verifies the complete live journal;
2. validates the proposed batch against that full history;
3. compiles every data object to canonical payload bytes;
4. predicts every event hash and displays the complete state diff;
5. requires the explicit `CONFIRM_PUBLISH=YES` irreversible-action gate;
6. verifies chain ID, contract address, expected count, and expected head;
7. appends the batch atomically;
8. verifies the resulting count and head against the preview;
9. waits for the configured confirmation count;
10. records the exact source batch, preview, and transaction receipt; and
11. resynchronizes the full mirror and checks every observed event hash.

Publication is irreversible. Review the complete preview before unlocking the
encrypted Foundry account and signing. Never put a private key in the environment,
command line, repository, or logs.

Base mainnet has an additional independent safety rail. Deployment requires
`CONFIRM_MAINNET_DEPLOY=YES`; event publication requires
`CONFIRM_MAINNET_PUBLISH=YES`. Never set either until the exact network, controller,
contract metadata, source commit, event payloads, agreement version/hash, calculated
opening state, predicted hashes, and state diff have been reviewed together.

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
