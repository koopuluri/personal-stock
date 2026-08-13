import json
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path


LEDGER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEDGER_ROOT / "script"))

import ledger_events as ledger


AGREEMENT_HASH = "0x" + "aa" * 32
SCHEMA_HASH = ledger.SCHEMA_HASHES["1.0.0"]
STOCK_ADDRESS = "0x" + "11" * 20
ZERO_HASH = "0x" + "00" * 32


def event(event_type, effective_at, data):
    return {"event_type": event_type, "effective_at": effective_at, "data": data}


def configuration():
    return {
        "floor_base_amount_usd": "10000000",
        "floor_cpi_series": "CUUR0000SA0",
        "floor_cpi_base_period": "2026-06",
        "floor_cpi_base_value": "333.952",
        "authorized_shares": 12000000,
        "royalty_rate": "0.05",
        "amendment_approval_threshold": "0.75",
    }


def base_events(shares=100):
    return [
        event(
            "SCHEMA",
            "2026-08-01T00:00:00-07:00",
            {"version": "1.0.0", "content_hash": SCHEMA_HASH},
        ),
        event(
            "FORMATION",
            "2026-08-01T00:00:01-07:00",
            {
                "owner_shareholder_id": "holder_000000",
                "owner_display_name": "Karthik Uppuluri",
                "owner_handle": "@koopuluri",
            },
        ),
        event(
            "AGREEMENT_ADOPTION",
            "2026-08-01T00:01:00-07:00",
            {
                "shareholder_id": "holder_000000",
                "agreement_version": "1.0.0",
                "agreement_content_hash": AGREEMENT_HASH,
            },
        ),
        event("AGREEMENT_CONFIGURATION", "2026-08-01T00:01:01-07:00", configuration()),
        event(
            "PORTFOLIO_COMMENCEMENT",
            "2026-08-01T00:02:00-07:00",
            {"opening_portfolio_net_gain_usd": "0", "opening_item_count": 0},
        ),
        event(
            "SHARE_ISSUANCE",
            "2026-08-01T00:02:00-07:00",
            {
                "recipient_shareholder_id": "holder_000000",
                "shares": shares,
                "actual_cash_paid_usd": "0",
            },
        ),
    ]


def batch(events, expected_count=0, expected_head=ZERO_HASH):
    return {
        "format": "personal-stock-ledger-batch",
        "format_version": 1,
        "chain_id": 8453,
        "stock_contract": STOCK_ADDRESS,
        "expected_event_count": expected_count,
        "expected_head": expected_head,
        "events": events,
    }


class LedgerEventsTest(unittest.TestCase):
    def load(self, source, *, initial_schema=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "batch.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            return ledger.load_batch(path, initial_schema=initial_schema)

    def full_state(self, events):
        parsed = self.load(batch(events))
        return ledger.replay(ledger.resolve_events(parsed.events))

    def test_schema_hash_constant_matches_canonical_file(self):
        actual = "0x" + hashlib.sha256((LEDGER_ROOT / "schema.md").read_bytes()).hexdigest()
        self.assertEqual(actual, SCHEMA_HASH)

    def test_valid_formation_and_issuance_replay(self):
        state = self.full_state(base_events())
        self.assertEqual(state.schema_version, "1.0.0")
        self.assertEqual(state.owner_id, "holder_000000")
        self.assertEqual(state.outstanding, 100)
        self.assertEqual(state.agreement_configuration["floor_cpi_base_value"], "333.952")

    def test_source_timestamp_is_san_francisco_time(self):
        _, seconds = ledger.expect_timestamp(
            "2026-08-12T21:00:00-07:00", "timestamp"
        )
        self.assertEqual(seconds, 1786593600)
        with self.assertRaisesRegex(ledger.ValidationError, "San Francisco"):
            ledger.expect_timestamp("2026-08-12T21:00:00-08:00", "timestamp")

    def test_initial_schema_and_formation_order_are_required(self):
        with self.assertRaisesRegex(ledger.ValidationError, "first ledger event must be SCHEMA"):
            self.load(batch(base_events()[1:]))
        events = base_events()
        events[1], events[2] = events[2], events[1]
        with self.assertRaisesRegex(ledger.ValidationError, "FORMATION must immediately follow"):
            self.load(batch(events))

    def test_compile_uses_simple_envelopes_and_canonical_payloads(self):
        parsed = self.load(batch(base_events()))
        compiled = ledger.compile_batch(parsed)
        self.assertEqual(compiled["event_count"], 6)
        self.assertNotIn("schema_version", compiled["events"][0])
        self.assertEqual(
            compiled["events"][0]["event_type"],
            "0x" + b"SCHEMA".hex().ljust(64, "0"),
        )
        payload = bytes.fromhex(compiled["events"][0]["payload"][2:]).decode()
        self.assertEqual(
            payload,
            json.dumps(base_events()[0]["data"], sort_keys=True, separators=(",", ":")),
        )

    def test_initial_configuration_must_be_complete(self):
        events = base_events()
        del events[3]["data"]["royalty_rate"]
        with self.assertRaisesRegex(ledger.ValidationError, "initial configuration must set every"):
            self.full_state(events)

    def test_floor_configuration_is_an_atomic_group(self):
        events = base_events()
        del events[3]["data"]["floor_cpi_base_value"]
        with self.assertRaisesRegex(ledger.ValidationError, "complete floor configuration"):
            self.load(batch(events))

    def test_configuration_values_are_exact_and_bounded(self):
        events = base_events()
        events[3]["data"]["royalty_rate"] = 0.05
        with self.assertRaisesRegex(ledger.ValidationError, "binary floating-point"):
            self.load(batch(events))
        events = base_events()
        events[3]["data"]["amendment_approval_threshold"] = "1.01"
        with self.assertRaisesRegex(ledger.ValidationError, "must not exceed 1"):
            self.load(batch(events))

    def test_owner_opening_issuance_is_effective_at_commencement(self):
        events = base_events()
        events[-1]["effective_at"] = "2026-08-01T00:03:00-07:00"
        with self.assertRaisesRegex(ledger.ValidationError, "effective at commencement"):
            self.full_state(events)

    def test_authorized_shares_come_from_configuration(self):
        events = base_events(shares=101)
        events[3]["data"]["authorized_shares"] = 100
        with self.assertRaisesRegex(ledger.ValidationError, "authorized share count exceeded"):
            self.full_state(events)

    def test_opening_items_determine_commencement_balance(self):
        events = base_events()
        opening = [
            event(
                "ASSET_REGISTERED",
                "2026-08-01T00:01:10-07:00",
                {
                    "asset_id": "asset_000001",
                    "asset_category": "private equity",
                    "description": None,
                    "acquired_at": "2024-01-01T00:00:00-08:00",
                    "opening_asset": True,
                },
            ),
            event(
                "OPENING_PORTFOLIO_ITEM",
                "2026-08-01T00:01:20-07:00",
                {
                    "asset_id": "asset_000001",
                    "item_type": "ELIGIBLE_COST",
                    "amount_usd": "100",
                    "occurred_at": "2024-01-01T00:00:00-08:00",
                },
            ),
            event(
                "OPENING_PORTFOLIO_ITEM",
                "2026-08-01T00:01:30-07:00",
                {
                    "asset_id": "asset_000001",
                    "item_type": "CASH_EVENT",
                    "amount_usd": "40",
                    "occurred_at": "2025-01-01T00:00:00-08:00",
                },
            ),
        ]
        events[4:4] = opening
        events[7]["data"]["opening_portfolio_net_gain_usd"] = "-60"
        events[7]["data"]["opening_item_count"] = 2
        state = self.full_state(events)
        self.assertEqual(state.portfolio_net_gain_usd, "-60")
        self.assertEqual(len(state.assets), 1)

    def test_shareholder_must_adopt_governing_agreement(self):
        events = base_events()
        events[4:4] = [
            event(
                "SHAREHOLDER_REGISTERED",
                "2026-08-01T00:01:10-07:00",
                {"shareholder_id": "holder_000001", "display_name": "Second", "handle": None},
            ),
            event(
                "AGREEMENT_ADOPTION",
                "2026-08-01T00:01:20-07:00",
                {
                    "shareholder_id": "holder_000001",
                    "agreement_version": "1.0.1",
                    "agreement_content_hash": "0x" + "bb" * 32,
                },
            ),
        ]
        with self.assertRaisesRegex(ledger.ValidationError, "did not adopt"):
            self.full_state(events)

    def test_supplement_enriches_old_event_under_active_schema(self):
        events = base_events()
        events.append(
            event(
                "EVENT_SUPPLEMENT",
                "2026-08-02T00:00:00-07:00",
                {
                    "target_sequence": 6,
                    "extension_type": "ISSUANCE_PROVENANCE",
                    "extension_data": {"private_record": "record-17"},
                    "reason": "Backfilled from private records.",
                },
            )
        )
        effective = ledger.resolve_events(self.load(batch(events)).events)
        issuance = next(item for item in effective if item.logical_sequence == 6)
        supplement = issuance.supplements["ISSUANCE_PROVENANCE"]
        self.assertEqual(supplement["schema_version"], "1.0.0")
        self.assertEqual(supplement["data"]["private_record"], "record-17")

    def test_revision_replaces_old_event_without_rewriting_it(self):
        events = base_events()
        replacement = event(
            "SHARE_ISSUANCE",
            "2026-08-01T00:02:00-07:00",
            {
                "recipient_shareholder_id": "holder_000000",
                "shares": 90,
                "actual_cash_paid_usd": "0",
            },
        )
        events.append(
            event(
                "EVENT_REVISION",
                "2026-08-02T00:00:00-07:00",
                {"target_sequence": 6, "replacement": replacement, "reason": "Correction."},
            )
        )
        self.assertEqual(self.full_state(events).outstanding, 90)

    def test_second_revision_must_supersede_active_revision(self):
        events = base_events()
        replacement = event(
            "SHARE_ISSUANCE",
            "2026-08-01T00:02:00-07:00",
            {
                "recipient_shareholder_id": "holder_000000",
                "shares": 90,
                "actual_cash_paid_usd": "0",
            },
        )
        events.extend(
            [
                event(
                    "EVENT_REVISION",
                    "2026-08-02T00:00:00-07:00",
                    {"target_sequence": 6, "replacement": replacement, "reason": "First."},
                ),
                event(
                    "EVENT_REVISION",
                    "2026-08-03T00:00:00-07:00",
                    {"target_sequence": 6, "replacement": replacement, "reason": "Second."},
                ),
            ]
        )
        with self.assertRaisesRegex(ledger.ValidationError, "must supersede"):
            self.load(batch(events))
        events[-1]["data"]["supersedes_sequence"] = 7
        self.assertEqual(self.full_state(events).outstanding, 90)

    def test_incremental_supplement_uses_active_global_schema(self):
        source = batch(
            [
                event(
                    "EVENT_SUPPLEMENT",
                    "2026-08-02T00:00:00-07:00",
                    {
                        "target_sequence": 6,
                        "extension_type": "ISSUANCE_PROVENANCE",
                        "extension_data": {"private_record": "record-1"},
                        "reason": "Historical backfill.",
                    },
                )
            ],
            expected_count=6,
            expected_head="0x" + "bb" * 32,
        )
        parsed = self.load(source, initial_schema=("1.0.0", SCHEMA_HASH))
        self.assertEqual(parsed.events[0].sequence, 7)
        self.assertEqual(parsed.events[0].schema_version, "1.0.0")


if __name__ == "__main__":
    unittest.main()
