import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


LEDGER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEDGER_ROOT / "script"))

import ledger_events as ledger
import preview_batch
import sync_ledger


ADDRESS = "0x1111111111111111111111111111111111111111"
ZERO_HASH = "0x" + "00" * 32


class OperationsTest(unittest.TestCase):
    def test_event_hash_preimage_matches_solidity_abi_encoding(self):
        payload_hash = "0x" + "22" * 32
        actual = ledger.event_hash_preimage(
            84532,
            ADDRESS,
            1,
            "FORMATION",
            1,
            123,
            payload_hash,
            ZERO_HASH,
        )
        expected = subprocess.check_output(
            [
                "cast",
                "abi-encode",
                "f(bytes32,uint256,address,uint256,bytes32,uint32,uint64,bytes32,bytes32)",
                ledger.EVENT_HASH_DOMAIN,
                "84532",
                ADDRESS,
                "1",
                ledger.event_type_bytes32("FORMATION"),
                "1",
                "123",
                payload_hash,
                ZERO_HASH,
            ],
            text=True,
        ).strip()
        self.assertEqual(actual, expected)

    def test_event_log_data_decoder(self):
        payload = b'{"owner":"holder_000000"}'
        previous = "0x" + "11" * 32
        event_hash = "0x" + "22" * 32
        encoded = subprocess.check_output(
            [
                "cast",
                "abi-encode",
                "f(uint64,bytes32,bytes32,bytes)",
                "123",
                previous,
                event_hash,
                "0x" + payload.hex(),
            ],
            text=True,
        ).strip()
        effective_at, decoded_previous, decoded_hash, decoded_payload = sync_ledger.decode_data(encoded)
        self.assertEqual(effective_at, 123)
        self.assertEqual(decoded_previous, previous)
        self.assertEqual(decoded_hash, event_hash)
        self.assertEqual(decoded_payload, payload)

    def test_empty_journal_formation_preview(self):
        journal = {
            "format": "personal-stock-ledger-journal",
            "format_version": 1,
            "chain_id": 84532,
            "stock_contract": ADDRESS,
            "deployment_block": 1,
            "observed_through_block": 1,
            "event_count": 0,
            "head": ZERO_HASH,
            "events": [],
        }
        batch = {
            "format": ledger.FORMAT,
            "format_version": ledger.FORMAT_VERSION,
            "chain_id": 84532,
            "stock_contract": ADDRESS,
            "expected_event_count": 0,
            "expected_head": ZERO_HASH,
            "events": [
                {
                    "event_type": "FORMATION",
                    "schema_version": 1,
                    "effective_at": "2026-08-01T00:00:00Z",
                    "data": {
                        "owner_shareholder_id": "holder_000000",
                        "owner_display_name": "Test Owner",
                        "owner_handle": None,
                    },
                },
                {
                    "event_type": "AGREEMENT_ADOPTION",
                    "schema_version": 1,
                    "effective_at": "2026-08-01T00:00:01Z",
                    "data": {
                        "shareholder_id": "holder_000000",
                        "agreement_version": "1.0.0",
                        "agreement_content_hash": "0x" + "aa" * 32,
                    },
                },
                {
                    "event_type": "PORTFOLIO_COMMENCEMENT",
                    "schema_version": 1,
                    "effective_at": "2026-08-01T00:00:02Z",
                    "data": {
                        "opening_portfolio_net_gain_usd": "0",
                        "opening_item_count": 0,
                        "cpi_2026_06": "1",
                    },
                },
                {
                    "event_type": "SHARE_ISSUANCE",
                    "schema_version": 1,
                    "effective_at": "2026-08-01T00:00:02Z",
                    "data": {
                        "recipient_shareholder_id": "holder_000000",
                        "shares": 100,
                        "actual_cash_paid_usd": "0",
                    },
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            journal_path = Path(directory) / "journal.json"
            batch_path = Path(directory) / "batch.json"
            journal_path.write_text(json.dumps(journal), encoding="utf-8")
            batch_path.write_text(json.dumps(batch), encoding="utf-8")
            result = preview_batch.preview(journal_path, batch_path)
        self.assertEqual(result["after"]["event_count"], 4)
        self.assertEqual(result["after"]["state"]["outstanding"], 100)
        self.assertEqual(result["proposed_events"][-1]["sequence"], 4)
        self.assertEqual(result["after"]["head"], result["proposed_events"][-1]["event_hash"])

    def test_preview_rejects_partial_formation(self):
        journal = {
            "format": "personal-stock-ledger-journal",
            "format_version": 1,
            "chain_id": 84532,
            "stock_contract": ADDRESS,
            "event_count": 0,
            "head": ZERO_HASH,
            "events": [],
        }
        batch = {
            "format": ledger.FORMAT,
            "format_version": ledger.FORMAT_VERSION,
            "chain_id": 84532,
            "stock_contract": ADDRESS,
            "expected_event_count": 0,
            "expected_head": ZERO_HASH,
            "events": [
                {
                    "event_type": "FORMATION",
                    "schema_version": 1,
                    "effective_at": "2026-08-01T00:00:00Z",
                    "data": {
                        "owner_shareholder_id": "holder_000000",
                        "owner_display_name": "Test Owner",
                        "owner_handle": None,
                    },
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            journal_path = Path(directory) / "journal.json"
            batch_path = Path(directory) / "batch.json"
            journal_path.write_text(json.dumps(journal), encoding="utf-8")
            batch_path.write_text(json.dumps(batch), encoding="utf-8")
            with self.assertRaisesRegex(ledger.ValidationError, "owner agreement adoption"):
                preview_batch.preview(journal_path, batch_path)


if __name__ == "__main__":
    unittest.main()
