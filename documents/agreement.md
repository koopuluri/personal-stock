# Personal Stock Agreement

```
VERSION      = 1.0
VERSION_NOTE = Published standard agreement
```

## Introduction

This agreement is a published standard that may be adopted for any personal stock. Each personal stock that adopts it is a separate application with its own owner, shareholders, shares, assets, official history, and state.

The personal stock gives its shareholders a contractual right to share in the owner’s lifetime net gains from stakes in companies, other personal stocks, and similar assets with extreme upside potential, after a defined portion of those gains is reserved for the owner.

This agreement establishes which assets and gains are covered, how shareable value is calculated and distributed, how shares may be issued and transferred, and the rights, duties, records, remedies, and succession rules governing the stock.

## 1. Definitions

These terms apply throughout this agreement. Other terms are defined in the sections where they are used.

A person “adopts” this agreement for a personal stock by signing a record that identifies that personal stock and this agreement by its version, blockchain network, authoritative onchain address, and content hash. An adoption applies only to the personal stock it identifies.

The “owner” is the person identified as the owner in the initial signed adoption for a personal stock.

A “share” is one equal unit of contractual participation in the owner's net portfolio gains above the `FLOOR` defined below.

A person who holds one or more shares is a “shareholder.” A “non-owner shareholder” is any shareholder other than the owner.

`COMMENCEMENT_TIME` is the date and time the applicable personal stock's initial capitalization becomes effective under this agreement.

## 2. Scope

```
IN_SCOPE_ASSETS =
  includes:
    - financial, investment, savings, retirement, ownership, equity-linked,
      debt, investment-deposit, revenue-sharing, royalty, digital, and similar
      economic assets, instruments, rights, and interests owned directly,
      indirectly, or beneficially by the owner;
    - public and private equity;
    - restricted stock, restricted stock units, options, warrants, SAFEs,
      convertible instruments, phantom equity, and similar interests, including
      interests received for employment or services;
    - debt and fixed-income interests;
    - funds, retirement accounts, pensions, and other pooled or savings vehicles;
    - royalties, revenue shares, another person's personal stock, and token-based
      financial or investment instruments; and
    - other assets or rights held primarily for investment or economic return.

  excludes:
    - salary, hourly pay, fees, commissions, cash bonuses, severance, benefits,
      reimbursements, and other wage-like cash compensation, except cash or
      other value arising from an included asset;
    - bona fide borrowing and rights to borrowed funds;
    - USD cash and principal held in an ordinary checking, savings, payment, or
      cash-management account for liquidity rather than investment, although
      interest or yield paid on it is included; and
    - a home, vehicle, personal possession, or other property held primarily for
      personal use rather than investment.
```

An asset, instrument, right, or interest is an in-scope asset if it falls within an included category and not an excluded category of `IN_SCOPE_ASSETS`.

Scope depends on what an asset is, not how the owner acquired it. An otherwise in-scope asset remains in scope whether purchased, granted, earned as compensation, exercised, converted, gifted, or otherwise acquired. Its later performance, vesting, tax treatment, account, wrapper, or change in form does not change its classification. For an interest in an entity or fund, the owner's interest is the in-scope asset; the entity's underlying assets are not separately traced unless the owner owns them directly.

An opening asset is classified at `COMMENCEMENT_TIME`; a later asset is classified when acquired. Once an asset is in scope, all sale proceeds, dividends, interest payments, distributions, settlements, recoveries, payment rights, and transferable items arising from it remain governed by this agreement. A payment right or transferable noncash item remains an in-scope asset until it becomes USD cash.

After USD cash has been accounted for under §3, that cash leaves scope. Merely holding it in an ordinary liquidity account does not bring the principal back into scope. If it is later used to acquire or increase an in-scope asset, the new investment is accounted for independently under §3.

Unrealized appreciation is never counted. A conversion, split, rollover, noncash exchange, or other continuation in form does not produce cash under this agreement, and every resulting in-scope asset remains governed. A forfeiture, abandonment, cancellation, expiration, or other good-faith ending without cash produces no value under this agreement.

Substance controls over form. A mixed receipt or expense must be allocated reasonably and in good faith. The owner may not intentionally remove value from scope through a gift, consumption, disguised payment, substitute noncash benefit, or other arrangement whose primary purpose is to defeat this agreement. A bona fide disposition or good-faith extinguishment in which the owner retains no economic interest is permitted.

## 3. Portfolio net gain

`PORTFOLIO_NET_GAIN` is one running USD balance for the owner's entire in-scope portfolio. Costs and returns are netted across all in-scope assets.

### Cash events

A `CASH_EVENT` occurs when USD cash arising from an in-scope asset is received by the owner or is irrevocably paid, withheld, or made available for the owner's benefit. Sales, dividends, interest, distributions, settlements, recoveries, and similar receipts are treated alike.

The amount of a `CASH_EVENT` is the gross USD cash arising from the asset, including measurable USD cash paid or withheld directly for an eligible expense or attributable tax. Non-USD currency is noncash until converted to USD; if tax or conversion expense is withheld before conversion, only the net USD actually produced is counted, and the withheld amount is not deducted again.

A refund or recovery of a previously counted eligible cost is a `CASH_EVENT` when available. A released unpaid reserve and an attributable tax credit or other tax benefit are also `CASH_EVENT`s when §3 says they are available or used.

The following do not create a `CASH_EVENT`:

- unrealized value or value retained inside an entity;
- a noncash transform, receipt, vesting, exercise, forfeiture, or ending;
- bona fide borrowed principal; or
- an issuance, transfer, royalty, buyout, surrender, distribution, or other transaction involving the owner's own personal-stock shares.

A nontransferable personal benefit is not an in-scope asset or `CASH_EVENT`, but the owner may not arrange such a benefit primarily in place of cash, a payment right, or transferable value that would otherwise be governed.

### Eligible costs

An `ELIGIBLE_COST` is one of the following, to the extent reasonable, documented, and caused by an in-scope asset:

- USD cash actually paid or irrevocably applied to acquire, exercise, or increase the asset;
- a direct third-party expense incurred to acquire, exercise, vest, preserve, enforce, maintain, transform, sell, or otherwise realize the asset; or
- an `ATTRIBUTABLE_TAX` recognized under this section.

Noncash consideration, the owner's time or imputed compensation, general personal or business overhead, financing costs, costs of administering this personal stock, and taxes imposed on a shareholder's distribution are not eligible costs. An asset received for no cash, including as compensation, therefore has no acquisition cost, although direct expenses and attributable taxes may still qualify.

### Attributable taxes and reserves

An `ATTRIBUTABLE_TAX` is an incremental income, payroll, capital-gain, net-investment-income, alternative-minimum, foreign, withholding, or similar tax caused by an in-scope asset or value arising from one. It may qualify even if it arises before the asset produces cash, including from vesting, exercise, or undistributed pass-through income.

Attributable taxes do not include:

- estate, inheritance, gift, or generation-skipping transfer taxes;
- taxes caused by issuing, transferring, conducting a buyout, administering, or distributing value under the personal stock, regardless of whether imposed on the owner, the estate, or a shareholder;
- unrelated personal taxes; or
- penalties or interest caused by late payment or other avoidable noncompliance by the owner.

A deduction, credit, refund, or other tax benefit caused by an excluded item is also excluded.

The owner must estimate and recognize an attributable tax when reasonably estimable, in good faith and with professional advice when appropriate. The recognized amount is treated as reserved whether or not held separately. The owner need not arrange the owner's life, investments, or tax affairs to minimize tax, but must allocate mixed taxes reasonably and may not shift an unrelated tax into the portfolio.

An estimated attributable tax or unpaid eligible expense, and any later increase, is an `ELIGIBLE_COST` when reasonably recognized. Paying an amount already recognized creates no additional cost or event. A decrease in an unpaid recognized amount is a `CASH_EVENT` when the reserve is released. A decrease in an amount already paid or withheld is a `CASH_EVENT` only when the refund becomes available or the corresponding credit or other benefit is actually used.

Any deduction, credit, loss carryforward, refund, or other tax benefit caused by an in-scope asset is a `CASH_EVENT` when it actually reduces tax otherwise payable, except to the extent already reflected in a lower attributable tax or previously counted. An unused or expired benefit counts for nothing.

For a measurable USD transaction, cash is recorded gross and a related eligible tax or expense is recorded separately. The only net-only treatments are tax or conversion expense withheld from non-USD currency before conversion and in-scope noncash property withheld or surrendered without a cash realization. In the latter case, only the property remaining continues in scope, and the satisfied tax or expense is not separately deducted unless matching proceeds are also recorded.

If a net-only treatment satisfies an amount previously recognized as an eligible cost or reserve, a matching `CASH_EVENT` equal to the entire previously recognized amount attributable to that settlement must be recorded. For a reserve recognized before `COMMENCEMENT_TIME`, the matching event is limited to the portion carried into and still reflected in the opening `PORTFOLIO_NET_GAIN`. This reverses the earlier deduction while leaving the actual withholding embedded in the net proceeds or remaining property. Any difference between the estimate and actual withholding is already reflected in that net value and creates no separate cost or `CASH_EVENT`. Every cash flow, cost, reserve, payment, refund, credit, and benefit is counted exactly once.

A good-faith estimate that later changes because of new information is adjusted when the change becomes known. A mistake in the original record or application based on information then available is instead corrected under §11.

Unresolved tax or expense may delay a distribution only to the extent of the amount reasonably reserved.

### Running balance and event order

The opening `PORTFOLIO_NET_GAIN` is determined chronologically from every pre-commencement eligible cost and every amount that would be a `CASH_EVENT`, in each case attributable to assets still in scope at commencement and their prior forms.

```
temporary_opening_balance = 0

for each pre-commencement item in chronological order:
  if the item is an ELIGIBLE_COST:
    temporary_opening_balance -= the cost amount

  if the item would be a CASH_EVENT:
    temporary_opening_balance = min(0,
                                    temporary_opening_balance + event amount)

PORTFOLIO_NET_GAIN at COMMENCEMENT_TIME = temporary_opening_balance
```

Event surplus is therefore discarded rather than carried forward. No cost, receipt, or loss from a position extinguished before commencement carries forward.

After commencement:

- each `ELIGIBLE_COST` decreases `PORTFOLIO_NET_GAIN`; and
- each `CASH_EVENT` increases `PORTFOLIO_NET_GAIN` by its event amount.

When related actions occur together, they are applied in this order:

1. recognize every eligible cost and attributable tax caused by or needed to produce the event cash;
2. add the `CASH_EVENT` and calculate any shareable value under §4; and
3. recognize any unrelated new investment or other later cost.

Cash invested immediately after receipt is therefore counted as event cash before the new investment reduces `PORTFOLIO_NET_GAIN`. A later cost can require recovery before another distribution, but never requires a completed distribution to be returned.

## 4. Floor and distributions

`FLOOR` is the level of `PORTFOLIO_NET_GAIN` reserved for the owner before value becomes shareable.

```
FLOOR = 10,000,000 USD × (CPI_CURRENT / CPI_2026_06)

CPI_CURRENT is the value most recently published as of the applicable CASH_EVENT
for the US Consumer Price Index for All Urban Consumers, All Items, U.S. City
Average, Not Seasonally Adjusted—BLS series CUUR0000SA0.

CPI_2026_06 is that series' value for June 2026.

If BLS discontinues the series, its officially designated successor applies.
If none exists, the closest published measure of US consumer prices selected
reasonably and in good faith applies.
```

`PORTFOLIO_PEAK` is the greatest `PORTFOLIO_NET_GAIN` immediately after step 2 of any prior `CASH_EVENT` under §3, before any unrelated new investment or later cost in step 3, whether or not that event produced a distribution.

```
PORTFOLIO_PEAK at COMMENCEMENT_TIME = 0
```

At each `CASH_EVENT`:

```
event_amount     = the amount of this CASH_EVENT
net_gain_after   = PORTFOLIO_NET_GAIN after related costs and this CASH_EVENT
threshold        = max(FLOOR at this event, PORTFOLIO_PEAK before this event)

SHAREABLE_VALUE  = max(0, min(event_amount, net_gain_after - threshold))
PORTFOLIO_PEAK   = max(PORTFOLIO_PEAK before this event, net_gain_after)
```

This calculation shares only new portfolio gain above both the owner's floor and every previous portfolio peak. A later decrease in the floor does not make old gain shareable, and a later increase in cost must be recovered before a new peak can be shared.

Each outstanding share is one equal unit of participation. At a `CASH_EVENT`, every non-owner shareholder becomes entitled to:

```
SHAREHOLDER_DISTRIBUTION = SHAREABLE_VALUE
                           × (shareholder's shares / all outstanding shares)
```

The portion attributable to owner shares belongs to the owner. If no non-owner shares are outstanding, no distribution is owed, but `PORTFOLIO_PEAK` still updates.

The holder at the time of the `CASH_EVENT` owns the resulting distribution. That right is fixed at the event and is not transferred or extinguished by a later issuance, transfer, royalty, buyout, surrender, amendment, incapacity, or death.

```
DISTRIBUTION_DEADLINE = 30 calendar days
```

The owner must calculate and settle each distribution within `DISTRIBUTION_DEADLINE` after the `CASH_EVENT`. If a shareholder has not provided payment instructions, tax documentation, or other information reasonably required for payment, that shareholder's deadline begins when the owner receives it. Payment may otherwise be delayed only as reasonably necessary to comply with law, maintain a permitted reserve, or resolve a good-faith dispute; every unaffected and undisputed amount must be paid on time.

Each shareholder is responsible for taxes imposed on that shareholder's distribution. Tax required by law to be withheld and remitted is treated as paid to the shareholder.

## 5. Shares and issuances

All shares are one class with equal rights. Shares are whole and indivisible; no fractional share may be issued, held, or transferred.

The shares and this agreement are contractual only. All in-scope assets remain solely owned and controlled by the owner. A shareholder has no ownership of, lien on, or other property right in an in-scope asset or its unrealized value, and no control over the owner's actions or life. This agreement creates no partnership, agency, or trust and creates no fiduciary relationship except for the administrative duties expressly stated in §10.

```
AUTHORIZED_SHARES = 12,000,000
```

Immediately before `COMMENCEMENT_TIME`, no shares are outstanding. The initial capitalization may occur only after the owner has adopted this agreement for the personal stock. At `COMMENCEMENT_TIME`, it issues the opening shares recorded in the official history. It must issue a positive whole number of shares to the owner, may issue shares to other persons, and may not cause outstanding shares to exceed `AUTHORIZED_SHARES`.

An unvested award is only a contractual right and carries no share rights. It reserves the whole number of shares that may issue under it. Shares issue as they vest, reducing the award's unvested reservation by the same number; a cancelled or forfeited unvested amount ceases to be reserved.

```
AVAILABLE_ISSUANCE_CAPACITY = AUTHORIZED_SHARES
                              - outstanding shares
                              - shares reserved under unvested awards
```

`AVAILABLE_ISSUANCE_CAPACITY` may never be negative. Increasing `AUTHORIZED_SHARES` requires an amendment under §12.

Only the owner acting personally may authorize an issuance or award. The owner may not be the recipient of an issuance or award after `COMMENCEMENT_TIME`. A vesting and issuance already authorized by an award may occur during the owner's incapacity without further authorization. No share may be issued, and no unvested award may vest, after the owner's death.

Subject to these limits, the owner may issue shares or grant awards whether or not the recipient pays cash. The owner may choose the non-owner recipient, number of shares, cash price, vesting, and other award terms without shareholder approval. No shareholder has a preemptive, pro rata, participation, anti-dilution, or other right to acquire newly issued shares. A transaction-specific invitation creates no right or precedent for a later issuance.

### Use and reporting of issuance proceeds

`ISSUANCE_PROCEEDS` are the `ACTUAL_CASH_PAID` assigned under §6 to an issuance of personal-stock shares. Money received from a transfer of the owner's existing shares is not `ISSUANCE_PROCEEDS`.

`ISSUANCE_PROCEEDS` belong solely to the owner. They are not a `CASH_EVENT`, do not increase `PORTFOLIO_NET_GAIN`, and give no shareholder any ownership of, lien on, security interest in, or control over the proceeds. Subject to those ownership rules, the owner must use all `ISSUANCE_PROCEEDS` in good faith for activities that the owner determines are expected to benefit the personal stock's long-term value. The owner may retain unused proceeds pending such use. The expected benefit may be direct or indirect, financial or nonfinancial, immediate or long-term.

The nature, selection, timing, amount, and expected benefit of a use are matters of owner judgment. No shareholder approval, consent, or consultation is required. A shareholder's different view of a use, or the use's failure to produce the expected result, creates no claim or remedy. This protection does not permit the owner to use `ISSUANCE_PROCEEDS` for a purpose the owner does not in good faith expect to benefit the personal stock.

For each calendar year during which `ISSUANCE_PROCEEDS` are received, remain unused, or are used, the owner must provide every then-current non-owner shareholder, within 90 calendar days after the end of that year, a report stating the opening unused balance, additional proceeds received, amounts used grouped into meaningful high-level categories, and the ending unused balance. Categories must be selected and applied reasonably and in good faith and must describe the general nature of the uses. The report need not identify or itemize individual transactions or include transaction-level supporting records.

On a non-owner shareholder's reasonable request, the owner must provide that shareholder a reasonably current update in the same categorized form covering the period after the most recent annual report. The owner must maintain private records reasonably sufficient to prepare and substantiate the required reports. The reports and underlying records are not required to be included in the official history. A shareholder must keep every nonpublic report and underlying record confidential and use it only to verify or enforce this agreement, except with confidential professional advisers or as required by law.

When `ISSUANCE_PROCEEDS` are used in accordance with this subsection to acquire or increase an in-scope asset, that use satisfies this subsection, and the asset and value later arising from it are governed under §§2–4 without separate continuing tracing of the original `ISSUANCE_PROCEEDS`.

Before a person who does not hold shares may receive shares by issuance or voluntary transfer, the owner and that person must sign a record by which that person adopts the then-current agreement for this personal stock. The record may also state transaction terms and separate obligations. Succession by operation of law under §13 is the only exception.

An issuance or transfer settles only when all conditions are satisfied and the share movement is irrevocable. Its actual settlement time controls even if it is recorded later.

Before or simultaneously with the initial capitalization, the owner must record every opening in-scope asset, the opening `PORTFOLIO_NET_GAIN`, every opening share issuance and resulting balance, and every other opening fact needed to apply this agreement.

## 6. Transfers

The owner may transfer the owner's existing shares for cash or no cash. Such a transfer is not an issuance and does not change outstanding shares or available issuance capacity.

Except for surrender under §9 or succession under §13, a non-owner shareholder may voluntarily transfer shares only through a bona fide sale solely for actual cash that the owner has approved and that complies with applicable law. The owner may grant or withhold approval in the owner's sole discretion. Approval must remain effective at settlement.

For a permitted sale, the cash payment, buyer-share transfer, and any royalty-share transfer required by §7 must occur as one settlement. A transfer does not carry a distribution that accrued to the seller before settlement.

The official history assigns `ACTUAL_CASH_PAID` as follows:

```
ACTUAL_CASH_PAID =
  issuance or transfer with a required USD cash purchase price:
    required USD cash purchase price actually and irrevocably paid in full

  issuance or transfer with no required USD cash purchase price:
    0
```

These amounts exist only for royalties and buyout minimums under this agreement; they are not tax basis, fair market value, or a legal characterization of the transaction.

`ACTUAL_CASH_PAID` is only the USD cash purchase price that the issuance or transfer expressly makes a condition of settlement and that the acquirer actually and irrevocably pays in full. Nothing else counts toward, substitutes for, reduces, or changes that required payment. A transaction with a required USD cash purchase price does not settle until that price has been paid in full.

## 7. Royalties

```
ROYALTY_RATE = 0.05
```

When a non-owner shareholder’s voluntary cash sales produce cumulative net profit not previously subject to a royalty, the seller owes the owner `ROYALTY_RATE` of that new profit. The royalty is paid in whole shares taken from the shares being sold; it does not add shares to the sale or require a cash payment.

For each non-owner shareholder, the official history tracks:

```
aggregate_actual_cash_paid = total ACTUAL_CASH_PAID assigned to shares currently held
average_actual_cash_paid   = aggregate_actual_cash_paid / shares currently held
cumulative_sale_result     = sum of results from prior voluntary cash sales
royalty_peak               = greatest cumulative_sale_result on which royalty
                             was assessed, never less than 0
unconverted_royalty_value  = royalty value left after prior whole-share rounding

for a new non-owner shareholder other than by legal succession:
  cumulative_sale_result    = 0
  royalty_peak              = 0
  unconverted_royalty_value = 0
```

Acquiring additional shares pools their `ACTUAL_CASH_PAID` with that of the shares already held and does not reset the holder's cumulative sale result, royalty peak, or unconverted royalty value.

For each permitted voluntary cash sale:

```
sale_shares         = total whole shares the seller will transfer
sale_price          = required USD cash purchase price per share transferred to the buyer
pre_royalty_value   = sale_shares × sale_price
allocated_cost      = average_actual_cash_paid × sale_shares
sale_result         = pre_royalty_value - allocated_cost

cumulative_after    = cumulative_sale_result + sale_result
new_royalty_gain    = max(0, cumulative_after - royalty_peak)
royalty_value       = new_royalty_gain × ROYALTY_RATE
total_royalty_value = royalty_value + unconverted_royalty_value
royalty_shares      = round down(total_royalty_value / sale_price)
buyer_shares        = sale_shares - royalty_shares
sale_proceeds       = buyer_shares × sale_price = ACTUAL_CASH_PAID
unconverted_after   = total_royalty_value - (royalty_shares × sale_price)
royalty_peak_after  = max(royalty_peak, cumulative_after)

sale_price > 0
buyer_shares > 0
```

The seller transfers exactly `sale_shares`: `buyer_shares` to the buyer and `royalty_shares` to the owner. The buyer pays `sale_proceeds`. A seller may therefore include every share held in a sale without retaining extra shares for the royalty. If the calculation would leave the buyer with no shares, the sale cannot settle on those terms. `unconverted_after` carries forward in USD and is applied at the next royalty-bearing sale; it is not independently payable in cash.

The seller's `aggregate_actual_cash_paid` is reduced proportionally for every share leaving the seller in the settlement, including royalty shares. If the buyer is a non-owner shareholder, the buyer's `aggregate_actual_cash_paid` increases by `sale_proceeds`. Seller expenses and taxes do not reduce the contractual sale result.

Losses offset later gain, and gain is charged only once. The carried unconverted royalty value prevents whole-share rounding from being used to avoid royalties.

Only a non-owner shareholder's permitted voluntary cash sale carries a royalty. An issuance, owner sale, buyout, replacement third-party sale under §8, surrender, or legal succession carries no royalty. Royalties and royalty shares do not affect `PORTFOLIO_NET_GAIN` or the number of outstanding shares.

## 8. Buyouts

The owner may require a non-owner shareholder to sell any whole number of shares up to all shares held if the owner determines, in the owner's sole judgment, that the shareholder's continued ownership creates a material misalignment with the purposes or interests of the personal stock and that the misalignment is, or is reasonably expected to be, detrimental to the personal stock. Such a transaction is a buyout and may be initiated at any time. The purchaser in a buyout (`BUYOUT_PURCHASER`) may be the owner or, in the owner's sole discretion, any other person except the shareholder being bought out. A person other than the owner may be designated as `BUYOUT_PURCHASER` only after that person has adopted the then-current agreement for this personal stock under §5.

```
BUYOUT_MINIMUM_NOTICE        = 15 business days
BUYOUT_NOTICE_EXPIRATION     = 20 business days after notice
HIGHER_OFFER_DEADLINE        = 2 business days before scheduled settlement
BUYOUT_DISPUTE_DEADLINE      = HIGHER_OFFER_DEADLINE
BUYOUT_RESUMPTION_NOTICE     = 2 business days
MINIMUM_BUYOUT_PRICE         = 1 USD per share
DISPUTE_RESOLUTION_PROVIDER  = American Arbitration Association (AAA)

BUYOUT_PRICE_FLOOR = max(
  MINIMUM_BUYOUT_PRICE,
  shareholder's average_actual_cash_paid immediately before notice
)
```

The owner must give written notice stating the `BUYOUT_PURCHASER`, number of shares, settlement date, price per share, and a brief good-faith explanation. The complete notice must be recorded in the official history when given. The settlement date may not precede `BUYOUT_MINIMUM_NOTICE` and the notice expires at `BUYOUT_NOTICE_EXPIRATION`. The `BUYOUT_PURCHASER` identified in the notice may not be changed; a different purchaser requires withdrawal and a new buyout notice. A later buyout requires a new notice and price. The price is fixed and assessed as of the notice date. It must be fair, determined reasonably and in good faith from the information then available, and no less than `BUYOUT_PRICE_FLOOR`.

In determining fairness, the owner must consider all material information reasonably available, including recent bona fide cash transactions in the shares; in-scope assets and reasonably expected distributions; outstanding shares; and material changes in the owner's reputation, audience, opportunities, and prospects. The owner may not use a buyout primarily to capture for the `BUYOUT_PURCHASER` a specific distribution the owner then reasonably expects would otherwise accrue to the shareholder. Any such expected distribution must also be reflected in the fair price.

The fair price may reflect all risks, uncertainties, restrictions, contingencies, and other factors affecting the value of the personal stock as a whole, but after that overall value is determined, each share must be valued at its pro rata portion without any additional discount for the size of the holding, minority status, lack of control, lack of marketability, or transfer restrictions.

By `HIGHER_OFFER_DEADLINE`, the shareholder may present a bona fide, binding, fully financed, lawful third-party offer to purchase the same shares solely for cash at a higher per-share price and capable of settling by the scheduled buyout. Before the scheduled settlement, the owner may withdraw the buyout, the `BUYOUT_PURCHASER` may match that higher price, or the owner may approve the third-party sale, subject to the buyer adopting the then-current agreement for this personal stock under §5 and satisfying legal requirements. If the `BUYOUT_PURCHASER` matches, the matched price replaces the price stated in the notice for all remaining purposes under this section. If the owner approves the third-party sale and it settles, or if the owner withdraws the buyout, the pending buyout ends. Withdrawal does not approve or permit the offered third-party sale. If the shareholder timely presents such a higher offer, the buyout may settle only if the `BUYOUT_PURCHASER` matches that higher price; otherwise, the owner must withdraw the buyout or approve the third-party sale. If the approved third-party sale settles, it carries no royalty and does not enter the seller's cumulative sale result because it replaces a required buyout rather than an independently chosen transfer. The seller's `aggregate_actual_cash_paid` is then reduced proportionally for the shares sold, and the buyer's `aggregate_actual_cash_paid` increases by the `ACTUAL_CASH_PAID` assigned to those shares.

By `BUYOUT_DISPUTE_DEADLINE`, the shareholder may give written notice specifically identifying facts that, if established, would show that the price is unfair, material information was omitted, the buyout was used primarily to capture a specific expected distribution in violation of this section, or the owner breached an administrative duty in pricing the buyout or carrying out a required procedure. The owner's determination concerning material misalignment and detriment is a matter of owner judgment under §10; a shareholder may not dispute, and the neutral may not review, the merits of that determination or substitute a different judgment. A shareholder's refusal or desire to remain a shareholder, without a claimed violation of this agreement, is not a dispute.

A timely dispute suspends settlement and tolls `BUYOUT_NOTICE_EXPIRATION`. The shares remain held by the shareholder while the dispute is pending, and §4 continues to determine who owns every distribution arising before settlement. The shareholder must proceed promptly and advance any filing or neutral fees required to initiate the process, subject to final cost allocation. If `DISPUTE_RESOLUTION_PROVIDER` closes the matter because the shareholder, without good cause, fails to pay or proceed, the dispute is treated as withdrawn.

The owner and shareholder may jointly select a single independent neutral with relevant expertise. If they cannot agree promptly, `DISPUTE_RESOLUTION_PROVIDER` appoints the neutral. The owner must provide the neutral every official-history entry and private supporting record reasonably necessary to decide the dispute. Before receiving private information, the neutral must agree in writing to protect it and may disclose only what is reasonably necessary to explain or enforce the decision.

The neutral must resolve the dispute as promptly as reasonably practicable and must assess price and compliance as of the original notice date using information then existing and reasonably knowable. A later development may be considered only as evidence of a condition or reasonable expectation that existed on that date; it does not itself increase the price.

The neutral may uphold the buyout, determine the fair price as of the notice date, or invalidate the notice for violating this section or the owner's administrative duties. The neutral may not reduce the price stated in the notice. The neutral's decision is binding for the pending buyout.

```
FINAL_BUYOUT_PRICE = max(
  price stated in the notice,
  fair price determined by the neutral
)
```

If the buyout remains valid after the decision, the owner may cause the `BUYOUT_PURCHASER` to complete it at `FINAL_BUYOUT_PRICE` under the schedule established by the neutral or may withdraw it. Neither the owner nor a designated purchaser has any obligation to complete a buyout at a higher price determined by the neutral. If the owner withdraws or the notice is invalidated, no shares transfer and a later buyout requires a new notice and price. Withdrawal does not prevent the neutral from allocating reasonable audit and dispute costs or deciding an alleged administrative breach arising before withdrawal.

The owner may also withdraw a buyout at any time before settlement. If no dispute is pending, withdrawal ends the notice. If a dispute is pending, it ends the proposed transfer but not the neutral's authority described above.

If the shareholder's dispute is withdrawn or treated as withdrawn, the tolling of `BUYOUT_NOTICE_EXPIRATION` ends. If the scheduled settlement date has passed, the owner may proceed under the same notice only by giving the shareholder a replacement settlement date at least `BUYOUT_RESUMPTION_NOTICE` in advance and no later than the resumed `BUYOUT_NOTICE_EXPIRATION`. Otherwise, the original settlement date remains effective.

A buyout settles when the `BUYOUT_PURCHASER` irrevocably deposits the full purchase price calculated using the price then governing under this section, less only tax required to be withheld and remitted, with a payment agent or in a segregated account solely for the shareholder, and the owner records the transfer to the `BUYOUT_PURCHASER`. The shareholder's consent, signature, cooperation, or payment instructions are not required. Without full funding, no buyout occurs.

The neutral may allocate reasonable audit and dispute costs based on the outcome and the parties' conduct. Except for fraud or intentional concealment that could not reasonably have been discovered before settlement, a completed buyout has no later price adjustment, true-up, additional payment, or challenge under §11.

A buyout carries no royalty and does not enter the seller's cumulative sale result. The seller's `aggregate_actual_cash_paid` is reduced proportionally for the shares sold. If the `BUYOUT_PURCHASER` is a non-owner shareholder, that purchaser's `aggregate_actual_cash_paid` increases by the `ACTUAL_CASH_PAID` assigned to the purchased shares. The shares transfer to the `BUYOUT_PURCHASER` and remain outstanding.

## 9. Surrender and dissolution

A non-owner shareholder may surrender all shares held by written notice to the owner. The surrender is effective when received, requires no approval, is irrevocable, transfers the shares to the owner for no consideration, and carries no royalty. It ends every future right attached to those shares but does not extinguish a distribution or other payment that accrued before surrender.

`DISSOLUTION` is the final recorded action terminating the personal stock. It extinguishes all outstanding shares, closes the accounting balances, ends this agreement's application to every person and asset, and permits no later economic event. The official history remains permanent.

During the owner's life, only the owner acting personally may cause dissolution, and only when no shares are held by another person and no obligation to another person remains. After the owner's death, dissolution occurs under §13.

## 10. Duties

Solely in administering this agreement, the owner owes every non-owner shareholder fiduciary duties of loyalty, reasonable care, candor, and impartiality. The owner must administer this agreement honestly and in good faith; must not manipulate or omit a classification, estimate, valuation, calculation, record, timing, or process to improperly benefit the owner or another person; must use reasonable care in maintaining records and performing calculations; must disclose the material information required to verify the administration of this agreement; and must apply this agreement consistently and treat equal shares equally except where it expressly permits holder-specific action.

A shareholder must hold and act with respect to shares solely for that shareholder's own benefit. Except for a legal representative under §13, no shareholder may use a nominee, agent, proxy, or other arrangement to give a non-shareholder the beneficial ownership or control of shares or to act on a non-shareholder's instructions.

### Owner judgment

The owner's administrative duties do not govern the owner's personal life, career, labor, reputation, spending, investment decisions, tax affairs, or decisions to acquire, retain, manage, or dispose of an in-scope asset, except where this agreement expressly prescribes how an event must be classified, recorded, calculated, or paid.

The owner will authorize an issuance or award only after determining that it is expected to benefit the personal stock. The expected benefit may be direct or indirect, financial or nonfinancial, immediate or long-term, and may be shared with the recipient or others.

Matters of owner judgment include that determination; the nature, selection, timing, amount, and expected benefit of a use of `ISSUANCE_PROCEEDS` under §5; the determination under §8 whether a shareholder's continued ownership creates a material misalignment with the purposes or interests of the personal stock and whether that misalignment is, or is reasonably expected to be, detrimental to the personal stock; whether, when, and whom to buy out under §8 and whom to select as the `BUYOUT_PURCHASER`; whether, when, to whom, and on what terms to issue shares or grant awards within available issuance capacity; whether, when, to whom, and on what terms the owner transfers the owner's shares; whether to approve or refuse a non-owner shareholder's voluntary transfer; whether to propose or withdraw an amendment; the personal and economic decisions described above; and any other decision that this agreement expressly places in the owner's sole discretion or states is not governed by a duty to shareholders.

A matter of owner judgment, including the owner's purpose, reasons, decision-making process, and assessment of its expected benefit to the personal stock, is final and non-reviewable. A shareholder's different view of the decision, its terms, its expected benefit, or its ultimate result creates no claim or remedy under this agreement. A matter of owner judgment may not be audited or disputed under §11, and a neutral has no authority to review it or grant relief based on it.

This protection does not excuse noncompliance with an express limit, condition, procedure, recording requirement, calculation, or payment obligation. The decision itself is a matter of owner judgment; its implementation and administration remain subject to the applicable terms of this agreement. With respect to `ISSUANCE_PROCEEDS`, this protection bars review of the merits or outcome of a use. Whether the owner made the good-faith determination required by §5, and whether the owner performed the reporting and recordkeeping duties required there, are matters of compliance rather than owner judgment and may be audited or disputed under §11.

## 11. Records, audits, and disputes

### Official history and supporting records

The owner must maintain one complete chronological official history sufficient to determine the current state, reproduce every calculation, and verify this agreement. It must record or identify:

- shareholders, share movements, `ACTUAL_CASH_PAID`, awards, vesting, cancellations, reserved shares, and available issuance capacity;
- amendment proposals, record times, approvals, and effective versions;
- in-scope assets and every input and result used for eligible costs, cash events, each reserve's recognized amount, paid or unpaid status, increase, payment, release, refund or used benefit, `PORTFOLIO_NET_GAIN`, the floor, portfolio peak, shareable value, and distributions; and
- transfers, royalty calculations, buyouts, surrenders, successions, dissolution, and corrections.

The agreement controls; the history is authoritative unless corrected. Facts must be recorded promptly at their actual occurrence, effectiveness, or settlement time and before use in a later calculation or transaction. Every amount is applied once, and every derived view must be reproducible from the history.

The complete event and calculation history and current state must remain directly observable by every shareholder without a request to or discretionary action by the owner. It may use display names, opaque asset identifiers, and aggregate amounts, but may not omit a numerical or logical input needed to reproduce a result. Underlying identities and source documents may remain in the private supporting records.

The owner may, but is not required to, make any portion or all of the official history and current state publicly observable. Making only part public does not require the owner to make any other part public. Except as provided below, the owner may not publicly disclose a shareholder's legal name unless the shareholder uses it as a display name or specifically consents in writing, and may not publish a copy of the shareholder's signature, electronic-signing record, private signed document, or private supporting record without the affected shareholder's specific written consent.

These restrictions do not prevent disclosure required by law or reasonably and in good faith necessary to assert, enforce, or defend a right under this agreement or to respond to a public accusation concerning the personal stock or the owner's administration of it. The owner must redact unrelated nonpublic contact, payment, tax, identity-verification, financial-account, and authentication information.

The owner must preserve the history. A correction identifies and supersedes rather than erases the error, and every affected result is recalculated chronologically. It does not automatically reverse a completed transaction or payment; practical consequences must be resolved reasonably and in good faith. Fraud, intentional misrepresentation, and intentional manipulation remain subject to otherwise available remedies.

The owner must maintain private records sufficient to substantiate the history and the issuance-proceeds reports required by §5. On reasonable request, the owner must provide evidence sufficient to verify a recorded matter and may use redactions, summaries, or professional certification. The categorized reporting right for `ISSUANCE_PROCEEDS` is governed by §5 and does not require transaction-level disclosure to a shareholder. A shareholder must keep nonpublic information confidential and use it only to verify or enforce this agreement, except with confidential professional advisers or as required by law.

### Independent audits

Any non-owner shareholder may engage an independent qualified professional to audit the owner's administration of this agreement. The audit may test both completeness and accuracy: whether every asset, event, transaction, cost, receipt, reserve, share movement, and other matter required by this agreement has been recorded, and whether every recorded input, classification, valuation, calculation, and payment is supported and correct.

The owner must give the reviewer access to the official history and every private supporting record reasonably necessary to conduct the audit. Before receiving access, the reviewer must agree in writing to protect confidential information and may disclose to shareholders only the findings and supporting information reasonably necessary to explain them.

The requesting shareholder initially pays the reasonable audit cost. If the audit identifies a material error or breach and the finding is not disputed in good faith or is sustained under the dispute-resolution process below, the owner must reimburse that cost solely from amounts that would otherwise belong to the owner under §4 at future `CASH_EVENT`s, as and when those amounts arise, and must correct every affected record, calculation, and payment. Until reimbursed from that source, the unpaid balance bears no interest and creates no default or recourse against the owner personally.

### Dispute resolution

An audit may examine a buyout, but any dispute concerning a buyout is governed exclusively by §8, including its deadlines, remedies, and finality rules.

Any other unresolved dispute concerning an audit, record, classification, valuation, calculation, payment, or administrative duty must be decided by a single independent neutral with relevant expertise. The owner and the disputing shareholder or shareholders may select the neutral jointly. If they cannot agree, `DISPUTE_RESOLUTION_PROVIDER` appoints the neutral. The decision is binding, and the neutral may order corrections, payments, and a fair allocation of audit and dispute costs.

## 12. Amendments

One published agreement version governs a personal stock, its owner, every shareholder, and every share at all times. No person-specific or parallel agreement version may govern the same personal stock.

An amendment under this section changes only the published agreement version governing this personal stock. It does not modify the shared publication or affect any other personal stock that has adopted it.

```
MAX_PENDING_AMENDMENT_PROPOSALS = 1
AMENDMENT_APPROVAL_THRESHOLD    = 0.75 of NON_OWNER_SHARES at RECORD_TIME
```

The owner may not exceed `MAX_PENDING_AMENDMENT_PROPOSALS`. A proposal must identify one replacement published agreement by version, blockchain network, authoritative onchain address, and content hash; include its full text and a plain-language summary of every material change; and be recorded and delivered to every current shareholder. `RECORD_TIME` is the time that complete proposal is recorded; it may not be backdated. The owner may withdraw the proposal before it becomes effective.

An amendment becomes effective for everyone simultaneously when approved in writing by:

- the owner; and
- record-time holders satisfying `AMENDMENT_APPROVAL_THRESHOLD`.

Owner shares are excluded from both the numerator and denominator. If no non-owner shares are outstanding at `RECORD_TIME`, the owner may approve an amendment alone.

The voters and approval weights are fixed at `RECORD_TIME`; a later ownership change does not alter them, and a later holder takes shares subject to the outcome. The owner may withdraw the proposal and submit a new one using the ownership at a new record time.

An approval is irrevocable for that proposal. When the last required approval is received and recorded, the replacement published agreement identified in the proposal takes effect for this personal stock, every current and future shareholder, and all shares. Until then, the existing agreement remains effective.

An amendment operates prospectively. It may not retroactively erase or reduce a distribution or payment already accrued, reverse a completed transaction, or impose a new obligation on a completed transaction without the affected person's consent. It must apply equally to all shares of this single class.

The owner may resolve an administrative matter not addressed by this agreement reasonably and in good faith, but may not change economic rights, contradict this agreement, or bypass an amendment or approval requirement.

## 13. Incapacity, death, and succession

If the owner or a shareholder becomes incapacitated, a person legally authorized to manage that person's property may exercise ordinary rights and perform ordinary duties under this agreement, subject to the same limits. Only the owner personally may authorize a new issuance, award, buyout, amendment, or voluntary dissolution. A previously authorized award may continue vesting during incapacity under §5.

If a non-owner shareholder dies or shares otherwise pass by operation of law, the legal successor becomes the shareholder and receives the shares with their associated `ACTUAL_CASH_PAID`, cumulative sale result, royalty peak, unconverted royalty value, and accrued distributions. If more than one successor receives shares, all holder-level amounts are allocated among them in proportion to the shares received and then combined with any existing state of a successor who already holds shares. The succession requires neither prior owner approval nor a prior signature and carries no royalty. The successor is bound by this agreement and must provide information reasonably needed to record the succession and comply with law.

On the owner's death:

- the owner's personal representative administers the personal stock;
- no amendment, issuance, new award, vesting, or buyout may occur;
- the `FLOOR` is permanently fixed using the CPI most recently published at death;
- shares held by the owner's estate remain owner shares;
- the same portfolio-net-gain, peak, cash-event, reserve, and distribution rules continue; and
- each in-scope asset must be preserved, administered, and converted to cash when reasonably practicable, with due regard for value and without requiring a forced or distressed sale.

A share that vested before the owner's death may be recorded afterward using its actual vesting time; this is not a post-death issuance or vesting.

The estate may incur direct costs of preserving, administering, or disposing of an in-scope asset and may maintain reasonable reserves for attributable income or realization taxes. General probate and estate-administration costs, and estate, inheritance, gift, or generation-skipping transfer taxes, do not reduce `PORTFOLIO_NET_GAIN`. Every later reserve release, refund, or credit must be accounted for and distributed as required before dissolution.

When every in-scope asset has been converted to cash or otherwise finally disposed of or extinguished, the personal representative must make a final good-faith estimate of any unresolved attributable tax or direct asset cost, using professional advice when appropriate. That final estimate is recognized before the final distribution. Once every distribution has been paid, any negative `PORTFOLIO_NET_GAIN` is borne by the estate and creates no shareholder repayment obligation, and the personal representative must record `DISSOLUTION`. A later tax or cost difference belongs solely to the estate and does not reopen the personal stock, except to correct fraud or an error in the pre-dissolution official history.

The agreement binds the owner's estate, and the owner must maintain estate-planning instructions directing the personal representative to perform it.

The owner may not intentionally create or permit a marital-property, nominee, creditor, pledge, security, or other arrangement whose primary purpose is to defeat or materially impair performance of this agreement. No such arrangement changes a shareholder's contractual rights to the extent enforceable by law.

## 14. General

Every share transaction is subject to all applicable laws. The owner may require reasonable compliance information and delay or refuse a transaction until satisfied; permission under this agreement does not itself establish legality.

A business day is a day other than Saturday, Sunday, or a US federal holiday.

Unless expressly stated otherwise, cash uses USD and every monetary calculation is denominated in it.

No tax will be withheld from a payment unless required by law. Tax properly withheld and remitted is treated as paid to the recipient.

If a provision or application is invalid or unenforceable, it is severed only to the extent necessary, and the remainder remains effective.

The owner and each shareholder must maintain a current electronic notice address in the private supporting records. Electronic notice satisfies a writing requirement and is received when it enters the designated system in retrievable form; known delivery failure requires another reasonable method.

The owner and any one or more shareholders may enter into a separate signed agreement, including a side letter granting a pro rata or other participation right, that creates additional personal rights or obligations between its parties. A separate agreement binds only its parties and any successor or assign bound under its terms and applicable law, and it is governed and enforced according to its own terms and applicable law. It is separate from and not part of this agreement and does not amend, waive, override, supersede, or control the interpretation or application of this agreement; alter any right or obligation attached to a share; bind the personal stock or any other person; or authorize, require, or validate anything this agreement prohibits. If a separate agreement conflicts with this agreement in governing or administering the personal stock, this agreement controls and the conflicting term has no effect to the extent of the conflict. A breach of a separate agreement may support a remedy between the persons bound by it, but every remedy remains subject to this agreement and may not dispense with any requirement of this agreement or alter a right of a person not bound by the separate agreement.

This agreement is the complete statement of the terms governing the personal stock. A signed adoption, award, transaction document, summary, or other record may identify the personal stock, the parties, and the applicable published agreement; reproduce this agreement for readability; and establish facts or separate obligations, but it changes this agreement only through §12. If a reproduction differs from the authoritative text identified in the signed adoption, the authoritative text controls.
