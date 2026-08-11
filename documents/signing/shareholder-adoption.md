# Shareholder Agreement Adoption

**{{DOCUMENT_STATUS}}**

Adoption document ID: `{{ADOPTION_DOCUMENT_ID}}`

This Shareholder Agreement Adoption identifies the personal stock, the prospective shareholder, and the exact published Personal Stock Agreement being adopted. It does not issue, transfer, reserve, or promise any shares.

## 1. Personal stock and agreement identification

| Personal stock | Identification |
| --- | --- |
| Name | {{PERSONAL_STOCK_NAME}} |
| Unique identifier | `{{PERSONAL_STOCK_IDENTIFIER}}` |
| Blockchain network | {{STOCK_BLOCKCHAIN_NETWORK}} |
| Chain ID | `{{STOCK_CHAIN_ID}}` |
| Authoritative stock contract | `{{STOCK_CONTRACT_ADDRESS}}` |

| Agreement | Identification |
| --- | --- |
| Title | Personal Stock Agreement |
| Version | `{{AGREEMENT_VERSION}}` |
| Blockchain network | {{AGREEMENT_BLOCKCHAIN_NETWORK}} |
| Chain ID | `{{AGREEMENT_CHAIN_ID}}` |
| Authoritative agreement contract | `{{AGREEMENT_CONTRACT_ADDRESS}}` |
| Content-hash algorithm | Keccak-256 |
| Agreement content hash | `{{AGREEMENT_CONTENT_HASH}}` |
| Hashed content | Exact {{AGREEMENT_BYTE_LENGTH}} bytes of the authoritative agreement content |

The complete agreement content identified above is reproduced as Exhibit A for review. As provided in the Agreement, the authoritative text identified by the version, blockchain network, authoritative onchain address, and content hash controls if a reproduction differs from it.

## 2. Adoption

I, **{{SHAREHOLDER_LEGAL_NAME}}**, identified in the personal stock's records as `{{SHAREHOLDER_ID}}`, adopt the Agreement identified in Section 1 solely for this personal stock and agree to be bound by it.

This adoption becomes effective when the shareholder and owner have both electronically signed this record. It may be used to support a share transaction only after an `AGREEMENT_ADOPTION` event identifying this shareholder, agreement version, and agreement content hash has been recorded in the official history.

This adoption does not itself create a right to receive shares or require the owner to authorize any issuance, award, or transfer. Every share transaction requires its own authorization, terms, conditions, settlement, and official-history entry.

## 3. Risk disclosure

The shares are unusual, speculative, illiquid contractual interests involving substantial risk. This disclosure summarizes material risks but does not replace or modify the Agreement.

- **No assured value or return.** Shares may have no realizable value. No distribution, recurring payment, market price, resale opportunity, or return of any amount paid or value contributed is promised.
- **Distributions may never occur.** Distributions depend on realized USD cash, portfolio-wide net gain, the inflation-adjusted `FLOOR`, the prior `PORTFOLIO_PEAK`, outstanding shares, eligible costs, taxes, reserves, and the other requirements of the Agreement.
- **No ownership or control of assets.** A share does not give its holder ownership of, a lien on, or control over any in-scope asset, its unrealized value, or issuance proceeds. Subject to the Agreement's limited good-faith use and reporting duties for issuance proceeds, the owner controls the owner's life, work, investments, spending, and other matters reserved to owner judgment.
- **Use of issuance proceeds.** Cash paid for an issuance belongs solely to the owner but must be used in good faith for activities the owner determines are expected to benefit the personal stock's long-term value. Shareholders receive annual reports, and reasonably requested updates, showing receipts, uses grouped into meaningful high-level categories, and the unused balance. Reports need not identify individual transactions, and shareholders have no approval or consultation right. The uses may not succeed or increase value.
- **Dilution.** Additional shares and awards may be issued within the Agreement's limits without a shareholder's consent or participation, reducing that shareholder's percentage interest in later shareable value.
- **Illiquidity, transfer restrictions, and buyouts.** There may be no market for the shares. Voluntary transfers are restricted, and the owner may require a non-owner shareholder to sell shares through the buyout process in Section 8.
- **Share-issuance adoption condition.** The separate Share Issuance Agreement requires the recipient to have a recorded adoption of the exact agreement version governing at settlement. If a later amendment becomes effective before settlement, that issuance requires adoption of the new governing version.
- **Limited review of owner judgment.** Matters designated as owner judgment, including the merits and outcome of issuance-proceeds uses, are final and non-reviewable. Compliance with the express good-faith use, reporting, recordkeeping, and other administrative requirements remains subject only to the duties, records, audits, disputes, deadlines, and remedies stated in the Agreement.
- **Tax, legal, and regulatory uncertainty.** A shareholder may incur taxes or other legal consequences, and the availability or enforceability of rights may be affected by applicable law. Each shareholder is responsible for obtaining advice appropriate to that shareholder's circumstances.
- **Operational and personal dependency.** Performance depends on accurate records, estimates, classifications, administration, and payment. Incapacity, death, succession, insolvency, disputes, mistakes, misconduct, or changes in law or circumstances may delay, impair, or prevent expected outcomes.

## 4. Acknowledgments and execution terms

By signing this record, the prospective shareholder acknowledges and agrees that:

- the shareholder received this record, the foregoing risk disclosure, and the complete Agreement reproduced as Exhibit A before signing;
- the shareholder had the opportunity to review those materials and is signing voluntarily with legal capacity to do so;
- amendments that become effective under Section 12 of the Agreement govern all shareholders and shares as provided there; a later transaction document may separately require a fresh adoption as a condition of that transaction;
- the risk disclosure is informational, does not expand or reduce the Agreement's rights or obligations, and does not waive any express right under the Agreement or any right that cannot lawfully be waived;
- this record adopts but does not amend the Agreement;
- electronic signatures and the electronic record of this transaction have the same intended effect as original signatures and records on paper; and
- the shareholder's electronic notice address for the private supporting records is **{{SHAREHOLDER_ELECTRONIC_NOTICE_ADDRESS}}**.

By signing this record, the owner confirms the shareholder's identity for this adoption and joins in the adoption record as required by the Agreement. The owner's signature does not authorize or promise a share transaction.

The Agreement and this record state their respective terms. No summary, presentation, discussion, or other communication changes them.

## 5. Signatures

[[ADOPTION_SIGNATURE_BLOCK]]
