# Personal Stock Agreement

```
VERSION      = 0.9
VERSION_NOTE = -
OWNER        = Karthik Uppuluri (@koopuluri)
```

`OWNER` identifies the person whose personal stock is governed by this agreement. That person is the “owner.” A person who holds shares is a “shareholder.” A “non-owner shareholder” is any shareholder other than the owner.

## Participation

`PARTICIPATION` is the contractual allocation mechanism under §4. Each outstanding share is one equal unit of `PARTICIPATION` in `NEWLY_QUALIFYING_VALUE` (defined in §4). The portion attributable to shares held by non-owner shareholders is `NON_OWNER_PARTICIPATION` (defined in §4); the remainder belongs to the owner.

`PARTICIPATION` creates only the economic rights expressly stated in this agreement. All in-scope holdings remain solely owned and controlled by the owner. No shareholder has any legal or beneficial ownership of, lien on, security interest in, or other property right in an in-scope holding or its unrealized value. Shareholders have only the election and approval rights expressly stated in this agreement and no broader control over the owner's actions or life. This agreement creates no partnership, agency, trust, or fiduciary relationship.

## 1. Scope

`SCOPE` identifies the categories of holdings whose realized value is accounted for under §3. An in-scope holding is the owner's position in one of those categories. Everything else the owner earns or owns is outside this agreement.

```
SCOPE =
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

The owner must include and account for every in-scope holding. Any payment right, substitute holding, or noncash consideration arising from one remains in scope until accounted for under §3.

The owner may not gift, consume, or otherwise voluntarily dispose of an in-scope holding except through a transform, terminal exit, or exit producing cash or substitute consideration governed by §3.

## 2. Floor

`FLOOR` is the amount of `CUMULATIVE_REALIZED_VALUE` (defined in §3) reserved for the owner when determining `NEWLY_QUALIFYING_VALUE` under §4.

```
FLOOR = 10,000,000 USD × (CPI_CURRENT / CPI_2026_06)

CPI_CURRENT is the value most recently published as of the applicable
REALIZATION_EVENT (defined in §3) for the US Consumer Price Index for All
Urban Consumers, All Items, U.S. City Average, Not Seasonally Adjusted—BLS
series CUUR0000SA0.

CPI_2026_06 is that series' value for June 2026.

If BLS discontinues the series, its officially designated successor applies.
If none exists, the closest published measure of US consumer prices selected
in good faith applies.
```

## 3. Realized value

This section determines when value from an in-scope holding counts as realized and how the resulting gains and losses are accounted for over time.

### Realization events

A `REALIZATION_EVENT` occurs only as one of the following types:

- Type A—cash receipt: when cash from an in-scope holding—including sale proceeds and every cash dividend, interest payment, income, or distribution—is actually received by the owner or irrevocably paid, withheld, or made available for the owner's benefit;
- Type B—terminal exit: when a terminal exit occurs; or
- Type C—tax recognition or reconciliation: when `ATTRIBUTABLE_TAXES`, as defined below, are first recognized or later reconciled under this section, except that a released reserve, refund, or credit is recognized only when available as cash.

Unpaid or unavailable cash and noncash consideration or distributions do not create a `REALIZATION_EVENT`; they remain in scope until accounted for under this section. One transaction may produce multiple `REALIZATION_EVENT`s.

Transactions in the owner's own personal-stock shares are not `REALIZATION_EVENT`s.

### Realized value

At each `REALIZATION_EVENT`:

```
REALIZED_VALUE = GROSS_CASH_PROCEEDS
                 - ALLOCATED_HOLDING_COST
                 - DIRECT_TRANSACTION_EXPENSES
                 - ATTRIBUTABLE_TAXES
```

`GROSS_CASH_PROCEEDS` is the gross cash described in a Type A `REALIZATION_EVENT`, before transaction expenses or attributable taxes. It includes cash paid directly toward those expenses or taxes. At a Type B or Type C `REALIZATION_EVENT`, it is zero.

`ALLOCATED_HOLDING_COST` is the holding-cost deduction determined under the holding-cost rules below.

`DIRECT_TRANSACTION_EXPENSES` are fees and costs incurred specifically to produce or complete a `REALIZATION_EVENT`.

`ATTRIBUTABLE_TAXES` is the tax charge or credit assigned to the event under the tax rules below.

### Cumulative realized value

`REALIZED_VALUE` may be negative. `CUMULATIVE_REALIZED_VALUE` is the sum of `REALIZED_VALUE` from every `REALIZATION_EVENT` at or after `COMMENCEMENT_TIME` (defined in §5).

### Exits, terminal exits, and transforms

An exit occurs when the owner sells, redeems, exchanges, or otherwise disposes of all or part of an in-scope holding.

An exit-equivalent distribution is a distribution from an in-scope holding whose principal economic effect is to monetize or materially reduce the holding's underlying value without a formal disposition. It includes a liquidating distribution, return of capital, recapitalization proceeds, a distribution funded by a sale of substantially all or a material part of the holding's underlying assets, cash received through another personal stock's distribution mechanism, and any economic equivalent. It is treated as a partial exit.

A terminal exit occurs when all or part of an in-scope holding is irrevocably forfeited, abandoned, cancelled, expired, or otherwise extinguished without consideration, in good faith, with no direct or indirect economic interest retained by the owner. A decline in estimated value, including to zero, is not a terminal exit while the owner retains the holding or any economic rights in it. At the resulting Type B `REALIZATION_EVENT`, `GROSS_CASH_PROCEEDS` is zero and `ALLOCATED_HOLDING_COST` is all remaining `HOLDING_COST` (defined under “Holding cost and allocation” below) attributable to the extinguished part. Any later recovery attributable to that part remains in scope with zero `HOLDING_COST`.

A transform is a conversion, split, rollover, exchange for another in-scope holding, or other change in form in which the owner's economic position continues. It is not itself a `REALIZATION_EVENT`, and unrecovered `HOLDING_COST` carries forward. A transaction may be partly a transform and partly an exit; the continuing in-scope portion is the transform, and any cash is tested separately under the `REALIZATION_EVENT` definition.

### Holding cost and allocation

`HOLDING_COST` is the owner's unrecovered economic investment in an in-scope holding. It includes:

- cash or other value paid to acquire, exercise, or increase the holding;
- direct expenses attributable to acquiring, exercising, vesting, preserving, enforcing, or transforming it; and
- taxes attributable to acquiring, receiving, exercising, vesting, maintaining, or transforming it.

An expense forms part of `HOLDING_COST` only to the extent it is reasonable, documented, actually incurred, and would not have been incurred without the particular holding. The owner's time or imputed compensation, general personal or business overhead, and interest or other financing costs are excluded. For a holding received without payment, including as compensation, the amount paid may be zero, but attributable expenses and taxes still form part of `HOLDING_COST`.

`HOLDING_COST` remains attached to a holding until allocated under the rules below. `ALLOCATED_HOLDING_COST` is the portion deducted in calculating `REALIZED_VALUE` for a particular `REALIZATION_EVENT`; any unallocated portion remains attached to a continuing holding or carries into a resulting holding.

At a Type A `REALIZATION_EVENT` that is neither an exit nor an exit-equivalent distribution, `ALLOCATED_HOLDING_COST` is zero and `HOLDING_COST` does not change. A payment containing more than one component is allocated in good faith according to its economic substance.

If a transform produces more than one in-scope holding, unrecovered `HOLDING_COST` is allocated among them proportionally in good faith according to relative value. When an exit produces noncash consideration, the cost allocated to it carries into the resulting in-scope holding or holdings; if there is more than one, it is allocated among them on the same basis. On a full exit producing only cash, `ALLOCATED_HOLDING_COST` is all remaining `HOLDING_COST` attributable to the disposed holding. On a full exit producing only noncash consideration, all remaining `HOLDING_COST` carries forward. For a partial exit or an exit producing both cash and noncash consideration, cost is allocated proportionally in good faith according to the relative value of each portion. Additional cash, expenses, or attributable taxes incurred to receive noncash consideration are added to its `HOLDING_COST`.

Whenever a noncash component or part of a mixed transaction must be valued under this section, including to determine or allocate `HOLDING_COST`, the first reasonably available method in this order applies:
1. a bona fide allocation expressly negotiated in arm's-length transaction documents;
2. a reliable quoted market price at the relevant event;
3. a contemporaneous independent third-party valuation; or
4. the owner's reasonable, documented good-faith estimate.

The same method must be applied consistently to every component of the transaction. Once recorded, the valuation and any resulting determination or allocation of `HOLDING_COST` do not change solely because value later changes. They may be corrected under §10 for objective error, fraud, or previously unavailable information showing that the valuation was materially incorrect when made.

### Taxes

Taxes attributable to acquiring, receiving, exercising, vesting, maintaining, or transforming an in-scope holding form part of its `HOLDING_COST`. `ATTRIBUTABLE_TAXES` are the incremental federal, state, local, foreign, withholding, and similar taxes the owner pays or reasonably expects to pay because of an in-scope holding or `REALIZATION_EVENT`, net of related refunds and credits, except to the extent included in `HOLDING_COST`. They exclude a shareholder's taxes on a distribution and penalties or interest caused by the owner's failure to pay taxes when due.

Each cost, expense, or tax may be included only once among `HOLDING_COST`, `DIRECT_TRANSACTION_EXPENSES`, and `ATTRIBUTABLE_TAXES`, and no item may otherwise be deducted twice.

A later adjustment, refund, or credit relating to tax included in `HOLDING_COST` adjusts remaining `HOLDING_COST`; any portion relating to cost already allocated is an `ATTRIBUTABLE_TAXES` reconciliation.

Attributable taxes may be estimated in good faith, with professional advice when reasonable, and reserved before value becomes distributable. The owner may retain a reasonable reserve until the liability is paid or otherwise sufficiently determined, but unresolved tax may not delay distribution of value remaining after that reserve.

The owner must recognize `ATTRIBUTABLE_TAXES` when reasonably estimable and reconcile them as they become sufficiently determined and whenever they later change. At the resulting Type C `REALIZATION_EVENT`, `GROSS_CASH_PROCEEDS` and `ALLOCATED_HOLDING_COST` are zero, and `ATTRIBUTABLE_TAXES` is the initial amount or incremental adjustment: positive for initial or additional tax and negative for a released reserve, refund, or credit.

## 4. Distribution

`REALIZED_VALUE` that did not become `NEWLY_QUALIFYING_VALUE` when evaluated remains the owner's. It does not become `NEWLY_QUALIFYING_VALUE` later solely because `FLOOR` decreases; a lower `FLOOR` applies only to later `REALIZATION_EVENT`s.

At each `REALIZATION_EVENT`, `NEWLY_QUALIFYING_VALUE` is the positive `REALIZED_VALUE` that takes `CUMULATIVE_REALIZED_VALUE` above both `FLOOR` and `DISTRIBUTION_HIGH_WATER_MARK`. It is allocated through `PARTICIPATION` according to share ownership at that event. The portion attributable to owner shares belongs to the owner. The portion attributable to non-owner shares is `NON_OWNER_PARTICIPATION`, which is distributed or retained as Reinvestment Capital.

`DISTRIBUTION_HIGH_WATER_MARK` is the greatest level of `CUMULATIVE_REALIZED_VALUE` reached at a `REALIZATION_EVENT` for which there was `NEWLY_QUALIFYING_VALUE`. It never decreases because of a later economic event, although a correction under §10 may recalculate it. A realized loss must therefore be recovered before value may qualify again, and no completed distribution must be returned solely because of a later loss.

Each share held by a non-owner shareholder carries that shareholder's standing election: `REINVEST` or `DISTRIBUTE`. A new shareholder defaults to `REINVEST`; additional shares acquired by an existing shareholder take that shareholder's election. A shareholder may change the election for all shares they hold by written notice to the owner. The change is effective when received and must be recorded promptly before calculating or recording any later `REALIZATION_EVENT`. The owner's shares do not vote.

`NON_OWNER_SHARES` is the number of outstanding shares held by non-owner shareholders. `REINVEST_SHARES` is the number of those shares whose holder elected `REINVEST`. The result is `REINVEST` if `NON_OWNER_SHARES` is zero or `REINVEST_SHARES` is more than half of `NON_OWNER_SHARES`; otherwise, including a tie, it is `DISTRIBUTE`.

At each `REALIZATION_EVENT`:

```
cumulative_before  = CUMULATIVE_REALIZED_VALUE before this event
event_value        = REALIZED_VALUE from this event
floor_at_event     = FLOOR at this event
high_water_before  = DISTRIBUTION_HIGH_WATER_MARK before this event
outstanding_shares = all outstanding shares at this event

cumulative_after        = cumulative_before + event_value
qualification_threshold = max(floor_at_event, high_water_before)

NEWLY_QUALIFYING_VALUE = max(0, min(event_value,
                                    cumulative_after - qualification_threshold))

NON_OWNER_PARTICIPATION = NEWLY_QUALIFYING_VALUE
                          × (NON_OWNER_SHARES / outstanding_shares)

if NEWLY_QUALIFYING_VALUE > 0:
  DISTRIBUTION_HIGH_WATER_MARK = cumulative_after

if NON_OWNER_PARTICIPATION > 0 and result = REINVEST:
  retain NON_OWNER_PARTICIPATION as Reinvestment Capital
else if NON_OWNER_PARTICIPATION > 0:
  distribute NON_OWNER_PARTICIPATION to non-owner shareholders
```

When the result is `DISTRIBUTE`, each non-owner shareholder receives `NEWLY_QUALIFYING_VALUE` multiplied by that shareholder's shares divided by all outstanding shares at the event.

The owner must calculate and settle each distribution within 30 calendar days after the `REALIZATION_EVENT`. If a shareholder has not provided payment instructions, tax documentation, or other information reasonably required for payment, that shareholder's deadline is 30 calendar days after the owner receives it. Payment may otherwise be delayed only as reasonably necessary to comply with law, maintain a permitted tax reserve, or resolve a good-faith dispute; any unaffected undisputed amount must be paid by the otherwise applicable deadline. Each shareholder is responsible for taxes imposed on that shareholder's distribution.

`REINVESTMENT_CAPITAL_BALANCE` increases by each `NON_OWNER_PARTICIPATION` retained under `REINVEST` and may never be less than zero. Deploying Reinvestment Capital into an in-scope holding does not itself change the balance. The owner must adjust it reasonably and in good faith for permitted uses that leave no continuing asset; attributable losses, expenses, taxes, releases, and distributions; and recoveries or refunds reversing those adjustments.

A recovery or refund restores `REINVESTMENT_CAPITAL_BALANCE` only to the extent it is not included in `NEWLY_QUALIFYING_VALUE`; an included amount is governed solely by the allocation and election rules above. Material adjustments must be recorded, but no separate account, tracing of particular funds, or per-holding or per-share allocation is required.

During the owner's life, Reinvestment Capital must be retained or used in good faith to maintain, develop, or increase the owner's capacity to create value through present or future in-scope holdings. The owner has sole discretion over its timing, form, and use, and no investment or return is guaranteed. Unrelated personal consumption and gratuitous transfers are not permitted uses. A use serving both a permitted and prohibited purpose must be allocated reasonably and in good faith, and only its permitted portion may reduce `REINVESTMENT_CAPITAL_BALANCE`.

No shareholder may withdraw Reinvestment Capital during the owner's life. A person participates in it only through shares held when this agreement requires a distribution. After transferring shares, the transferor retains no interest in it, and no separate amount is added to the transfer price.

The owner may not require a buyback if a material purpose is (a) to cause Reinvestment Capital to be released to the owner or (b) to prevent value from a specific `REALIZATION_EVENT` the owner then reasonably expects from being allocated under §4 to the shares being bought back.

Designating value as Reinvestment Capital does not create a holding or `REALIZATION_EVENT`.

If no shares remain held by anyone other than the owner, any remaining `REINVESTMENT_CAPITAL_BALANCE` ceases to be purpose-bound and belongs to the owner. The release must be recorded and is not a `REALIZATION_EVENT` or `NEWLY_QUALIFYING_VALUE`.

Each `REALIZATION_EVENT` is evaluated using the shares, elections, `FLOOR`, `DISTRIBUTION_HIGH_WATER_MARK`, and other applicable terms then in effect.

## 5. Shares and issuances

Shares are whole and indivisible. No fractional share may be issued, held, or transferred.

```
AUTHORIZED_SHARES = 20,000,000
```

Outstanding shares may never exceed `AUTHORIZED_SHARES`. The limit may increase only when every current shareholder adopts an agreement version containing the increase under §11.

Before a person who does not currently hold shares may receive any shares, that person must sign the latest agreement version. This applies to an issuance, transfer, or directed sale. Temporary succession by operation of law under §12 is the only exception.

Shareholders must hold shares for their own benefit. Except for a legal representative or temporary holder under §12, no shareholder may act as a nominee, agent, or proxy for a third party; hold shares on another's behalf; transfer the economic interest to a non-shareholder; or exercise an election on another's instructions.

Only the owner acting personally may authorize an issuance. This power is nondelegable, and no issuance may settle during the owner's incapacity or after death.

Except for a below-benchmark issuance requiring approval under §6, the owner may issue authorized but unissued shares at any time, to any recipient, for cash, services, no consideration, or any other lawful consideration, without shareholder approval. No shareholder has any preemptive or anti-dilution right, including any right to participate pro rata in an issuance. Subject to this agreement, the owner may choose to offer a shareholder a transaction-specific opportunity to acquire shares, but no offer, policy, or past practice creates a right to any future offer.

Money received from issuing shares belongs solely to the owner. It is not a `REALIZATION_EVENT`, creates no `REALIZED_VALUE`, and need not be used for any particular purpose. If later used to acquire an in-scope holding, that holding is governed like any other.

Except for a required sale under §9, an issuance or transfer settles when every action and condition required to complete it has occurred and the share movement has become irrevocable. Its event time is the actual settlement time, regardless of when it is recorded.

`COMMENCEMENT_TIME` is the date and time the first issuance under this agreement settles. Immediately before it, no shares are outstanding; `CUMULATIVE_REALIZED_VALUE`, `DISTRIBUTION_HIGH_WATER_MARK`, and `REINVESTMENT_CAPITAL_BALANCE` are zero; and the benchmark window under §6 is empty. By completing the first issuance, the owner adopts this agreement and becomes bound by it.

Before or simultaneously with the first issuance, the owner must record every in-scope holding then owned, its unrecovered opening `HOLDING_COST`, the first issuance, resulting share ownership, applicable agreement versions, and every other opening input needed to apply this agreement. No event before `COMMENCEMENT_TIME` is itself included in `CUMULATIVE_REALIZED_VALUE`, `DISTRIBUTION_HIGH_WATER_MARK`, or any other event-based calculation under this agreement. An in-scope holding, payment right, or substitute holding existing at `COMMENCEMENT_TIME` enters the agreement only as an opening position, together with the unrecovered `HOLDING_COST` then attributable to that position. Pre-commencement transactions may be considered only to determine that opening `HOLDING_COST`; no cost or other amount carries forward independently of an opening position.

## 6. Benchmark price

`BENCHMARK_PRICE` is the per-share price used under this agreement to record noncash share transactions, establish `ROYALTY_BASIS` under §8 for noncash acquisitions, and set the minimum price for buybacks and directed sales under §9. It is the volume-weighted average recorded transaction price of the most recent `BENCHMARK_WINDOW` eligible shares.

```
INITIAL_BENCHMARK_PRICE = 1 USD per share
BENCHMARK_WINDOW        = 100,000 shares
```

If fewer than `BENCHMARK_WINDOW` eligible shares have moved, all eligible shares are used. If none have moved, `INITIAL_BENCHMARK_PRICE` applies. If the oldest included transaction crosses the window boundary, only the shares needed to complete the window are included from that transaction.

Each share moved in an issuance or transfer has the following recorded transaction price, except that a royalty share transferred to the owner under §8 has no recorded transaction price:

```
cash-only movement          = actual USD price paid per share received
all other non-§9 movements  = BENCHMARK_PRICE immediately before the movement
buyback or directed sale    = actual settlement price per share
```

For a cash-only movement, actual price includes every linked cash or cash-equivalent arrangement, including a rebate, refund, reimbursement, credit, debt forgiveness, offset, or indirect payment. Related arrangements must be combined and valued in good faith so the recorded price reflects the transaction's effective cash economics.

A recorded transaction price is a contractual input for the benchmark and `ROYALTY_BASIS` under §8. It is not fair market value, compensation value, tax basis, proof of consideration, or evidence that shares were acquired in any particular manner. Private consideration, payment, employment, gift, and tax details remain in the supporting records under §10.

An issuance or voluntary transfer by the owner whose recorded transaction price would be below `BENCHMARK_PRICE` immediately before settlement requires the written approval of the owner and every other current shareholder. This does not restrict a noncash issuance or owner transfer whose recorded transaction price equals the benchmark under this section.

Issuances and transfers other than buybacks and directed sales are eligible benchmark movements unless disregarded or corrected under the anti-manipulation rule below. When a sale includes royalty shares, only the shares purchased by the buyer are eligible.

The owner and each shareholder must administer and use the benchmark rules in good faith. Neither the owner nor any shareholder may structure, divide, combine, time, price, fund, characterize, or record a transaction or related series primarily to artificially increase, decrease, preserve, or otherwise manipulate `BENCHMARK_PRICE` or any royalty, buyback price, or directed-sale price derived from it. A bona fide transaction is not prohibited merely because it affects the benchmark. A violating transaction remains otherwise effective but must be disregarded or corrected for benchmark purposes, and every affected calculation must be recalculated under §10. Correcting its benchmark treatment does not require public disclosure of private consideration or acquisition type.

## 7. Transfers

Subject to §6's below-benchmark restriction, the owner may transfer the owner's existing shares for cash or noncash consideration.

A non-owner shareholder may voluntarily transfer shares only through a bona fide cash sale permitted by the owner in the owner's sole discretion at settlement. Gifts, donations, transfers for services, and other noncash voluntary transfers by a non-owner shareholder are prohibited.

Permission may arise from a generally applicable policy, a transaction-specific writing, or both. The owner may change a policy or withdraw transaction-specific permission before settlement, affecting any unsettled transfer if communicated before it settles. A completed transfer is unaffected. Transaction-specific permission is irrevocable only if it expressly says so.

The owner's permission does not override any other requirement of this agreement, including legal compliance under §13.

For a permitted cash sale, payment and every required share transfer must occur as one settlement.

## 8. Royalties

A royalty is the additional whole shares that a non-owner shareholder transfers to the owner when a permitted cash sale produces new cumulative contractual sale gain for that seller. A royalty is paid in shares, not cash.

`ROYALTY_BASIS` is the recorded transaction price under §6 assigned to a share solely to calculate later royalty gain. It does not change until shares leave the shareholder's holdings. If shares were acquired at different bases, the bases are pooled and allocated using a weighted average.

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
sale_price          = recorded transaction price under §6
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

## 9. Buybacks and directed sales

The owner may require a non-owner shareholder to sell any whole number of shares up to all shares held. A required sale to the owner is a `buyback`; one to a purchaser designated by the owner is a `directed sale`. Neither is a voluntary transfer or requires permission under §7.

The shareholder's consent, signature, cooperation, payment instructions, and advance notice are not required. Each shareholder irrevocably authorizes the owner to record a required sale. The price per share must be at or above `BENCHMARK_PRICE` immediately before settlement.

A required sale settles only when both: (a) the purchaser irrevocably deposits the purchase price, less any tax required to be withheld and properly remitted under §13, with a payment agent or in a segregated account solely for the shareholder; and (b) the owner records the transfer. The owner must notify the shareholder promptly. The deposited funds must remain unconditionally available to the shareholder. Without full funding, no sale occurs.

A buyback or directed sale carries no royalty and does not enter the seller's `cumulative_sale_result` or `royalty_high_water`. The seller's aggregate royalty basis is reduced proportionally, and the purchaser receives royalty basis equal to the actual price paid.

A buyback transfers shares to the owner; it does not cancel them or reduce outstanding shares.

## 10. Records, corrections, and information

The owner must maintain one complete chronological official history sufficient to determine the stock's current state and reproduce every result under this agreement. That history is authoritative: the current state and every result are determined by applying this agreement to it. Derived views, caches, or other implementation artifacts may be maintained, but they have no independent contractual authority and must remain reproducible from the official history.

The official history must record or identify all material inputs, including share movements and prices; agreement versions, elections, approvals, and amendments; holdings, costs, valuations, realization events, taxes, and distributions; Reinvestment Capital adjustments; royalties; and corrections. Each record must use the event's actual occurrence or settlement time even if entered later. Material events and inputs must be recorded promptly and before they or later events are relied on to calculate or complete a transaction.

The official history must be preserved. A correction must identify the matter corrected rather than erase it, and every affected result must be recalculated from the corrected history.

If a correction affects a completed transaction or payment, the owner and affected persons must resolve the consequences reasonably, proportionately, and in good faith, considering materiality and the practical consequences of reversal. Resolution may include corrected records, supplemental payment, repayment, offset, agreed reversal, or another appropriate adjustment. A correction alone does not invalidate or reverse a completed transaction. Fraud, intentional misrepresentation, and intentional manipulation remain subject to all otherwise available remedies.

The owner must maintain accurate and reasonably current supporting records sufficient to substantiate the official history. The owner must provide shareholders with updated information relevant to their rights and, on reasonable request, evidence reasonably sufficient to verify a recorded matter. The owner may use redacted documents, summaries, or professional certification and need not disclose privileged or unrelated confidential information.

A shareholder receiving nonpublic information must keep it confidential and use it only to verify or enforce rights under this agreement, except for disclosure to professional advisers bound by confidentiality or as required by law.

### Public history

By signing this agreement, each shareholder agrees that the owner must permanently publish the public subset of the official history: each shareholder's immutable shareholder ID, display names, public handles, share ownership, agreement versions, distribution elections, and events involving their shares, including recorded quantities, prices, royalties, transfers, buybacks, and directed sales.

The public history remains available after a person ceases to be a shareholder. Prior identities and historical information are not erased; a correction may update the current record but must preserve the prior history.

The owner generally will not publish a shareholder's legal name unless the shareholder uses it as a display name or consents to publication. The owner may disclose it when reasonably necessary to comply with law, verify or reconcile stock records, enforce or defend legal rights, or prevent the public record from being materially misleading, and only to the extent reasonably necessary. Signed agreements, private payment records, tax information, and other supporting materials remain private subject to the same limited exceptions.

## 11. Amendments

The latest version is the most recent agreement version the owner has issued for adoption. A shareholder adopts a version by signing it. The owner may issue a new version at any time with a plain-language summary of its changes, and each existing shareholder may choose whether to adopt it.

Seller-side transfer obligations, royalties, and buyback and directed-sale rules may operate separately by shareholder. Each shareholder's latest adopted version governs that shareholder for those terms. The seller's version governs a transaction; the recipient's version governs the recipient and the shares after settlement. No shareholder is bound by an individual change they have not adopted.

Every other term governing the stock as a whole is a shared term, including `SCOPE`, `FLOOR`, `AUTHORIZED_SHARES`, the benchmark rules, holding and realized-value accounting, distribution and Reinvestment Capital rules, official-history and correction rules, and this amendment process. One set of shared terms applies to everyone, and signing any version incorporates the shared terms then in effect.

A proposed shared-term change takes effect at the time recorded by the owner only when every current shareholder's latest adopted version contains the same change. Until then, the existing shared term governs everyone. A version proposing a shared-term change must identify the existing term that remains effective while the proposal is pending.

The owner may resolve administrative matters not addressed by this agreement reasonably and in good faith but may not contradict this agreement, change its economic rights, or bypass an approval or amendment requirement.

## 12. Incapacity, death, marital covenants, and pledges

If the owner or a shareholder becomes incapacitated, a person legally authorized to manage that person's property may exercise their rights and perform their duties under this agreement, subject to the same limits.

If a non-owner shareholder dies or their shares otherwise pass by operation of law, the legally recognized successor becomes a temporary holder under the prior holder's applicable version and election. The temporary holder may receive notices and payments and preserve the shares but may not change the election. If the prior holder died, the shares may be transferred only through a buyback, which the owner must complete under §9 as soon as reasonably practicable. Otherwise, the temporary holder becomes permanent upon signing the latest version with the owner's written approval. To the extent permitted by law, this agreement binds the temporary holder and successor.

On the owner's death, the owner's personal representative administers the stock, and in-scope holdings must be converted to cash as promptly as their terms reasonably permit. Shares held by the owner's estate are treated as the owner's shares under §4 and are not `NON_OWNER_SHARES`. For every later `REALIZATION_EVENT`, the distribution result is `DISTRIBUTE` regardless of standing elections, and no further value may become Reinvestment Capital.

At the owner's death, notwithstanding §4's Reinvestment Capital rules, entitlement to the final `REINVESTMENT_CAPITAL_BALANCE` vests pro rata in the persons then holding non-owner shares, based on shares held at death, and passes to their legal successors. The balance is paid after all in-scope holdings and tax reserves are finally resolved under §§3 and 4. The owner's estate has no interest in it.

`FLOOR` and all other value belonging to the owner after applying this agreement belong to the owner's estate. This agreement remains in effect until every holding, substitute holding, payment right, tax reserve, distribution, and other obligation is finally resolved; the stock dissolves only then. The agreement binds the owner's estate, and the owner must maintain a will directing the estate to perform it.

Before marrying, the owner must enter into and maintain a marital agreement recognizing and preserving this agreement's obligations. With respect to in-scope holdings and their proceeds, value distributable to non-owner shareholders and Reinvestment Capital must be excluded from marital or community property. Only value belonging to the owner after applying this agreement may enter the marital estate.

The owner may pledge or use the owner's shares, or amounts belonging to the owner after this agreement is applied, to support an obligation. The obligation must remain expressly subject to this agreement, may not be secured by an in-scope holding or Reinvestment Capital, and may not reduce or redirect an amount distributable to another shareholder. Any enforcement transfer remains subject to the recipient-signature, transfer, and legal-compliance rules. The owner may not voluntarily incur an obligation the owner reasonably expects would materially impair performance of this agreement.

## 13. General

Notwithstanding anything else in this agreement, a transaction involving shares may occur only if the owner reasonably determines that it complies with securities law and all other applicable law. The owner may require information, representations, certifications, supporting documents, or other verification reasonably needed to determine or document compliance and may delay or refuse the transaction until those requirements are satisfied. Permission under this agreement does not itself establish legality.

Every monetary amount under this agreement is denominated in USD, and any cash paid, received, withheld, or settled in connection with an issuance, transfer, holding acquisition, holding exit, distribution, expense, tax, or other transaction governed by this agreement must be USD.

No tax will be withheld from a payment unless required by law. Tax properly withheld and remitted is treated as paid to the recipient.

If any provision or application is invalid or unenforceable, it is severed only to the extent necessary, and the remainder remains effective.

The owner and each shareholder must maintain a current electronic notice address in the private records under §10. Electronic notice satisfies a writing requirement and is received when it enters the designated system in retrievable form; known delivery failure requires another reasonable method.

This agreement is the complete statement of the terms governing the stock. A separate record, transaction document, summary, or communication may establish transaction facts or separate obligations but changes this agreement only as it expressly permits or through §11.

This agreement may be signed electronically. The signature packet must contain or identify the complete agreement version accepted, which governs over any summary or explanatory copy.
