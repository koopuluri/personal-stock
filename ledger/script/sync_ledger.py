#!/usr/bin/env python3
"""Fetch StockLedger logs, verify the journal, and write reproducible public views."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import ledger_events as ledger


EVENT_TOPIC = "0xac58f73f0dd927ad4060bc9f19bc05c95ed0d3be6c6b042b3144b200defc5a0d"
ZERO_HASH = "0x" + "00" * 32
LOG_BLOCK_SPAN = 10_000


class SyncError(ValueError):
    pass


def run(*args: str) -> str:
    process = subprocess.run(args, check=False, capture_output=True, text=True)
    if process.returncode:
        detail = process.stderr.strip() or process.stdout.strip()
        raise SyncError(f"command failed: {' '.join(args)}\n{detail}")
    return process.stdout.strip()


def rpc(rpc_url: str, method: str, params: list[Any]) -> Any:
    output = run(
        "cast",
        "rpc",
        "--rpc-url",
        rpc_url,
        method,
        *(json.dumps(param) for param in params),
    )
    return json.loads(output)


def quantity(value: str) -> int:
    return int(value, 16)


def word(value: str, index: int) -> str:
    raw = value[2:]
    start = index * 64
    return raw[start : start + 64]


def decode_data(value: str) -> tuple[int, str, str, bytes]:
    effective_at = int(word(value, 0), 16)
    previous_head = "0x" + word(value, 1).lower()
    event_hash = "0x" + word(value, 2).lower()
    payload_offset = int(word(value, 3), 16)
    payload_length_word = payload_offset // 32
    payload_length = int(word(value, payload_length_word), 16)
    payload_start = 2 + (payload_offset + 32) * 2
    payload = bytes.fromhex(value[payload_start : payload_start + payload_length * 2])
    return effective_at, previous_head, event_hash, payload


def decode_event_type(topic: str) -> str:
    raw = bytes.fromhex(topic[2:]).rstrip(b"\0")
    try:
        return raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise SyncError("event type is not ASCII") from error


def decode_payload(payload: bytes) -> dict[str, Any]:
    try:
        text = payload.decode("utf-8")
        data = json.loads(text, object_pairs_hook=ledger.reject_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError, ledger.ValidationError) as error:
        raise SyncError(f"invalid canonical event payload: {error}") from error
    if ledger.canonical_payload(data) != payload:
        raise SyncError("event payload is not canonical JSON")
    return data


def fetch_block_metadata(rpc_url: str, block_number: int) -> tuple[int, str]:
    block = rpc(rpc_url, "eth_getBlockByNumber", [hex(block_number), False])
    if block is None:
        raise SyncError(f"block {block_number} was not found")
    return quantity(block["timestamp"]), block["hash"].lower()


def iso_timestamp(seconds: int) -> str:
    from datetime import datetime

    return datetime.fromtimestamp(seconds, ledger.SAN_FRANCISCO).isoformat(timespec="seconds")


def fetch_journal(
    rpc_url: str, chain_id: int, address: str, deployment_block: int
) -> tuple[list[dict[str, Any]], int, str]:
    latest = quantity(rpc(rpc_url, "eth_blockNumber", []))
    raw_logs: list[dict[str, Any]] = []
    for start in range(deployment_block, latest + 1, LOG_BLOCK_SPAN):
        end = min(start + LOG_BLOCK_SPAN - 1, latest)
        raw_logs.extend(
            rpc(
                rpc_url,
                "eth_getLogs",
                [
                    {
                        "address": address,
                        "fromBlock": hex(start),
                        "toBlock": hex(end),
                        "topics": [EVENT_TOPIC],
                    }
                ],
            )
        )
    raw_logs.sort(key=lambda item: (quantity(item["blockNumber"]), quantity(item["transactionIndex"]), quantity(item["logIndex"])))

    events: list[dict[str, Any]] = []
    prior = ZERO_HASH
    block_cache: dict[int, tuple[int, str]] = {}
    for index, raw in enumerate(raw_logs, start=1):
        topics = raw["topics"]
        if len(topics) != 3:
            raise SyncError(f"sequence {index} has an unexpected topic count")
        sequence = int(topics[1], 16)
        if sequence != index:
            raise SyncError(f"expected sequence {index}, found {sequence}")
        event_type = decode_event_type(topics[2])
        effective_at, previous_head, event_hash, payload = decode_data(raw["data"])
        if previous_head != prior:
            raise SyncError(f"sequence {sequence} previous head mismatch")
        data = decode_payload(payload)

        source_event = {
            "event_type": event_type,
            "effective_at": iso_timestamp(effective_at),
            "data": data,
        }

        payload_hash = run("cast", "keccak", "0x" + payload.hex()).lower()
        compiled = ledger.event_hash_preimage(
            chain_id,
            address,
            sequence,
            event_type,
            effective_at,
            payload_hash,
            previous_head,
        )
        calculated = run("cast", "keccak", compiled).lower()
        if calculated != event_hash:
            raise SyncError(f"sequence {sequence} event hash mismatch")

        block_number = quantity(raw["blockNumber"])
        if block_number not in block_cache:
            block_cache[block_number] = fetch_block_metadata(rpc_url, block_number)
        block_timestamp, block_hash = block_cache[block_number]
        events.append(
            {
                "sequence": sequence,
                **source_event,
                "previous_head": previous_head,
                "event_hash": event_hash,
                "payload_hash": payload_hash,
                "transaction_hash": raw["transactionHash"].lower(),
                "block_number": block_number,
                "block_hash": block_hash,
                "log_index": quantity(raw["logIndex"]),
                "published_at": iso_timestamp(block_timestamp),
            }
        )
        prior = event_hash

    return events, latest, prior


def source_journal(chain_id: int, address: str, events: list[dict[str, Any]], head: str) -> dict[str, Any]:
    return {
        "format": ledger.FORMAT,
        "format_version": ledger.FORMAT_VERSION,
        "chain_id": chain_id,
        "stock_contract": address,
        "expected_event_count": 0,
        "expected_head": ZERO_HASH,
        "events": [
            {
                "event_type": item["event_type"],
                "effective_at": item["effective_at"],
                "data": item["data"],
            }
            for item in events
        ],
        "observed_event_count": len(events),
        "observed_head": head,
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync(deployment_path: Path, rpc_url: str) -> None:
    deployment = json.loads(deployment_path.read_text(encoding="utf-8"))
    chain_id = int(run("cast", "chain-id", "--rpc-url", rpc_url))
    if chain_id != deployment["chain_id"]:
        raise SyncError("RPC chain ID does not match deployment metadata")
    address = deployment["stock_contract"]
    deployment_block = rpc(
        rpc_url,
        "eth_getBlockByNumber",
        [hex(deployment["deployment_block"]), False],
    )
    if deployment_block is None or deployment_block["hash"].lower() != deployment["block_hash"].lower():
        raise SyncError("deployment block hash does not match deployment metadata")
    if quantity(deployment_block["timestamp"]) != deployment["deployed_at_unix"]:
        raise SyncError("deployment timestamp does not match deployment metadata")
    deployment_receipt = rpc(
        rpc_url,
        "eth_getTransactionReceipt",
        [deployment["transaction_hash"]],
    )
    if (
        deployment_receipt is None
        or deployment_receipt["contractAddress"].lower() != address.lower()
        or quantity(deployment_receipt["blockNumber"]) != deployment["deployment_block"]
        or deployment_receipt["blockHash"].lower() != deployment["block_hash"].lower()
        or quantity(deployment_receipt["status"]) != 1
        or deployment_receipt["from"].lower() != deployment["deployer"].lower()
    ):
        raise SyncError("deployment transaction does not match deployment metadata")
    code = run("cast", "code", address, "--rpc-url", rpc_url)
    if code == "0x":
        raise SyncError("deployment address has no contract code")
    code_hash = run("cast", "keccak", code).lower()
    if code_hash != deployment["runtime_code_hash"].lower():
        raise SyncError("runtime code hash does not match deployment metadata")
    stock_name_output = run("cast", "call", address, "stockName()(string)", "--rpc-url", rpc_url)
    try:
        stock_name = json.loads(stock_name_output)
    except json.JSONDecodeError:
        stock_name = stock_name_output
    if stock_name != deployment["stock_name"]:
        raise SyncError("contract stock name does not match deployment metadata")
    controller = run("cast", "call", address, "controller()(address)", "--rpc-url", rpc_url)
    if controller.lower() != deployment["controller"].lower():
        raise SyncError("contract controller does not match deployment metadata")
    onchain_count = int(run("cast", "to-dec", run("cast", "call", address, "eventCount()(uint256)", "--rpc-url", rpc_url)))
    onchain_head = run("cast", "call", address, "head()(bytes32)", "--rpc-url", rpc_url).lower()
    events, latest, calculated_head = fetch_journal(
        rpc_url, chain_id, address, deployment["deployment_block"]
    )
    if len(events) != onchain_count:
        raise SyncError(f"contract count {onchain_count} does not match {len(events)} logs")
    if calculated_head != onchain_head:
        raise SyncError("contract head does not match verified journal head")

    output_dir = deployment_path.parent
    journal = {
        "format": "personal-stock-ledger-journal",
        "format_version": 1,
        "chain_id": chain_id,
        "stock_contract": address,
        "deployment_block": deployment["deployment_block"],
        "last_event_block": events[-1]["block_number"] if events else deployment["deployment_block"],
        "event_count": onchain_count,
        "head": onchain_head,
        "events": events,
    }
    write_json(output_dir / "journal.json", journal)

    if events:
        source = source_journal(chain_id, address, events, onchain_head)
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory) / "source-journal.json"
            write_json(
                temporary,
                {key: value for key, value in source.items() if not key.startswith("observed_")},
            )
            parsed = ledger.load_batch(temporary, allow_large_journal=True)
            effective = ledger.resolve_events(parsed.events)
            write_json(output_dir / "effective.json", [ledger.effective_json(item) for item in effective])
            write_json(output_dir / "state.json", ledger.replay(effective).as_json())
    else:
        write_json(output_dir / "effective.json", [])
        write_json(output_dir / "state.json", None)

    print(f"verified {onchain_count} events through block {latest}")
    print(f"head: {onchain_head}")
    print(f"wrote: {output_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deployment", type=Path)
    parser.add_argument("--rpc-url", required=True)
    args = parser.parse_args()
    try:
        sync(args.deployment, args.rpc_url)
        return 0
    except (OSError, KeyError, ValueError, SyncError, ledger.ValidationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
