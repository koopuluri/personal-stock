#!/usr/bin/env python3
"""Validate a proposed append against the verified full journal and preview its effects."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import ledger_events as ledger


ZERO_HASH = "0x" + "00" * 32


class PreviewError(ValueError):
    pass


def run(*args: str) -> str:
    process = subprocess.run(args, check=False, capture_output=True, text=True)
    if process.returncode:
        detail = process.stderr.strip() or process.stdout.strip()
        raise PreviewError(f"command failed: {' '.join(args)}\n{detail}")
    return process.stdout.strip()


def source_events(journal: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "event_type": item["event_type"],
            "effective_at": item["effective_at"],
            "data": item["data"],
        }
        for item in journal["events"]
    ]


def load_complete(source: dict[str, Any]) -> ledger.Batch:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "complete.json"
        path.write_text(json.dumps(source, ensure_ascii=False) + "\n", encoding="utf-8")
        return ledger.load_batch(path, allow_large_journal=True)


def state_for(events: list[dict[str, Any]], chain_id: int, address: str) -> dict[str, Any] | None:
    if not events:
        return None
    complete = {
        "format": ledger.FORMAT,
        "format_version": ledger.FORMAT_VERSION,
        "chain_id": chain_id,
        "stock_contract": address,
        "expected_event_count": 0,
        "expected_head": ZERO_HASH,
        "events": events,
    }
    parsed = load_complete(complete)
    return ledger.replay(ledger.resolve_events(parsed.events)).as_json()


def changes(before: Any, after: Any, path: str = "$") -> list[dict[str, Any]]:
    if before == after:
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        result: list[dict[str, Any]] = []
        for key in sorted(before.keys() | after.keys()):
            child = f"{path}.{key}"
            if key not in before:
                result.append({"path": child, "before": None, "after": after[key]})
            elif key not in after:
                result.append({"path": child, "before": before[key], "after": None})
            else:
                result.extend(changes(before[key], after[key], child))
        return result
    return [{"path": path, "before": before, "after": after}]


def preview(journal_path: Path, batch_path: Path) -> dict[str, Any]:
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    if journal.get("format") != "personal-stock-ledger-journal":
        raise PreviewError("journal has an unsupported format")
    active_schema = ledger.active_schema_from_journal(journal_path)
    batch = ledger.load_batch(batch_path, initial_schema=active_schema)
    if batch.chain_id != journal["chain_id"]:
        raise PreviewError("batch chain ID does not match journal")
    if batch.stock_contract.lower() != journal["stock_contract"].lower():
        raise PreviewError("batch contract does not match journal")
    if batch.expected_event_count != journal["event_count"]:
        raise PreviewError("batch expected count does not match verified journal")
    if batch.expected_head.lower() != journal["head"].lower():
        raise PreviewError("batch expected head does not match verified journal")

    prior_events = source_events(journal)
    proposed_events = [
        {
            "event_type": event.event_type,
            "effective_at": event.effective_at,
            "data": event.data,
        }
        for event in batch.events
    ]
    after_state = state_for(
        prior_events + proposed_events,
        batch.chain_id,
        batch.stock_contract,
    )
    before_state = state_for(prior_events, batch.chain_id, batch.stock_contract)

    predicted: list[dict[str, Any]] = []
    prior_head = journal["head"].lower()
    for event in batch.events:
        payload = ledger.canonical_payload(event.data)
        payload_hash = run("cast", "keccak", "0x" + payload.hex()).lower()
        preimage = ledger.event_hash_preimage(
            batch.chain_id,
            batch.stock_contract,
            event.sequence,
            event.event_type,
            event.effective_at_unix,
            payload_hash,
            prior_head,
        )
        event_hash = run("cast", "keccak", preimage).lower()
        predicted.append(
            {
                "sequence": event.sequence,
                "event_type": event.event_type,
                "schema_version": event.schema_version,
                "schema_content_hash": event.schema_content_hash,
                "effective_at": event.effective_at,
                "previous_head": prior_head,
                "payload_hash": payload_hash,
                "event_hash": event_hash,
                "data": event.data,
            }
        )
        prior_head = event_hash

    return {
        "format": "personal-stock-ledger-batch-preview",
        "format_version": 1,
        "chain_id": batch.chain_id,
        "stock_contract": batch.stock_contract,
        "before": {
            "event_count": journal["event_count"],
            "head": journal["head"],
            "state": before_state,
        },
        "proposed_events": predicted,
        "after": {
            "event_count": journal["event_count"] + len(predicted),
            "head": prior_head,
            "state": after_state,
        },
        "state_changes": changes(before_state, after_state),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal", type=Path)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = preview(args.journal, args.batch)
        output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.write_text(output, encoding="utf-8")
            print(f"wrote: {args.output}")
        else:
            print(output, end="")
        return 0
    except (OSError, KeyError, ValueError, PreviewError, ledger.ValidationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
