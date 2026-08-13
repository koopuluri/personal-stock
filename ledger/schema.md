# Personal Stock Ledger Schema 1.0.0

This file is the canonical public specification for global ledger schema `1.0.0`.
Its SHA-256 over the exact UTF-8 file bytes is the `content_hash` in the first
`SCHEMA` event. No newline conversion, Unicode normalization, or Markdown rendering
is part of that hash.

The agreement controls legal and economic meaning. `StockLedger` supplies immutable
ordering and publication. This schema supplies event representation, correction
semantics, and deterministic replay rules.

## Schema activation

Raw sequence 1 must be:

```json
{
  "event_type": "SCHEMA",
  "effective_at": "2026-08-12T22:00:00-07:00",
  "data": {
    "version": "1.0.0",
    "content_hash": "0x...32-byte SHA-256..."
  }
}
```

`SCHEMA` has this fixed bootstrap shape independent of every versioned decoder. It
activates the identified global schema for the events after it. A later `SCHEMA`
event uses the same shape and changes the active decoder from that raw sequence
forward. It never changes how prior raw events were decoded. `SCHEMA` events cannot
be supplemented, revised, voided, inserted, or embedded.

Event names have no version suffix and raw events have no per-event schema field. A
public effective view may annotate an event with the schema active at its source
sequence so readers can reproduce its decoding.

## Raw envelope and source representation

The contract assigns every event a contiguous positive `sequence` and emits:

```text
event_type     uppercase ASCII name of at most 32 bytes
effective_at   positive uint64 Unix timestamp
payload        canonical UTF-8 JSON object bytes
previous_head  hash of the preceding raw event, or zero at sequence 1
event_hash     hash committing to the envelope and previous_head
```

`effective_at` is the represented fact's effective time. The block timestamp is its
separate publication time. Source batches express all timestamps as San Francisco
local civil time with an explicit offset, either `-07:00` or `-08:00`; tooling checks
the offset against `America/Los_Angeles` daylight-saving rules and converts it to
Unix seconds for the contract. For example, `2026-08-12T21:00:00-07:00` becomes
`1786593600`.

Payload objects are serialized with keys sorted lexicographically, no insignificant
whitespace, and no ASCII escaping requirement. Binary floating-point JSON numbers
are prohibited. Exact decimal values are strings. Share counts and sequence numbers
are JSON integers.

Except for `SCHEMA`, every data object may also contain an optional `public_note`
string. Unknown fields are invalid. Shareholder IDs use `holder_000001`; asset IDs
use `asset_000001`; hashes are 32-byte hexadecimal values prefixed with `0x`; and
versions use `MAJOR.MINOR.PATCH` without leading zeroes.

## Formation and configuration

### `FORMATION`

```text
owner_shareholder_id  SHAREHOLDER_ID
owner_display_name    nonempty string
owner_handle          nonempty string or null
```

This must be raw sequence 2, immediately after the initial `SCHEMA`, and may occur
only once. It registers the owner but creates no shares.

### `SHAREHOLDER_REGISTERED`

```text
shareholder_id  new SHAREHOLDER_ID
display_name    nonempty string
handle          nonempty string or null
```

Registration assigns a stable public ID and initial public profile. Private legal
identity and authentication evidence remain in supporting records.

### `AGREEMENT_ADOPTION`

```text
shareholder_id          existing SHAREHOLDER_ID
agreement_version       MAJOR.MINOR.PATCH
agreement_content_hash  HASH (SHA-256 of the exact agreement bytes)
```

This records adoption of the exact agreement identified by its release version and
content hash. The agreement source is not copied into the ledger.

### `AGREEMENT_CONFIGURATION`

This event copies only executable values needed for deterministic state calculation:

```text
floor_base_amount_usd          USD_POSITIVE, optional group
floor_cpi_series               nonempty string, optional group
floor_cpi_base_period          YYYY-MM, optional group
floor_cpi_base_value           DECIMAL_POSITIVE, optional group
authorized_shares              positive integer, optional
royalty_rate                   DECIMAL from 0 through 1, optional
amendment_approval_threshold   DECIMAL greater than 0 through 1, optional
```

At least one field is required. The four floor fields are one coherent group: if one
is present, all four must be present. The first configuration follows the owner's
adoption and must set every field. A later governing agreement can use one
configuration event that supplies only changed values; omitted values carry forward.
The reducer binds each configuration to the governing agreement active when the
event becomes effective, so its version and hash are not redundantly repeated.

`floor_base_amount_usd` is the agreement's base floor, not a minimum buyout price.
The floor's current nominal value is calculated when needed from the stated CPI
series, base period, and base value.

## Portfolio commencement

### `ASSET_REGISTERED`

```text
asset_id        new ASSET_ID
asset_category  nonempty public category
description     nonempty public string or null
acquired_at     San Francisco local timestamp with explicit offset
opening_asset   boolean
```

Descriptions must not expose private issuer, account, grant, or security details. A
pre-commencement asset must be an opening asset; a later asset must not be marked as
opening.

### `OPENING_PORTFOLIO_ITEM`

```text
asset_id     existing opening ASSET_ID
item_type    ELIGIBLE_COST or CASH_EVENT
amount_usd   USD_POSITIVE
occurred_at  San Francisco local timestamp with explicit offset
```

These events record the chronological pre-commencement inputs needed to calculate
the opening portfolio net gain. An eligible cost decreases the running amount. A
cash event increases it but the running amount is capped at zero.

### `PORTFOLIO_COMMENCEMENT`

```text
opening_portfolio_net_gain_usd  signed, nonpositive exact USD amount
opening_item_count              nonnegative integer
```

This occurs once after the owner's adoption, the complete initial configuration, and
all opening items. Its envelope time establishes `COMMENCEMENT_TIME`. The declared
count and balance must exactly match replay. `PORTFOLIO_PEAK` begins at zero.

## Shares

### `SHARE_ISSUANCE`

```text
recipient_shareholder_id  existing SHAREHOLDER_ID
shares                    positive integer
actual_cash_paid_usd       USD_NONNEGATIVE
```

The event creates outstanding shares. The recipient must have adopted the governing
agreement. The owner's opening issuance must be effective exactly at commencement;
the owner cannot receive a later issuance. Total outstanding shares may not exceed
the active `authorized_shares` configuration.

### `OWNER_TRANSFER`

```text
recipient_shareholder_id  existing SHAREHOLDER_ID
shares                    positive integer
actual_cash_paid_usd       USD_NONNEGATIVE
```

This moves existing owner shares to an eligible recipient without changing total
outstanding shares.

### `BUYOUT`

```text
seller_shareholder_id           existing non-owner SHAREHOLDER_ID
purchaser_shareholder_id        existing SHAREHOLDER_ID other than seller
shares                          positive integer
settlement_price_usd_per_share  USD_POSITIVE
```

Recording this event attests that the purchaser irrevocably funded the settlement.
The shares move to the purchaser and remain outstanding.

## Historical overlays

Overlays remain in the raw journal but are resolved before chronological domain
replay. Their own envelope time is the correction's publication/effective time;
embedded historical events carry the represented fact's time.

### `EVENT_SUPPLEMENT`

```text
target_sequence      prior logical event sequence
extension_type       uppercase ASCII extension name
extension_data       nonempty JSON object
reason               nonempty public string
supersedes_sequence  prior supplement sequence, optional
```

A supplement adds typed information without changing existing fields. It is decoded
under the schema active at the supplement's raw sequence. There is one active
supplement for each `(target_sequence, extension_type)`.

### `EVENT_REVISION`

```text
target_sequence      prior logical event sequence
replacement          complete embedded event
reason               nonempty public string
supersedes_sequence  prior active revision or void sequence, optional
after_sequence       corrected placement anchor, optional
```

The replacement retains the target's logical sequence and, by default, its historical
position. `after_sequence` repositions it if a corrected effective time changes order.

### `EVENT_VOID`

```text
target_sequence      prior logical event sequence
reason               nonempty public string
supersedes_sequence  prior active revision or void sequence, optional
```

A void removes the target's effect from replay without removing any raw record.
Revisions and voids form one linear supersession chain per target.

### `EVENT_INSERTION`

```text
after_sequence  prior logical event sequence
inserted        complete embedded event
reason          nonempty public string
```

An insertion records an omitted historical event after its anchor. Its raw sequence
becomes the inserted event's logical sequence.

An embedded event contains exactly `event_type`, a San Francisco `effective_at`, and
`data`. It is decoded under the schema active at the overlay's raw sequence and may
not itself be an overlay or `SCHEMA` event.

## Resolution and replay

Readers must:

1. verify raw sequences, canonical payloads, and the contract hash chain;
2. process `SCHEMA` activations by raw sequence and decode each later event under the
   active global version;
3. select the valid supplement and revision/void heads;
4. apply insertions and corrected placements;
5. reject cycles, duplicate placement, and nonchronological effective order; and
6. replay the effective domain history from formation.

A correction changes the ledger's effective interpretation, not an external payment
or transaction. Any real repayment, offset, or other consequence is a new ordinary
event. Operational details live in [`README.md`](README.md).
