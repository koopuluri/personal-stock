# Personal Stock State Document Schema

```
Schema version  1
Applies to      documents/stock.md
```

## 1. Purpose and authority

This document defines the machine-readable shape of the personal-stock state document: its header, its chronological event ledger, and the rules for reconstructing current state from those events.

The agreement defines the parties' legal and economic rights. This schema defines only how facts governed by the agreement are represented and validated. If the two conflict, the agreement controls. A schema migration may change representation but may not change an event's meaning or any result under the agreement.

The state document is published as a complete canonical snapshot. Earlier snapshots remain permanently available through the publication history. The current snapshot contains the complete event ledger under the schema version named in its header.

Everything in the state document is public and permanent. Legal names, signed agreements, payment records, tax documents, transaction consideration categories, and other private supporting materials do not belong in it. Public events may use opaque identifiers and aggregate accounting inputs substantiated by the private records maintained under the agreement.

## 2. Document layout

The state document contains exactly two fenced `json` blocks:

1. one header object; and
2. one array containing all ledger events.

Text outside those blocks is ignored by the parser. The event array is ordered by record sequence. Event IDs preserve that sequence.

## 3. Header

The header has this shape:

```text
document_type              "personal_stock"
schema_version             positive integer
chain_id                   positive integer
stock_contract             ADDRESS
agreement_contract         ADDRESS
owner
  shareholder_id           SHAREHOLDER_ID
  display_name             nonempty string
  handle                   nonempty string or null
update                     UPDATE
```

`document_type`, `chain_id`, `stock_contract`, `agreement_contract`, and the owner's `shareholder_id` are immutable after the initial publication. The owner's current public profile in the header must match the latest profile derived from the ledger.

`schema_version` applies to the entire current snapshot. Events do not carry separate schema versions. Once a schema version has been used in a publication, its meaning is immutable.

### Update

`update` identifies how the current publication differs from the immediately preceding publication:

```text
type                       UPDATE_TYPE
previous_content_hash      HASH or null
summary                    nonempty public string
```

`UPDATE_TYPE` is exactly one of:

- `INITIAL`: the first publication;
- `APPEND`: one or more new factual events were appended;
- `CORRECTION`: one or more correction events were appended; or
- `MIGRATION`: the complete snapshot was converted to a new schema version.

The variants have these additional rules:

```text
INITIAL
  previous_content_hash    must be null

APPEND
  previous_content_hash    HASH of the exact preceding state document

CORRECTION
  previous_content_hash    HASH of the exact preceding state document
  correction_event_ids     nonempty array of EVENT_ID

MIGRATION
  previous_content_hash    HASH of the exact preceding state document
  from_schema_version      positive integer less than schema_version
```

An `APPEND` publication keeps the preceding event array as an exact prefix and appends only non-correction events.

A `CORRECTION` publication keeps the preceding event array as an exact prefix and appends only the `CORRECTION` events listed in `correction_event_ids`. Any supplemental payment, repayment, offset, reversal, or other practical consequence is recorded later through an `APPEND` publication.

A `MIGRATION` publication may rewrite the header and every event into the new schema's shape. It may not add, remove, reorder, correct, or change the meaning of an event, and the fully derived state before and after migration must be identical. A migration and a correction must be separate publications.

`APPEND` and `CORRECTION` keep the preceding schema version. Only `MIGRATION` changes it.

## 4. Common value types

```text
ADDRESS
  A 20-byte hexadecimal Ethereum address with a leading 0x.

HASH
  A 32-byte hexadecimal value with a leading 0x.

EVENT_ID
  "event_" followed by exactly six decimal digits.

SHAREHOLDER_ID
  "holder_" followed by exactly six decimal digits.

HOLDING_ID
  "holding_" followed by exactly six decimal digits.

TIMESTAMP
  An RFC 3339 timestamp in UTC, ending in Z. Fractional seconds are allowed.

SHARE_COUNT
  A positive JSON integer. Shares are never encoded as strings or fractions.

USD_VALUE
  An exact base-10 decimal or reduced fraction encoded as a JSON string.
  Examples: "0", "1.00", "2500000.75", "5/3", "-1000".
  Commas, currency symbols, exponents, leading plus signs, and binary floating
  point are prohibited. A fractional denominator must be a positive integer.

USD_NONNEGATIVE
  A USD_VALUE greater than or equal to zero.

USD_POSITIVE
  A USD_VALUE greater than zero.

CPI_VALUE
  A positive exact base-10 decimal encoded as a JSON string.

CPI_PERIOD
  A calendar month encoded as YYYY-MM.
```

Exact fractions are permitted so a benchmark, proportional allocation, or other derived value can be represented without introducing an unstated rounding rule. Calculations use exact rational arithmetic. The only rounding performed by the ledger is rounding royalty shares down to a whole share as required by the agreement.

Unless a field is expressly described as optional or nullable, it is required. Optional fields are omitted rather than set to null. Unknown fields are invalid under schema version 1.

## 5. Common event envelope

Every event has:

```text
event_id                   EVENT_ID
timestamp                  TIMESTAMP
event_type                 one event type defined below
public_note                string, optional
```

`event_id` values are unique and sequential in array order, beginning with `event_000001`. An event reference must normally identify an earlier event. The sole exception is a transaction approval that identifies the preassigned ID of the immediately contemplated later transaction.

For an ordinary event, `timestamp` is the time the represented action settled, became effective, or was recorded when the agreement expressly makes recording effective. Events are entered chronologically. If two events have the same timestamp, array order controls. A correction event's timestamp is the time the correction was recorded; its replacement is applied at the target event's original position during replay.

`public_note` is permanent public text. It must not contain private supporting information.

## 6. Administrative events

### `FORMATION`

```text
No event-specific fields.
```

`FORMATION` must be `event_000001` and may occur only once. It establishes the ledger before commencement. Authorized shares, benchmark parameters, the floor, and other agreement terms are not repeated in this event. Immediately before commencement, outstanding shares, cumulative realized value, both high-water marks, Reinvestment Capital, and the benchmark window are derived as zero or empty under the agreement.

### `SHAREHOLDER_REGISTERED`

```text
shareholder_id             new SHAREHOLDER_ID
display_name               nonempty string
handle                     nonempty string or null
```

This assigns an immutable public identifier and public profile. Registration alone does not make the person a shareholder; that status is derived from share ownership. A legal name is included only if the person deliberately uses it as the public display name.

### `SHAREHOLDER_PROFILE_UPDATED`

```text
shareholder_id             existing SHAREHOLDER_ID
display_name               nonempty string, optional
handle                     nonempty string or null, optional
```

At least one profile field must be present. Earlier public profiles remain in publication history.

### `AGREEMENT_VERSION_ISSUED`

```text
agreement_version          nonempty string
agreement_content_hash     HASH
```

The hash must identify the exact agreement content issued through the agreement contract. The latest issued version is the version a new recipient must adopt before first receiving shares.

### `AGREEMENT_ADOPTION`

```text
shareholder_id             existing SHAREHOLDER_ID
agreement_version          previously issued version string
agreement_content_hash     HASH for that exact version
```

The event records adoption of the complete agreement version. A person's applicable agreement version is the latest version that person has adopted, subject to the shared-term rules in the agreement.

### `SHARED_TERMS_EFFECTIVE`

```text
agreement_version          issued version string
agreement_content_hash     HASH for that exact version
changed_terms              nonempty array of nonempty strings
adoption_event_ids         nonempty array of EVENT_ID
```

The event may be recorded only after every current shareholder has adopted the same shared-term change. `adoption_event_ids` must identify the qualifying adoptions. The exact operative language comes from the agreement version, not from `changed_terms`, which is an index for readers.

### `TRANSFER_POLICY_SET`

```text
policy_code                "OWNER_APPROVAL_REQUIRED", "CURRENT_HOLDERS_ONLY",
                           "ALL_TRANSFERS_PERMITTED", or "NO_VOLUNTARY_TRANSFERS"
policy                     nonempty public string
replaces_event_id          EVENT_ID, optional
```

This records the owner's generally applicable voluntary-transfer policy. `policy_code` supplies the machine-enforceable rule, while `policy` states the same rule for readers. `OWNER_APPROVAL_REQUIRED` means a transaction-specific permission is required; `CURRENT_HOLDERS_ONLY` permits a sale whose buyer already holds shares immediately before settlement; `ALL_TRANSFERS_PERMITTED` supplies general permission; and `NO_VOLUNTARY_TRANSFERS` supplies none. If a prior policy exists, `replaces_event_id` must identify the latest `TRANSFER_POLICY_SET` event. The newest effective event controls unsettled transfers; it does not affect completed transfers.

### `TRANSFER_PERMISSION_GRANTED`

```text
seller_shareholder_id      existing SHAREHOLDER_ID
recipient_shareholder_id   existing SHAREHOLDER_ID
maximum_shares             SHARE_COUNT or null
expires_at                 TIMESTAMP or null
irrevocable                boolean
```

The event records transaction-specific permission. Null `maximum_shares` means no quantity cap; null `expires_at` means no stated expiration. Permission remains subject to the agreement and applicable law.

### `TRANSFER_PERMISSION_REVOKED`

```text
permission_event_id        prior EVENT_ID for TRANSFER_PERMISSION_GRANTED
```

The permission must still be revocable and no transfer relying on it may already have settled.

### `TRANSACTION_APPROVAL`

```text
subject_event_id           preassigned EVENT_ID of the contemplated transaction
approval_type              "BELOW_BENCHMARK"
approving_shareholder_ids  nonempty array of unique SHAREHOLDER_ID
```

The approvers must be the owner and every other current shareholder required by the agreement immediately before the contemplated issuance or owner transfer. The referenced transaction must be the next transaction using this approval.

### `DISTRIBUTION_ELECTION_CHANGED`

```text
shareholder_id             current non-owner SHAREHOLDER_ID
election                   "REINVEST" or "DISTRIBUTE"
```

The election applies to every share held by that shareholder from the event's effective time. A new shareholder's initial `REINVEST` election is derived from the agreement and requires no event.

### `CPI_OBSERVATION`

```text
series_id                  nonempty string
series_status              "AGREEMENT_SERIES", "OFFICIAL_SUCCESSOR",
                           or "CLOSEST_AVAILABLE"
period                     CPI_PERIOD
value                      CPI_VALUE
publication_date           calendar date encoded as YYYY-MM-DD
```

This records a published CPI input used to evaluate the floor. For the agreement's named series, `series_id` is `CUUR0000SA0` and `series_status` is `AGREEMENT_SERIES`. A successor status may be used only under the fallback order in the agreement. The base observation for June 2026 and every later observation relied upon by a realization or tax reconciliation must be recorded. The most recently published eligible observation at the evaluation timestamp controls.

## 7. Share events

### `SHARE_ISSUANCE`

```text
recipient_shareholder_id                       existing SHAREHOLDER_ID
shares                                         SHARE_COUNT
recorded_transaction_price_usd_per_share       USD_POSITIVE
approval_event_id                              EVENT_ID, optional
```

The event increases outstanding shares. The recipient must have adopted the latest agreement version before the event. The event contributes `shares` to the benchmark window. `approval_event_id` is required only for a below-benchmark issuance requiring unanimous approval.

The first `SHARE_ISSUANCE` establishes `COMMENCEMENT_TIME`. Before or simultaneously with it, every opening holding and opening holding cost required by the agreement must have been recorded.

### `OWNER_TRANSFER`

```text
recipient_shareholder_id                       existing SHAREHOLDER_ID
shares                                         SHARE_COUNT
recorded_transaction_price_usd_per_share       USD_POSITIVE
approval_event_id                              EVENT_ID, optional
```

The owner is the sender. The event moves existing shares without changing outstanding shares and contributes `shares` to the benchmark window. It never states whether consideration was cash, services, a gift, or something else. `approval_event_id` is required only for a below-benchmark transfer requiring unanimous approval.

### `VOLUNTARY_SALE`

```text
seller_shareholder_id      existing non-owner SHAREHOLDER_ID
buyer_shareholder_id       existing SHAREHOLDER_ID
buyer_shares               SHARE_COUNT
sale_price_usd_per_share   USD_POSITIVE
royalty_shares             nonnegative JSON integer
permission_basis           "POLICY" or "SPECIFIC_PERMISSION"
permission_event_id        EVENT_ID, optional
```

`permission_event_id` is required exactly when `permission_basis` is `SPECIFIC_PERMISSION`. Payment, the buyer's receipt of `buyer_shares`, and the owner's receipt of `royalty_shares` constitute one settlement represented by this event.

The sale price is the recorded transaction price for `buyer_shares`. Only `buyer_shares` enter the benchmark window; royalty shares are excluded. The validator derives and verifies sale result, cumulative sale result, royalty high-water mark, royalty value, royalty shares, and the seller's required share balance under the seller's applicable agreement version.

### `BUYBACK`

```text
seller_shareholder_id      existing non-owner SHAREHOLDER_ID
shares                     SHARE_COUNT
settlement_price_usd_per_share                  USD_POSITIVE
```

The purchaser is the owner. Recording the event attests that the full purchase price was irrevocably funded as required by the agreement. Shares move to the owner and remain outstanding. The event has no royalty and is excluded from benchmark volume.

### `DIRECTED_SALE`

```text
seller_shareholder_id      existing non-owner SHAREHOLDER_ID
purchaser_shareholder_id   existing SHAREHOLDER_ID
shares                     SHARE_COUNT
settlement_price_usd_per_share                  USD_POSITIVE
```

Recording the event attests that the full purchase price was irrevocably funded as required by the agreement. The purchaser must satisfy the recipient requirements before settlement. The event has no royalty and is excluded from benchmark volume.

### `LEGAL_SUCCESSION`

```text
prior_holder_id                                existing SHAREHOLDER_ID
temporary_holder_id                            existing SHAREHOLDER_ID
shares                                         SHARE_COUNT
recorded_transaction_price_usd_per_share       USD_POSITIVE
```

This records shares passing by operation of law to a temporary holder under the agreement. It does not make that person the permanent holder or permit an election change or voluntary transfer. The prior holder's applicable agreement version and election continue to govern. If the prior holder is the deceased owner, the reducer continues treating those shares as the owner's shares while held by the estate. Because legal succession is a noncash share movement other than a buyback or directed sale, its recorded price is the benchmark immediately before the movement, and its shares enter the benchmark window.

## 8. Holding and realized-value events

### `HOLDING_REGISTERED`

```text
holding_id                                     new HOLDING_ID
registration_type                              "OPENING", "ACQUISITION", or "SUBSTITUTE"
public_label                                   nonempty string or null
holding_cost_usd                               USD_NONNEGATIVE
reinvestment_capital_funded_cost_usd           USD_NONNEGATIVE
```

`reinvestment_capital_funded_cost_usd` may not exceed `holding_cost_usd`. A public label may be omitted by setting it to null; private records must still identify and substantiate the holding. Every in-scope holding owned at commencement must have an `OPENING` registration before or simultaneously with the first issuance.

### `HOLDING_COST_ADDED`

```text
holding_id                                     existing open HOLDING_ID
cost_type                                      "ACQUISITION", "EXERCISE", "VESTING",
                                               "PRESERVATION", "ENFORCEMENT", "TRANSFORM",
                                               "ATTRIBUTABLE_TAX", or "OTHER_ALLOWED"
cost_added_usd                                 USD_POSITIVE
reinvestment_capital_funded_cost_usd           USD_NONNEGATIVE
```

The Reinvestment-Capital-funded portion may not exceed `cost_added_usd`. The event increases the holding's unrecovered holding cost and records the source allocation needed to derive later Reinvestment Capital losses and recoveries.

### `VALUATION_RECORDED`

```text
holding_ids                 nonempty array of existing HOLDING_ID
valuation_purpose           "COST_ALLOCATION", "TRANSFORM", "MIXED_EXIT",
                            or "OTHER_AGREEMENT_PURPOSE"
method                      ALLOCATION_METHOD
components                  nonempty array of VALUATION_COMPONENT
```

`VALUATION_COMPONENT` has:

```text
component                   nonempty public string
value_usd                   USD_NONNEGATIVE
```

`ALLOCATION_METHOD` is exactly one of `TRANSACTION_DOCUMENTS`, `QUOTED_MARKET_PRICE`, `INDEPENDENT_VALUATION`, or `OWNER_GOOD_FAITH_ESTIMATE`, in the priority order established by the agreement. Components may use opaque public labels. Private valuation materials remain in supporting records.

This event records the contemporaneous values needed to reproduce a later cost allocation. A transform or realization that requires valuation judgment must reference the applicable prior valuation event.

### `HOLDING_TRANSFORMED`

```text
transformation_type        "TRANSFORM" or "NONCASH_EXIT"
source_holdings            nonempty array of SOURCE_HOLDING
resulting_holdings         nonempty array of RESULTING_HOLDING
valuation_event_id         prior EVENT_ID for VALUATION_RECORDED, optional
```

`SOURCE_HOLDING` has:

```text
holding_id                                     existing open HOLDING_ID
holding_cost_removed_usd                       USD_NONNEGATIVE
reinvestment_capital_cost_removed_usd          USD_NONNEGATIVE
closes_holding                                 boolean
```

`RESULTING_HOLDING` has:

```text
holding_id                                     new HOLDING_ID
public_label                                   nonempty string or null
holding_cost_usd                               USD_NONNEGATIVE
reinvestment_capital_funded_cost_usd           USD_NONNEGATIVE
```

The total cost and Reinvestment-Capital-funded cost removed from source holdings must equal the respective totals assigned to resulting holdings. `valuation_event_id` is required when cost is divided using relative values and omitted for a simple carry with no allocation judgment. The event creates no realized value.

### `REALIZATION`

```text
holding_id                     existing HOLDING_ID
realization_type               "CASH_EXIT", "EXIT_EQUIVALENT_DISTRIBUTION",
                               "TERMINAL_EXIT", or "LATER_RECOVERY"
floor_cpi_event_id             prior EVENT_ID for CPI_OBSERVATION
gross_cash_proceeds_usd        USD_NONNEGATIVE
allocated_holding_cost_usd     USD_NONNEGATIVE
direct_transaction_expenses_usd                     USD_NONNEGATIVE
attributable_taxes_usd         USD_NONNEGATIVE
closes_holding                 boolean
resulting_holdings             array of RESULTING_HOLDING, optional
valuation_event_id             prior EVENT_ID for VALUATION_RECORDED, optional
```

The validator derives:

```text
REALIZED_VALUE = gross_cash_proceeds_usd
                 - allocated_holding_cost_usd
                 - direct_transaction_expenses_usd
                 - attributable_taxes_usd
```

`floor_cpi_event_id` identifies the recorded observation controlling the floor at this evaluation. The validator verifies that it was the most recently published eligible observation at the event timestamp, calculates the applicable floor, and then updates cumulative realized value, the distribution high-water mark, newly qualifying value, owner value, non-owner participation, distribution result, Reinvestment Capital, and any Reinvestment-Capital-attributable loss or recovery.

For `TERMINAL_EXIT`, gross cash proceeds must be zero, allocated holding cost must equal all remaining cost attributable to the extinguished portion, and no direct or indirect economic interest may remain. A later recovery may reference the closed holding and begins with zero remaining holding cost.

`resulting_holdings` is used for mixed cash-and-noncash exits. `valuation_event_id` is required whenever cost must be allocated among cash, retained, or resulting components using relative values, and must be omitted when no allocation judgment is required.

### `TAX_RECONCILIATION`

```text
source_realization_event_id   prior EVENT_ID for REALIZATION
reconciliation_type           "ADDITIONAL_TAX" or "REFUND_OR_RESERVE_RELEASE"
amount_usd                    USD_POSITIVE
floor_cpi_event_id           prior EVENT_ID for CPI_OBSERVATION
```

An additional tax creates a negative realized-value adjustment. A refund or released reserve creates a positive adjustment when available as cash. `floor_cpi_event_id` identifies the observation controlling the floor at this evaluation. The validator evaluates the adjustment as a realization event under the shares, elections, floor, and other terms effective at the reconciliation timestamp, and makes the required Reinvestment Capital adjustment without reversing a completed distribution.

## 9. Distribution and Reinvestment Capital events

### `REINVESTMENT_DEPLOYED`

```text
holding_event_id            prior EVENT_ID for HOLDING_REGISTERED or HOLDING_COST_ADDED
holding_id                  existing HOLDING_ID
amount_usd                  USD_POSITIVE
```

The amount must equal part or all of the Reinvestment-Capital-funded cost recorded by `holding_event_id`. Deployment maps Reinvestment Capital to a holding but does not reduce cumulative realized value, the distribution high-water mark, or the Reinvestment Capital balance.

### `DISTRIBUTION_PAYMENT`

```text
source_event_id             prior EVENT_ID creating the distribution obligation
recipient_shareholder_id    existing SHAREHOLDER_ID other than the owner
gross_distribution_usd      USD_POSITIVE
withholding_usd             USD_NONNEGATIVE
net_payment_usd             USD_NONNEGATIVE
```

`gross_distribution_usd` must equal `withholding_usd + net_payment_usd`. Withholding must be zero unless required by law. Multiple partial payments may reference the same source event, but cumulative payments may not exceed the recipient's derived obligation.

### `REINVESTMENT_RELEASED_TO_OWNER`

```text
amount_usd                  USD_POSITIVE
```

This may occur only when no shares remain held by anyone other than the owner. The amount must equal the complete remaining Reinvestment Capital balance. It creates no realization event or newly qualifying value.

### `FINAL_REINVESTMENT_DISTRIBUTION`

```text
amount_usd                  USD_POSITIVE
```

This may occur only during administration after the owner's death, when the agreement requires the remaining Reinvestment Capital balance to be distributed. The amount must equal that balance. Recipient obligations are derived pro rata from then-current non-owner shares and are settled through `DISTRIBUTION_PAYMENT` events referencing this event.

## 10. Status and succession events

### `OWNER_STATUS_CHANGED`

```text
status                      "ACTIVE", "INCAPACITATED", or "DECEASED"
```

`DECEASED` is permanent. `INCAPACITATED` may later return to `ACTIVE`. Authority of a personal representative or property manager is substantiated in private supporting records. The reducer applies the distribution and administration consequences specified by the agreement.

## 11. Correction events

### `CORRECTION`

```text
target_event_id                 prior EVENT_ID for an effective event
operation                       "REPLACE", "VOID", or "INSERT_AFTER"
reason                          nonempty public string
supersedes_correction_event_id  prior EVENT_ID for CORRECTION, optional
replacement_event               EVENT_BODY or null
```

`EVENT_BODY` contains a complete effective event's `timestamp`, `event_type`, optional `public_note`, and every field required by that event type, but omits `event_id`. For a replacement, the target retains its original event ID and position.

For `REPLACE`, `replacement_event` is required and replaces the target while retaining the target's event ID and position. For `VOID`, it must be null and the target is omitted during replay. If the target has already been corrected, `supersedes_correction_event_id` must identify the latest correction of that target.

`INSERT_AFTER` records a material event that was omitted from the historical sequence. `target_event_id` identifies the event after which it belongs, and `replacement_event` supplies the inserted event body. The correction event's own event ID becomes the inserted event's effective ID during replay. A later correction may target that inserted effective event; otherwise, a correction may not target another correction. `supersedes_correction_event_id` is prohibited for an initial insertion.

Correction events are administrative overlays. Before state replay, the validator resolves insertions and the latest correction for every target, replaces, removes, or inserts effective events as directed, and then replays the resulting effective event sequence from formation. Except when its ID identifies an inserted effective event, the correction event itself does not create an additional economic event at its recording timestamp.

A correction does not by itself reverse a completed transaction or payment. Any resulting settlement action is recorded separately through the applicable ordinary event type, consistent with the agreement.

## 12. Deterministic replay

For every snapshot, the validator performs these steps:

1. validate the header and update type against the preceding published snapshot;
2. validate JSON types, event IDs, references, and event-specific fields;
3. resolve correction overlays;
4. replay effective events from `FORMATION` in the effective sequence produced by correction resolution;
5. apply the agreement version and shared terms effective at each event;
6. derive all current state and accounting results; and
7. verify every invariant below.

Derived state includes at least:

- registered public profiles and current holders;
- applicable agreement versions and effective shared terms;
- outstanding shares and the cap table;
- current distribution elections and result;
- in-scope holdings, unrecovered holding costs, and funding allocations;
- cumulative realized value and the distribution high-water mark;
- distribution obligations, payments, and Reinvestment Capital balance;
- the benchmark window and benchmark price;
- each holder's aggregate and average royalty basis;
- each seller's cumulative sale result and royalty high-water mark; and
- the current transfer policy and unexpired transaction-specific permissions.

No derived value is independently selected. A displayed or cached result, if added by a later schema version, must be recomputed and verified from the events.

## 13. Required invariants

At every effective event:

- no share balance is negative;
- shares are whole, and outstanding shares do not exceed authorized shares;
- the cap table equals the complete history of share movements;
- a first-time recipient has already adopted the latest agreement version;
- only the event types and quantities permitted by the agreement affect the benchmark;
- a below-benchmark issuance or owner transfer has a valid unanimous approval;
- every voluntary sale has valid permission and settles atomically;
- royalty basis, cumulative sale result, royalty high-water mark, and royalty shares are correct;
- buyback and directed-sale prices are at least the immediately preceding benchmark;
- every holding cost is unrecovered, allowed, and deducted no more than once;
- every realization and tax reconciliation produces the correct realized-value change;
- losses must be recovered before value qualifies again under either high-water rule;
- distribution and Reinvestment Capital calculations use the shares and elections effective at the relevant event;
- distribution payments do not exceed derived obligations;
- Reinvestment Capital never falls below zero and is never counted twice; and
- corrections and migrations preserve the complete public publication history.

## 14. Privacy and interpretation rules

The state document records a personal-stock movement's contractual accounting price but never its acquisition category. In particular, `SHARE_ISSUANCE` and `OWNER_TRANSFER` do not state whether the recipient paid cash, provided services, received a gift, or gave no consideration. The recorded price must not be interpreted as evidence of any such fact, fair market value, compensation value, or tax basis.

Opaque holding IDs and aggregate accounting values may be used instead of publicly identifying an underlying holding or disclosing supporting documents. The owner must still maintain the private substantiation required by the agreement.

Schema fields and event names must not be extended casually. A backward-compatible clarification may be made within schema version 1 only if it does not change accepted data, rejected data, replay, or meaning. Every other schema change requires a new schema version followed by a separate `MIGRATION` publication of the state document.
