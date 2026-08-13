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
SCHEMA_HASH = ledger.SCHEMA_HASHES["1.0.0"]
AGREEMENT_HASH = "0x" + "aa" * 32


def source_event(event_type, effective_at, data):
    return {"event_type": event_type, "effective_at": effective_at, "data": data}


def complete_formation():
    configuration = {
        "floor_base_amount_usd": "10000000",
        "floor_cpi_series": "CUUR0000SA0",
        "floor_cpi_base_period": "2026-06",
        "floor_cpi_base_value": "333.952",
        "authorized_shares": 12000000,
        "royalty_rate": "0.05",
        "amendment_approval_threshold": "0.75",
    }
    return [
        source_event(
            "SCHEMA",
            "2026-08-01T00:00:00-07:00",
            {"version": "1.0.0", "content_hash": SCHEMA_HASH},
        ),
        source_event(
            "FORMATION",
            "2026-08-01T00:00:01-07:00",
            {
                "owner_shareholder_id": "holder_000000",
                "owner_display_name": "Test Owner",
                "owner_handle": None,
            },
        ),
        source_event(
            "AGREEMENT_ADOPTION",
            "2026-08-01T00:00:02-07:00",
            {
                "shareholder_id": "holder_000000",
                "agreement_version": "1.0.0",
                "agreement_content_hash": AGREEMENT_HASH,
            },
        ),
        source_event(
            "AGREEMENT_CONFIGURATION",
            "2026-08-01T00:00:03-07:00",
            configuration,
        ),
        source_event(
            "PORTFOLIO_COMMENCEMENT",
            "2026-08-01T00:00:04-07:00",
            {"opening_portfolio_net_gain_usd": "0", "opening_item_count": 0},
        ),
        source_event(
            "SHARE_ISSUANCE",
            "2026-08-01T00:00:04-07:00",
            {
                "recipient_shareholder_id": "holder_000000",
                "shares": 100,
                "actual_cash_paid_usd": "0",
            },
        ),
    ]


def empty_journal():
    return {
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


def batch(events, expected_count=0, expected_head=ZERO_HASH):
    return {
        "format": ledger.FORMAT,
        "format_version": ledger.FORMAT_VERSION,
        "chain_id": 84532,
        "stock_contract": ADDRESS,
        "expected_event_count": expected_count,
        "expected_head": expected_head,
        "events": events,
    }


class OperationsTest(unittest.TestCase):
    def test_event_hash_preimage_matches_solidity_abi_encoding(self):
        payload_hash = "0x" + "22" * 32
        actual = ledger.event_hash_preimage(
            84532,
            ADDRESS,
            1,
            "FORMATION",
            123,
            payload_hash,
            ZERO_HASH,
        )
        expected = subprocess.check_output(
            [
                "cast",
                "abi-encode",
                "f(bytes32,uint256,address,uint256,bytes32,uint64,bytes32,bytes32)",
                ledger.EVENT_HASH_DOMAIN,
                "84532",
                ADDRESS,
                "1",
                ledger.event_type_bytes32("FORMATION"),
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
        with tempfile.TemporaryDirectory() as directory:
            journal_path = Path(directory) / "journal.json"
            batch_path = Path(directory) / "batch.json"
            journal_path.write_text(json.dumps(empty_journal()), encoding="utf-8")
            batch_path.write_text(json.dumps(batch(complete_formation())), encoding="utf-8")
            result = preview_batch.preview(journal_path, batch_path)
        self.assertEqual(result["after"]["event_count"], 6)
        self.assertEqual(result["after"]["state"]["outstanding"], 100)
        self.assertEqual(result["proposed_events"][-1]["sequence"], 6)
        self.assertEqual(result["after"]["head"], result["proposed_events"][-1]["event_hash"])

    def test_preview_rejects_partial_formation(self):
        events = complete_formation()[:2]
        with tempfile.TemporaryDirectory() as directory:
            journal_path = Path(directory) / "journal.json"
            batch_path = Path(directory) / "batch.json"
            journal_path.write_text(json.dumps(empty_journal()), encoding="utf-8")
            batch_path.write_text(json.dumps(batch(events)), encoding="utf-8")
            with self.assertRaisesRegex(ledger.ValidationError, "owner agreement adoption"):
                preview_batch.preview(journal_path, batch_path)

    def test_incremental_batch_requires_verified_active_schema(self):
        increment = batch(
            [
                source_event(
                    "EVENT_SUPPLEMENT",
                    "2026-08-02T00:00:00-07:00",
                    {
                        "target_sequence": 6,
                        "extension_type": "ISSUANCE_PROVENANCE",
                        "extension_data": {"record": "private-1"},
                        "reason": "Backfill.",
                    },
                )
            ],
            expected_count=6,
            expected_head="0x" + "bb" * 32,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "batch.json"
            path.write_text(json.dumps(increment), encoding="utf-8")
            with self.assertRaisesRegex(ledger.ValidationError, "no active schema"):
                ledger.load_batch(path)


if __name__ == "__main__":
    unittest.main()
