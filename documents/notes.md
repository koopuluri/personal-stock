# Design Notes

These are nonbinding commentaries on deliberate choices that the agreement leaves implicit. The agreement controls.

## Tax refunds follow current ownership

A tax-reconciliation `REALIZATION_EVENT` uses the shares and distribution election then in effect, not those at the related exit. Example: A holds shares at an exit, sells them to B, and a tax refund later arrives; B participates in the refund. A keeps any completed distribution, while a later tax shortfall reduces `CUMULATIVE_REALIZED_VALUE` and, where applicable, Reinvestment Capital under the agreement.

## Entity holdings are not looked through

When the owner holds an interest in a company or fund, that interest is the in-scope holding; the entity's underlying assets are not separate personal-stock holdings. Example: an investment fund may sell portfolio companies and retain the proceeds without creating the owner's `REALIZATION_EVENT`; §4 governs when the fund interest produces one.

## Cash, currency, and event time are literal

Except for terminal exits and `ATTRIBUTABLE_TAXES` events, only actual USD cash from an in-scope holding creates a `REALIZATION_EVENT`. This includes every cash dividend, interest payment, income, and distribution; no distinction is made between ordinary and special dividends. Noncash value remains in scope rather than being deemed cash, and no currency-conversion method is intended. The actual event or settlement time controls even if recorded later; no second contractual timestamp is required.

## Reinvestment Capital is an aggregate balance

Reinvestment Capital is purpose-bound in the aggregate, not a segregated fund, trust, or set of per-holding or per-share accounts. Adjustments are made reasonably and in good faith without tracing particular dollars. A transferor retains no residual interest, except that §13 fixes entitlement to the final balance among non-owner holders at the owner's death.

Reinvestment Capital is expected to be reflected in the economic value of the shares, as retained capital ordinarily is in company stock, so it is not paid separately when shares are transferred. With sufficient liquidity, recent transaction prices should cause `BENCHMARK_PRICE` to reflect that value; with illiquid stock, the benchmark may be stale and fail to do so. The benchmark is only the contractual minimum, and the owner is expected to ensure that a buyback reflects fair market value when it is higher, but that expectation is nonbinding and is not part of the agreement.

## Incapacity and death use limited succession rules

During incapacity, a legal representative may administer ordinary rights and duties, but only the owner personally may authorize an issuance and none may settle during incapacity or after death. A deceased non-owner's shares must be bought back rather than remain permanently with an estate. The agreement intentionally imposes no broader incapacity freeze or alternative death-transfer path.

## Shareholders need not all be natural persons

The owner may prefer natural-person shareholders and enforce that preference through issuance and transfer discretion, but the agreement intentionally contains no general natural-person-only restriction. The mandatory buyback following a non-owner's death is a separate succession rule.

## Rare non-tax reversals are deferred

The agreement intentionally has no bespoke rule for a later refund or reimbursement of a previously deducted non-tax expense. That is an accepted launch edge case to address, if material, through a future agreement version rather than by expanding the core `REALIZATION_EVENT` rules now.

## The distribution electorate may change

The owner may use compliant buybacks and directed sales to replace shareholders who prefer `DISTRIBUTE` with shareholders who prefer `REINVEST`; no neutrality or anti-circumvention rule prevents this. Example: if the current majority selects `DISTRIBUTE`, shares may settle to new holders before a later `REALIZATION_EVENT`, which uses the new holders' standing elections.

## Governing law and forum remain open

The agreement intentionally selects neither governing law nor an exclusive forum. Example: a dispute among San Francisco parties may naturally proceed in California, but the agreement does not require that result; the parties or the court apply the otherwise applicable rules when needed.
