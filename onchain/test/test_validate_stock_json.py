import json
import sys
import tempfile
import unittest
from pathlib import Path


ONCHAIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ONCHAIN_ROOT.parent
sys.path.insert(0, str(ONCHAIN_ROOT / "script"))

import validate_stock_json as validator


AGREEMENT_HASH = "0x" + "aa" * 32
STOCK_ADDRESS = "0x" + "11" * 20
AGREEMENT_ADDRESS = "0x" + "22" * 20


def header(update=None):
    return {
        "document_type": "personal_stock",
        "schema_version": 1,
        "chain_id": 8453,
        "stock_contract": STOCK_ADDRESS,
        "agreement_contract": AGREEMENT_ADDRESS,
        "owner": {
            "shareholder_id": "holder_000000",
            "display_name": "Karthik Uppuluri",
            "handle": "@koopuluri",
        },
        "update": update
        or {
            "type": "INITIAL",
            "previous_content_hash": None,
            "summary": "Initial publication.",
        },
    }


def base_events():
    return [
        {
            "event_id": "event_000001",
            "timestamp": "2026-08-01T00:00:00Z",
            "event_type": "FORMATION",
        },
        {
            "event_id": "event_000002",
            "timestamp": "2026-08-01T00:01:00Z",
            "event_type": "AGREEMENT_VERSION_ISSUED",
            "agreement_version": "1.0",
            "agreement_content_hash": AGREEMENT_HASH,
        },
        {
            "event_id": "event_000003",
            "timestamp": "2026-08-01T00:02:00Z",
            "event_type": "AGREEMENT_ADOPTION",
            "shareholder_id": "holder_000000",
            "agreement_version": "1.0",
            "agreement_content_hash": AGREEMENT_HASH,
        },
        {
            "event_id": "event_000004",
            "timestamp": "2026-08-01T00:03:00Z",
            "event_type": "TRANSFER_POLICY_SET",
            "policy_code": "OWNER_APPROVAL_REQUIRED",
            "policy": "Voluntary transfers require owner permission.",
        },
        {
            "event_id": "event_000005",
            "timestamp": "2026-08-01T00:04:00Z",
            "event_type": "SHARE_ISSUANCE",
            "recipient_shareholder_id": "holder_000000",
            "shares": 100,
            "recorded_transaction_price_usd_per_share": "1.00",
        },
    ]


def markdown(metadata, events):
    return (
        "# Test Stock\n\n```json\n"
        + json.dumps(metadata, indent=2)
        + "\n```\n\n```json\n"
        + json.dumps(events, indent=2)
        + "\n```\n"
    )


class ValidatorTest(unittest.TestCase):
    def write_document(self, directory, name, metadata, events):
        path = Path(directory) / name
        path.write_text(markdown(metadata, events), encoding="utf-8")
        return path

    def validate(self, metadata, events):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_document(directory, "stock.md", metadata, events)
            return validator.validate_document(validator.load_document(path), draft=False)

    def test_valid_initial_ledger_replays(self):
        state = self.validate(header(), base_events())
        self.assertEqual(state.outstanding, 100)
        self.assertEqual(state.balances["holder_000000"], 100)
        self.assertEqual(state.benchmark_price(), validator.Fraction(1))

    def test_first_recipient_must_adopt_latest_agreement(self):
        events = [event for event in base_events() if event["event_type"] != "AGREEMENT_ADOPTION"]
        for index, event in enumerate(events, start=1):
            event["event_id"] = f"event_{index:06d}"
        with self.assertRaisesRegex(validator.ValidationError, "has not adopted the latest agreement"):
            self.validate(header(), events)

    def test_unknown_event_field_is_rejected(self):
        events = base_events()
        events[-1]["unexpected"] = True
        with self.assertRaisesRegex(validator.ValidationError, "unknown fields"):
            self.validate(header(), events)

    def test_correction_replaces_event_and_replays_history(self):
        events = base_events()
        events.append(
            {
                "event_id": "event_000006",
                "timestamp": "2026-08-01T00:05:00Z",
                "event_type": "CORRECTION",
                "target_event_id": "event_000005",
                "operation": "REPLACE",
                "reason": "Corrected the issued quantity.",
                "replacement_event": {
                    "timestamp": "2026-08-01T00:04:00Z",
                    "event_type": "SHARE_ISSUANCE",
                    "recipient_shareholder_id": "holder_000000",
                    "shares": 90,
                    "recorded_transaction_price_usd_per_share": "1.00",
                },
            }
        )
        metadata = header(
            {
                "type": "CORRECTION",
                "previous_content_hash": "0x" + "bb" * 32,
                "summary": "Corrected event_000005.",
                "correction_event_ids": ["event_000006"],
            }
        )
        state = self.validate(metadata, events)
        self.assertEqual(state.outstanding, 90)

    def test_royalty_is_calculated_from_sale_history(self):
        events = base_events()
        events.extend(
            [
                {
                    "event_id": "event_000006",
                    "timestamp": "2026-08-01T00:05:00Z",
                    "event_type": "SHAREHOLDER_REGISTERED",
                    "shareholder_id": "holder_000001",
                    "display_name": "Seller",
                    "handle": "@seller",
                },
                {
                    "event_id": "event_000007",
                    "timestamp": "2026-08-01T00:06:00Z",
                    "event_type": "AGREEMENT_ADOPTION",
                    "shareholder_id": "holder_000001",
                    "agreement_version": "1.0",
                    "agreement_content_hash": AGREEMENT_HASH,
                },
                {
                    "event_id": "event_000008",
                    "timestamp": "2026-08-01T00:07:00Z",
                    "event_type": "SHARE_ISSUANCE",
                    "recipient_shareholder_id": "holder_000001",
                    "shares": 200,
                    "recorded_transaction_price_usd_per_share": "1.00",
                },
                {
                    "event_id": "event_000009",
                    "timestamp": "2026-08-01T00:08:00Z",
                    "event_type": "TRANSFER_PERMISSION_GRANTED",
                    "seller_shareholder_id": "holder_000001",
                    "recipient_shareholder_id": "holder_000000",
                    "maximum_shares": 100,
                    "expires_at": None,
                    "irrevocable": False,
                },
                {
                    "event_id": "event_000010",
                    "timestamp": "2026-08-01T00:09:00Z",
                    "event_type": "VOLUNTARY_SALE",
                    "seller_shareholder_id": "holder_000001",
                    "buyer_shareholder_id": "holder_000000",
                    "buyer_shares": 100,
                    "sale_price_usd_per_share": "100",
                    "royalty_shares": 4,
                    "permission_basis": "SPECIFIC_PERMISSION",
                    "permission_event_id": "event_000009",
                },
            ]
        )
        state = self.validate(header(), events)
        self.assertEqual(state.balances["holder_000001"], 96)
        self.assertEqual(state.balances["holder_000000"], 204)

        events[-1]["royalty_shares"] = 3
        with self.assertRaisesRegex(validator.ValidationError, "royalty_shares must be 4"):
            self.validate(header(), events)

    def test_realizations_drive_reinvestment_and_distribution(self):
        events = base_events()
        events.extend(
            [
                {
                    "event_id": "event_000006",
                    "timestamp": "2026-08-01T00:05:00Z",
                    "event_type": "SHAREHOLDER_REGISTERED",
                    "shareholder_id": "holder_000001",
                    "display_name": "Investor",
                    "handle": "@investor",
                },
                {
                    "event_id": "event_000007",
                    "timestamp": "2026-08-01T00:06:00Z",
                    "event_type": "AGREEMENT_ADOPTION",
                    "shareholder_id": "holder_000001",
                    "agreement_version": "1.0",
                    "agreement_content_hash": AGREEMENT_HASH,
                },
                {
                    "event_id": "event_000008",
                    "timestamp": "2026-08-01T00:07:00Z",
                    "event_type": "SHARE_ISSUANCE",
                    "recipient_shareholder_id": "holder_000001",
                    "shares": 100,
                    "recorded_transaction_price_usd_per_share": "1.00",
                },
                {
                    "event_id": "event_000009",
                    "timestamp": "2026-08-01T00:08:00Z",
                    "event_type": "CPI_OBSERVATION",
                    "series_id": "CUUR0000SA0",
                    "series_status": "AGREEMENT_SERIES",
                    "period": "2026-06",
                    "value": "100",
                    "publication_date": "2026-07-15",
                },
                {
                    "event_id": "event_000010",
                    "timestamp": "2026-08-01T00:09:00Z",
                    "event_type": "HOLDING_REGISTERED",
                    "holding_id": "holding_000001",
                    "registration_type": "ACQUISITION",
                    "public_label": None,
                    "holding_cost_usd": "0",
                    "reinvestment_capital_funded_cost_usd": "0",
                },
                {
                    "event_id": "event_000011",
                    "timestamp": "2026-08-01T00:10:00Z",
                    "event_type": "REALIZATION",
                    "holding_id": "holding_000001",
                    "realization_type": "CASH_EXIT",
                    "floor_cpi_event_id": "event_000009",
                    "gross_cash_proceeds_usd": "11000000",
                    "allocated_holding_cost_usd": "0",
                    "direct_transaction_expenses_usd": "0",
                    "attributable_taxes_usd": "0",
                    "closes_holding": True,
                },
                {
                    "event_id": "event_000012",
                    "timestamp": "2026-08-01T00:11:00Z",
                    "event_type": "DISTRIBUTION_ELECTION_CHANGED",
                    "shareholder_id": "holder_000001",
                    "election": "DISTRIBUTE",
                },
                {
                    "event_id": "event_000013",
                    "timestamp": "2026-08-01T00:12:00Z",
                    "event_type": "HOLDING_REGISTERED",
                    "holding_id": "holding_000002",
                    "registration_type": "ACQUISITION",
                    "public_label": None,
                    "holding_cost_usd": "0",
                    "reinvestment_capital_funded_cost_usd": "0",
                },
                {
                    "event_id": "event_000014",
                    "timestamp": "2026-08-01T00:13:00Z",
                    "event_type": "REALIZATION",
                    "holding_id": "holding_000002",
                    "realization_type": "CASH_EXIT",
                    "floor_cpi_event_id": "event_000009",
                    "gross_cash_proceeds_usd": "1000000",
                    "allocated_holding_cost_usd": "0",
                    "direct_transaction_expenses_usd": "0",
                    "attributable_taxes_usd": "0",
                    "closes_holding": True,
                },
            ]
        )
        state = self.validate(header(), events)
        self.assertEqual(state.cumulative_realized_value, validator.Fraction(12_000_000))
        self.assertEqual(state.distribution_high_water, validator.Fraction(12_000_000))
        self.assertEqual(state.reinvestment_balance, validator.Fraction(500_000))
        self.assertEqual(
            state.obligations[("event_000014", "holder_000001")],
            validator.Fraction(500_000),
        )

    def test_append_transition_verifies_prefix_and_previous_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            previous_path = self.write_document(directory, "previous.md", header(), base_events())
            previous = validator.load_document(previous_path)
            events = base_events()
            events.append(
                {
                    "event_id": "event_000006",
                    "timestamp": "2026-08-01T00:05:00Z",
                    "event_type": "SHAREHOLDER_REGISTERED",
                    "shareholder_id": "holder_000001",
                    "display_name": "New Holder",
                    "handle": "@newholder",
                }
            )
            metadata = header(
                {
                    "type": "APPEND",
                    "previous_content_hash": validator.keccak256(previous.raw),
                    "summary": "Registered a prospective holder.",
                }
            )
            current_path = self.write_document(directory, "current.md", metadata, events)
            current = validator.load_document(current_path)
            state = validator.validate_document(current, draft=False, previous=previous)
            self.assertIn("holder_000001", state.profiles)

    def test_repository_draft_has_empty_ledger(self):
        document = validator.load_document(REPO_ROOT / "documents" / "stock.md")
        state = validator.validate_document(document, draft=True)
        self.assertEqual(state.outstanding, 0)


if __name__ == "__main__":
    unittest.main()
