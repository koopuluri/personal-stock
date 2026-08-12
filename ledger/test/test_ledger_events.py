import json
import sys
import tempfile
import unittest
from pathlib import Path


LEDGER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEDGER_ROOT / "script"))

import ledger_events as ledger


AGREEMENT_HASH = "0x" + "aa" * 32
STOCK_ADDRESS = "0x" + "11" * 20
ZERO_HASH = "0x" + "00" * 32


def event(event_type, effective_at, data, schema_version=1):
    return {
        "event_type": event_type,
        "schema_version": schema_version,
        "effective_at": effective_at,
        "data": data,
    }


def base_events(shares=100):
    return [
        event(
            "FORMATION",
            "2026-08-01T00:00:00Z",
            {
                "owner_shareholder_id": "holder_000000",
                "owner_display_name": "Karthik Uppuluri",
                "owner_handle": "@koopuluri",
            },
        ),
        event(
            "AGREEMENT_ADOPTION",
            "2026-08-01T00:01:00Z",
            {
                "shareholder_id": "holder_000000",
                "agreement_version": "1.0.0",
                "agreement_content_hash": AGREEMENT_HASH,
            },
        ),
        event(
            "SHARE_ISSUANCE",
            "2026-08-01T00:02:00Z",
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
    def load(self, source):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "batch.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            return ledger.load_batch(path)

    def full_state(self, events):
        parsed = self.load(batch(events))
        return ledger.replay(ledger.resolve_events(parsed.events))

    def test_valid_formation_and_issuance_replay(self):
        state = self.full_state(base_events())
        self.assertEqual(state.owner_id, "holder_000000")
        self.assertEqual(state.outstanding, 100)
        self.assertEqual(state.balances["holder_000000"], 100)

    def test_compile_uses_event_envelopes_and_canonical_payloads(self):
        parsed = self.load(batch(base_events()))
        compiled = ledger.compile_batch(parsed)
        self.assertEqual(compiled["event_count"], 3)
        self.assertEqual(
            compiled["events"][0]["event_type"],
            "0x" + b"FORMATION".hex().ljust(64, "0"),
        )
        payload = bytes.fromhex(compiled["events"][0]["payload"][2:]).decode()
        self.assertEqual(payload, json.dumps(base_events()[0]["data"], sort_keys=True, separators=(",", ":")))

    def test_unknown_field_is_rejected(self):
        events = base_events()
        events[-1]["data"]["unexpected"] = True
        with self.assertRaisesRegex(ledger.ValidationError, "unknown fields"):
            self.load(batch(events))

    def test_binary_float_is_rejected(self):
        events = base_events()
        events[-1]["data"]["actual_cash_paid_usd"] = 1.5
        with self.assertRaisesRegex(ledger.ValidationError, "binary floating-point"):
            self.load(batch(events))

    def test_agreement_version_requires_three_numeric_parts(self):
        events = base_events()
        events[1]["data"]["agreement_version"] = "1.0"
        with self.assertRaisesRegex(ledger.ValidationError, "agreement_version"):
            self.load(batch(events))

    def test_additive_supplement_enriches_without_replacing(self):
        events = base_events()
        events.append(
            event(
                "EVENT_SUPPLEMENT",
                "2026-08-02T00:00:00Z",
                {
                    "target_sequence": 3,
                    "extension_type": "ISSUANCE_PROVENANCE",
                    "extension_schema_version": 1,
                    "extension_data": {
                        "authorization_record": "private-record-17",
                        "authorization_date": "2026-07-31",
                    },
                    "reason": "Backfilled from private records.",
                },
            )
        )
        parsed = self.load(batch(events))
        effective = ledger.resolve_events(parsed.events)
        issuance = next(item for item in effective if item.logical_sequence == 3)
        self.assertEqual(issuance.data["shares"], 100)
        self.assertEqual(
            issuance.supplements["ISSUANCE_PROVENANCE"]["data"]["authorization_record"],
            "private-record-17",
        )

    def test_revision_replaces_old_event_and_replays_from_its_position(self):
        events = base_events()
        events.append(
            event(
                "EVENT_REVISION",
                "2026-08-02T00:00:00Z",
                {
                    "target_sequence": 3,
                    "replacement": event(
                        "SHARE_ISSUANCE",
                        "2026-08-01T00:02:00Z",
                        {
                            "recipient_shareholder_id": "holder_000000",
                            "shares": 90,
                            "actual_cash_paid_usd": "0",
                        },
                    ),
                    "reason": "Corrected executed quantity.",
                },
            )
        )
        state = self.full_state(events)
        self.assertEqual(state.outstanding, 90)

    def test_second_revision_must_supersede_active_revision(self):
        events = base_events()
        replacement = event(
            "SHARE_ISSUANCE",
            "2026-08-01T00:02:00Z",
            {
                "recipient_shareholder_id": "holder_000000",
                "shares": 90,
                "actual_cash_paid_usd": "0",
            },
        )
        events.append(
            event(
                "EVENT_REVISION",
                "2026-08-02T00:00:00Z",
                {"target_sequence": 3, "replacement": replacement, "reason": "First correction."},
            )
        )
        events.append(
            event(
                "EVENT_REVISION",
                "2026-08-03T00:00:00Z",
                {"target_sequence": 3, "replacement": replacement, "reason": "Second correction."},
            )
        )
        with self.assertRaisesRegex(ledger.ValidationError, "must supersede"):
            self.load(batch(events))

        events[-1]["data"]["supersedes_sequence"] = 4
        self.assertEqual(self.full_state(events).outstanding, 90)

    def test_revision_can_correct_an_events_chronological_position(self):
        events = base_events()
        events.extend(
            [
                event(
                    "SHAREHOLDER_REGISTERED",
                    "2026-08-01T00:04:00Z",
                    {"shareholder_id": "holder_000001", "display_name": "First", "handle": None},
                ),
                event(
                    "SHAREHOLDER_REGISTERED",
                    "2026-08-01T00:05:00Z",
                    {"shareholder_id": "holder_000002", "display_name": "Second", "handle": None},
                ),
                event(
                    "EVENT_REVISION",
                    "2026-08-02T00:00:00Z",
                    {
                        "target_sequence": 5,
                        "after_sequence": 3,
                        "replacement": event(
                            "SHAREHOLDER_REGISTERED",
                            "2026-08-01T00:03:00Z",
                            {
                                "shareholder_id": "holder_000002",
                                "display_name": "Second",
                                "handle": None,
                            },
                        ),
                        "reason": "Corrected the registration time.",
                    },
                ),
            ]
        )
        parsed = self.load(batch(events))
        effective = ledger.resolve_events(parsed.events)
        self.assertEqual([item.logical_sequence for item in effective], [1, 2, 3, 5, 4])
        state = ledger.replay(effective)
        self.assertIn("holder_000001", state.profiles)
        self.assertIn("holder_000002", state.profiles)

    def test_void_removes_effect_but_not_audit_record(self):
        events = base_events()
        events.append(
            event(
                "EVENT_VOID",
                "2026-08-02T00:00:00Z",
                {"target_sequence": 3, "reason": "Issuance never settled."},
            )
        )
        parsed = self.load(batch(events))
        effective = ledger.resolve_events(parsed.events)
        self.assertNotIn(3, [item.logical_sequence for item in effective])
        self.assertEqual(ledger.replay(effective).outstanding, 0)

    def test_insertion_places_an_omitted_event_in_historical_order(self):
        events = base_events()
        events.append(
            event(
                "EVENT_INSERTION",
                "2026-08-02T00:00:00Z",
                {
                    "after_sequence": 1,
                    "inserted": event(
                        "SHAREHOLDER_REGISTERED",
                        "2026-08-01T00:00:30Z",
                        {
                            "shareholder_id": "holder_000001",
                            "display_name": "Historical holder",
                            "handle": None,
                        },
                    ),
                    "reason": "Registration was omitted from the public history.",
                },
            )
        )
        parsed = self.load(batch(events))
        effective = ledger.resolve_events(parsed.events)
        self.assertEqual([item.logical_sequence for item in effective], [1, 4, 2, 3])
        self.assertIn("holder_000001", ledger.replay(effective).profiles)

    def test_incremental_batch_accepts_references_to_prior_chain_events(self):
        source = batch(
            [
                event(
                    "EVENT_SUPPLEMENT",
                    "2026-08-02T00:00:00Z",
                    {
                        "target_sequence": 3,
                        "extension_type": "ISSUANCE_PROVENANCE",
                        "extension_schema_version": 1,
                        "extension_data": {"private_record": "record-1"},
                        "reason": "Historical backfill.",
                    },
                )
            ],
            expected_count=3,
            expected_head="0x" + "bb" * 32,
        )
        parsed = self.load(source)
        self.assertEqual(parsed.events[0].sequence, 4)

    def test_initial_batch_requires_formation(self):
        with self.assertRaisesRegex(ledger.ValidationError, "first ledger event"):
            self.load(batch(base_events()[1:]))


if __name__ == "__main__":
    unittest.main()
