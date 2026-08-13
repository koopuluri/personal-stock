# Personal Stock Ledger Event Schema

This document describes event schema version 1 for formation and the initial seed
round, together with the generic overlays used to enrich or correct history. The
agreement controls legal and economic meaning; the contract supplies immutable order
and publication; this schema supplies payload representation and replay rules.

Schema versions belong to individual event types. Once an `(event_type,
schema_version)` pair is published, its accepted fields and meaning are immutable. A
later version or supplement adds representation without reinterpreting earlier bytes.

## Raw ledger envelope

The `StockLedger` contract assigns every event a sequential positive `sequence` and
emits:

```text
event_type       uppercase ASCII name of at most 32 bytes
schema_version   positive uint32
effective_at     positive uint64 Unix timestamp
payload          canonical UTF-8 JSON object bytes
previous_head    hash of the preceding raw event, or zero for sequence 1
event_hash       hash committing to this envelope and previous_head
```

`effective_at` is when the represented fact occurred, settled, or became effective.
The block timestamp separately shows when it was recorded. Overlay envelopes use the
recording time; embedded replacements and insertions carry the affected fact's
historical effective time.

Source batches express `effective_at` as an RFC 3339 UTC timestamp ending in `Z` and
place the event-specific payload in `data`. The publication tooling validates the
source and serializes `data` with sorted keys and no insignificant whitespace.

Every data object may contain an optional `public_note` string. Unknown fields are
invalid. Exact USD amounts are nonnegative base-10 strings, shares are positive JSON
integers, shareholder IDs use `holder_000001`, and hashes are 32-byte hexadecimal
values prefixed by `0x`. Binary floating-point numbers are prohibited.

## `FORMATION@1`

```text
owner_shareholder_id  SHAREHOLDER_ID
owner_display_name    nonempty string
owner_handle          nonempty string or null
```

This must be raw sequence 1 and may occur only once. It creates the ledger and
registers the owner. Formation itself creates no shares.

## `SHAREHOLDER_REGISTERED@1`

```text
shareholder_id  new SHAREHOLDER_ID
display_name    nonempty string
handle          nonempty string or null
```

Registration assigns an immutable public identifier and initial public profile. It
does not give the person shares. Private legal identity and authentication evidence
remain in supporting records.

## `AGREEMENT_ADOPTION@1`

```text
shareholder_id          existing SHAREHOLDER_ID
agreement_version       MAJOR.MINOR.PATCH version without leading zeroes
agreement_content_hash  HASH (SHA-256 agreement digest)
```

This records adoption of the exact agreement bytes identified by version and content
hash. The agreement content is maintained in the public source repository, not copied
into this event or a separate agreement contract.

## `ASSET_REGISTERED@1`

```text
asset_id        new ASSET_ID such as asset_000001
asset_category  nonempty public category
description     nonempty public string or null
acquired_at     RFC 3339 UTC timestamp
opening_asset   boolean
```

This assigns an opaque public identifier and classification to an in-scope asset.
`description` must not expose private issuer, account, grant, or security information.
An asset recorded before `PORTFOLIO_COMMENCEMENT` must be an opening asset. A later
asset must not be marked as opening.

## `OPENING_PORTFOLIO_ITEM@1`

```text
asset_id     existing opening ASSET_ID
item_type    ELIGIBLE_COST or CASH_EVENT
amount_usd   USD_POSITIVE
occurred_at  RFC 3339 UTC timestamp
```

These events record, in chronological order, every pre-commencement input required to
calculate the opening `PORTFOLIO_NET_GAIN` for assets still in scope. The envelope
time is the recording time during formation; `occurred_at` is the historical time of
the input. The agreement's opening-balance algorithm is applied in event order.

## `PORTFOLIO_COMMENCEMENT@1`

```text
opening_portfolio_net_gain_usd  signed, nonpositive exact USD amount
opening_item_count              nonnegative integer
cpi_2026_06                     positive exact index value
```

This occurs once, after the owner's agreement adoption and all opening assets and
opening portfolio items, and establishes `COMMENCEMENT_TIME` from its envelope time.
The declared opening balance must exactly match replay of the recorded opening items.
`PORTFOLIO_PEAK` begins at zero. Opening share issuances follow at the same timestamp
or later.

## `SHARE_ISSUANCE@1`

```text
recipient_shareholder_id  existing SHAREHOLDER_ID
shares                    SHARE_COUNT
actual_cash_paid_usd       USD_NONNEGATIVE
```

The event creates new outstanding shares. The recipient must be registered and must
have adopted the governing agreement. `actual_cash_paid_usd` is the total
`ACTUAL_CASH_PAID` assigned under the agreement and is `"0"` when no USD cash purchase
price was required. The owner's one opening issuance must be effective exactly at
`COMMENCEMENT_TIME`; the owner cannot receive a later issuance.

## `OWNER_TRANSFER@1`

```text
recipient_shareholder_id  existing SHAREHOLDER_ID
shares                    SHARE_COUNT
actual_cash_paid_usd       USD_NONNEGATIVE
```

The event moves existing owner shares to the recipient without changing outstanding
shares. The recipient must be registered and must have adopted the governing
agreement.

## `BUYOUT@1`

```text
seller_shareholder_id          existing non-owner SHAREHOLDER_ID
purchaser_shareholder_id       existing SHAREHOLDER_ID other than seller
shares                         SHARE_COUNT
settlement_price_usd_per_share USD_POSITIVE
```

Recording the event attests that the purchaser irrevocably funded the required
settlement price. The shares move to the purchaser and remain outstanding.

## Historical overlays

Overlays are raw ledger events but do not independently apply at their publication
position during domain replay. The resolver first constructs the effective
chronological history.

### `EVENT_SUPPLEMENT@1`

```text
target_sequence          prior logical event sequence
extension_type           uppercase ASCII extension name
extension_schema_version positive uint32
extension_data           nonempty JSON object
reason                   nonempty public string
supersedes_sequence      prior supplement sequence, optional
```

A supplement adds typed information without altering existing fields. There is one
active supplement for each `(target_sequence, extension_type)`. A later supplement
must identify the active supplement it replaces.

### `EVENT_REVISION@1`

```text
target_sequence       prior logical event sequence
replacement           complete embedded event
reason                nonempty public string
supersedes_sequence   prior active revision or void sequence, optional
after_sequence        corrected prior placement anchor, optional
```

The complete replacement retains the target's logical sequence. By default it retains
the target's historical position. `after_sequence` repositions it when correcting its
effective time also changes event order.

### `EVENT_VOID@1`

```text
target_sequence       prior logical event sequence
reason                nonempty public string
supersedes_sequence   prior active revision or void sequence, optional
```

A void removes the target's effect from replay without removing any raw record.
Revisions and voids form one linear supersession chain for each target.

### `EVENT_INSERTION@1`

```text
after_sequence  prior logical event sequence
inserted        complete embedded event
reason          nonempty public string
```

An insertion records an omitted historical event immediately after its anchor. The
insertion's raw sequence becomes the inserted event's logical sequence.

An embedded event contains `event_type`, `schema_version`, RFC 3339 `effective_at`,
and `data`. It may not itself be an overlay.

## Resolution and replay

To derive state:

1. verify the raw sequence and contract hash chain;
2. decode every immutable event schema version;
3. select the latest valid supplement and revision/void in each linear chain;
4. apply insertions and corrected placements;
5. reject cycles, duplicate placement, and nonchronological effective order; and
6. replay the resulting effective domain events from formation.

A correction changes the effective ledger interpretation, not physical history. A
payment, repayment, offset, or other practical consequence of a correction is a new
ordinary event. Complete implementation and operational details live in
[`README.md`](README.md).
