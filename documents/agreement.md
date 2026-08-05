# Personal Stock Agreement

```
VERSION      = 0.9
VERSION_NOTE = -
OWNER        = Karthik Uppuluri (@koopuluri)
```

## Introduction

`OWNER` identifies the person whose personal stock is governed by this agreement. That person is the “owner.” A person who holds shares is a “shareholder.” A “non-owner shareholder” is any shareholder other than the owner.

Each share represents a proportional contractual participation in the owner's net realized economic upside from in-scope assets over the owner's life, above a defined portion of upside that is excluded from shareholder participation.

Personal stock is contractual only. All in-scope assets remain solely owned and controlled by the owner. A shareholder has only the economic, election, and approval rights expressly stated in this agreement and has no ownership of, lien on, or other property right in any in-scope asset or its unrealized value. This agreement gives shareholders no control over the owner's actions or life and creates no partnership, agency, trust, or fiduciary relationship.

`COMMENCEMENT_TIME` is the date and time the first issuance under this agreement settles. Immediately before it, no shares are outstanding. By completing the first issuance, the owner adopts this agreement and becomes bound by it.

## 1. Scope

Personal stock is intended to represent the net economic value the owner creates over the owner's life through endeavors whose economic outcomes are characterized by extreme upside potential, power-law distributions, and superlinear growth.

`IN_SCOPE_ASSETS` includes the owner's investment and ownership assets broadly. Scope does not depend on expected return, diversification, account type, or eventual outcome.

```
IN_SCOPE_ASSETS =
  includes:
    - direct equity in individual private and public companies;
    - equity-linked interests, including restricted stock, restricted stock
      units, options, warrants, SAFEs, convertible notes, stock-appreciation
      rights, phantom equity, and physical- or cash-settled equivalents;
    - debt, fixed-income, deposit, revenue-share, royalty, and other financial
      interests;
    - shares in other persons' personal stocks;
    - interests in investment, savings, retirement, and pooled vehicles, whether
      concentrated or diversified, including venture, private-equity,
      single-asset, index, mutual, exchange-traded, target-date, pension, and
      similar vehicles;
    - token-based financial or investment instruments; and
    - other assets, instruments, rights, or interests held for investment or
      capable of producing economic return or appreciation.

  excludes:
    - salary, hourly pay, fees, commissions, cash bonuses, severance, benefits,
      reimbursements, and other wage-like compensation paid for employment or
      services, other than an included asset or value paid in settlement of one;
    - bona fide borrowing and rights to borrowed funds.
```

An asset, instrument, right, or ownership-like interest is an in-scope asset if it falls within an included category and not an excluded category of `IN_SCOPE_ASSETS`.

The listed categories govern the asset forms they cover. A future asset class or instrument not reasonably covered by them is also an in-scope asset if, assessed reasonably and in good faith when classified, its economic character falls within the purpose stated above and it is not substantially equivalent to an excluded category. An included asset requires no forecast, minimum investment or ownership, or particular outcome.

Scope depends on what a position is, not how the owner acquired it. An otherwise included asset remains included whether purchased, granted, earned as compensation, exercised, converted, gifted, or otherwise acquired. Employment, service conditions, vesting, payroll or tax treatment, and characterization as compensation do not exclude equity or an equity-linked interest. Salary, fees, cash bonuses, and other wage-like cash compensation remain excluded; cash or noncash value received in settlement of an included equity or equity-linked interest is value from that asset and remains governed by this agreement.

An opening asset is classified at `COMMENCEMENT_TIME`; a later asset is classified when acquired. Later performance does not change the classification.

The scope boundary exists only at the asset level, not again around each kind of value the asset produces. Once an asset is in scope, all sale proceeds, dividends, interest payments, distributions, settlements, recoveries, and other items of value arising from it are governed by this agreement.

An in-scope payment right or transferable noncash item remains an in-scope asset until it becomes cash. Once accounted for under §2, the cash itself leaves scope; any asset later acquired with it is classified independently under this section. Everything else the owner earns, owns, or receives is outside this agreement.

The owner may not remove an in-scope asset from this agreement through a gift, consumption, or other voluntary transfer, except through a bona fide disposition or a good-faith extinguishment in which no economic interest is retained.

## 2. Realized value

This agreement accounts for value from in-scope assets when a `REALIZATION_EVENT` occurs. At each event, any related eligible expense or attributable tax not already recognized is recognized first, the event's cash then reduces the portfolio's single `GLOBAL_COST` balance, and only the cash left after that balance reaches zero is the event's `REALIZED_VALUE`. Section 3 adds each event's `REALIZED_VALUE` to `LIFETIME_REALIZED_VALUE` and applies the floor; §4 allocates any resulting `NEWLY_QUALIFYING_VALUE` among the shares.

### When a realization event occurs

A `REALIZATION_EVENT` occurs at the moment cash arising from an in-scope asset is received by the owner or irrevocably paid, withheld, or made available for the owner's benefit, or when an amount is expressly treated as `GROSS_CASH_PROCEEDS` under the attributable-tax rules below. Cash arises from an in-scope asset when received because of owning, holding, enforcing, lending, transferring, redeeming, or ending it. Sales, dividends, interest, distributions, settlements, recoveries, and distributions from another personal stock are treated alike.

A cash refund, reimbursement, or recovery attributable to an amount previously added to `GLOBAL_COST` also creates a `REALIZATION_EVENT` when the cash becomes available. A decrease in a previously recognized unpaid eligible expense or attributable-tax reserve creates a `REALIZATION_EVENT` for the amount released at the time of reconciliation, even if the amount was not held separately.

Transactions in the owner's own personal-stock shares are not `REALIZATION_EVENT`s.

### What does not create a realization event

Unrealized appreciation and value retained inside an entity do not create a `REALIZATION_EVENT`. An in-scope payment right or transferable noncash item remains an in-scope asset and creates no event until it becomes cash. Non-USD currency is noncash until converted to USD.

A transform is a conversion, split, rollover, noncash exchange, or other change in form through which a position continues. It creates no `REALIZATION_EVENT`, and every resulting in-scope asset remains governed. Granting, vesting, or exercising an included compensatory interest without cash likewise creates no event.

A forfeiture, abandonment, cancellation, expiration, or other good-faith ending without cash creates no `REALIZATION_EVENT` and does not reduce `GLOBAL_COST`. Any later cash recovery remains governed.

Payment by the same issuer or in the same transaction is not enough: separate wage-like compensation, employment- or service-related reimbursement, excluded rights, and bona fide borrowed principal remain outside scope. Substance controls. A disguised or mixed payment and its related costs, expenses, and taxes must be allocated reasonably and in good faith.

To avoid subjective valuation, a nontransferable noncash benefit that is not an enforceable payment right is not an in-scope asset or `REALIZATION_EVENT`. The owner may not arrange one in place of cash, a payment right, or transferable noncash consideration that would otherwise arise.

Once cash has been accounted for at a `REALIZATION_EVENT`, it leaves scope. Its later earnings or use do not arise from the original asset. If the cash is used to acquire or increase an in-scope asset, that new investment instead increases `GLOBAL_COST`.

### Global cost

`GLOBAL_COST` is the single running balance of eligible costs that the owner's entire in-scope portfolio has not yet recovered. It determines how much cash from the next `REALIZATION_EVENT` must be applied before any of that event's cash can become `REALIZED_VALUE`. Costs and returns net across all in-scope assets: no cost is assigned to an individual asset, and the source of the cash used to pay a cost does not matter.

`GLOBAL_COST` begins at the opening amount determined under §5 and increases by:

- cash actually paid or irrevocably applied to acquire, exercise, or increase an in-scope asset;
- direct expenses actually incurred to acquire, exercise, vest, preserve, enforce, maintain, transform, sell, or otherwise realize one; and
- `ATTRIBUTABLE_TAXES` when initially recognized or later increased under this section.

Every increase must be reasonable, documented, and caused by an in-scope asset. Noncash consideration, the owner's time or imputed compensation, general overhead, financing costs, and shareholder distribution taxes do not increase `GLOBAL_COST`. An asset received without a cash payment, including as compensation, may therefore add no acquisition cost, while its eligible expenses and attributable taxes still increase `GLOBAL_COST`.

An increase to `GLOBAL_COST` does not itself create a `REALIZATION_EVENT` or `REALIZED_VALUE`; it increases the amount that later event cash must recover. A transform, noncash receipt, or ending without cash neither changes nor allocates `GLOBAL_COST`. A correction to a recorded increase is handled under §11.

### Attributable taxes

`ATTRIBUTABLE_TAXES` are the incremental federal, state, local, foreign, withholding, and similar taxes caused by an in-scope asset or cash arising from one. They exclude shareholder distribution taxes and penalties or interest caused by the owner's late payment.

The owner must recognize attributable taxes when reasonably estimable, may determine them in good faith with professional advice when appropriate, and must reconcile them whenever the estimate or actual liability later changes. A recognized amount is treated as reserved whether or not held separately. A change based on later information or a later determination of liability is a reconciliation; a mistake in the original record or application based on information then available is an error. Tax adjustments are accounted for as follows:

- An initial recognition or later increase increases `GLOBAL_COST` when recognized.
- Payment of an amount already recognized consumes the corresponding reserve but does not increase `GLOBAL_COST` again or create a `REALIZATION_EVENT`.
- To the extent a decrease reduces an unpaid recognized amount, it releases the same amount of reserve. The released amount is `GROSS_CASH_PROCEEDS` from a `REALIZATION_EVENT` at the time of reconciliation and is accounted for like any other event cash.
- To the extent the reduced tax was already paid or withheld, the reduction creates no `REALIZATION_EVENT` until the corresponding refund becomes available or credit is used. That refund or used credit is then `GROSS_CASH_PROCEEDS`. The same amount may not be counted more than once.
- Any other tax benefit caused by an in-scope asset is `GROSS_CASH_PROCEEDS` to the extent and at the time it actually reduces tax otherwise payable and is not already reflected in `ATTRIBUTABLE_TAXES` or counted under this section.
- An error in an earlier recognition is corrected under §11 rather than treated as a new economic event.

Unresolved tax may not delay a distribution beyond the amount reasonably recognized as reserved. Tax or expense withheld from non-USD currency before conversion is already reflected in the net USD proceeds and does not increase `GLOBAL_COST`.

### Calculating realized value at an event

Events occurring together are applied in economic order: every eligible expense or attributable tax caused by or required to produce the event cash and not already recognized is added to `GLOBAL_COST` first; the event cash is applied next; and any unrelated new investment is added last. Cash invested or reinvested immediately after an event is therefore accounted for as event cash before it becomes new `GLOBAL_COST`.

`GROSS_CASH_PROCEEDS` for a `REALIZATION_EVENT` is all cash giving rise to that event before reducing `GLOBAL_COST`, including cash applied directly toward an eligible investment, expense, or tax, plus any amount expressly treated as proceeds under the attributable-tax rules. For non-USD currency, it is only the USD actually produced by conversion, net of tax or expense withheld before conversion. Each cost, cash flow, and reserve adjustment is recorded once.

`REALIZED_VALUE` for a `REALIZATION_EVENT` is the portion of that event's `GROSS_CASH_PROCEEDS` remaining after the proceeds have reduced `GLOBAL_COST` to zero. It is specific to that event and cannot be negative:

```
cash = GROSS_CASH_PROCEEDS for this event
cost = GLOBAL_COST immediately before applying that cash

if cash <= cost:
  GLOBAL_COST after the event = cost - cash
  REALIZED_VALUE for the event = 0

otherwise:
  GLOBAL_COST after the event = 0
  REALIZED_VALUE for the event = cash - cost
```

For example, if `GLOBAL_COST` is 20 million and an asset produces 12 million of `GROSS_CASH_PROCEEDS` with no additional cost, that event's `REALIZED_VALUE` is zero and `GLOBAL_COST` becomes 8 million. If any asset later produces 20 million with no additional cost, the first 8 million clears `GLOBAL_COST` and that later event's `REALIZED_VALUE` is 12 million.

Each event is calculated at its actual occurrence time using the agreement state and terms then in effect.

## 3. Floor and qualification

`LIFETIME_REALIZED_VALUE` is the running total that begins at zero at `COMMENCEMENT_TIME` and, after each `REALIZATION_EVENT`, increases by that event's `REALIZED_VALUE`.

`FLOOR` is the level of `LIFETIME_REALIZED_VALUE` reserved for the owner before value can qualify for allocation.

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

`DISTRIBUTION_HIGH_WATER_MARK` begins at zero at `COMMENCEMENT_TIME`. Immediately before each `REALIZATION_EVENT`, it is the greatest prior level of `LIFETIME_REALIZED_VALUE` through which value has already qualified under this section. It never decreases because of a later economic event, although a correction under §11 may recalculate it.

At each `REALIZATION_EVENT`, `NEWLY_QUALIFYING_VALUE` is the portion of that event's `REALIZED_VALUE` that takes `LIFETIME_REALIZED_VALUE` above both `FLOOR` and `DISTRIBUTION_HIGH_WATER_MARK`:

```
lifetime_before   = LIFETIME_REALIZED_VALUE before this event
event_value       = REALIZED_VALUE from this event
floor_at_event    = FLOOR at this event
high_water_before = DISTRIBUTION_HIGH_WATER_MARK before this event

lifetime_after          = lifetime_before + event_value
qualification_threshold = max(floor_at_event, high_water_before)

NEWLY_QUALIFYING_VALUE = max(0, min(event_value,
                                    lifetime_after - qualification_threshold))

if NEWLY_QUALIFYING_VALUE > 0:
  DISTRIBUTION_HIGH_WATER_MARK = lifetime_after
```

`REALIZED_VALUE` that did not become `NEWLY_QUALIFYING_VALUE` when evaluated remains the owner's. It does not become `NEWLY_QUALIFYING_VALUE` later solely because `FLOOR` decreases; a lower `FLOOR` applies only to later `REALIZATION_EVENT`s. A later cost or loss increases `GLOBAL_COST` and must be recovered before more cash can qualify. No completed distribution must be returned solely because of a later cost or loss.

Each `REALIZATION_EVENT` is evaluated using the `FLOOR`, `DISTRIBUTION_HIGH_WATER_MARK`, and other applicable terms then in effect.

## 4. Participation and distribution

Cash becomes shareable only after the portfolio's global cost has been recovered and the owner's floor has been cleared. Non-owner shareholders then choose collectively whether their portion is paid now or retained as Reinvestment Capital; retained value is deemed to fund new in-scope investment first, while investment activity itself only updates `GLOBAL_COST`.

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

`REINVESTMENT_CAPITAL_BALANCE` begins at zero at `COMMENCEMENT_TIME`, increases by each `NON_OWNER_PARTICIPATION` retained under `REINVEST`, and may never be less than zero. For accounting purposes, the entire balance is deemed deployed first and foremost into the in-scope portfolio's new investments, before the owner's capital. This is a contractual portfolio-level convention: no portion of Reinvestment Capital is attributed to a particular dollar, asset, cost, or shareholder.

Deploying Reinvestment Capital into an in-scope asset does not itself change `REINVESTMENT_CAPITAL_BALANCE`; the investment increases `GLOBAL_COST` like any other. Because costs and returns remain in that single global balance, no asset-level Reinvestment Capital gain or loss is calculated.

During the owner's life, Reinvestment Capital must be retained or used first and foremost for present or future in-scope assets and may otherwise be used in good faith to maintain, develop, or increase the owner's capacity to create value through them. The owner has sole discretion over its timing, form, and use, and no investment or return is guaranteed. Unrelated personal consumption and gratuitous transfers are not permitted uses.

A permitted expenditure is handled exactly once. If eligible for `GLOBAL_COST`, it increases that balance and does not directly reduce `REINVESTMENT_CAPITAL_BALANCE`. Otherwise, if it leaves no recoverable asset, it reduces `REINVESTMENT_CAPITAL_BALANCE`, but not below zero, and a direct recovery or refund reverses only that reduction without creating `REALIZED_VALUE`. A mixed use must be allocated reasonably and in good faith.

No shareholder may withdraw Reinvestment Capital during the owner's life. A person participates in it only through shares held when this agreement requires a distribution. After transferring shares, the transferor retains no interest in it, and no separate Reinvestment Capital amount is added to the transfer price.

Designating value as Reinvestment Capital does not create an in-scope asset or `REALIZATION_EVENT`.

If no shares remain held by anyone other than the owner, any remaining `REINVESTMENT_CAPITAL_BALANCE` ceases to be purpose-bound and belongs to the owner. The release must be recorded and is not a `REALIZATION_EVENT` or `NEWLY_QUALIFYING_VALUE`.

Each `REALIZATION_EVENT` is allocated using the shares, elections, and other applicable terms then in effect.

## 5. Shares and issuances

Shares are whole and indivisible. No fractional share may be issued, held, or transferred.

```
AUTHORIZED_SHARES = 20,000,000
```

Outstanding shares may never exceed `AUTHORIZED_SHARES`. The limit may increase only when every current shareholder adopts an agreement version containing the increase under §12.

The “latest agreement version” is the most recent agreement version the owner has issued for adoption.

Before a person who does not currently hold shares may receive any shares, that person must sign the latest agreement version. This applies to an issuance, transfer, or directed sale. Temporary succession by operation of law under §13 is the only exception.

Shareholders must hold shares for their own benefit. Except for a legal representative or temporary holder under §13, no shareholder may act as a nominee, agent, or proxy for a third party; hold shares on another's behalf; transfer the economic interest to a non-shareholder; or exercise an election on another's instructions.

Only the owner acting personally may authorize an issuance. This power is nondelegable, and no issuance may settle during the owner's incapacity or after death.

Except for a below-benchmark issuance requiring approval under §6, the owner may issue authorized but unissued shares at any time, to any recipient, for cash, services, no consideration, or any other lawful consideration, without shareholder approval. No shareholder has any preemptive or anti-dilution right, including any right to participate pro rata in an issuance. Subject to this agreement, the owner may choose to offer a shareholder a transaction-specific opportunity to acquire shares, but no offer, policy, or past practice creates a right to any future offer.

Money received from issuing shares belongs solely to the owner. It is not a `REALIZATION_EVENT`, creates no `REALIZED_VALUE`, and need not be used for any particular purpose. An in-scope asset later acquired with it is governed like any other.

Except for a required sale under §9, an issuance or transfer settles when every action and condition required to complete it has occurred and the share movement has become irrevocable. Its event time is the actual settlement time, regardless of when it is recorded.

Before or simultaneously with the first issuance, the owner must record every in-scope asset then owned, the opening `GLOBAL_COST`, the first issuance, resulting share ownership, applicable agreement versions, and every other opening input needed to apply this agreement.

The opening `GLOBAL_COST` is determined reasonably and in good faith by applying §2 chronologically to every eligible pre-commencement cost and cash receipt attributable to the opening assets and their prior forms, all treated as one portfolio. No cost, receipt, or loss from a position extinguished before `COMMENCEMENT_TIME` and not represented by an opening asset carries into it.

No event before `COMMENCEMENT_TIME` is itself included in `LIFETIME_REALIZED_VALUE`, `DISTRIBUTION_HIGH_WATER_MARK`, or any other event-based calculation under this agreement. Every in-scope asset existing then enters only as an opening asset; any later recovery from a pre-commencement position not represented by one is outside this agreement.

## 6. Benchmark price

`BENCHMARK_PRICE` is the per-share price used under this agreement to record noncash share transactions, establish `ROYALTY_BASIS` under §8 for noncash acquisitions, and set the minimum price for buybacks and directed sales under §9. It is the volume-weighted average recorded transaction price of the most recent `BENCHMARK_WINDOW` eligible shares.

```
INITIAL_BENCHMARK_PRICE = 1 USD per share
BENCHMARK_WINDOW        = 100,000 shares
```

The benchmark history is empty at `COMMENCEMENT_TIME`. If fewer than `BENCHMARK_WINDOW` eligible shares have moved, all eligible shares are used. If none have moved, `INITIAL_BENCHMARK_PRICE` applies. If the oldest included transaction crosses the window boundary, only the shares needed to complete the window are included from that transaction.

Each share moved in an issuance or transfer has the following recorded transaction price, except that a royalty share transferred to the owner under §8 and a share surrendered under §10 have no recorded transaction price:

```
cash-only movement          = actual USD price paid per share received
all other non-§9 movements  = BENCHMARK_PRICE immediately before the movement
buyback or directed sale    = actual settlement price per share
```

For a cash-only movement, actual price includes every linked cash or cash-equivalent arrangement, including a rebate, refund, reimbursement, credit, debt forgiveness, offset, or indirect payment. Related arrangements must be combined and valued in good faith so the recorded price reflects the transaction's effective cash economics.

A recorded transaction price is a contractual input for the benchmark and `ROYALTY_BASIS` under §8. It is not fair market value, compensation value, tax basis, proof of consideration, or evidence that shares were acquired in any particular manner. Private consideration, payment, employment, gift, and tax details remain in the supporting records under §11.

An issuance or voluntary transfer by the owner whose recorded transaction price would be below `BENCHMARK_PRICE` immediately before settlement requires the written approval of the owner and every other current shareholder. This does not restrict a noncash issuance or owner transfer whose recorded transaction price equals the benchmark under this section.

Issuances and transfers other than buybacks, directed sales, and surrenders are eligible benchmark movements unless disregarded or corrected under the anti-manipulation rule below. When a sale includes royalty shares, only the shares purchased by the buyer are eligible.

The owner and each shareholder must administer and use the benchmark rules in good faith. Neither the owner nor any shareholder may structure, divide, combine, time, price, fund, characterize, or record a transaction or related series primarily to artificially increase, decrease, preserve, or otherwise manipulate `BENCHMARK_PRICE` or any royalty, buyback price, or directed-sale price derived from it. A bona fide transaction is not prohibited merely because it affects the benchmark. A violating transaction remains otherwise effective but must be disregarded or corrected for benchmark purposes, and every affected calculation must be recalculated under §11. Correcting its benchmark treatment does not require public disclosure of private consideration or acquisition type.

## 7. Transfers

Subject to §6's below-benchmark restriction, the owner may transfer the owner's existing shares for cash or noncash consideration.

Except for a surrender under §10, a non-owner shareholder may voluntarily transfer shares only through a bona fide cash sale permitted by the owner in the owner's sole discretion at settlement. Gifts, donations, transfers for services, and other noncash voluntary transfers by a non-owner shareholder are prohibited.

Permission may arise from a generally applicable policy, a transaction-specific writing, or both. The owner may change a policy or withdraw transaction-specific permission before settlement, affecting any unsettled transfer if communicated before it settles. A completed transfer is unaffected. Transaction-specific permission is irrevocable only if it expressly says so.

The owner's permission does not override any other requirement of this agreement, including legal compliance under §14.

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

The seller's aggregate royalty basis is reduced proportionally for every share transferred in the sale. The buyer receives royalty basis equal to the cash price paid. The owner's own sales carry no royalty.

Prior negative sale results must be recovered before an additional royalty applies. Once royalty has been assessed on a level of cumulative contractual sale gain, recovery after a later negative result does not cause that gain to be charged again.

## 9. Buybacks and directed sales

The owner may require a non-owner shareholder to sell any whole number of shares up to all shares held. A required sale to the owner is a `buyback`; one to a purchaser designated by the owner is a `directed sale`. Neither is a voluntary transfer or requires permission under §7.

The shareholder's consent, signature, cooperation, payment instructions, and advance notice are not required. Each shareholder irrevocably authorizes the owner to record a required sale. The price per share must be at or above `BENCHMARK_PRICE` immediately before settlement.

No separate Reinvestment Capital amount is added to the price of a buyback or directed sale. The owner may not require a buyback if a material purpose is (a) to cause Reinvestment Capital to be released to the owner or (b) to prevent value from a specific `REALIZATION_EVENT` the owner then reasonably expects from being allocated under §4 to the shares being bought back.

A required sale settles only when both: (a) the purchaser irrevocably deposits the purchase price, less any tax required to be withheld and properly remitted under §14, with a payment agent or in a segregated account solely for the shareholder; and (b) the owner records the transfer. The owner must notify the shareholder promptly. The deposited funds must remain unconditionally available to the shareholder. Without full funding, no sale occurs.

A buyback or directed sale carries no royalty and does not enter the seller's `cumulative_sale_result` or `royalty_high_water`. The seller's aggregate royalty basis is reduced proportionally, and the purchaser receives royalty basis equal to the actual price paid.

A buyback transfers shares to the owner; it does not cancel them or reduce outstanding shares.

## 10. Surrender and dissolution

A non-owner shareholder may at any time surrender all shares held by giving written notice to the owner. The surrender is effective when the notice is received, requires no approval, is irrevocable, and transfers the shares to the owner without consideration. It relinquishes all existing and future economic rights under this agreement, including unpaid distributions and participation through Reinvestment Capital. The shares remain outstanding; the surrender carries no royalty or recorded transaction price and does not enter the benchmark history. The owner must record it promptly.

`DISSOLUTION` is the irrevocable final recorded action terminating the personal stock. It extinguishes all outstanding shares, terminates all accounting balances, ends this agreement's application to every person and asset, permits no later economic event, and leaves the official history permanent.

Only the owner acting personally may cause a voluntary dissolution. It may occur only when no shares are held by anyone else, no economic obligation to another person remains, and any remaining Reinvestment Capital has been released under §4. It requires no sale, disposition, or extinguishment of an in-scope asset.

## 11. Records, corrections, and information

The owner must maintain one complete chronological official history sufficient to determine the stock's current state and reproduce every result under this agreement. That history is authoritative: the current state and every result are determined by applying this agreement to it. Derived views, caches, or other implementation artifacts may be maintained, but they have no independent contractual authority and must remain reproducible from the official history.

The official history must record or identify all inputs needed to apply this agreement, including share movements and prices; agreement versions, elections, approvals, and amendments; in-scope assets and transforms; every change to `GLOBAL_COST`; every cash receipt, payment right, and transferable noncash item arising from an in-scope asset; `REALIZATION_EVENT`s, `ATTRIBUTABLE_TAXES`, and distributions under §4; Reinvestment Capital adjustments; royalties; and corrections. Each record must use the event's actual occurrence or settlement time even if entered later. Events and inputs must be recorded promptly and before they or later events are relied on to calculate or complete a transaction.

The official history must be preserved. A correction must identify the matter corrected rather than erase it, and every affected result must be recalculated from the corrected history.

If a correction affects a completed transaction or payment, the owner and affected persons must resolve the consequences reasonably, proportionately, and in good faith, considering materiality and the practical consequences of reversal. Resolution may include corrected records, supplemental payment, repayment, offset, agreed reversal, or another appropriate adjustment. A correction alone does not invalidate or reverse a completed transaction. Fraud, intentional misrepresentation, and intentional manipulation remain subject to all otherwise available remedies.

The owner must maintain accurate and reasonably current supporting records sufficient to substantiate the official history. The owner must provide shareholders with updated information relevant to their rights and, on reasonable request, evidence reasonably sufficient to verify a recorded matter. The owner may use redacted documents, summaries, or professional certification and need not disclose privileged or unrelated confidential information.

A shareholder receiving nonpublic information must keep it confidential and use it only to verify or enforce rights under this agreement, except for disclosure to professional advisers bound by confidentiality or as required by law.

### Public history

By signing this agreement, each shareholder agrees that the owner must permanently publish the public subset of the official history: each shareholder's immutable shareholder ID, display names, public handles, share ownership, agreement versions, distribution elections, and events involving their shares, including recorded quantities, prices, royalties, transfers, buybacks, directed sales, surrenders, and dissolution.

The public history remains available after a person ceases to be a shareholder. Prior identities and historical information are not erased; a correction may update the current record but must preserve the prior history.

The owner generally will not publish a shareholder's legal name unless the shareholder uses it as a display name or consents to publication. The owner may disclose it when reasonably necessary to comply with law, verify or reconcile stock records, enforce or defend legal rights, or prevent the public record from being materially misleading, and only to the extent reasonably necessary. Signed agreements, private payment records, tax information, and other supporting materials remain private subject to the same limited exceptions.

## 12. Amendments

A shareholder adopts an agreement version by signing it. The owner may issue a new version at any time with a plain-language summary of its changes, and each existing shareholder may choose whether to adopt it.

Seller-side transfer obligations, royalties, and buyback and directed-sale rules may operate separately by shareholder. Each shareholder's latest adopted version governs that shareholder for those terms. The seller's version governs a transaction; the recipient's version governs the recipient and the shares after settlement. No shareholder is bound by an individual change they have not adopted.

Every other term governing the stock as a whole is a shared term, including `IN_SCOPE_ASSETS`, `FLOOR`, `AUTHORIZED_SHARES`, the benchmark rules, global-cost and realized-value accounting, distribution and Reinvestment Capital rules, official-history and correction rules, and this amendment process. One set of shared terms applies to everyone, and signing any version incorporates the shared terms then in effect.

A proposed shared-term change takes effect at the time recorded by the owner only when every current shareholder's latest adopted version contains the same change. Until then, the existing shared term governs everyone. A version proposing a shared-term change must identify the existing term that remains effective while the proposal is pending.

The owner may resolve administrative matters not addressed by this agreement reasonably and in good faith but may not contradict this agreement, change its economic rights, or bypass an approval or amendment requirement.

## 13. Incapacity, death, marital covenants, and pledges

If the owner or a shareholder becomes incapacitated, a person legally authorized to manage that person's property may exercise their rights and perform their duties under this agreement, subject to the same limits.

If a non-owner shareholder dies or their shares otherwise pass by operation of law, the legally recognized successor becomes a temporary holder under the prior holder's applicable version and election. The temporary holder may receive notices and payments and preserve the shares but may not change the election. If the prior holder died, the shares may be transferred only through a buyback, which the owner must complete under §9 as soon as reasonably practicable. Otherwise, the temporary holder becomes permanent upon signing the latest version with the owner's written approval. To the extent permitted by law, this agreement binds the temporary holder and successor.

On the owner's death, the owner's personal representative administers the stock, and each in-scope asset must be converted to cash as promptly as its terms reasonably permit or, if it cannot reasonably be converted, otherwise finally disposed of or extinguished. Shares held by the owner's estate are treated as the owner's shares under §4 and are not `NON_OWNER_SHARES`. For every later `REALIZATION_EVENT`, the distribution result is `DISTRIBUTE` regardless of standing elections, and no further value may become Reinvestment Capital.

At the owner's death, the persons then holding non-owner shares acquire a pro rata entitlement, based on shares held at death, to whatever `REINVESTMENT_CAPITAL_BALANCE` remains after the following terminal accounting; that entitlement passes to their legal successors. After every in-scope asset has been converted to cash or otherwise finally disposed of or extinguished, every related cost and tax reserve has been resolved, and every resulting `REALIZATION_EVENT` has been accounted for, any `GLOBAL_COST` then remaining reduces `REINVESTMENT_CAPITAL_BALANCE` dollar for dollar until either balance reaches zero. `GLOBAL_COST` then becomes zero; any amount that exceeded Reinvestment Capital is borne by the owner's estate. The remaining Reinvestment Capital is paid pro rata to those entitled to it, and the owner's estate has no interest in that balance.

`FLOOR` and all other value belonging to the owner after applying this agreement belong to the owner's estate. When every action and payment required by this section is complete, the owner's personal representative must record a `DISSOLUTION` under §10. The agreement binds the owner's estate, and the owner must maintain a will directing the estate to perform it.

Before marrying, the owner must enter into and maintain a marital agreement recognizing and preserving this agreement's obligations. With respect to in-scope assets and value arising from them, value distributable to non-owner shareholders and Reinvestment Capital must be excluded from marital or community property. Only value belonging to the owner after applying this agreement may enter the marital estate.

The owner may pledge or use the owner's shares, or amounts belonging to the owner after this agreement is applied, to support an obligation. The obligation must remain expressly subject to this agreement, may not be secured by an in-scope asset or Reinvestment Capital, and may not reduce or redirect an amount distributable to another shareholder. Any enforcement transfer remains subject to the recipient-signature, transfer, and legal-compliance rules. The owner may not voluntarily incur an obligation the owner reasonably expects would materially impair performance of this agreement.

## 14. General

Notwithstanding anything else in this agreement, a transaction involving shares may occur only if the owner reasonably determines that it complies with securities law and all other applicable law. The owner may require information, representations, certifications, supporting documents, or other verification reasonably needed to determine or document compliance and may delay or refuse the transaction until those requirements are satisfied. Permission under this agreement does not itself establish legality.

Unless expressly stated otherwise, every reference to cash means USD, and every monetary calculation under this agreement is denominated in USD. Non-USD currency is treated as noncash consideration until converted into USD.

No tax will be withheld from a payment unless required by law. Tax properly withheld and remitted is treated as paid to the recipient.

If any provision or application is invalid or unenforceable, it is severed only to the extent necessary, and the remainder remains effective.

The owner and each shareholder must maintain a current electronic notice address in the private records under §11. Electronic notice satisfies a writing requirement and is received when it enters the designated system in retrievable form; known delivery failure requires another reasonable method.

This agreement is the complete statement of the terms governing the stock. A separate record, transaction document, summary, or communication may establish transaction facts or separate obligations but changes this agreement only as it expressly permits or through §12.

This agreement may be signed electronically. The signature packet must contain or identify the complete agreement version accepted, which governs over any summary or explanatory copy.
