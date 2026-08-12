# Karthik Uppuluri Stock

This repository contains the public agreement and implementation for Karthik
Uppuluri Stock.

- [`documents/agreement.md`](documents/agreement.md) is the published standard
  agreement. Each released version is identified by its version and Keccak-256
  content hash; the exact agreement bytes remain in the public source repository.
- [`ledger/schema.md`](ledger/schema.md) describes the public event formats used
  by the stock ledger.
- [`ledger/`](ledger/) contains the append-only Base ledger contract, event tooling,
  deterministic resolver, replay code, and tests.
- [`documents/signing/`](documents/signing/) contains email templates for agreement
  adoption and immediate share issuance. Private identities, correspondence,
  signatures, and supporting records do not belong in this public repository.

There is no onchain agreement document and no replaceable stock-state document. The
authoritative stock history is the immutable event journal at the deployed ledger
contract. Current state is derived by resolving overlays and replaying that history.

The ledger address will be recorded here after deployment.

| Network | Ledger address |
| --- | --- |
| Base mainnet | _not deployed_ |
| Base Sepolia | _not deployed_ |
