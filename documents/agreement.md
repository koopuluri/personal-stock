# Personal Stock Agreement

```
VERSION      = 0.9
VERSION_NOTE = -
OWNER        = Karthik Uppuluri (@koopuluri)
```

`OWNER` identifies the person whose personal stock is governed by this agreement. That person is the “owner.” A person who holds shares is a “shareholder.” A “non-owner shareholder” is any shareholder other than the owner.

Each share represents a proportional contractual economic participation in the owner's in-scope realized upside over the owner's life, as defined by this agreement.

`COMMENCEMENT_TIME` is the date and time the first issuance under this agreement settles. Immediately before it, no shares are outstanding. By completing the first issuance, the owner adopts this agreement and becomes bound by it.

## 1. Scope

The scope of this agreement has two parts:

1) `IN_SCOPE_ASSETS` - the owner's assets, instruments, rights, and ownership-like interests that are governed
2) `IN_SCOPE_PROCEEDS` - the value from those assets that is included

Everything else the owner earns, owns, or receives is outside this agreement.

### In-scope assets

`IN_SCOPE_ASSETS` identifies the categories of assets, instruments, rights, and ownership-like interests governed by this agreement.

```
IN_SCOPE_ASSETS =
  includes:
    - equity in private and public companies;
    - instruments convertible into equity, including options, warrants, SAFEs,
      and convertible notes;
    - shares in other persons' personal stocks;
    - token-based upside instruments; and
    - other ownership-like interests whose upside is primarily realized on exit.

  excludes:
    - wages and wage-like compensation, including salary, fees, and bonuses;
    - income-like cashflow rights, including revenue shares and royalties;
    - borrowing and leverage;
    - personal consumption; and
    - retirement accounts and similar long-term savings wrappers.
```

An asset, instrument, right, or ownership-like interest is an in-scope asset if it falls within an included category and not an excluded category of `IN_SCOPE_ASSETS`.

### Continuation and exit

A transform is a conversion, split, rollover, exchange for another in-scope asset, or other change in form in which the owner's economic position continues. The resulting substitute asset remains an in-scope asset.

An exit occurs to the extent the owner sells, redeems, exchanges, or otherwise disposes of all or part of an in-scope asset for cash or noncash consideration other than through a transform.

A terminal exit occurs when all or part of an in-scope asset is irrevocably forfeited, abandoned, cancelled, expired, or otherwise extinguished without consideration, in good faith, with no direct or indirect economic interest retained by the owner. A decline in estimated value, including to zero, is not a terminal exit while the owner retains the asset or any economic rights in it.

A transaction may be partly a transform and partly an exit. The continuing portion is the transform; any other consideration arises from the exit and is tested under the `IN_SCOPE_PROCEEDS` rules below.

### In-scope proceeds

An exit-equivalent distribution is a distribution, or a separately allocable component of one, whose principal economic effect is to monetize all or part of an in-scope asset, or the assets from which it derives its principal value, without a formal disposition of the owner's position.

`IN_SCOPE_PROCEEDS` is the value from in-scope assets that this agreement includes. It means cash, a payment right, or noncash consideration arising from:

- an exit;
- an exit-equivalent distribution; or
- a later recovery attributable to a terminal exit.

`IN_SCOPE_PROCEEDS` includes, without limitation:

- cash or noncash consideration from a sale, redemption, exchange, or other disposition constituting an exit;
- installment payments, deferred consideration, and contingent consideration from an exit;
- a liquidating distribution or return of capital;
- recapitalization proceeds;
- a distribution funded by the sale of substantially all or a material part of the position's underlying assets;
- a distribution through another person's personal stock, but only to the extent attributable to a transaction involving an underlying asset that would constitute an exit or exit-equivalent distribution under this agreement if that asset were held directly by the owner; and
- a later recovery attributable to a terminal exit.

`IN_SCOPE_PROCEEDS` does not include, without limitation:

- an ordinary or special dividend funded by earnings or operating revenue rather than an exit or exit-equivalent transaction;
- interest, coupon payments, or other yield;
- an operating, pass-through, or tax distribution funded by earnings, operating revenue, or other ordinary income;
- a revenue-share, royalty, or other income payment that is not consideration from an exit or exit-equivalent transaction; or
- a distribution through another person's personal stock to the extent attributable to income or yield that would be excluded under this agreement if received directly by the owner.

A payment's economic source and substance—not its amount, timing, frequency, or label—determine whether it is `IN_SCOPE_PROCEEDS`. A transaction or payment containing both `IN_SCOPE_PROCEEDS` and excluded value must be allocated reasonably and in good faith according to its economic substance. Any cost, expense, or tax attributable to both components must be allocated on the same basis.

Value that is not `IN_SCOPE_PROCEEDS` remains outside this agreement even when it comes from an in-scope asset. The owner must include and account for every in-scope asset and every item of `IN_SCOPE_PROCEEDS`.

## 2. Holdings

An in-scope holding is the owner's distinct economic position in a particular in-scope asset, or in a payment right or item of noncash consideration constituting `IN_SCOPE_PROCEEDS`. This section governs how a holding enters the agreement, changes form, and leaves the agreement.

### Ownership and shareholder rights

Shares create only the economic, election, and approval rights expressly stated in this agreement. All in-scope holdings remain solely owned and controlled by the owner. No shareholder has any legal or beneficial ownership of, lien on, security interest in, or other property right in an in-scope holding or its unrealized value. Shareholders have no control over the owner's actions or life beyond the election and approval rights expressly stated in this agreement. This agreement creates no partnership, agency, trust, or fiduciary relationship.

### Holding lifecycle

An in-scope holding enters the agreement when recorded as an opening position at `COMMENCEMENT_TIME`, when the owner later acquires it, when a transform produces it, or when a payment right or item of noncash consideration becomes `IN_SCOPE_PROCEEDS`. It may be increased, transformed, partially or fully exited, or terminally exited. A full transform replaces it with one or more substitute holdings; a full exit or terminal exit removes it.

Every acquisition, increase, transform, exit, and terminal exit of an in-scope holding takes effect at its actual occurrence or settlement time, regardless of when it is recorded.

A transform does not itself produce `IN_SCOPE_PROCEEDS`; the resulting substitute holding remains in scope. A payment right or item of noncash consideration constituting `IN_SCOPE_PROCEEDS` remains an in-scope holding until it is fully converted to cash or terminally exits.

The owner may not gift, consume, or otherwise voluntarily dispose of an in-scope holding except through an exit, transform, or terminal exit.

## 3. Realized value

`REALIZED_VALUE` is the net gain or loss from in-scope holdings recognized under this agreement. It ordinarily arises when `IN_SCOPE_PROCEEDS` become cash, after deducting `ALLOCATED_HOLDING_COST`, `DIRECT_TRANSACTION_EXPENSES`, and `ATTRIBUTABLE_TAXES`. A terminal exit or attributable-tax reconciliation may also create `REALIZED_VALUE` as provided below.

### Holding cost and allocation

`HOLDING_COST` is the owner's unrecovered economic investment in an in-scope holding, tracked solely to calculate `REALIZED_VALUE`. It includes:

- cash or other value paid to acquire, exercise, or increase the holding;
- direct expenses attributable to acquiring, exercising, vesting, preserving, enforcing, or transforming it; and
- taxes attributable to acquiring, receiving, exercising, vesting, maintaining, or transforming it.

An expense forms part of `HOLDING_COST` only to the extent it is reasonable, documented, actually incurred, and would not have been incurred without the particular holding. The owner's time or imputed compensation, general personal or business overhead, and interest or other financing costs are excluded. For a holding received without payment, including as compensation, the amount paid may be zero, but attributable expenses and taxes still form part of `HOLDING_COST`.

`HOLDING_COST` remains attached to a holding until allocated under the rules below. `ALLOCATED_HOLDING_COST` is the portion removed from a holding when an exit or terminal exit causes that cost to be recognized. Any unallocated portion remains attached to a continuing holding or carries into a resulting holding.

Receiving cash or other value from an in-scope holding that is not `IN_SCOPE_PROCEEDS` does not allocate or otherwise change `HOLDING_COST`. An exit-equivalent distribution is treated as a partial exit for these cost-allocation rules.

A transform does not allocate `HOLDING_COST`. Unrecovered `HOLDING_COST` carries into the resulting in-scope holding; if a transform produces more than one, it is allocated among them proportionally in good faith according to relative value.

When an exit produces noncash consideration, the cost allocated to it carries into the resulting in-scope holding or holdings; if there is more than one, it is allocated among them on the same basis. On a full exit producing only cash, `ALLOCATED_HOLDING_COST` is all remaining `HOLDING_COST` attributable to the disposed holding. On a full exit producing only noncash consideration, all remaining `HOLDING_COST` carries forward. For a partial exit or an exit producing both cash and noncash consideration, cost is allocated proportionally in good faith according to the relative value of each portion. Additional cash, expenses, or attributable taxes incurred to receive noncash consideration are added to its `HOLDING_COST`.

At a terminal exit, `ALLOCATED_HOLDING_COST` is all remaining `HOLDING_COST` attributable to the extinguished part. A later recovery attributable to that part has zero `HOLDING_COST`.

Whenever a noncash component or part of a mixed transaction must be valued under this section, including to determine or allocate `HOLDING_COST`, the first reasonably available method in this order applies:
1. a bona fide allocation expressly negotiated in arm's-length transaction documents;
2. a reliable quoted market price at the relevant event;
3. a contemporaneous independent third-party valuation; or
4. the owner's reasonable, documented good-faith estimate.

The same method must be applied consistently to every component of the transaction. Once recorded, the valuation and any resulting determination or allocation of `HOLDING_COST` do not change solely because value later changes. They may be corrected under §11 for objective error, fraud, or previously unavailable information showing that the valuation was materially incorrect when made.

A later adjustment, refund, or credit relating to tax included in `HOLDING_COST` adjusts remaining `HOLDING_COST`; any portion relating to cost already allocated is an `ATTRIBUTABLE_TAXES` reconciliation under the rules below.

### Attributable taxes

A tax attributable to income or other value arising from an in-scope holding that is not `IN_SCOPE_PROCEEDS` does not form part of `HOLDING_COST`.

`ATTRIBUTABLE_TAXES` are the incremental federal, state, local, foreign, withholding, and similar taxes the owner pays or reasonably expects to pay because of `IN_SCOPE_PROCEEDS` or a terminal exit, net of related refunds and credits, except to the extent included in `HOLDING_COST`. They exclude taxes attributable to income or other value arising from an in-scope holding that is not `IN_SCOPE_PROCEEDS`, a shareholder's taxes on a distribution, and penalties or interest caused by the owner's failure to pay taxes when due.

Attributable taxes may be estimated in good faith, with professional advice when reasonable, and reserved before value becomes distributable. The owner may retain a reasonable reserve until the liability is paid or otherwise sufficiently determined, but unresolved tax may not delay distribution of value remaining after that reserve.

The owner must recognize `ATTRIBUTABLE_TAXES` when reasonably estimable and reconcile them as they become sufficiently determined and whenever they later change.

### Realization events

A `REALIZATION_EVENT` occurs only as one of the following types:

- Type A—cash realization: when cash forming part of `IN_SCOPE_PROCEEDS` is actually received by the owner or irrevocably paid, withheld, or made available for the owner's benefit;
- Type B—terminal exit: when a terminal exit under §1 occurs; or
- Type C—tax recognition or reconciliation: when `ATTRIBUTABLE_TAXES` are first recognized or later reconciled, except that a released reserve, refund, or credit is recognized only when available as cash.

`IN_SCOPE_PROCEEDS` does not create a Type A `REALIZATION_EVENT` until and to the extent it is cash satisfying the Type A receipt condition. Any remaining payment right or noncash consideration stays in scope until accounted for under this section. One transaction may produce multiple `REALIZATION_EVENT`s.

Transactions in the owner's own personal-stock shares are not `REALIZATION_EVENT`s.

### Event calculation

`GROSS_CASH_PROCEEDS` is the gross cash component of `IN_SCOPE_PROCEEDS` giving rise to a Type A `REALIZATION_EVENT`, before transaction expenses or attributable taxes. It includes cash paid directly toward those expenses or taxes. At a Type B or Type C `REALIZATION_EVENT`, it is zero.

`ALLOCATED_HOLDING_COST` is the `HOLDING_COST` recognized at the event under the cost-allocation rules above. At a Type B `REALIZATION_EVENT`, it is all remaining `HOLDING_COST` attributable to the extinguished part. At a Type C `REALIZATION_EVENT`, it is zero.

`DIRECT_TRANSACTION_EXPENSES` are fees and costs incurred specifically to produce or complete a `REALIZATION_EVENT`.

At a Type C `REALIZATION_EVENT`, `ATTRIBUTABLE_TAXES` is the initial amount or incremental adjustment: positive for initial or additional tax and negative for a released reserve, refund, or credit.

Each cost, expense, or tax may be included only once among `HOLDING_COST`, `DIRECT_TRANSACTION_EXPENSES`, and `ATTRIBUTABLE_TAXES`, and no item may otherwise be deducted twice.

At each `REALIZATION_EVENT`:

```
REALIZED_VALUE = GROSS_CASH_PROCEEDS
                 - ALLOCATED_HOLDING_COST
                 - DIRECT_TRANSACTION_EXPENSES
                 - ATTRIBUTABLE_TAXES
```

### Cumulative realized value

`REALIZED_VALUE` may be negative. `CUMULATIVE_REALIZED_VALUE` begins at zero at `COMMENCEMENT_TIME` and is the sum of `REALIZED_VALUE` from every `REALIZATION_EVENT` at or after that time.

## 4. Floor and qualification

`FLOOR` is the level of `CUMULATIVE_REALIZED_VALUE` reserved for the owner before value can qualify for allocation.

```
FLOOR = 10,000,000 USD × (CPI_CURRENT / CPI_2026_06)

CPI_CURRENT is the value most recently published as of the applicable
REALIZATION_EVENT for the US Consumer Price Index for All Urban Consumers,
All Items, U.S. City Average, Not Seasonally Adjusted—BLS series CUUR0000SA0.

CPI_2026_06 is that series' value for June 2026.

If BLS discontinues the series, its officially designated successor applies.
If none exists, the closest published measure of US consumer prices selected
in good faith applies.
```

`DISTRIBUTION_HIGH_WATER_MARK` begins at zero at `COMMENCEMENT_TIME`. Immediately before each `REALIZATION_EVENT`, it is the greatest prior level of `CUMULATIVE_REALIZED_VALUE` through which value has already qualified under this section. It never decreases because of a later economic event, although a correction under §11 may recalculate it.

At each `REALIZATION_EVENT`, `NEWLY_QUALIFYING_VALUE` is the positive `REALIZED_VALUE` that takes `CUMULATIVE_REALIZED_VALUE` above both `FLOOR` and `DISTRIBUTION_HIGH_WATER_MARK`:

```
cumulative_before = CUMULATIVE_REALIZED_VALUE before this event
event_value       = REALIZED_VALUE from this event
floor_at_event    = FLOOR at this event
high_water_before = DISTRIBUTION_HIGH_WATER_MARK before this event

cumulative_after        = cumulative_before + event_value
qualification_threshold = max(floor_at_event, high_water_before)

NEWLY_QUALIFYING_VALUE = max(0, min(event_value,
                                    cumulative_after - qualification_threshold))

if NEWLY_QUALIFYING_VALUE > 0:
  DISTRIBUTION_HIGH_WATER_MARK = cumulative_after
```

`REALIZED_VALUE` that did not become `NEWLY_QUALIFYING_VALUE` when evaluated remains the owner's. It does not become `NEWLY_QUALIFYING_VALUE` later solely because `FLOOR` decreases; a lower `FLOOR` applies only to later `REALIZATION_EVENT`s. A realized loss must be recovered before value may qualify again, and no completed distribution must be returned solely because of a later loss.

Each `REALIZATION_EVENT` is evaluated using the `FLOOR`, `DISTRIBUTION_HIGH_WATER_MARK`, and other applicable terms then in effect.

## 5. Participation and distribution

`PARTICIPATION` is the contractual allocation of `NEWLY_QUALIFYING_VALUE` among the outstanding shares at a `REALIZATION_EVENT`. Each outstanding share is one equal unit of `PARTICIPATION`. The portion attributable to owner shares belongs to the owner; the portion attributable to non-owner shares is `NON_OWNER_PARTICIPATION`.

`NON_OWNER_SHARES` is the number of outstanding shares held by non-owner shareholders. At each `REALIZATION_EVENT`:

```
outstanding_shares = all outstanding shares at this event

NON_OWNER_PARTICIPATION = NEWLY_QUALIFYING_VALUE
                          × (NON_OWNER_SHARES / outstanding_shares)
```

Each share held by a non-owner shareholder carries that shareholder's standing election: `REINVEST` or `DISTRIBUTE`. A new shareholder defaults to `REINVEST`; additional shares acquired by an existing shareholder take that shareholder's election. A shareholder may change the election for all shares they hold by written notice to the owner. The change is effective when received and must be recorded promptly before calculating or recording any later `REALIZATION_EVENT`. The owner's shares do not vote.

`REINVEST_SHARES` is the number of `NON_OWNER_SHARES` whose holder elected `REINVEST`. The result is `REINVEST` if `NON_OWNER_SHARES` is zero or `REINVEST_SHARES` is more than half of `NON_OWNER_SHARES`; otherwise, including a tie, it is `DISTRIBUTE`.

```
if NON_OWNER_PARTICIPATION > 0 and result = REINVEST:
  retain NON_OWNER_PARTICIPATION as Reinvestment Capital
else if NON_OWNER_PARTICIPATION > 0:
  distribute NON_OWNER_PARTICIPATION to non-owner shareholders
```

When the result is `DISTRIBUTE`, each non-owner shareholder receives `NEWLY_QUALIFYING_VALUE` multiplied by that shareholder's shares divided by all outstanding shares at the event.

The owner must calculate and settle each distribution within 30 calendar days after the `REALIZATION_EVENT`. If a shareholder has not provided payment instructions, tax documentation, or other information reasonably required for payment, that shareholder's deadline is 30 calendar days after the owner receives it. Payment may otherwise be delayed only as reasonably necessary to comply with law, maintain a permitted tax reserve, or resolve a good-faith dispute; any unaffected undisputed amount must be paid by the otherwise applicable deadline. Each shareholder is responsible for taxes imposed on that shareholder's distribution.

`REINVESTMENT_CAPITAL_BALANCE` begins at zero at `COMMENCEMENT_TIME`, increases by each `NON_OWNER_PARTICIPATION` retained under `REINVEST`, and may never be less than zero. Deploying Reinvestment Capital into an in-scope holding does not itself change the balance. The owner must adjust it reasonably and in good faith for permitted uses that leave no continuing asset; attributable losses, expenses, taxes, releases, and distributions; and recoveries or refunds reversing those adjustments.

A recovery or refund restores `REINVESTMENT_CAPITAL_BALANCE` only to the extent it is not included in `NEWLY_QUALIFYING_VALUE`; an included amount is governed solely by the allocation and election rules above. Material adjustments must be recorded, but no separate account, tracing of particular funds, or per-holding or per-share allocation is required.

During the owner's life, Reinvestment Capital must be retained or used in good faith to maintain, develop, or increase the owner's capacity to create value through present or future in-scope holdings. The owner has sole discretion over its timing, form, and use, and no investment or return is guaranteed. Unrelated personal consumption and gratuitous transfers are not permitted uses. A use serving both a permitted and prohibited purpose must be allocated reasonably and in good faith, and only its permitted portion may reduce `REINVESTMENT_CAPITAL_BALANCE`.

No shareholder may withdraw Reinvestment Capital during the owner's life. A person participates in it only through shares held when this agreement requires a distribution. After transferring shares, the transferor retains no interest in it, and no separate Reinvestment Capital amount is added to the transfer price.

Designating value as Reinvestment Capital does not create a holding or `REALIZATION_EVENT`.

If no shares remain held by anyone other than the owner, any remaining `REINVESTMENT_CAPITAL_BALANCE` ceases to be purpose-bound and belongs to the owner. The release must be recorded and is not a `REALIZATION_EVENT` or `NEWLY_QUALIFYING_VALUE`.

Each `REALIZATION_EVENT` is allocated using the shares, elections, and other applicable terms then in effect.

## 6. Shares and issuances

Shares are whole and indivisible. No fractional share may be issued, held, or transferred.

```
AUTHORIZED_SHARES = 20,000,000
```

Outstanding shares may never exceed `AUTHORIZED_SHARES`. The limit may increase only when every current shareholder adopts an agreement version containing the increase under §12.

The “latest agreement version” is the most recent agreement version the owner has issued for adoption.

Before a person who does not currently hold shares may receive any shares, that person must sign the latest agreement version. This applies to an issuance, transfer, or directed sale. Temporary succession by operation of law under §13 is the only exception.

Shareholders must hold shares for their own benefit. Except for a legal representative or temporary holder under §13, no shareholder may act as a nominee, agent, or proxy for a third party; hold shares on another's behalf; transfer the economic interest to a non-shareholder; or exercise an election on another's instructions.

Only the owner acting personally may authorize an issuance. This power is nondelegable, and no issuance may settle during the owner's incapacity or after death.

Except for a below-benchmark issuance requiring approval under §7, the owner may issue authorized but unissued shares at any time, to any recipient, for cash, services, no consideration, or any other lawful consideration, without shareholder approval. No shareholder has any preemptive or anti-dilution right, including any right to participate pro rata in an issuance. Subject to this agreement, the owner may choose to offer a shareholder a transaction-specific opportunity to acquire shares, but no offer, policy, or past practice creates a right to any future offer.

Money received from issuing shares belongs solely to the owner. It is not a `REALIZATION_EVENT`, creates no `REALIZED_VALUE`, and need not be used for any particular purpose. If later used to acquire an in-scope holding, that holding is governed like any other.

Except for a required sale under §10, an issuance or transfer settles when every action and condition required to complete it has occurred and the share movement has become irrevocable. Its event time is the actual settlement time, regardless of when it is recorded.

Before or simultaneously with the first issuance, the owner must record every in-scope holding then owned, its unrecovered opening `HOLDING_COST`, the first issuance, resulting share ownership, applicable agreement versions, and every other opening input needed to apply this agreement. No event before `COMMENCEMENT_TIME` is itself included in `CUMULATIVE_REALIZED_VALUE`, `DISTRIBUTION_HIGH_WATER_MARK`, or any other event-based calculation under this agreement. An in-scope holding, or a payment right or noncash consideration constituting `IN_SCOPE_PROCEEDS`, that exists at `COMMENCEMENT_TIME` enters the agreement only as an opening position, together with the unrecovered `HOLDING_COST` then attributable to that position. Pre-commencement transactions may be considered only to determine that opening `HOLDING_COST`; no cost or other amount carries forward independently of an opening position.

## 7. Benchmark price

`BENCHMARK_PRICE` is the per-share price used under this agreement to record noncash share transactions, establish `ROYALTY_BASIS` under §9 for noncash acquisitions, and set the minimum price for buybacks and directed sales under §10. It is the volume-weighted average recorded transaction price of the most recent `BENCHMARK_WINDOW` eligible shares.

```
INITIAL_BENCHMARK_PRICE = 1 USD per share
BENCHMARK_WINDOW        = 100,000 shares
```

The benchmark history is empty at `COMMENCEMENT_TIME`. If fewer than `BENCHMARK_WINDOW` eligible shares have moved, all eligible shares are used. If none have moved, `INITIAL_BENCHMARK_PRICE` applies. If the oldest included transaction crosses the window boundary, only the shares needed to complete the window are included from that transaction.

Each share moved in an issuance or transfer has the following recorded transaction price, except that a royalty share transferred to the owner under §9 has no recorded transaction price:

```
cash-only movement          = actual USD price paid per share received
all other non-§10 movements = BENCHMARK_PRICE immediately before the movement
buyback or directed sale    = actual settlement price per share
```

For a cash-only movement, actual price includes every linked cash or cash-equivalent arrangement, including a rebate, refund, reimbursement, credit, debt forgiveness, offset, or indirect payment. Related arrangements must be combined and valued in good faith so the recorded price reflects the transaction's effective cash economics.

A recorded transaction price is a contractual input for the benchmark and `ROYALTY_BASIS` under §9. It is not fair market value, compensation value, tax basis, proof of consideration, or evidence that shares were acquired in any particular manner. Private consideration, payment, employment, gift, and tax details remain in the supporting records under §11.

An issuance or voluntary transfer by the owner whose recorded transaction price would be below `BENCHMARK_PRICE` immediately before settlement requires the written approval of the owner and every other current shareholder. This does not restrict a noncash issuance or owner transfer whose recorded transaction price equals the benchmark under this section.

Issuances and transfers other than buybacks and directed sales are eligible benchmark movements unless disregarded or corrected under the anti-manipulation rule below. When a sale includes royalty shares, only the shares purchased by the buyer are eligible.

The owner and each shareholder must administer and use the benchmark rules in good faith. Neither the owner nor any shareholder may structure, divide, combine, time, price, fund, characterize, or record a transaction or related series primarily to artificially increase, decrease, preserve, or otherwise manipulate `BENCHMARK_PRICE` or any royalty, buyback price, or directed-sale price derived from it. A bona fide transaction is not prohibited merely because it affects the benchmark. A violating transaction remains otherwise effective but must be disregarded or corrected for benchmark purposes, and every affected calculation must be recalculated under §11. Correcting its benchmark treatment does not require public disclosure of private consideration or acquisition type.

## 8. Transfers

Subject to §7's below-benchmark restriction, the owner may transfer the owner's existing shares for cash or noncash consideration.

A non-owner shareholder may voluntarily transfer shares only through a bona fide cash sale permitted by the owner in the owner's sole discretion at settlement. Gifts, donations, transfers for services, and other noncash voluntary transfers by a non-owner shareholder are prohibited.

Permission may arise from a generally applicable policy, a transaction-specific writing, or both. The owner may change a policy or withdraw transaction-specific permission before settlement, affecting any unsettled transfer if communicated before it settles. A completed transfer is unaffected. Transaction-specific permission is irrevocable only if it expressly says so.

The owner's permission does not override any other requirement of this agreement, including legal compliance under §14.

For a permitted cash sale, payment and every required share transfer must occur as one settlement.

## 9. Royalties

A royalty is the additional whole shares that a non-owner shareholder transfers to the owner when a permitted cash sale produces new cumulative contractual sale gain for that seller. A royalty is paid in shares, not cash.

`ROYALTY_BASIS` is the recorded transaction price under §7 assigned to a share solely to calculate later royalty gain. It does not change until shares leave the shareholder's holdings. If shares were acquired at different bases, the bases are pooled and allocated using a weighted average.

```
ROYALTY_RATE = 0.05
```

The seller's expenses and taxes do not reduce contractual sale gain.

For each shareholder:

```
aggregate_royalty_basis = total ROYALTY_BASIS of shares currently held
average_royalty_basis   = aggregate_royalty_basis / shares currently held
cumulative_sale_result  = sum of realized results from prior royalty-bearing
                          sales, including losses
royalty_high_water      = greatest cumulative_sale_result on which royalty has
                          been assessed, never less than zero
```

When a shareholder first acquires shares at or after `COMMENCEMENT_TIME`, `cumulative_sale_result` and `royalty_high_water` begin at zero, and each acquired share receives `ROYALTY_BASIS`.

For a permitted cash sale by a non-owner shareholder:

```
buyer_shares        = whole shares the buyer will receive
sale_price          = recorded transaction price under §7
sale_proceeds       = buyer_shares × sale_price
allocated_basis     = average_royalty_basis × buyer_shares
sale_result         = sale_proceeds - allocated_basis

cumulative_after    = cumulative_sale_result + sale_result
new_royalty_gain    = max(0, cumulative_after - royalty_high_water)
royalty_value       = new_royalty_gain × ROYALTY_RATE
royalty_shares      = round_down_to_whole_share(royalty_value / sale_price)
high_water_after    = max(royalty_high_water, cumulative_after)
```

`sale_price` must be greater than zero. `round_down_to_whole_share` discards any fractional share; the remainder is waived rather than paid or carried forward.

The negotiated quantity is `buyer_shares`. The buyer pays `sale_proceeds` and receives those shares. The seller must own and simultaneously transfer both `buyer_shares` to the buyer and `royalty_shares` to the owner. The sale result, royalty assessment, and resulting state must be recorded as part of that settlement.

The seller's aggregate royalty basis is reduced proportionally for every share surrendered. The buyer receives royalty basis equal to the cash price paid. The owner's own sales carry no royalty.

Prior negative sale results must be recovered before an additional royalty applies. Once royalty has been assessed on a level of cumulative contractual sale gain, recovery after a later negative result does not cause that gain to be charged again.

## 10. Buybacks and directed sales

The owner may require a non-owner shareholder to sell any whole number of shares up to all shares held. A required sale to the owner is a `buyback`; one to a purchaser designated by the owner is a `directed sale`. Neither is a voluntary transfer or requires permission under §8.

The shareholder's consent, signature, cooperation, payment instructions, and advance notice are not required. Each shareholder irrevocably authorizes the owner to record a required sale. The price per share must be at or above `BENCHMARK_PRICE` immediately before settlement.

No separate Reinvestment Capital amount is added to the price of a buyback or directed sale. The owner may not require a buyback if a material purpose is (a) to cause Reinvestment Capital to be released to the owner or (b) to prevent value from a specific `REALIZATION_EVENT` the owner then reasonably expects from being allocated under §5 to the shares being bought back.

A required sale settles only when both: (a) the purchaser irrevocably deposits the purchase price, less any tax required to be withheld and properly remitted under §14, with a payment agent or in a segregated account solely for the shareholder; and (b) the owner records the transfer. The owner must notify the shareholder promptly. The deposited funds must remain unconditionally available to the shareholder. Without full funding, no sale occurs.

A buyback or directed sale carries no royalty and does not enter the seller's `cumulative_sale_result` or `royalty_high_water`. The seller's aggregate royalty basis is reduced proportionally, and the purchaser receives royalty basis equal to the actual price paid.

A buyback transfers shares to the owner; it does not cancel them or reduce outstanding shares.

## 11. Records, corrections, and information

The owner must maintain one complete chronological official history sufficient to determine the stock's current state and reproduce every result under this agreement. That history is authoritative: the current state and every result are determined by applying this agreement to it. Derived views, caches, or other implementation artifacts may be maintained, but they have no independent contractual authority and must remain reproducible from the official history.

The official history must record or identify all material inputs, including share movements and prices; agreement versions, elections, approvals, and amendments; holdings, costs, and valuations; material cash or other value arising from in-scope holdings and whether it is `IN_SCOPE_PROCEEDS`; `REALIZATION_EVENT`s, `ATTRIBUTABLE_TAXES`, and distributions under §5; Reinvestment Capital adjustments; royalties; and corrections. Each record must use the event's actual occurrence or settlement time even if entered later. Material events and inputs must be recorded promptly and before they or later events are relied on to calculate or complete a transaction.

The official history must be preserved. A correction must identify the matter corrected rather than erase it, and every affected result must be recalculated from the corrected history.

If a correction affects a completed transaction or payment, the owner and affected persons must resolve the consequences reasonably, proportionately, and in good faith, considering materiality and the practical consequences of reversal. Resolution may include corrected records, supplemental payment, repayment, offset, agreed reversal, or another appropriate adjustment. A correction alone does not invalidate or reverse a completed transaction. Fraud, intentional misrepresentation, and intentional manipulation remain subject to all otherwise available remedies.

The owner must maintain accurate and reasonably current supporting records sufficient to substantiate the official history. The owner must provide shareholders with updated information relevant to their rights and, on reasonable request, evidence reasonably sufficient to verify a recorded matter. The owner may use redacted documents, summaries, or professional certification and need not disclose privileged or unrelated confidential information.

A shareholder receiving nonpublic information must keep it confidential and use it only to verify or enforce rights under this agreement, except for disclosure to professional advisers bound by confidentiality or as required by law.

### Public history

By signing this agreement, each shareholder agrees that the owner must permanently publish the public subset of the official history: each shareholder's immutable shareholder ID, display names, public handles, share ownership, agreement versions, distribution elections, and events involving their shares, including recorded quantities, prices, royalties, transfers, buybacks, and directed sales.

The public history remains available after a person ceases to be a shareholder. Prior identities and historical information are not erased; a correction may update the current record but must preserve the prior history.

The owner generally will not publish a shareholder's legal name unless the shareholder uses it as a display name or consents to publication. The owner may disclose it when reasonably necessary to comply with law, verify or reconcile stock records, enforce or defend legal rights, or prevent the public record from being materially misleading, and only to the extent reasonably necessary. Signed agreements, private payment records, tax information, and other supporting materials remain private subject to the same limited exceptions.

## 12. Amendments

A shareholder adopts an agreement version by signing it. The owner may issue a new version at any time with a plain-language summary of its changes, and each existing shareholder may choose whether to adopt it.

Seller-side transfer obligations, royalties, and buyback and directed-sale rules may operate separately by shareholder. Each shareholder's latest adopted version governs that shareholder for those terms. The seller's version governs a transaction; the recipient's version governs the recipient and the shares after settlement. No shareholder is bound by an individual change they have not adopted.

Every other term governing the stock as a whole is a shared term, including `IN_SCOPE_ASSETS`, `IN_SCOPE_PROCEEDS`, `FLOOR`, `AUTHORIZED_SHARES`, the benchmark rules, holding and realized-value accounting, distribution and Reinvestment Capital rules, official-history and correction rules, and this amendment process. One set of shared terms applies to everyone, and signing any version incorporates the shared terms then in effect.

A proposed shared-term change takes effect at the time recorded by the owner only when every current shareholder's latest adopted version contains the same change. Until then, the existing shared term governs everyone. A version proposing a shared-term change must identify the existing term that remains effective while the proposal is pending.

The owner may resolve administrative matters not addressed by this agreement reasonably and in good faith but may not contradict this agreement, change its economic rights, or bypass an approval or amendment requirement.

## 13. Incapacity, death, marital covenants, and pledges

If the owner or a shareholder becomes incapacitated, a person legally authorized to manage that person's property may exercise their rights and perform their duties under this agreement, subject to the same limits.

If a non-owner shareholder dies or their shares otherwise pass by operation of law, the legally recognized successor becomes a temporary holder under the prior holder's applicable version and election. The temporary holder may receive notices and payments and preserve the shares but may not change the election. If the prior holder died, the shares may be transferred only through a buyback, which the owner must complete under §10 as soon as reasonably practicable. Otherwise, the temporary holder becomes permanent upon signing the latest version with the owner's written approval. To the extent permitted by law, this agreement binds the temporary holder and successor.

On the owner's death, the owner's personal representative administers the stock, and in-scope holdings must be converted to cash as promptly as their terms reasonably permit. Shares held by the owner's estate are treated as the owner's shares under §5 and are not `NON_OWNER_SHARES`. For every later `REALIZATION_EVENT`, the distribution result is `DISTRIBUTE` regardless of standing elections, and no further value may become Reinvestment Capital.

At the owner's death, notwithstanding §5's Reinvestment Capital rules, entitlement to the final `REINVESTMENT_CAPITAL_BALANCE` vests pro rata in the persons then holding non-owner shares, based on shares held at death, and passes to their legal successors. The balance is paid after all in-scope holdings and tax reserves are finally resolved under §§2–5. The owner's estate has no interest in it.

`FLOOR` and all other value belonging to the owner after applying this agreement belong to the owner's estate. This agreement remains in effect until every in-scope holding, item of `IN_SCOPE_PROCEEDS`, tax reserve, distribution, and other obligation is finally resolved; the stock dissolves only then. The agreement binds the owner's estate, and the owner must maintain a will directing the estate to perform it.

Before marrying, the owner must enter into and maintain a marital agreement recognizing and preserving this agreement's obligations. With respect to in-scope holdings and `IN_SCOPE_PROCEEDS` derived from them, value distributable to non-owner shareholders and Reinvestment Capital must be excluded from marital or community property. Only value belonging to the owner after applying this agreement may enter the marital estate.

The owner may pledge or use the owner's shares, or amounts belonging to the owner after this agreement is applied, to support an obligation. The obligation must remain expressly subject to this agreement, may not be secured by an in-scope holding or Reinvestment Capital, and may not reduce or redirect an amount distributable to another shareholder. Any enforcement transfer remains subject to the recipient-signature, transfer, and legal-compliance rules. The owner may not voluntarily incur an obligation the owner reasonably expects would materially impair performance of this agreement.

## 14. General

Notwithstanding anything else in this agreement, a transaction involving shares may occur only if the owner reasonably determines that it complies with securities law and all other applicable law. The owner may require information, representations, certifications, supporting documents, or other verification reasonably needed to determine or document compliance and may delay or refuse the transaction until those requirements are satisfied. Permission under this agreement does not itself establish legality.

Every monetary amount under this agreement is denominated in USD, and any cash paid, received, withheld, or settled in connection with an issuance, transfer, holding acquisition, `IN_SCOPE_PROCEEDS`, distribution under §5, expense, tax, or other transaction governed by this agreement must be USD.

No tax will be withheld from a payment unless required by law. Tax properly withheld and remitted is treated as paid to the recipient.

If any provision or application is invalid or unenforceable, it is severed only to the extent necessary, and the remainder remains effective.

The owner and each shareholder must maintain a current electronic notice address in the private records under §11. Electronic notice satisfies a writing requirement and is received when it enters the designated system in retrievable form; known delivery failure requires another reasonable method.

This agreement is the complete statement of the terms governing the stock. A separate record, transaction document, summary, or communication may establish transaction facts or separate obligations but changes this agreement only as it expressly permits or through §12.

This agreement may be signed electronically. The signature packet must contain or identify the complete agreement version accepted, which governs over any summary or explanatory copy.
