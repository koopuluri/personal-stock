# Signing by email

This directory contains retainable email templates for the electronic-signature
process described in §14 of the Personal Stock Agreement:

- [`shareholder-adoption.md`](shareholder-adoption.md) records a person's adoption of
  an exact agreement version and content hash.
- [`share-issuance.md`](share-issuance.md) records the terms and owner authorization
  for an immediate share issuance.

Use the templates directly as email content; no generated execution artifact is
produced. Replace every `{{PLACEHOLDER}}` in private working storage, send the
resulting request from the stated electronic notice address, retain the complete email
thread and attachment, and record the resulting ledger event only after the legal
action becomes effective or settles.

For a new recipient, the operational order is:

1. prepare the shareholder's opaque public identifier and private identity record;
2. execute the agreement adoption by email, attaching the exact complete agreement;
3. append `SHAREHOLDER_REGISTERED` and `AGREEMENT_ADOPTION` as appropriate;
4. execute the share-issuance terms by email;
5. satisfy the payment, capacity, legal, and settlement conditions; and
6. append `SHARE_ISSUANCE` using the actual settlement time and cash paid.

Legal names, email addresses, executed messages, delivery evidence, payment evidence,
tax information, and other supporting records are private. Do not commit them here.
