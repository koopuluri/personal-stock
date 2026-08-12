# Shareholder Agreement Adoption by Email

Under [§14 of the Personal Stock Agreement](../agreement.md#14-general), the owner's request and the shareholder's response below are the complete signed adoption record; no confirmation email or separately signed PDF is required. Attach a retainable copy of the exact complete Agreement identified in the request, send the request from the owner's electronic notice address, and retain the request, response, attachment, full email headers, and available delivery and timestamp evidence in the private supporting records. The same thread may later be used for amendment proposals, but each proposal must provide and identify the proposed replacement Agreement and state what an **I agree** response means. Record the corresponding `AGREEMENT_ADOPTION` event before relying on an adoption for a share transaction.

### 1. Adoption request

```text
Subject: {{PERSONAL_STOCK_NAME}} agreement

Hi {{SHAREHOLDER_LEGAL_NAME}},

Please review the attached Personal Stock Agreement.

Personal stock: {{PERSONAL_STOCK_NAME}}
Chain ID: {{CHAIN_ID}}
Stock contract: {{STOCK_CONTRACT_ADDRESS}}

Agreement version: {{AGREEMENT_VERSION}}
Keccak-256 hash: {{AGREEMENT_CONTENT_HASH}}

The shares are speculative and illiquid, may have no value or distributions, may be diluted, and are subject to the restrictions and risks in the Agreement.

I, {{OWNER_LEGAL_NAME}}, approve this adoption and intend this email to be my
electronic signature as owner.

To adopt the attached Agreement for this personal stock, reply:

I agree

By replying "I agree," you adopt and agree to be bound by the attached Agreement,
confirm that you received it and had the opportunity to review it, consent to sign electronically, and intend your reply to be your electronic signature. This
adoption does not itself issue or promise you any shares.
```

### 2. Shareholder response

```text
I agree
```
