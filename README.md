# Personal Stock Ledger

This repository contains the public ledger implementation and event history for
Karthik Uppuluri Stock.

The governing [Personal Stock agreement](https://github.com/onrootnet/personal-stock) is published separately by Rootnet. Agreement adoption events identify an exact published agreement by its version and SHA-256 content hash; agreement source and signing materials are not duplicated here.

- [`ledger/schema.md`](ledger/schema.md) defines the public event formats.
- [`ledger/src/StockLedger.sol`](ledger/src/StockLedger.sol) implements the
  append-only Base ledger contract.
- [`ledger/script/`](ledger/script/) contains validation, replay, deployment, and
  publication tooling.
- [`ledger/test/`](ledger/test/) contains Solidity and Python tests.
- [`ledger/README.md`](ledger/README.md) documents the ledger model and operations.

The authoritative stock history is the immutable event journal at the deployed
ledger contract. Current state is derived by resolving overlays and replaying that
history; repository copies of event batches and receipts are operational evidence,
not an alternative ledger.

The ledger address will be recorded here after deployment.

| Network | Ledger address |
| --- | --- |
| Base mainnet | _not deployed_ |
| Base Sepolia | _not deployed_ |
