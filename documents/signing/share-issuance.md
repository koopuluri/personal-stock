# Share Issuance by Email

Under [§14 of the Personal Stock Agreement](../agreement.md#14-general), the owner's request and the recipient's response below are the complete signed issuance agreement; no confirmation email or separately signed PDF is required. Send the request from the owner's electronic notice address, receive the response from the recipient's electronic notice address, and retain both messages with their full headers and available delivery and timestamp evidence in the private supporting records. This exchange authorizes the issuance but does not itself issue shares or complete settlement.

### 1. Issuance request

```text
Subject: {{PERSONAL_STOCK_NAME}} share issuance

Hi {{RECIPIENT_LEGAL_NAME}},

I am offering to issue you {{ISSUED_SHARES}} new shares of
{{PERSONAL_STOCK_NAME}} for a total USD cash purchase price of
{{REQUIRED_CASH_PURCHASE_PRICE_DISPLAY}}.

Chain ID: {{STOCK_CHAIN_ID}}
Stock contract: {{STOCK_CONTRACT_ADDRESS}}

Agreement version: {{AGREEMENT_VERSION}}
Keccak-256 hash: {{AGREEMENT_CONTENT_HASH}}

I, {{OWNER_LEGAL_NAME}}, acting personally, authorize this issuance and intend
this email to be my electronic signature as owner.

To accept, reply:

I agree

By replying "I agree," you accept this issuance subject to the Agreement, consent
to sign electronically, and intend your reply to be your electronic signature.
This exchange does not itself issue shares. The issuance settles only after you
have a recorded adoption of the Agreement then governing, any required payment
has been made in full, sufficient issuance capacity and all legal requirements
are satisfied, and the irrevocable issuance is recorded in the official history.
If the Agreement changes before settlement, you must first adopt the new version.
```

### 2. Recipient response

```text
I agree
```
