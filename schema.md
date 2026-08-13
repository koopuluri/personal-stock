# Personal Stock Ledger Schema 1.0.0

This schema defines the JSON structure used by [`ledger.json`](ledger.json). The
Personal Stock Agreement controls the legal and economic meaning of every entry.

## Ledger document

The root object contains exactly:

```text
format           "personal-stock-ledger"
format_version   1
personal_stock   personal-stock identity object
schema_version   version of this schema
current_state    current public state derived from the effective events
events           complete recorded event array
```

The `personal_stock` object contains:

```text
id                    stable public identifier used in signing records
name                  public name
official_history_url  public URL of the live ledger.json
```

For this stock, `id` is `@koopuluri`. Moving the official-history location does not
create a new personal stock; the move must be recorded and access to the complete
history preserved.

## Current state

`current_state` appears before the event array so a reader sees the present position
first. It contains:

```text
as_of_sequence               last event sequence reflected in this state
status                       current lifecycle status
summary                      nonempty plain-language current summary
owner                        shareholder_id, name, and username
governing_agreement          version, content_hash, and release_url
commencement_time            timestamp or null before commencement
shares                       current capitalization and balances
configuration                current floor, royalty, and amendment settings
portfolio                    current public portfolio state
pending_amendment_proposals  current pending proposal array
```

The summary puts closely related figures together so a reader can understand the
current position without traversing the events. It is updated whenever an event
changes the state, and Git history preserves each earlier summary.

The `shares` object contains the three related capitalization figures together:

```text
authorized                        positive whole number of authorized shares
outstanding                       nonnegative whole number of issued shares
reserved_under_unvested_awards    nonnegative whole number committed to unvested awards
balances                          shareholder ID to whole outstanding-share balance
```

Available issuance capacity is not stored. When needed, it is derived as authorized
minus outstanding minus shares reserved under unvested awards.

The `configuration` object groups the current executable agreement settings:

```text
floor.base_amount_usd             positive decimal string
floor.cpi_series                  nonempty public series identifier
floor.cpi_base_period             YYYY-MM
floor.cpi_base_value              positive decimal string
royalty_rate                      decimal string from 0 through 1
amendment_approval_threshold      decimal string greater than 0 through 1
```

The `portfolio` object contains:

```text
assets               asset ID to current public asset information
opening_item_count   nonnegative whole number
net_gain_usd         signed decimal string
peak_usd             nonnegative decimal string
```

`events` is the complete recorded history. `current_state` is a convenient derived
view, not a separate source of authority. If it conflicts with the effective event
history, the event history controls and the state must be corrected.

## Event envelope

Every event contains:

```json
{
  "sequence": 1,
  "event_type": "FORMATION",
  "effective_at": "2026-08-13T14:15:00-07:00",
  "recorded_at": "2026-08-13T14:15:00-07:00",
  "data": {}
}
```

- `sequence` is a positive integer. It begins at 1 and increases contiguously in
  recording order.
- `event_type` is an uppercase name using letters, numbers, and underscores.
- `effective_at` is when the represented fact actually occurred, became effective,
  or settled.
- `recorded_at` is when the entry was added to the official history.
- `data` is an object containing the public inputs and results necessary to apply
  the event under the agreement.

An event may also contain `supporting_record_refs`, an array of opaque identifiers
for private supporting records. It may not expose private documents, legal names,
email addresses, account information, signatures, or authentication material.

All timestamps use San Francisco local civil time in RFC 3339 form with the correct
explicit `-07:00` or `-08:00` offset. Exact monetary and ratio values are decimal
strings; share counts and sequence numbers are JSON integers. Binary floating-point
numbers are not used for agreement calculations.

## Ordering and replay

Sequence records when entries were made. Agreement calculations use the events'
actual effective order: sort effective events by `effective_at`, using `sequence` to
break an exact timestamp tie, after applying corrections. A late entry may therefore
have an earlier effective time than the preceding sequence and must explain the delay
in `data.public_note`.

`current_state.as_of_sequence` equals the last event sequence, or 0 for an empty
ledger. Before formation the status is `not_formed`. After formation the state must
contain the current public values needed to determine share ownership, governing
agreement, portfolio calculations, obligations, and pending actions required by the
agreement.

## Event data

Every data object may also contain a nonempty `public_note`.

### `FORMATION`

```text
owner.shareholder_id  stable opaque shareholder identifier
owner.name            nonempty public name
owner.username        nonempty public username or null
```

Formation is sequence 1 and occurs once. It registers the owner but creates no
shares.

### `SHAREHOLDER_REGISTERED`

```text
shareholder_id  new stable opaque shareholder identifier
name            nonempty public name
username        nonempty public username or null
```

### `AGREEMENT_ADOPTION`

```text
shareholder_id           existing shareholder identifier
agreement_version        three-part published version
agreement_content_hash   SHA-256 of the exact published agreement bytes
agreement_release_url    immutable GitHub Release URL for those bytes
```

### `AGREEMENT_CONFIGURATION`

```text
floor_base_amount_usd          positive decimal string, optional group
floor_cpi_series               nonempty string, optional group
floor_cpi_base_period          YYYY-MM, optional group
floor_cpi_base_value           positive decimal string, optional group
authorized_shares              positive integer, optional
royalty_rate                   decimal string from 0 through 1, optional
amendment_approval_threshold   decimal string greater than 0 through 1, optional
```

At least one setting is present. The four floor fields are supplied together. The
first configuration follows the owner's adoption and supplies every setting. A later
configuration may contain only values changed by an effective agreement amendment.

### `ASSET_REGISTERED`

```text
asset_id        new stable opaque asset identifier
asset_category  nonempty public category
description     nonempty public description or null
acquired_at     San Francisco timestamp
opening_asset   boolean
```

### `OPENING_PORTFOLIO_ITEM`

```text
asset_id     registered opening asset identifier
item_type    ELIGIBLE_COST or CASH_EVENT
amount_usd   positive decimal string
occurred_at  San Francisco timestamp
```

### `PORTFOLIO_COMMENCEMENT`

```text
opening_portfolio_net_gain_usd  nonpositive decimal string
opening_item_count              nonnegative integer
```

This occurs once after the owner's adoption, initial configuration, and all opening
items. Its `effective_at` establishes `COMMENCEMENT_TIME`.

### `SHARE_ISSUANCE`

```text
recipient_shareholder_id  existing shareholder identifier
shares                    positive integer
actual_cash_paid_usd       nonnegative decimal string
```

### `OWNER_TRANSFER`

```text
recipient_shareholder_id  existing shareholder identifier
shares                    positive integer
actual_cash_paid_usd       nonnegative decimal string
```

### `BUYOUT`

```text
seller_shareholder_id           existing non-owner shareholder identifier
purchaser_shareholder_id        existing shareholder identifier other than seller
shares                          positive integer
settlement_price_usd_per_share  positive decimal string
```

Additional agreement events are added to this schema before first use. Schema
changes preserve the meaning of existing events.

## Corrections

A published or otherwise relied-upon event is never silently edited. Append:

```json
{
  "sequence": 10,
  "event_type": "CORRECTION",
  "effective_at": "2026-08-20T09:00:00-07:00",
  "recorded_at": "2026-08-20T09:00:00-07:00",
  "data": {
    "target_sequence": 4,
    "action": "REPLACE",
    "replacement": {
      "event_type": "OPENING_PORTFOLIO_ITEM",
      "effective_at": "2026-08-13T11:00:00-07:00",
      "data": {}
    },
    "reason": "Nonempty public explanation."
  }
}
```

`action` is `REPLACE` or `VOID`. `replacement` is required only for `REPLACE` and
may not itself be a `CORRECTION`. If more than one correction names the same target,
the correction with the highest sequence controls. The original entry and every
correction remain visible.

An omitted historical fact is appended as its ordinary event type with its actual
`effective_at`, current `recorded_at`, and an explanation. A correction changes the
ledger's effective interpretation; it does not by itself reverse a completed payment
or transaction outside the ledger.
