# Share Issuance Agreement

**{{DOCUMENT_STATUS}}**

Issuance document ID: `{{ISSUANCE_DOCUMENT_ID}}`

This Share Issuance Agreement states the terms on which the personal stock will issue new shares to the recipient. It is separate from the recipient's adoption of the Personal Stock Agreement and covers an immediate issuance, not an unvested award or a transfer of existing shares.

## 1. Personal stock and governing agreement

| Personal stock | Identification |
| --- | --- |
| Name | {{PERSONAL_STOCK_NAME}} |
| Unique identifier | `{{PERSONAL_STOCK_IDENTIFIER}}` |
| Blockchain network | {{STOCK_BLOCKCHAIN_NETWORK}} |
| Chain ID | `{{STOCK_CHAIN_ID}}` |
| Authoritative stock contract | `{{STOCK_CONTRACT_ADDRESS}}` |

| Agreement governing when this record was signed | Identification |
| --- | --- |
| Version | `{{AGREEMENT_VERSION}}` |
| Authoritative agreement contract | `{{AGREEMENT_CONTRACT_ADDRESS}}` |
| Agreement content hash | `{{AGREEMENT_CONTENT_HASH}}` |

The agreement version governing the personal stock at actual settlement controls. If an amendment becomes effective after this record is signed but before settlement, the amended version controls as provided by the Agreement.

## 2. Parties and adoption prerequisite

| Party | Identification |
| --- | --- |
| Owner and issuer | {{OWNER_LEGAL_NAME}} (`{{OWNER_SHAREHOLDER_ID}}`) |
| Recipient | {{RECIPIENT_LEGAL_NAME}} (`{{RECIPIENT_SHAREHOLDER_ID}}`) |
| Recipient adoption document | `{{RECIPIENT_ADOPTION_DOCUMENT_ID}}` |
| Recipient `AGREEMENT_ADOPTION` event | `{{RECIPIENT_ADOPTION_EVENT_ID}}` |

**MANDATORY ADOPTION CONDITION.** As a separate transaction-specific condition under this record, this issuance is permitted and may settle only if, at settlement, the recipient has a recorded adoption of the exact agreement version then governing the personal stock. The adoption event identified above must record the governing version and its content hash. This condition applies even if the recipient already holds shares or adopted an earlier version.

If an amendment becomes effective before settlement, the adoption identified above no longer satisfies this condition unless it identifies the newly governing version and content hash. The recipient and owner must complete and record a new adoption before the issuance may settle. A purported issuance that does not satisfy this condition is not permitted and does not settle.

## 3. Issuance terms

| Term | Agreed value |
| --- | --- |
| Whole new shares to be issued | **{{ISSUED_SHARES}} shares** |
| Required USD cash purchase price | **{{REQUIRED_CASH_PURCHASE_PRICE_DISPLAY}}** |

The owner personally authorizes the personal stock to issue the stated whole shares, and the recipient agrees to accept them, subject to every condition in this record and the Agreement.

This is an issuance, not a transfer. It creates new outstanding shares, reduces `AVAILABLE_ISSUANCE_CAPACITY` by the same number, and does not reduce or move the owner's existing share balance. It carries no royalty. Money paid for the issuance is `ISSUANCE_PROCEEDS` under the Agreement. It belongs solely to the owner and is not a `CASH_EVENT`, subject to the Agreement's good-faith use and categorized-reporting requirements.

The required USD cash purchase price is the total amount the recipient must actually and irrevocably pay for the issuance to settle. If no USD cash purchase price is required, the issuance may settle without a cash payment. Upon settlement, the official history records `ACTUAL_CASH_PAID` equal to the required USD cash purchase price paid in full, or `0` if no cash purchase price was required. `ACTUAL_CASH_PAID` exists only for the Agreement's royalty and buyout calculations; it is not tax basis, fair market value, compensation value, or a legal characterization of the transaction.

This record does not create an unvested award, vesting condition, service obligation, repurchase right, or reservation of shares. Any such terms require a separate signed award record and corresponding official-history support.

## 4. Settlement

Signing this record authorizes and establishes terms for the proposed issuance but does not itself issue shares or complete settlement.

The issuance settles only when all of the following are true:

1. both parties have signed this record;
2. the recipient is registered in the official history;
3. the mandatory adoption condition in Section 2 is satisfied at settlement;
4. the personal stock has at least the stated number of shares of `AVAILABLE_ISSUANCE_CAPACITY`;
5. if a USD cash purchase price is required, the recipient has actually and irrevocably paid it in full;
6. every legal and compliance requirement applicable to the issuance has been satisfied; and
7. the issuance has become irrevocable and has been recorded in the official history.

The actual settlement time controls even if a supporting record is entered later. The resulting `SHARE_ISSUANCE` event must record the recipient, issued shares, and `actual_cash_paid_usd` equal to the amount determined above.

## 5. Representations and execution terms

The owner represents that the owner is acting personally and that sufficient `AVAILABLE_ISSUANCE_CAPACITY` will exist at settlement. The recipient represents that the recipient information and adoption references in this record are accurate.

The recipient acknowledges that this issuance may dilute every existing shareholder's percentage interest in later shareable value and that no distribution or other right accruing before settlement belongs to the recipient by reason of this issuance.

Each party is responsible for that party's own taxes and professional advice. Authorization under the Agreement and this record does not itself establish that the issuance complies with applicable law.

Electronic signatures and the electronic record of this transaction have the same intended effect as original signatures and records on paper. This record establishes transaction-specific terms but does not amend the Agreement.

## 6. Signatures

[[ISSUANCE_SIGNATURE_BLOCK]]
