#!/usr/bin/env python3
"""Create a new append-batch draft pinned to a verified journal position."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError(f"refusing to replace existing file: {args.output}")
        journal = json.loads(args.journal.read_text(encoding="utf-8"))
        if journal.get("format") != "personal-stock-ledger-journal":
            raise ValueError("journal has an unsupported format")
        draft = {
            "format": "personal-stock-ledger-batch",
            "format_version": 1,
            "chain_id": journal["chain_id"],
            "stock_contract": journal["stock_contract"],
            "expected_event_count": journal["event_count"],
            "expected_head": journal["head"],
            "events": [],
        }
        args.output.write_text(json.dumps(draft, indent=2) + "\n", encoding="utf-8")
        print(f"created batch draft: {args.output}")
        print("add one or more events, then run check.sh and preview_batch.py")
        return 0
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
