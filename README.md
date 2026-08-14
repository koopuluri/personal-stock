# Karthik Uppuluri Stock Ledger

This repository contains the official public history of Karthik Uppuluri Stock.
The governing [Personal Stock Agreement](https://github.com/onrootnet/personal-stock)
is published separately by Rootnet.

The repository intentionally has only three files:

- [`ledger.json`](ledger.json) begins with a plain-language current summary and
  state, followed by the complete event history;
- [`schema.md`](schema.md) defines its structure and recording rules; and
- this file explains how the ledger is maintained and published.

## Authority

`ledger.json` on `main` is the current official history. An event is recorded when
it is committed and made available there; a later release is not required for the
event to take effect. The agreement controls if this repository or schema conflicts
with the agreement.

Events are appended promptly after the represented fact occurs, becomes effective,
or settles. The current state is updated in the same commit and must be reproducible
from the effective event history. A public entry may use opaque identifiers, while
legal identities, signed messages, payment evidence, tax records, and other
supporting records remain private.

The short `current_state.summary` at the top of `ledger.json` explains the current
position and latest changes for readers who do not need to inspect every event.

An error is corrected by appending a `CORRECTION` event. A recorded fact is not
silently erased or rewritten. A disclosed schema migration may re-encode the same
facts under a new `schema_version` as described in `schema.md`, with the prior
representation preserved in Git history. Private supporting records remain the
evidence used to substantiate entries, answer shareholder requests, and conduct
audits.

## Periodic releases

The owner may periodically publish an immutable GitHub Release as an archival
checkpoint, normally once a month when activity exists. Each checkpoint freezes the
three repository files at one reviewed commit. Work may continue on `main`
immediately afterward.

Releases improve retrieval and make historical versions easy to verify, but they do
not replace the live official history and are not a prerequisite to recording an
event. If an event must support a later calculation or transaction, it is recorded
on `main` before that use rather than waiting for the next monthly release.

## Editing the ledger

For an ordinary event:

1. append the next contiguous sequence to `events` in `ledger.json`;
2. use the fact's actual `effective_at` and the entry's actual `recorded_at`;
3. include the public inputs and results required to reproduce its effect;
4. update `current_state` and its plain-language `summary` through that sequence; and
5. review the complete diff before committing and pushing it.

Earlier test implementations and rehearsal data had no legal effect. They remain
recoverable from Git history but are not part of this ledger.
