#!/usr/bin/env python3
"""Verify StockLedger source through Sourcify API v2 and record the exact-match result."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SERVER = "https://sourcify.dev/server"
CONTRACT_IDENTIFIER = "src/StockLedger.sol:StockLedger"


class VerificationError(ValueError):
    pass


def request_json(url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise VerificationError(f"Sourcify HTTP {error.code}: {detail}") from error


def standard_json(ledger_dir: Path, chain_id: int, address: str) -> dict[str, Any]:
    environment = dict(os.environ)
    environment.setdefault("BASESCAN_API_KEY", "unused")
    process = subprocess.run(
        [
            "forge",
            "verify-contract",
            address,
            CONTRACT_IDENTIFIER,
            "--chain",
            str(chain_id),
            "--verifier",
            "sourcify",
            "--show-standard-json-input",
        ],
        cwd=ledger_dir,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode:
        raise VerificationError(process.stderr.strip() or process.stdout.strip())
    try:
        return json.loads(process.stdout)
    except json.JSONDecodeError as error:
        raise VerificationError("Foundry did not produce valid standard JSON input") from error


def compiler_version(ledger_dir: Path) -> str:
    artifact = ledger_dir / "out" / "StockLedger.sol" / "StockLedger.json"
    source = json.loads(artifact.read_text(encoding="utf-8"))
    return source["metadata"]["compiler"]["version"]


def exact_result(result: dict[str, Any]) -> bool:
    return (
        result.get("match") == "exact_match"
        and result.get("creationMatch") == "exact_match"
        and result.get("runtimeMatch") == "exact_match"
    )


def verify(deployment_path: Path) -> dict[str, Any]:
    deployment = json.loads(deployment_path.read_text(encoding="utf-8"))
    chain_id = deployment["chain_id"]
    address = deployment["stock_contract"]
    contract_url = f"{SERVER}/v2/contract/{chain_id}/{address}?fields=all"
    try:
        result = request_json(contract_url)
    except VerificationError as error:
        if "HTTP 404" not in str(error):
            raise
        result = {}

    if not exact_result(result):
        ledger_dir = Path(__file__).resolve().parents[1]
        payload = {
            "stdJsonInput": standard_json(ledger_dir, chain_id, address),
            "compilerVersion": compiler_version(ledger_dir),
            "contractIdentifier": CONTRACT_IDENTIFIER,
            "creationTransactionHash": deployment["transaction_hash"],
        }
        ticket = request_json(f"{SERVER}/v2/verify/{chain_id}/{address}", payload)
        verification_id = ticket.get("verificationId")
        if not verification_id:
            raise VerificationError(f"Sourcify rejected verification: {ticket}")
        for _ in range(60):
            job = request_json(f"{SERVER}/v2/verify/{verification_id}")
            if job.get("isJobCompleted"):
                result = job.get("contract") or {}
                break
            time.sleep(2)
        else:
            raise VerificationError("Sourcify verification did not finish within two minutes")

    if not exact_result(result):
        raise VerificationError(f"Sourcify did not report an exact match: {result}")
    proof = {
        "provider": "sourcify-v2",
        "match": result["match"],
        "creation_match": result["creationMatch"],
        "runtime_match": result["runtimeMatch"],
        "verified_at": result["verifiedAt"],
        "match_id": str(result["matchId"]),
        "url": f"https://repo.sourcify.dev/{chain_id}/{result.get('address', address)}",
    }
    deployment["source_verification"] = proof
    deployment_path.write_text(json.dumps(deployment, indent=2) + "\n", encoding="utf-8")
    return proof


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deployment", type=Path)
    args = parser.parse_args()
    try:
        proof = verify(args.deployment)
        print(f"source verification: {proof['match']} ({proof['url']})")
        return 0
    except (OSError, KeyError, ValueError, VerificationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
