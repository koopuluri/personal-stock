# Published Ledger Mirrors

Each network directory contains a verified, reproducible mirror of one deployed
`StockLedger` journal:

- `deployment.json` identifies the chain, contract, controller, deployment transaction,
  and deployment block;
- `batches/` preserves the exact source batch, pre-publication preview, and transaction
  receipt for each atomic append;
- `journal.json` is the complete raw event journal reconstructed from contract logs;
- `effective.json` resolves revisions, voids, insertions, and supplements; and
- `state.json` is the disposable current state produced by replay.

The contract logs are authoritative. These committed files are a human-readable,
cryptographically verified public mirror and audit trail. Never edit generated views
by hand; regenerate them with `ledger/script/sync.sh`.

Network directories are intentionally separate. Base Sepolia is a rehearsal ledger
and has no legal or operational effect on the Base mainnet personal stock.
