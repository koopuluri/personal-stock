# Shareholder Agreement Adoption by Email

Under [§14 of the Personal Stock Agreement](../agreement.md#14-general), this email exchange is itself the adoption record and contains the parties' electronic signatures; no separately signed PDF is required. The owner sends the request below with a retainable copy of the exact complete Agreement attached, the shareholder replies **I agree**, and the owner sends the confirmation. The request defines that exact reply as the shareholder's unambiguous assent and electronic signature and associates it with the identified adoption record and Agreement. Use the stated electronic notice addresses, keep the subject line and thread intact, and retain the raw messages with full headers, the attachment, and reasonably available delivery and timestamp evidence in the private supporting records. Do not treat another abbreviated response, including a bare "yes," as execution without obtaining the exact **I agree** response. After confirmation, record the corresponding `AGREEMENT_ADOPTION` event before relying on the adoption for a share transaction.

### 1. Request to adopt

```text
Subject: Adoption request — {{PERSONAL_STOCK_NAME}} — {{ADOPTION_DOCUMENT_ID}}
From: {{OWNER_LEGAL_NAME}} <{{OWNER_ELECTRONIC_NOTICE_ADDRESS}}>
To: {{SHAREHOLDER_LEGAL_NAME}} <{{SHAREHOLDER_ELECTRONIC_NOTICE_ADDRESS}}>

Hi {{SHAREHOLDER_LEGAL_NAME}},

I am asking you to adopt the attached Personal Stock Agreement for
{{PERSONAL_STOCK_NAME}}. Please review and retain this email and the attachment
before deciding whether to agree.

Adoption record
  Status: {{DOCUMENT_STATUS}}
  Adoption ID: {{ADOPTION_DOCUMENT_ID}}
  Shareholder: {{SHAREHOLDER_LEGAL_NAME}} ({{SHAREHOLDER_ID}})
  Shareholder email: {{SHAREHOLDER_ELECTRONIC_NOTICE_ADDRESS}}
  Owner: {{OWNER_LEGAL_NAME}} ({{OWNER_SHAREHOLDER_ID}})
  Owner email: {{OWNER_ELECTRONIC_NOTICE_ADDRESS}}
  Chain ID: {{CHAIN_ID}}
  Personal stock: {{PERSONAL_STOCK_NAME}}
  Stock contract: {{STOCK_CONTRACT_ADDRESS}}
  Agreement version: {{AGREEMENT_VERSION}}
  Agreement content hash (Keccak-256): {{AGREEMENT_CONTENT_HASH}}
  Authoritative content: Exact {{AGREEMENT_BYTE_LENGTH}} UTF-8 source bytes

The attached Agreement is the complete Agreement identified above and is provided
in retainable form as Exhibit A. This released version is also made available in a
public source repository. Repository URLs, commits, tags, filenames, and rendered
copies help locate and read it but do not identify the authoritative text. The
exact source bytes matching the version and content hash above control if any
source reference or reproduction differs from them.

These shares are unusual, speculative, and illiquid contractual interests. They
may have no value, may never produce a distribution, provide no ownership or
control of the underlying assets, may be diluted, are subject to transfer and
buyout restrictions, and may create tax, legal, and operational risks. The
Agreement contains the complete terms and controls this summary.

If you choose to adopt the Agreement, reply from
{{SHAREHOLDER_ELECTRONIC_NOTICE_ADDRESS}} in this same thread with exactly:

I agree

By replying "I agree," you:

- adopt the Agreement identified above solely for this personal stock and agree
  to be bound by it;
- confirm that you received and could retain this request and the complete
  Agreement, had the opportunity to review them, and are acting voluntarily with
  legal capacity;
- acknowledge the risks summarized above and the complete terms in the Agreement;
- understand that this adoption does not itself give you shares or require any
  issuance, award, or transfer;
- understand that amendments effective under §12 govern as provided in the
  Agreement;
- confirm that {{SHAREHOLDER_ELECTRONIC_NOTICE_ADDRESS}} is your electronic
  notice address; and
- consent to conduct this adoption electronically and intend your reply to be your
  writing and electronic signature under §14 of the Agreement.

The adoption becomes effective after the owner sends the confirmation below. It
may support a share transaction only after the corresponding AGREEMENT_ADOPTION
event is recorded in the official history.
```

### 2. Shareholder response

```text
Subject: Re: Adoption request — {{PERSONAL_STOCK_NAME}} — {{ADOPTION_DOCUMENT_ID}}
From: {{SHAREHOLDER_LEGAL_NAME}} <{{SHAREHOLDER_ELECTRONIC_NOTICE_ADDRESS}}>
To: {{OWNER_LEGAL_NAME}} <{{OWNER_ELECTRONIC_NOTICE_ADDRESS}}>

I agree
```

### 3. Owner confirmation

```text
Subject: Re: Adoption request — {{PERSONAL_STOCK_NAME}} — {{ADOPTION_DOCUMENT_ID}}
From: {{OWNER_LEGAL_NAME}} <{{OWNER_ELECTRONIC_NOTICE_ADDRESS}}>
To: {{SHAREHOLDER_LEGAL_NAME}} <{{SHAREHOLDER_ELECTRONIC_NOTICE_ADDRESS}}>

Confirmed. I, {{OWNER_LEGAL_NAME}} ({{OWNER_SHAREHOLDER_ID}}), confirm your
identity, join in adoption record {{ADOPTION_DOCUMENT_ID}}, and electronically
sign your adoption of Personal Stock Agreement version {{AGREEMENT_VERSION}},
content hash {{AGREEMENT_CONTENT_HASH}}, for {{PERSONAL_STOCK_NAME}}. I intend
this reply to be my writing and electronic signature under §14 of the Agreement.

The adoption is effective upon receipt of this confirmation. It may support a
share transaction only after the corresponding AGREEMENT_ADOPTION event is
recorded in the official history. This adoption does not itself issue, transfer,
reserve, or promise any shares.
```
