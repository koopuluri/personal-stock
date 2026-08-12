# Share Issuance by Email

Under [§14 of the Personal Stock Agreement](../agreement.md#14-general), this email exchange is itself the signed Share Issuance Agreement; no separately signed PDF is required. The owner sends the complete issuance request below, the recipient replies **I agree**, and the owner sends the confirmation personally authorizing the issuance. Use the stated electronic notice addresses, keep the subject line and thread intact, and retain the raw messages with full headers and reasonably available delivery and timestamp evidence in the private supporting records. The exchange establishes and signs the issuance terms but does not itself issue shares or complete settlement. Settlement occurs only after every stated condition is satisfied and the issuance becomes irrevocable and is recorded in the official history.

### 1. Issuance request

```text
Subject: Share issuance request — {{PERSONAL_STOCK_NAME}} — {{ISSUANCE_DOCUMENT_ID}}
From: {{OWNER_LEGAL_NAME}} <{{OWNER_ELECTRONIC_NOTICE_ADDRESS}}>
To: {{RECIPIENT_LEGAL_NAME}} <{{RECIPIENT_ELECTRONIC_NOTICE_ADDRESS}}>

Hi {{RECIPIENT_LEGAL_NAME}},

I am offering to issue you {{ISSUED_SHARES}} new shares of
{{PERSONAL_STOCK_NAME}} for a total USD cash purchase price of
{{REQUIRED_CASH_PURCHASE_PRICE_DISPLAY}} on the terms below. Please review and
retain this email before deciding whether to agree.

Issuance record
  Status: {{DOCUMENT_STATUS}}
  Issuance ID: {{ISSUANCE_DOCUMENT_ID}}
  Owner and issuer: {{OWNER_LEGAL_NAME}} ({{OWNER_SHAREHOLDER_ID}})
  Owner email: {{OWNER_ELECTRONIC_NOTICE_ADDRESS}}
  Recipient: {{RECIPIENT_LEGAL_NAME}} ({{RECIPIENT_SHAREHOLDER_ID}})
  Recipient email: {{RECIPIENT_ELECTRONIC_NOTICE_ADDRESS}}
  Personal stock: {{PERSONAL_STOCK_NAME}}
  Personal stock ID: {{PERSONAL_STOCK_IDENTIFIER}}
  Stock network: {{STOCK_BLOCKCHAIN_NETWORK}}
  Stock chain ID: {{STOCK_CHAIN_ID}}
  Stock contract: {{STOCK_CONTRACT_ADDRESS}}
  Agreement version: {{AGREEMENT_VERSION}}
  Agreement content hash (Keccak-256): {{AGREEMENT_CONTENT_HASH}}
  Adoption document: {{RECIPIENT_ADOPTION_DOCUMENT_ID}}
  AGREEMENT_ADOPTION sequence: {{RECIPIENT_ADOPTION_SEQUENCE}}
  New shares: {{ISSUED_SHARES}}
  Total USD cash purchase price: {{REQUIRED_CASH_PURCHASE_PRICE_DISPLAY}}

This is an immediate issuance of new shares, not a transfer, unvested award,
promise, or reservation. It creates new outstanding shares, reduces available
issuance capacity by the same number, and carries no royalty. Any cash paid is
ISSUANCE_PROCEEDS under the Agreement, belongs solely to the owner, is not a
CASH_EVENT, and remains subject to the Agreement's good-faith use and reporting
requirements.

The issuance may settle only if, at settlement:

- you are registered in the official history;
- you have a recorded adoption of the exact Agreement version then governing;
- sufficient issuance capacity exists;
- the total cash purchase price, if any, has been paid fully and irrevocably;
- all applicable legal and compliance requirements have been satisfied; and
- the issuance has become irrevocable and is recorded in the official history.

If the governing Agreement changes before settlement, the version then governing
controls and you and the owner must complete and record a new adoption of that
version before this issuance may settle. Signing this record does not itself issue shares, complete settlement, or give you any distribution or other right that accrued before settlement. Each party is responsible for that party's own taxes and professional advice.

If you accept these terms, reply from {{RECIPIENT_ELECTRONIC_NOTICE_ADDRESS}} in
this same thread with exactly:

I agree

By replying "I agree," you:

- accept the issuance described above subject to every stated condition and the
  governing Agreement;
- confirm that your identity and adoption references above are accurate;
- acknowledge that the issuance may dilute every existing shareholder and that
  you receive no right accruing before settlement;
- understand the payment and settlement requirements and that no shares issue
  merely because you sign; and
- consent to conduct this transaction electronically and intend your reply to be
  your writing and electronic signature under §14 of the Agreement.

The owner must send the confirmation below before this issuance is authorized.
```

### 2. Recipient response

```text
Subject: Re: Share issuance request — {{PERSONAL_STOCK_NAME}} — {{ISSUANCE_DOCUMENT_ID}}
From: {{RECIPIENT_LEGAL_NAME}} <{{RECIPIENT_ELECTRONIC_NOTICE_ADDRESS}}>
To: {{OWNER_LEGAL_NAME}} <{{OWNER_ELECTRONIC_NOTICE_ADDRESS}}>

I agree
```

### 3. Owner confirmation

```text
Subject: Re: Share issuance request — {{PERSONAL_STOCK_NAME}} — {{ISSUANCE_DOCUMENT_ID}}
From: {{OWNER_LEGAL_NAME}} <{{OWNER_ELECTRONIC_NOTICE_ADDRESS}}>
To: {{RECIPIENT_LEGAL_NAME}} <{{RECIPIENT_ELECTRONIC_NOTICE_ADDRESS}}>

Confirmed. I, {{OWNER_LEGAL_NAME}} ({{OWNER_SHAREHOLDER_ID}}), acting personally,
authorize the issuance described in issuance record {{ISSUANCE_DOCUMENT_ID}} and
electronically sign it as owner and issuer. I represent that sufficient available
issuance capacity will exist at settlement and intend this reply to be my writing
and electronic signature under §14 of the Agreement.

This confirmation signs and authorizes the issuance terms but does not itself
issue shares or complete settlement. The issuance will settle only after every
condition stated in the request is satisfied and the irrevocable SHARE_ISSUANCE
event records the recipient, issued shares, and actual_cash_paid_usd.
```
