#!/usr/bin/env python3
"""Validate and deterministically replay a personal-stock state document."""

from __future__ import annotations

import argparse
import copy
import json
import math
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any


SUPPORTED_SCHEMA_VERSION = 1
AUTHORIZED_SHARES = 20_000_000
INITIAL_BENCHMARK_PRICE = Fraction(1)
BENCHMARK_WINDOW = 100_000
ROYALTY_RATE_BY_AGREEMENT_VERSION = {"1.0": Fraction(1, 20)}
FLOOR_BASE_USD = Fraction(10_000_000)
FLOOR_BASE_PERIOD = "2026-06"
AGREEMENT_CPI_SERIES = "CUUR0000SA0"

ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")
HASH_RE = re.compile(r"^0x[0-9a-fA-F]{64}$")
EVENT_ID_RE = re.compile(r"^event_[0-9]{6}$")
SHAREHOLDER_ID_RE = re.compile(r"^holder_[0-9]{6}$")
HOLDING_ID_RE = re.compile(r"^holding_[0-9]{6}$")
CPI_PERIOD_RE = re.compile(r"^[0-9]{4}-(0[1-9]|1[0-2])$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
DECIMAL_RE = re.compile(r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?$")
FRACTION_RE = re.compile(r"^-?(0|[1-9][0-9]*)/([1-9][0-9]*)$")
DRAFT_TIMESTAMP = "2026-XX-XXTXX:XX:XXZ"
DRAFT_ADDRESSES = {"0xSTOCK_CONTRACT", "0xAGREEMENT_CONTRACT"}
DRAFT_HASH = "0xHASH"


class ValidationError(ValueError):
    pass


def object_without_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


def expect_object(value: Any, path: str) -> dict:
    require(isinstance(value, dict), f"{path} must be an object")
    return value


def expect_array(value: Any, path: str, *, nonempty: bool = False) -> list:
    require(isinstance(value, list), f"{path} must be an array")
    if nonempty:
        require(value, f"{path} must not be empty")
    return value


def expect_string(value: Any, path: str, *, nonempty: bool = True) -> str:
    require(isinstance(value, str), f"{path} must be a string")
    if nonempty:
        require(value != "", f"{path} must not be empty")
    return value


def expect_bool(value: Any, path: str) -> bool:
    require(type(value) is bool, f"{path} must be a boolean")
    return value


def expect_int(value: Any, path: str, *, minimum: int | None = None) -> int:
    require(type(value) is int, f"{path} must be an integer")
    if minimum is not None:
        require(value >= minimum, f"{path} must be at least {minimum}")
    return value


def expect_enum(value: Any, allowed: set[str], path: str) -> str:
    value = expect_string(value, path)
    require(value in allowed, f"{path} must be one of {', '.join(sorted(allowed))}")
    return value


def exact_keys(obj: dict, required: set[str], optional: set[str], path: str):
    missing = required - obj.keys()
    extra = obj.keys() - required - optional
    require(not missing, f"{path} missing fields: {', '.join(sorted(missing))}")
    require(not extra, f"{path} has unknown fields: {', '.join(sorted(extra))}")


def expect_pattern(value: Any, pattern: re.Pattern, path: str) -> str:
    value = expect_string(value, path)
    require(pattern.fullmatch(value) is not None, f"invalid {path}: {value}")
    return value


def expect_address(value: Any, path: str, draft: bool) -> str:
    value = expect_string(value, path)
    if draft and value in DRAFT_ADDRESSES:
        return value
    require(ADDRESS_RE.fullmatch(value) is not None, f"invalid {path}: {value}")
    return value


def expect_hash(value: Any, path: str, draft: bool) -> str:
    value = expect_string(value, path)
    if draft and value == DRAFT_HASH:
        return value
    require(HASH_RE.fullmatch(value) is not None, f"invalid {path}: {value}")
    return value


def timestamp_value(value: Any, path: str, draft: bool) -> datetime | None:
    value = expect_string(value, path)
    if draft and value == DRAFT_TIMESTAMP:
        return None
    require(value.endswith("Z"), f"{path} must be an RFC 3339 UTC timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise ValidationError(f"invalid {path}: {value}") from error
    require(parsed.tzinfo is not None, f"{path} must include a timezone")
    return parsed


def expect_date(value: Any, path: str) -> date:
    value = expect_pattern(value, DATE_RE, path)
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValidationError(f"invalid {path}: {value}") from error


def parse_exact_value(value: Any, path: str) -> Fraction:
    value = expect_string(value, path)
    if DECIMAL_RE.fullmatch(value):
        return Fraction(value)
    match = FRACTION_RE.fullmatch(value)
    require(match is not None, f"{path} must be an exact decimal or reduced fraction")
    numerator_text, denominator_text = value.split("/", 1)
    numerator = int(numerator_text)
    denominator = int(denominator_text)
    require(math.gcd(abs(numerator), denominator) == 1, f"{path} fraction must be reduced")
    return Fraction(numerator, denominator)


def expect_amount(
    value: Any,
    path: str,
    *,
    minimum: Fraction | None = None,
    strictly_positive: bool = False,
) -> Fraction:
    amount = parse_exact_value(value, path)
    if strictly_positive:
        require(amount > 0, f"{path} must be positive")
    if minimum is not None:
        require(amount >= minimum, f"{path} must be at least {minimum}")
    return amount


def expect_id_array(
    value: Any,
    pattern: re.Pattern,
    path: str,
    *,
    nonempty: bool = True,
) -> list[str]:
    values = expect_array(value, path, nonempty=nonempty)
    parsed = [expect_pattern(item, pattern, f"{path}[{index}]") for index, item in enumerate(values)]
    require(len(parsed) == len(set(parsed)), f"{path} must contain unique values")
    return parsed


@dataclass
class Document:
    path: Path
    raw: bytes
    header: dict
    events: list[dict]


def load_document(path: Path) -> Document:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValidationError(f"{path} is not valid UTF-8") from error
    blocks = re.findall(r"^```json\n(.*?)^```$", text, flags=re.MULTILINE | re.DOTALL)
    require(len(blocks) == 2, "stock document must contain exactly two fenced JSON blocks")
    try:
        header = json.loads(blocks[0], object_pairs_hook=object_without_duplicate_keys)
        events = json.loads(blocks[1], object_pairs_hook=object_without_duplicate_keys)
    except (json.JSONDecodeError, ValidationError) as error:
        raise ValidationError(f"invalid stock JSON: {error}") from error
    require(isinstance(header, dict), "first JSON block must be a header object")
    require(isinstance(events, list), "second JSON block must be an event array")
    return Document(path=path, raw=raw, header=header, events=events)


def validate_header(header: dict, draft: bool):
    required = {
        "document_type",
        "schema_version",
        "chain_id",
        "stock_contract",
        "agreement_contract",
        "owner",
        "update",
    }
    exact_keys(header, required, set(), "header")
    require(header["document_type"] == "personal_stock", 'header.document_type must be "personal_stock"')
    schema_version = expect_int(header["schema_version"], "header.schema_version", minimum=1)
    require(
        schema_version == SUPPORTED_SCHEMA_VERSION,
        f"unsupported schema version {schema_version}; validator supports {SUPPORTED_SCHEMA_VERSION}",
    )
    expect_int(header["chain_id"], "header.chain_id", minimum=1)
    expect_address(header["stock_contract"], "header.stock_contract", draft)
    expect_address(header["agreement_contract"], "header.agreement_contract", draft)

    owner = expect_object(header["owner"], "header.owner")
    exact_keys(owner, {"shareholder_id", "display_name", "handle"}, set(), "header.owner")
    expect_pattern(owner["shareholder_id"], SHAREHOLDER_ID_RE, "header.owner.shareholder_id")
    expect_string(owner["display_name"], "header.owner.display_name")
    if owner["handle"] is not None:
        expect_string(owner["handle"], "header.owner.handle")

    update = expect_object(header["update"], "header.update")
    update_type = expect_enum(
        update.get("type"), {"INITIAL", "APPEND", "CORRECTION", "MIGRATION"}, "header.update.type"
    )
    common = {"type", "previous_content_hash", "summary"}
    optional = set()
    if update_type == "CORRECTION":
        optional = {"correction_event_ids"}
    elif update_type == "MIGRATION":
        optional = {"from_schema_version"}
    exact_keys(update, common | optional, set(), "header.update")
    expect_string(update["summary"], "header.update.summary")
    previous_hash = update["previous_content_hash"]
    if update_type == "INITIAL":
        require(previous_hash is None, "INITIAL update must have null previous_content_hash")
    else:
        expect_hash(previous_hash, "header.update.previous_content_hash", draft)
    if update_type == "CORRECTION":
        expect_id_array(update["correction_event_ids"], EVENT_ID_RE, "header.update.correction_event_ids")
    if update_type == "MIGRATION":
        from_version = expect_int(update["from_schema_version"], "header.update.from_schema_version", minimum=1)
        require(from_version < schema_version, "MIGRATION from_schema_version must be less than schema_version")


COMMON_EVENT_KEYS = {"timestamp", "event_type"}
COMMON_EVENT_OPTIONAL_KEYS = {"public_note"}


def event_path(event: dict, fallback: str) -> str:
    return event.get("event_id", fallback)


def validate_resulting_holding(value: Any, path: str):
    value = expect_object(value, path)
    exact_keys(
        value,
        {"holding_id", "public_label", "holding_cost_usd", "reinvestment_capital_funded_cost_usd"},
        set(),
        path,
    )
    expect_pattern(value["holding_id"], HOLDING_ID_RE, f"{path}.holding_id")
    if value["public_label"] is not None:
        expect_string(value["public_label"], f"{path}.public_label")
    cost = expect_amount(value["holding_cost_usd"], f"{path}.holding_cost_usd", minimum=Fraction(0))
    rc_cost = expect_amount(
        value["reinvestment_capital_funded_cost_usd"],
        f"{path}.reinvestment_capital_funded_cost_usd",
        minimum=Fraction(0),
    )
    require(rc_cost <= cost, f"{path} Reinvestment Capital cost may not exceed holding cost")


def validate_source_holding(value: Any, path: str):
    value = expect_object(value, path)
    exact_keys(
        value,
        {
            "holding_id",
            "holding_cost_removed_usd",
            "reinvestment_capital_cost_removed_usd",
            "closes_holding",
        },
        set(),
        path,
    )
    expect_pattern(value["holding_id"], HOLDING_ID_RE, f"{path}.holding_id")
    cost = expect_amount(value["holding_cost_removed_usd"], f"{path}.holding_cost_removed_usd", minimum=Fraction(0))
    rc_cost = expect_amount(
        value["reinvestment_capital_cost_removed_usd"],
        f"{path}.reinvestment_capital_cost_removed_usd",
        minimum=Fraction(0),
    )
    require(rc_cost <= cost, f"{path} Reinvestment Capital cost may not exceed removed holding cost")
    expect_bool(value["closes_holding"], f"{path}.closes_holding")


def validate_event_object(event: dict, draft: bool, *, body: bool = False, path: str = "event"):
    expect_object(event, path)
    base_required = set(COMMON_EVENT_KEYS)
    if not body:
        base_required.add("event_id")
    if not body:
        expect_pattern(event.get("event_id"), EVENT_ID_RE, f"{path}.event_id")
    timestamp_value(event.get("timestamp"), f"{path}.timestamp", draft)
    event_type = expect_string(event.get("event_type"), f"{path}.event_type")
    if "public_note" in event:
        expect_string(event["public_note"], f"{path}.public_note", nonempty=False)

    fields: dict[str, tuple[set[str], set[str]]] = {
        "FORMATION": (set(), set()),
        "SHAREHOLDER_REGISTERED": ({"shareholder_id", "display_name", "handle"}, set()),
        "SHAREHOLDER_PROFILE_UPDATED": ({"shareholder_id"}, {"display_name", "handle"}),
        "AGREEMENT_VERSION_ISSUED": ({"agreement_version", "agreement_content_hash"}, set()),
        "AGREEMENT_ADOPTION": ({"shareholder_id", "agreement_version", "agreement_content_hash"}, set()),
        "SHARED_TERMS_EFFECTIVE": (
            {"agreement_version", "agreement_content_hash", "changed_terms", "adoption_event_ids"},
            set(),
        ),
        "TRANSFER_POLICY_SET": ({"policy_code", "policy"}, {"replaces_event_id"}),
        "TRANSFER_PERMISSION_GRANTED": (
            {
                "seller_shareholder_id",
                "recipient_shareholder_id",
                "maximum_shares",
                "expires_at",
                "irrevocable",
            },
            set(),
        ),
        "TRANSFER_PERMISSION_REVOKED": ({"permission_event_id"}, set()),
        "TRANSACTION_APPROVAL": ({"subject_event_id", "approval_type", "approving_shareholder_ids"}, set()),
        "DISTRIBUTION_ELECTION_CHANGED": ({"shareholder_id", "election"}, set()),
        "CPI_OBSERVATION": ({"series_id", "series_status", "period", "value", "publication_date"}, set()),
        "SHARE_ISSUANCE": (
            {
                "recipient_shareholder_id",
                "shares",
                "recorded_transaction_price_usd_per_share",
            },
            {"approval_event_id"},
        ),
        "OWNER_TRANSFER": (
            {
                "recipient_shareholder_id",
                "shares",
                "recorded_transaction_price_usd_per_share",
            },
            {"approval_event_id"},
        ),
        "VOLUNTARY_SALE": (
            {
                "seller_shareholder_id",
                "buyer_shareholder_id",
                "buyer_shares",
                "sale_price_usd_per_share",
                "royalty_shares",
                "permission_basis",
            },
            {"permission_event_id"},
        ),
        "BUYBACK": ({"seller_shareholder_id", "shares", "settlement_price_usd_per_share"}, set()),
        "DIRECTED_SALE": (
            {"seller_shareholder_id", "purchaser_shareholder_id", "shares", "settlement_price_usd_per_share"},
            set(),
        ),
        "LEGAL_SUCCESSION": (
            {
                "prior_holder_id",
                "temporary_holder_id",
                "shares",
                "recorded_transaction_price_usd_per_share",
            },
            set(),
        ),
        "HOLDING_REGISTERED": (
            {
                "holding_id",
                "registration_type",
                "public_label",
                "holding_cost_usd",
                "reinvestment_capital_funded_cost_usd",
            },
            set(),
        ),
        "HOLDING_COST_ADDED": (
            {
                "holding_id",
                "cost_type",
                "cost_added_usd",
                "reinvestment_capital_funded_cost_usd",
            },
            set(),
        ),
        "VALUATION_RECORDED": ({"holding_ids", "valuation_purpose", "method", "components"}, set()),
        "HOLDING_TRANSFORMED": (
            {"transformation_type", "source_holdings", "resulting_holdings"},
            {"valuation_event_id"},
        ),
        "REALIZATION": (
            {
                "holding_id",
                "realization_type",
                "floor_cpi_event_id",
                "gross_cash_proceeds_usd",
                "allocated_holding_cost_usd",
                "direct_transaction_expenses_usd",
                "attributable_taxes_usd",
                "closes_holding",
            },
            {"resulting_holdings", "valuation_event_id"},
        ),
        "TAX_RECONCILIATION": (
            {"source_realization_event_id", "reconciliation_type", "amount_usd", "floor_cpi_event_id"},
            set(),
        ),
        "REINVESTMENT_DEPLOYED": ({"holding_event_id", "holding_id", "amount_usd"}, set()),
        "DISTRIBUTION_PAYMENT": (
            {
                "source_event_id",
                "recipient_shareholder_id",
                "gross_distribution_usd",
                "withholding_usd",
                "net_payment_usd",
            },
            set(),
        ),
        "REINVESTMENT_RELEASED_TO_OWNER": ({"amount_usd"}, set()),
        "FINAL_REINVESTMENT_DISTRIBUTION": ({"amount_usd"}, set()),
        "OWNER_STATUS_CHANGED": ({"status"}, set()),
        "CORRECTION": (
            {"target_event_id", "operation", "reason", "replacement_event"},
            {"supersedes_correction_event_id"},
        ),
    }
    require(event_type in fields, f"{path}.event_type is unsupported: {event_type}")
    required_specific, optional_specific = fields[event_type]
    exact_keys(
        event,
        base_required | required_specific,
        COMMON_EVENT_OPTIONAL_KEYS | optional_specific,
        path,
    )

    def sid(name: str):
        expect_pattern(event[name], SHAREHOLDER_ID_RE, f"{path}.{name}")

    def eid(name: str):
        expect_pattern(event[name], EVENT_ID_RE, f"{path}.{name}")

    def hid(name: str):
        expect_pattern(event[name], HOLDING_ID_RE, f"{path}.{name}")

    if event_type == "SHAREHOLDER_REGISTERED":
        sid("shareholder_id")
        expect_string(event["display_name"], f"{path}.display_name")
        if event["handle"] is not None:
            expect_string(event["handle"], f"{path}.handle")
    elif event_type == "SHAREHOLDER_PROFILE_UPDATED":
        sid("shareholder_id")
        require("display_name" in event or "handle" in event, f"{path} must update at least one profile field")
        if "display_name" in event:
            expect_string(event["display_name"], f"{path}.display_name")
        if "handle" in event and event["handle"] is not None:
            expect_string(event["handle"], f"{path}.handle")
    elif event_type == "AGREEMENT_VERSION_ISSUED":
        expect_string(event["agreement_version"], f"{path}.agreement_version")
        expect_hash(event["agreement_content_hash"], f"{path}.agreement_content_hash", draft)
    elif event_type == "AGREEMENT_ADOPTION":
        sid("shareholder_id")
        expect_string(event["agreement_version"], f"{path}.agreement_version")
        expect_hash(event["agreement_content_hash"], f"{path}.agreement_content_hash", draft)
    elif event_type == "SHARED_TERMS_EFFECTIVE":
        expect_string(event["agreement_version"], f"{path}.agreement_version")
        expect_hash(event["agreement_content_hash"], f"{path}.agreement_content_hash", draft)
        changed = expect_array(event["changed_terms"], f"{path}.changed_terms", nonempty=True)
        for index, item in enumerate(changed):
            expect_string(item, f"{path}.changed_terms[{index}]")
        expect_id_array(event["adoption_event_ids"], EVENT_ID_RE, f"{path}.adoption_event_ids")
    elif event_type == "TRANSFER_POLICY_SET":
        expect_enum(
            event["policy_code"],
            {
                "OWNER_APPROVAL_REQUIRED",
                "CURRENT_HOLDERS_ONLY",
                "ALL_TRANSFERS_PERMITTED",
                "NO_VOLUNTARY_TRANSFERS",
            },
            f"{path}.policy_code",
        )
        expect_string(event["policy"], f"{path}.policy")
        if "replaces_event_id" in event:
            eid("replaces_event_id")
    elif event_type == "TRANSFER_PERMISSION_GRANTED":
        sid("seller_shareholder_id")
        sid("recipient_shareholder_id")
        if event["maximum_shares"] is not None:
            expect_int(event["maximum_shares"], f"{path}.maximum_shares", minimum=1)
        if event["expires_at"] is not None:
            timestamp_value(event["expires_at"], f"{path}.expires_at", draft)
        expect_bool(event["irrevocable"], f"{path}.irrevocable")
    elif event_type == "TRANSFER_PERMISSION_REVOKED":
        eid("permission_event_id")
    elif event_type == "TRANSACTION_APPROVAL":
        eid("subject_event_id")
        require(event["approval_type"] == "BELOW_BENCHMARK", f"{path}.approval_type must be BELOW_BENCHMARK")
        expect_id_array(
            event["approving_shareholder_ids"],
            SHAREHOLDER_ID_RE,
            f"{path}.approving_shareholder_ids",
        )
    elif event_type == "DISTRIBUTION_ELECTION_CHANGED":
        sid("shareholder_id")
        expect_enum(event["election"], {"REINVEST", "DISTRIBUTE"}, f"{path}.election")
    elif event_type == "CPI_OBSERVATION":
        expect_string(event["series_id"], f"{path}.series_id")
        expect_enum(
            event["series_status"],
            {"AGREEMENT_SERIES", "OFFICIAL_SUCCESSOR", "CLOSEST_AVAILABLE"},
            f"{path}.series_status",
        )
        expect_pattern(event["period"], CPI_PERIOD_RE, f"{path}.period")
        require(parse_exact_value(event["value"], f"{path}.value") > 0, f"{path}.value must be positive")
        expect_date(event["publication_date"], f"{path}.publication_date")
    elif event_type in {"SHARE_ISSUANCE", "OWNER_TRANSFER"}:
        sid("recipient_shareholder_id")
        expect_int(event["shares"], f"{path}.shares", minimum=1)
        expect_amount(
            event["recorded_transaction_price_usd_per_share"],
            f"{path}.recorded_transaction_price_usd_per_share",
            strictly_positive=True,
        )
        if "approval_event_id" in event:
            eid("approval_event_id")
    elif event_type == "VOLUNTARY_SALE":
        sid("seller_shareholder_id")
        sid("buyer_shareholder_id")
        expect_int(event["buyer_shares"], f"{path}.buyer_shares", minimum=1)
        expect_amount(event["sale_price_usd_per_share"], f"{path}.sale_price_usd_per_share", strictly_positive=True)
        expect_int(event["royalty_shares"], f"{path}.royalty_shares", minimum=0)
        basis = expect_enum(event["permission_basis"], {"POLICY", "SPECIFIC_PERMISSION"}, f"{path}.permission_basis")
        require(
            (basis == "SPECIFIC_PERMISSION") == ("permission_event_id" in event),
            f"{path}.permission_event_id is required exactly for SPECIFIC_PERMISSION",
        )
        if "permission_event_id" in event:
            eid("permission_event_id")
    elif event_type == "BUYBACK":
        sid("seller_shareholder_id")
        expect_int(event["shares"], f"{path}.shares", minimum=1)
        expect_amount(
            event["settlement_price_usd_per_share"],
            f"{path}.settlement_price_usd_per_share",
            strictly_positive=True,
        )
    elif event_type == "DIRECTED_SALE":
        sid("seller_shareholder_id")
        sid("purchaser_shareholder_id")
        expect_int(event["shares"], f"{path}.shares", minimum=1)
        expect_amount(
            event["settlement_price_usd_per_share"],
            f"{path}.settlement_price_usd_per_share",
            strictly_positive=True,
        )
    elif event_type == "LEGAL_SUCCESSION":
        sid("prior_holder_id")
        sid("temporary_holder_id")
        expect_int(event["shares"], f"{path}.shares", minimum=1)
        expect_amount(
            event["recorded_transaction_price_usd_per_share"],
            f"{path}.recorded_transaction_price_usd_per_share",
            strictly_positive=True,
        )
    elif event_type == "HOLDING_REGISTERED":
        hid("holding_id")
        expect_enum(event["registration_type"], {"OPENING", "ACQUISITION", "SUBSTITUTE"}, f"{path}.registration_type")
        if event["public_label"] is not None:
            expect_string(event["public_label"], f"{path}.public_label")
        cost = expect_amount(event["holding_cost_usd"], f"{path}.holding_cost_usd", minimum=Fraction(0))
        rc_cost = expect_amount(
            event["reinvestment_capital_funded_cost_usd"],
            f"{path}.reinvestment_capital_funded_cost_usd",
            minimum=Fraction(0),
        )
        require(rc_cost <= cost, f"{path} Reinvestment Capital cost may not exceed holding cost")
    elif event_type == "HOLDING_COST_ADDED":
        hid("holding_id")
        expect_enum(
            event["cost_type"],
            {"ACQUISITION", "EXERCISE", "VESTING", "PRESERVATION", "ENFORCEMENT", "TRANSFORM", "ATTRIBUTABLE_TAX", "OTHER_ALLOWED"},
            f"{path}.cost_type",
        )
        cost = expect_amount(event["cost_added_usd"], f"{path}.cost_added_usd", strictly_positive=True)
        rc_cost = expect_amount(
            event["reinvestment_capital_funded_cost_usd"],
            f"{path}.reinvestment_capital_funded_cost_usd",
            minimum=Fraction(0),
        )
        require(rc_cost <= cost, f"{path} Reinvestment Capital cost may not exceed added cost")
    elif event_type == "VALUATION_RECORDED":
        expect_id_array(event["holding_ids"], HOLDING_ID_RE, f"{path}.holding_ids")
        expect_enum(
            event["valuation_purpose"],
            {"COST_ALLOCATION", "TRANSFORM", "MIXED_EXIT", "OTHER_AGREEMENT_PURPOSE"},
            f"{path}.valuation_purpose",
        )
        expect_enum(
            event["method"],
            {"TRANSACTION_DOCUMENTS", "QUOTED_MARKET_PRICE", "INDEPENDENT_VALUATION", "OWNER_GOOD_FAITH_ESTIMATE"},
            f"{path}.method",
        )
        components = expect_array(event["components"], f"{path}.components", nonempty=True)
        for index, component in enumerate(components):
            component_path = f"{path}.components[{index}]"
            component = expect_object(component, component_path)
            exact_keys(component, {"component", "value_usd"}, set(), component_path)
            expect_string(component["component"], f"{component_path}.component")
            expect_amount(component["value_usd"], f"{component_path}.value_usd", minimum=Fraction(0))
    elif event_type == "HOLDING_TRANSFORMED":
        expect_enum(event["transformation_type"], {"TRANSFORM", "NONCASH_EXIT"}, f"{path}.transformation_type")
        sources = expect_array(event["source_holdings"], f"{path}.source_holdings", nonempty=True)
        results = expect_array(event["resulting_holdings"], f"{path}.resulting_holdings", nonempty=True)
        for index, source in enumerate(sources):
            validate_source_holding(source, f"{path}.source_holdings[{index}]")
        for index, result in enumerate(results):
            validate_resulting_holding(result, f"{path}.resulting_holdings[{index}]")
        require(
            len({source["holding_id"] for source in sources}) == len(sources),
            f"{path}.source_holdings must contain unique holding IDs",
        )
        require(
            len({result["holding_id"] for result in results}) == len(results),
            f"{path}.resulting_holdings must contain unique holding IDs",
        )
        if "valuation_event_id" in event:
            eid("valuation_event_id")
    elif event_type == "REALIZATION":
        hid("holding_id")
        expect_enum(
            event["realization_type"],
            {"CASH_EXIT", "EXIT_EQUIVALENT_DISTRIBUTION", "TERMINAL_EXIT", "LATER_RECOVERY"},
            f"{path}.realization_type",
        )
        eid("floor_cpi_event_id")
        for name in (
            "gross_cash_proceeds_usd",
            "allocated_holding_cost_usd",
            "direct_transaction_expenses_usd",
            "attributable_taxes_usd",
        ):
            expect_amount(event[name], f"{path}.{name}", minimum=Fraction(0))
        expect_bool(event["closes_holding"], f"{path}.closes_holding")
        if "resulting_holdings" in event:
            results = expect_array(event["resulting_holdings"], f"{path}.resulting_holdings", nonempty=True)
            for index, result in enumerate(results):
                validate_resulting_holding(result, f"{path}.resulting_holdings[{index}]")
            require(
                len({result["holding_id"] for result in results}) == len(results),
                f"{path}.resulting_holdings must contain unique holding IDs",
            )
        if "valuation_event_id" in event:
            eid("valuation_event_id")
    elif event_type == "TAX_RECONCILIATION":
        eid("source_realization_event_id")
        expect_enum(
            event["reconciliation_type"],
            {"ADDITIONAL_TAX", "REFUND_OR_RESERVE_RELEASE"},
            f"{path}.reconciliation_type",
        )
        expect_amount(event["amount_usd"], f"{path}.amount_usd", strictly_positive=True)
        eid("floor_cpi_event_id")
    elif event_type == "REINVESTMENT_DEPLOYED":
        eid("holding_event_id")
        hid("holding_id")
        expect_amount(event["amount_usd"], f"{path}.amount_usd", strictly_positive=True)
    elif event_type == "DISTRIBUTION_PAYMENT":
        eid("source_event_id")
        sid("recipient_shareholder_id")
        expect_amount(event["gross_distribution_usd"], f"{path}.gross_distribution_usd", strictly_positive=True)
        expect_amount(event["withholding_usd"], f"{path}.withholding_usd", minimum=Fraction(0))
        expect_amount(event["net_payment_usd"], f"{path}.net_payment_usd", minimum=Fraction(0))
    elif event_type in {"REINVESTMENT_RELEASED_TO_OWNER", "FINAL_REINVESTMENT_DISTRIBUTION"}:
        expect_amount(event["amount_usd"], f"{path}.amount_usd", strictly_positive=True)
    elif event_type == "OWNER_STATUS_CHANGED":
        expect_enum(event["status"], {"ACTIVE", "INCAPACITATED", "DECEASED"}, f"{path}.status")
    elif event_type == "CORRECTION":
        require(not body, f"{path} may not contain a nested CORRECTION event")
        eid("target_event_id")
        operation = expect_enum(event["operation"], {"REPLACE", "VOID", "INSERT_AFTER"}, f"{path}.operation")
        expect_string(event["reason"], f"{path}.reason")
        if "supersedes_correction_event_id" in event:
            eid("supersedes_correction_event_id")
        replacement = event["replacement_event"]
        if operation == "VOID":
            require(replacement is None, f"{path}.replacement_event must be null for VOID")
        else:
            require(isinstance(replacement, dict), f"{path}.replacement_event must be an object")
            validate_event_object(replacement, draft, body=True, path=f"{path}.replacement_event")
            require(replacement["event_type"] != "CORRECTION", f"{path} replacement may not be CORRECTION")
        if operation == "INSERT_AFTER":
            require("supersedes_correction_event_id" not in event, f"{path} INSERT_AFTER may not supersede a correction")


def validate_events(events: list[dict], draft: bool):
    require(events, "event array must not be empty")
    previous_timestamp = None
    for index, event in enumerate(events, start=1):
        path = f"events[{index - 1}]"
        validate_event_object(event, draft, path=path)
        expected_id = f"event_{index:06d}"
        require(event["event_id"] == expected_id, f"{path}.event_id must be {expected_id}")
        current_timestamp = timestamp_value(event["timestamp"], f"{path}.timestamp", draft)
        if event["event_type"] != "CORRECTION" and previous_timestamp is not None and current_timestamp is not None:
            require(current_timestamp >= previous_timestamp, f"{path}.timestamp is earlier than the preceding factual event")
        if event["event_type"] != "CORRECTION" and current_timestamp is not None:
            previous_timestamp = current_timestamp


def resolve_corrections(events: list[dict], draft: bool) -> list[dict]:
    slots: list[dict[str, Any]] = []
    slot_by_id: dict[str, dict[str, Any]] = {}
    latest_correction: dict[str, str] = {}

    def rebuild_positions():
        for position, slot in enumerate(slots):
            slot["position"] = position

    for physical in events:
        if physical["event_type"] != "CORRECTION":
            event = copy.deepcopy(physical)
            slot = {"event_id": event["event_id"], "event": event, "position": len(slots)}
            slots.append(slot)
            slot_by_id[event["event_id"]] = slot
            continue

        correction_id = physical["event_id"]
        target_id = physical["target_event_id"]
        require(target_id in slot_by_id, f"{correction_id} targets unknown effective event {target_id}")
        operation = physical["operation"]
        if operation == "INSERT_AFTER":
            require(correction_id not in slot_by_id, f"{correction_id} duplicates an effective event ID")
            replacement = copy.deepcopy(physical["replacement_event"])
            replacement["event_id"] = correction_id
            anchor = slot_by_id[target_id]
            slot = {"event_id": correction_id, "event": replacement, "position": anchor["position"] + 1}
            slots.insert(anchor["position"] + 1, slot)
            slot_by_id[correction_id] = slot
            rebuild_positions()
            continue

        prior_correction = latest_correction.get(target_id)
        supersedes = physical.get("supersedes_correction_event_id")
        if prior_correction is None:
            require(supersedes is None, f"{correction_id} names a superseded correction but {target_id} was not corrected")
        else:
            require(
                supersedes == prior_correction,
                f"{correction_id} must supersede latest correction {prior_correction} for {target_id}",
            )
        slot = slot_by_id[target_id]
        if operation == "VOID":
            slot["event"] = None
        else:
            replacement = copy.deepcopy(physical["replacement_event"])
            replacement["event_id"] = target_id
            slot["event"] = replacement
        latest_correction[target_id] = correction_id

    effective = [slot["event"] for slot in slots if slot["event"] is not None]
    require(effective, "corrections removed every effective event")
    require(effective[0]["event_type"] == "FORMATION", "effective ledger must begin with FORMATION")
    require(effective[0]["event_id"] == "event_000001", "FORMATION must retain event_000001")

    previous_timestamp = None
    for event in effective:
        parsed = timestamp_value(event["timestamp"], f"{event['event_id']}.timestamp", draft)
        if previous_timestamp is not None and parsed is not None:
            require(parsed >= previous_timestamp, f"effective event {event['event_id']} is out of chronological order")
        if parsed is not None:
            previous_timestamp = parsed
    return effective


def keccak256(raw: bytes) -> str:
    try:
        result = subprocess.run(
            ["cast", "keccak", "0x" + raw.hex()],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        raise ValidationError("cast is required to verify previous_content_hash") from error
    digest = result.stdout.strip()
    require(HASH_RE.fullmatch(digest) is not None, f"cast returned invalid Keccak hash: {digest}")
    return digest


def validate_publication_transition(current: Document, previous: Document, draft: bool):
    update = current.header["update"]
    update_type = update["type"]
    require(update_type != "INITIAL", "INITIAL publication may not specify a previous document")
    expected_hash = keccak256(previous.raw)
    if not (draft and update["previous_content_hash"] == DRAFT_HASH):
        require(
            update["previous_content_hash"].lower() == expected_hash.lower(),
            f"previous_content_hash must equal {expected_hash}",
        )
    for field in ("document_type", "chain_id", "stock_contract", "agreement_contract"):
        require(current.header[field] == previous.header[field], f"header.{field} is immutable")
    require(
        current.header["owner"]["shareholder_id"] == previous.header["owner"]["shareholder_id"],
        "header.owner.shareholder_id is immutable",
    )

    if update_type in {"APPEND", "CORRECTION"}:
        require(
            current.header["schema_version"] == previous.header["schema_version"],
            f"{update_type} may not change schema_version",
        )
        require(
            len(current.events) > len(previous.events),
            f"{update_type} must append at least one event",
        )
        require(
            current.events[: len(previous.events)] == previous.events,
            f"{update_type} must preserve the preceding event array as an exact prefix",
        )
        appended = current.events[len(previous.events) :]
        if update_type == "APPEND":
            require(
                all(event["event_type"] != "CORRECTION" for event in appended),
                "APPEND may not append CORRECTION events",
            )
        else:
            appended_ids = [event["event_id"] for event in appended]
            require(
                all(event["event_type"] == "CORRECTION" for event in appended),
                "CORRECTION may append only CORRECTION events",
            )
            require(
                appended_ids == update["correction_event_ids"],
                "correction_event_ids must exactly match the appended correction events",
            )
    elif update_type == "MIGRATION":
        require(
            update["from_schema_version"] == previous.header["schema_version"],
            "from_schema_version must equal the preceding schema version",
        )
        require(
            current.header["schema_version"] > previous.header["schema_version"],
            "MIGRATION must increase schema_version",
        )
        require(len(current.events) == len(previous.events), "MIGRATION may not add or remove physical events")
        require(
            [event["event_id"] for event in current.events]
            == [event["event_id"] for event in previous.events],
            "MIGRATION may not reorder or replace event IDs",
        )


@dataclass
class Holding:
    cost: Fraction
    rc_cost: Fraction
    open: bool
    public_label: str | None
    rc_loss_deficit: Fraction = Fraction(0)


class LedgerState:
    def __init__(self, header: dict, draft: bool):
        self.header = header
        self.draft = draft
        self.owner_id = header["owner"]["shareholder_id"]
        self.profiles = {
            self.owner_id: {
                "display_name": header["owner"]["display_name"],
                "handle": header["owner"]["handle"],
            }
        }
        self.issued_versions: dict[str, str] = {}
        self.latest_issued_version: str | None = None
        self.adoptions: dict[str, tuple[str, str, str]] = {}
        self.adoption_events: dict[str, tuple[str, str]] = {}
        self.balances: defaultdict[str, int] = defaultdict(int)
        self.basis: defaultdict[str, Fraction] = defaultdict(Fraction)
        self.elections: dict[str, str] = {}
        self.owner_equivalent = {self.owner_id}
        self.temporary_holders: set[str] = set()
        self.outstanding = 0
        self.benchmark_movements: list[tuple[int, Fraction]] = []
        self.cumulative_sale_result: defaultdict[str, Fraction] = defaultdict(Fraction)
        self.royalty_high_water: defaultdict[str, Fraction] = defaultdict(Fraction)
        self.transfer_policy_event_id: str | None = None
        self.transfer_policy_code: str | None = None
        self.permissions: dict[str, dict] = {}
        self.approvals: dict[str, dict] = {}
        self.holdings: dict[str, Holding] = {}
        self.valuations: dict[str, dict] = {}
        self.holding_event_rc_funding: dict[str, tuple[str, Fraction]] = {}
        self.deployment_used: defaultdict[str, Fraction] = defaultdict(Fraction)
        self.cpi_observations: list[dict] = []
        self.cpi_by_event: dict[str, dict] = {}
        self.cumulative_realized_value = Fraction(0)
        self.distribution_high_water = Fraction(0)
        self.reinvestment_balance = Fraction(0)
        self.realization_records: dict[str, dict] = {}
        self.obligations: defaultdict[tuple[str, str], Fraction] = defaultdict(Fraction)
        self.payments: defaultdict[tuple[str, str], Fraction] = defaultdict(Fraction)
        self.owner_status = "ACTIVE"
        self.commencement_event_id: str | None = None
        self.seen_effective_ids: set[str] = set()

    def error(self, event: dict, message: str):
        raise ValidationError(f"{event['event_id']}: {message}")

    def require_profile(self, event: dict, holder_id: str):
        if holder_id not in self.profiles:
            self.error(event, f"unknown shareholder ID {holder_id}")

    def current_holders(self) -> set[str]:
        return {holder_id for holder_id, shares in self.balances.items() if shares > 0}

    def voting_holders(self) -> list[str]:
        return [
            holder_id
            for holder_id, shares in self.balances.items()
            if shares > 0 and holder_id not in self.owner_equivalent
        ]

    def benchmark_price(self) -> Fraction:
        remaining = BENCHMARK_WINDOW
        volume = 0
        value = Fraction(0)
        for shares, price in reversed(self.benchmark_movements):
            if remaining == 0:
                break
            included = min(shares, remaining)
            value += included * price
            volume += included
            remaining -= included
        return value / volume if volume else INITIAL_BENCHMARK_PRICE

    def add_benchmark_movement(self, shares: int, price: Fraction):
        self.benchmark_movements.append((shares, price))

    def latest_agreement_adopted(self, holder_id: str) -> bool:
        if self.latest_issued_version is None:
            return False
        adoption = self.adoptions.get(holder_id)
        return adoption is not None and adoption[0] == self.latest_issued_version

    def ensure_recipient(self, event: dict, holder_id: str, *, legal_succession: bool = False):
        self.require_profile(event, holder_id)
        if holder_id in self.temporary_holders and not legal_succession:
            if not self.latest_agreement_adopted(holder_id):
                self.error(event, f"temporary holder {holder_id} has not adopted the latest agreement version")
            self.temporary_holders.remove(holder_id)
        if self.balances[holder_id] == 0 and not legal_succession:
            if not self.latest_agreement_adopted(holder_id):
                self.error(event, f"first-time recipient {holder_id} has not adopted the latest agreement version")
            self.elections[holder_id] = "REINVEST"

    def holder_average_basis(self, holder_id: str) -> Fraction:
        shares = self.balances[holder_id]
        require(shares > 0, f"cannot calculate royalty basis for empty holder {holder_id}")
        return self.basis[holder_id] / shares

    def remove_shares(self, event: dict, holder_id: str, shares: int) -> Fraction:
        if self.balances[holder_id] < shares:
            self.error(event, f"{holder_id} does not own {shares} shares")
        average = self.holder_average_basis(holder_id)
        removed_basis = average * shares
        self.balances[holder_id] -= shares
        self.basis[holder_id] -= removed_basis
        if self.balances[holder_id] == 0:
            require(self.basis[holder_id] == 0, f"basis did not clear for {holder_id}")
        return removed_basis

    def add_shares(self, holder_id: str, shares: int, basis_per_share: Fraction):
        self.balances[holder_id] += shares
        self.basis[holder_id] += shares * basis_per_share

    def validate_below_benchmark_approval(self, event: dict, price: Fraction, benchmark_before: Fraction):
        approval_id = event.get("approval_event_id")
        if price >= benchmark_before:
            if approval_id is not None:
                self.error(event, "approval_event_id is allowed only for a below-benchmark transaction")
            return
        if approval_id is None or approval_id not in self.approvals:
            self.error(event, "below-benchmark transaction lacks unanimous approval")
        approval = self.approvals[approval_id]
        if approval.get("used"):
            self.error(event, f"approval {approval_id} was already used")
        if approval["subject_event_id"] != event["event_id"]:
            self.error(event, f"approval {approval_id} identifies a different transaction")
        required_approvers = self.current_holders() | {self.owner_id}
        if set(approval["approving_shareholder_ids"]) != required_approvers:
            self.error(event, "below-benchmark approval does not include every required approver")
        approval["used"] = True

    def require_current_cpi(self, event: dict) -> tuple[Fraction, Fraction]:
        cpi_event_id = event["floor_cpi_event_id"]
        if not self.cpi_observations:
            self.error(event, "floor calculation has no recorded CPI observation")
        if self.cpi_observations[-1]["event_id"] != cpi_event_id:
            self.error(event, "floor_cpi_event_id is not the latest recorded eligible CPI observation")
        base_candidates = [item for item in self.cpi_observations if item["period"] == FLOOR_BASE_PERIOD]
        if not base_candidates:
            self.error(event, f"floor calculation lacks base CPI observation for {FLOOR_BASE_PERIOD}")
        base = base_candidates[-1]["value"]
        current = self.cpi_by_event[cpi_event_id]["value"]
        return current, FLOOR_BASE_USD * current / base

    def distribution_result(self) -> str:
        if self.owner_status == "DECEASED":
            return "DISTRIBUTE"
        holders = self.voting_holders()
        voting_shares = sum(self.balances[holder_id] for holder_id in holders)
        if voting_shares == 0:
            return "REINVEST"
        reinvest_shares = sum(
            self.balances[holder_id]
            for holder_id in holders
            if self.elections.get(holder_id, "REINVEST") == "REINVEST"
        )
        return "REINVEST" if reinvest_shares * 2 > voting_shares else "DISTRIBUTE"

    def apply_realized_value(self, event: dict, event_value: Fraction) -> dict:
        _, floor = self.require_current_cpi(event)
        if self.outstanding <= 0:
            self.error(event, "realization occurred before any shares were outstanding")
        cumulative_before = self.cumulative_realized_value
        cumulative_after = cumulative_before + event_value
        threshold = max(floor, self.distribution_high_water)
        newly_qualifying = max(Fraction(0), min(event_value, cumulative_after - threshold))
        voting_holders = self.voting_holders()
        voting_shares = sum(self.balances[holder_id] for holder_id in voting_holders)
        non_owner_participation = newly_qualifying * voting_shares / self.outstanding
        result = self.distribution_result()
        reinvest_designation = Fraction(0)
        if newly_qualifying > 0:
            self.distribution_high_water = cumulative_after
        if non_owner_participation > 0 and result == "REINVEST":
            self.reinvestment_balance += non_owner_participation
            reinvest_designation = non_owner_participation
        elif non_owner_participation > 0:
            for holder_id in voting_holders:
                amount = newly_qualifying * self.balances[holder_id] / self.outstanding
                self.obligations[(event["event_id"], holder_id)] += amount
        self.cumulative_realized_value = cumulative_after
        record = {
            "event_value": event_value,
            "cumulative_before": cumulative_before,
            "threshold": threshold,
            "newly_qualifying": newly_qualifying,
            "non_owner_participation": non_owner_participation,
            "non_owner_fraction": Fraction(voting_shares, self.outstanding),
            "distribution_result": result,
            "reinvest_designation": reinvest_designation,
            "tax_reduction": Fraction(0),
        }
        self.realization_records[event["event_id"]] = record
        return record

    def replay(self, events: list[dict]):
        formation_seen = False
        for event in events:
            event_id = event["event_id"]
            if event_id in self.seen_effective_ids:
                self.error(event, "duplicate effective event ID")
            self.seen_effective_ids.add(event_id)
            event_type = event["event_type"]

            if event_type == "FORMATION":
                if formation_seen or event is not events[0]:
                    self.error(event, "FORMATION must occur exactly once at the start")
                formation_seen = True
                continue
            if not formation_seen:
                self.error(event, "event precedes FORMATION")

            if event_type == "SHAREHOLDER_REGISTERED":
                holder_id = event["shareholder_id"]
                if holder_id in self.profiles:
                    self.error(event, f"shareholder ID {holder_id} is already registered")
                self.profiles[holder_id] = {"display_name": event["display_name"], "handle": event["handle"]}
            elif event_type == "SHAREHOLDER_PROFILE_UPDATED":
                holder_id = event["shareholder_id"]
                self.require_profile(event, holder_id)
                if "display_name" in event:
                    self.profiles[holder_id]["display_name"] = event["display_name"]
                if "handle" in event:
                    self.profiles[holder_id]["handle"] = event["handle"]
            elif event_type == "AGREEMENT_VERSION_ISSUED":
                version = event["agreement_version"]
                if version in self.issued_versions:
                    self.error(event, f"agreement version {version} was already issued")
                self.issued_versions[version] = event["agreement_content_hash"]
                self.latest_issued_version = version
            elif event_type == "AGREEMENT_ADOPTION":
                holder_id = event["shareholder_id"]
                self.require_profile(event, holder_id)
                version = event["agreement_version"]
                if self.issued_versions.get(version) != event["agreement_content_hash"]:
                    self.error(event, f"adoption does not match issued agreement version {version}")
                self.adoptions[holder_id] = (version, event["agreement_content_hash"], event_id)
                self.adoption_events[event_id] = (holder_id, version)
            elif event_type == "SHARED_TERMS_EFFECTIVE":
                version = event["agreement_version"]
                if self.issued_versions.get(version) != event["agreement_content_hash"]:
                    self.error(event, "shared terms reference an unknown agreement version")
                current = self.current_holders()
                adoptions = {self.adoption_events[item] for item in event["adoption_event_ids"] if item in self.adoption_events}
                if len(adoptions) != len(event["adoption_event_ids"]):
                    self.error(event, "shared terms reference an invalid adoption event")
                if {holder for holder, adopted_version in adoptions if adopted_version == version} != current:
                    self.error(event, "shared terms do not identify matching adoptions by every current shareholder")
                self.error(event, "validator rules must be updated before a new shared-term version becomes effective")
            elif event_type == "TRANSFER_POLICY_SET":
                prior = event.get("replaces_event_id")
                if self.transfer_policy_event_id is None:
                    if prior is not None:
                        self.error(event, "first transfer policy may not replace another event")
                elif prior != self.transfer_policy_event_id:
                    self.error(event, f"transfer policy must replace {self.transfer_policy_event_id}")
                self.transfer_policy_event_id = event_id
                self.transfer_policy_code = event["policy_code"]
            elif event_type == "TRANSFER_PERMISSION_GRANTED":
                self.require_profile(event, event["seller_shareholder_id"])
                self.require_profile(event, event["recipient_shareholder_id"])
                if event["seller_shareholder_id"] == self.owner_id:
                    self.error(event, "transaction-specific voluntary-sale permission requires a non-owner seller")
                self.permissions[event_id] = {**event, "revoked": False, "used": False}
            elif event_type == "TRANSFER_PERMISSION_REVOKED":
                permission_id = event["permission_event_id"]
                permission = self.permissions.get(permission_id)
                if permission is None:
                    self.error(event, f"unknown permission {permission_id}")
                if permission["irrevocable"]:
                    self.error(event, f"permission {permission_id} is irrevocable")
                if permission["revoked"]:
                    self.error(event, f"permission {permission_id} was already revoked")
                if permission["used"]:
                    self.error(event, f"permission {permission_id} was already used by a settled transfer")
                permission["revoked"] = True
            elif event_type == "TRANSACTION_APPROVAL":
                subject = event["subject_event_id"]
                if subject in self.approvals:
                    self.error(event, f"transaction {subject} already has an approval")
                for holder_id in event["approving_shareholder_ids"]:
                    self.require_profile(event, holder_id)
                self.approvals[event_id] = {**event, "used": False}
            elif event_type == "DISTRIBUTION_ELECTION_CHANGED":
                holder_id = event["shareholder_id"]
                if holder_id == self.owner_id or self.balances[holder_id] <= 0:
                    self.error(event, "only a current non-owner shareholder may change an election")
                if holder_id in self.temporary_holders:
                    self.error(event, "a temporary holder may not change the inherited election")
                self.elections[holder_id] = event["election"]
            elif event_type == "CPI_OBSERVATION":
                if event["series_status"] == "AGREEMENT_SERIES" and event["series_id"] != AGREEMENT_CPI_SERIES:
                    self.error(event, f"AGREEMENT_SERIES must use {AGREEMENT_CPI_SERIES}")
                observation = {
                    **event,
                    "value": parse_exact_value(event["value"], f"{event_id}.value"),
                }
                event_timestamp = timestamp_value(event["timestamp"], f"{event_id}.timestamp", self.draft)
                publication_date = expect_date(event["publication_date"], f"{event_id}.publication_date")
                if event_timestamp is not None and publication_date > event_timestamp.date():
                    self.error(event, "CPI observation was recorded before its publication date")
                self.cpi_observations.append(observation)
                self.cpi_by_event[event_id] = observation
            elif event_type == "SHARE_ISSUANCE":
                recipient = event["recipient_shareholder_id"]
                self.ensure_recipient(event, recipient)
                price = parse_exact_value(event["recorded_transaction_price_usd_per_share"], "price")
                benchmark_before = self.benchmark_price()
                self.validate_below_benchmark_approval(event, price, benchmark_before)
                if self.outstanding + event["shares"] > AUTHORIZED_SHARES:
                    self.error(event, "issuance exceeds authorized shares")
                if self.commencement_event_id is None:
                    self.commencement_event_id = event_id
                self.outstanding += event["shares"]
                self.add_shares(recipient, event["shares"], price)
                self.add_benchmark_movement(event["shares"], price)
            elif event_type == "OWNER_TRANSFER":
                recipient = event["recipient_shareholder_id"]
                self.ensure_recipient(event, recipient)
                price = parse_exact_value(event["recorded_transaction_price_usd_per_share"], "price")
                benchmark_before = self.benchmark_price()
                self.validate_below_benchmark_approval(event, price, benchmark_before)
                self.remove_shares(event, self.owner_id, event["shares"])
                self.add_shares(recipient, event["shares"], price)
                self.add_benchmark_movement(event["shares"], price)
            elif event_type == "VOLUNTARY_SALE":
                self.replay_voluntary_sale(event)
            elif event_type == "BUYBACK":
                seller = event["seller_shareholder_id"]
                if seller == self.owner_id:
                    self.error(event, "owner may not be the seller in a buyback")
                price = parse_exact_value(event["settlement_price_usd_per_share"], "price")
                if price < self.benchmark_price():
                    self.error(event, "buyback price is below the benchmark")
                self.remove_shares(event, seller, event["shares"])
                self.add_shares(self.owner_id, event["shares"], price)
            elif event_type == "DIRECTED_SALE":
                seller = event["seller_shareholder_id"]
                purchaser = event["purchaser_shareholder_id"]
                if seller == self.owner_id or seller == purchaser:
                    self.error(event, "invalid directed-sale parties")
                self.ensure_recipient(event, purchaser)
                price = parse_exact_value(event["settlement_price_usd_per_share"], "price")
                if price < self.benchmark_price():
                    self.error(event, "directed-sale price is below the benchmark")
                self.remove_shares(event, seller, event["shares"])
                self.add_shares(purchaser, event["shares"], price)
            elif event_type == "LEGAL_SUCCESSION":
                prior = event["prior_holder_id"]
                temporary = event["temporary_holder_id"]
                if prior == temporary:
                    self.error(event, "legal succession must change holders")
                if self.balances[temporary] > 0:
                    self.error(event, "legal succession temporary holder must not already hold shares")
                self.ensure_recipient(event, temporary, legal_succession=True)
                price = parse_exact_value(event["recorded_transaction_price_usd_per_share"], "price")
                if price != self.benchmark_price():
                    self.error(event, "legal succession recorded price must equal the preceding benchmark")
                inherited_election = self.elections.get(prior, "REINVEST")
                self.remove_shares(event, prior, event["shares"])
                self.add_shares(temporary, event["shares"], price)
                self.elections[temporary] = inherited_election
                self.temporary_holders.add(temporary)
                if prior in self.owner_equivalent:
                    if self.owner_status != "DECEASED":
                        self.error(event, "owner shares may pass to an estate only after owner death")
                    self.owner_equivalent.add(temporary)
                self.add_benchmark_movement(event["shares"], price)
            elif event_type == "HOLDING_REGISTERED":
                self.replay_holding_registered(event)
            elif event_type == "HOLDING_COST_ADDED":
                self.replay_holding_cost_added(event)
            elif event_type == "VALUATION_RECORDED":
                for holding_id in event["holding_ids"]:
                    if holding_id not in self.holdings:
                        self.error(event, f"valuation references unknown holding {holding_id}")
                self.valuations[event_id] = event
            elif event_type == "HOLDING_TRANSFORMED":
                self.replay_holding_transformed(event)
            elif event_type == "REALIZATION":
                self.replay_realization(event)
            elif event_type == "TAX_RECONCILIATION":
                self.replay_tax_reconciliation(event)
            elif event_type == "REINVESTMENT_DEPLOYED":
                self.replay_reinvestment_deployed(event)
            elif event_type == "DISTRIBUTION_PAYMENT":
                source = event["source_event_id"]
                recipient = event["recipient_shareholder_id"]
                if recipient == self.owner_id:
                    self.error(event, "owner may not receive a shareholder distribution")
                gross = parse_exact_value(event["gross_distribution_usd"], "gross distribution")
                withholding = parse_exact_value(event["withholding_usd"], "withholding")
                net = parse_exact_value(event["net_payment_usd"], "net payment")
                if gross != withholding + net:
                    self.error(event, "gross distribution must equal withholding plus net payment")
                key = (source, recipient)
                if self.payments[key] + gross > self.obligations[key]:
                    self.error(event, "distribution payment exceeds the derived obligation")
                self.payments[key] += gross
            elif event_type == "REINVESTMENT_RELEASED_TO_OWNER":
                amount = parse_exact_value(event["amount_usd"], "release amount")
                if self.voting_holders():
                    self.error(event, "Reinvestment Capital may be released only when no non-owner shares remain")
                if amount != self.reinvestment_balance:
                    self.error(event, "release must equal the complete Reinvestment Capital balance")
                self.reinvestment_balance = Fraction(0)
            elif event_type == "FINAL_REINVESTMENT_DISTRIBUTION":
                amount = parse_exact_value(event["amount_usd"], "final distribution amount")
                if self.owner_status != "DECEASED":
                    self.error(event, "final Reinvestment Capital distribution requires owner death")
                if amount != self.reinvestment_balance:
                    self.error(event, "final distribution must equal the complete Reinvestment Capital balance")
                if any(holding.open for holding in self.holdings.values()):
                    self.error(event, "final distribution requires every remaining holding to be resolved")
                holders = self.voting_holders()
                voting_shares = sum(self.balances[holder_id] for holder_id in holders)
                if voting_shares <= 0:
                    self.error(event, "final distribution has no eligible non-owner shareholders")
                for holder_id in holders:
                    self.obligations[(event_id, holder_id)] += amount * self.balances[holder_id] / voting_shares
                self.reinvestment_balance = Fraction(0)
            elif event_type == "OWNER_STATUS_CHANGED":
                status = event["status"]
                if self.owner_status == "DECEASED":
                    self.error(event, "owner status may not change after death")
                if status == self.owner_status:
                    self.error(event, f"owner status is already {status}")
                if self.owner_status == "ACTIVE" and status not in {"INCAPACITATED", "DECEASED"}:
                    self.error(event, "invalid owner status transition")
                if self.owner_status == "INCAPACITATED" and status not in {"ACTIVE", "DECEASED"}:
                    self.error(event, "invalid owner status transition")
                self.owner_status = status
            else:
                self.error(event, f"replay is not implemented for {event_type}")

            if sum(self.balances.values()) != self.outstanding:
                self.error(event, "cap table does not equal outstanding shares")
            if self.outstanding > AUTHORIZED_SHARES:
                self.error(event, "outstanding shares exceed authorized shares")
            if any(shares < 0 for shares in self.balances.values()):
                self.error(event, "share balance became negative")
            if self.reinvestment_balance < 0:
                self.error(event, "Reinvestment Capital balance became negative")

        if not formation_seen:
            raise ValidationError("ledger has no FORMATION event")
        owner_profile = self.profiles[self.owner_id]
        require(
            owner_profile["display_name"] == self.header["owner"]["display_name"]
            and owner_profile["handle"] == self.header["owner"]["handle"],
            "header owner profile does not match the latest ledger profile",
        )

    def replay_voluntary_sale(self, event: dict):
        seller = event["seller_shareholder_id"]
        buyer = event["buyer_shareholder_id"]
        if seller == self.owner_id or seller == buyer:
            self.error(event, "invalid voluntary-sale parties")
        self.ensure_recipient(event, buyer)
        buyer_shares = event["buyer_shares"]
        sale_price = parse_exact_value(event["sale_price_usd_per_share"], "sale price")

        if event["permission_basis"] == "SPECIFIC_PERMISSION":
            permission_id = event["permission_event_id"]
            permission = self.permissions.get(permission_id)
            if permission is None or permission["revoked"]:
                self.error(event, "sale lacks an active transaction-specific permission")
            if permission["used"]:
                self.error(event, "transaction-specific permission was already used")
            if permission["seller_shareholder_id"] != seller or permission["recipient_shareholder_id"] != buyer:
                self.error(event, "transaction-specific permission names different parties")
            if permission["maximum_shares"] is not None and buyer_shares > permission["maximum_shares"]:
                self.error(event, "sale exceeds the permission's share limit")
            if permission["expires_at"] is not None:
                expires = timestamp_value(permission["expires_at"], "permission.expires_at", self.draft)
                settled = timestamp_value(event["timestamp"], "sale.timestamp", self.draft)
                if expires is not None and settled is not None and settled > expires:
                    self.error(event, "transaction-specific permission expired before settlement")
            permission["used"] = True
        else:
            if self.transfer_policy_code is None:
                self.error(event, "sale relies on a policy but no transfer policy exists")
            if self.transfer_policy_code in {"OWNER_APPROVAL_REQUIRED", "NO_VOLUNTARY_TRANSFERS"}:
                self.error(event, f"current policy {self.transfer_policy_code} does not permit this sale")
            if self.transfer_policy_code == "CURRENT_HOLDERS_ONLY" and self.balances[buyer] <= 0:
                self.error(event, "current policy permits only buyers who already hold shares")

        if self.balances[seller] <= 0:
            self.error(event, "seller owns no shares")
        if seller in self.temporary_holders:
            self.error(event, "temporary holder may not make a voluntary sale")
        seller_version = self.adoptions.get(seller, (None, None, None))[0]
        royalty_rate = ROYALTY_RATE_BY_AGREEMENT_VERSION.get(seller_version)
        if royalty_rate is None:
            self.error(event, f"validator has no royalty rules for seller agreement version {seller_version}")
        average_basis = self.holder_average_basis(seller)
        sale_result = buyer_shares * (sale_price - average_basis)
        cumulative_after = self.cumulative_sale_result[seller] + sale_result
        new_royalty_gain = max(Fraction(0), cumulative_after - self.royalty_high_water[seller])
        royalty_value = new_royalty_gain * royalty_rate
        expected_royalty_shares = royalty_value // sale_price
        if event["royalty_shares"] != expected_royalty_shares:
            self.error(event, f"royalty_shares must be {expected_royalty_shares}")
        total_surrendered = buyer_shares + event["royalty_shares"]
        self.remove_shares(event, seller, total_surrendered)
        self.add_shares(buyer, buyer_shares, sale_price)
        if event["royalty_shares"]:
            self.add_shares(self.owner_id, event["royalty_shares"], Fraction(0))
        self.cumulative_sale_result[seller] = cumulative_after
        self.royalty_high_water[seller] = max(self.royalty_high_water[seller], cumulative_after)
        self.add_benchmark_movement(buyer_shares, sale_price)

    def replay_holding_registered(self, event: dict):
        holding_id = event["holding_id"]
        if holding_id in self.holdings:
            self.error(event, f"holding {holding_id} is already registered")
        if event["registration_type"] == "OPENING" and self.commencement_event_id is not None:
            self.error(event, "opening holding was registered after commencement")
        if event["registration_type"] != "OPENING" and self.commencement_event_id is None:
            self.error(event, "non-opening holding was registered before commencement")
        cost = parse_exact_value(event["holding_cost_usd"], "holding cost")
        rc_cost = parse_exact_value(event["reinvestment_capital_funded_cost_usd"], "Reinvestment Capital cost")
        self.holdings[holding_id] = Holding(cost=cost, rc_cost=rc_cost, open=True, public_label=event["public_label"])
        self.holding_event_rc_funding[event["event_id"]] = (holding_id, rc_cost)

    def replay_holding_cost_added(self, event: dict):
        holding_id = event["holding_id"]
        holding = self.holdings.get(holding_id)
        if holding is None or not holding.open:
            self.error(event, f"cannot add cost to unknown or closed holding {holding_id}")
        cost = parse_exact_value(event["cost_added_usd"], "added cost")
        rc_cost = parse_exact_value(event["reinvestment_capital_funded_cost_usd"], "Reinvestment Capital cost")
        holding.cost += cost
        holding.rc_cost += rc_cost
        self.holding_event_rc_funding[event["event_id"]] = (holding_id, rc_cost)

    def require_valuation(self, event: dict):
        valuation_id = event.get("valuation_event_id")
        if valuation_id is not None and valuation_id not in self.valuations:
            self.error(event, f"unknown valuation event {valuation_id}")

    def replay_holding_transformed(self, event: dict):
        self.require_valuation(event)
        total_cost = Fraction(0)
        total_rc_cost = Fraction(0)
        for source in event["source_holdings"]:
            holding_id = source["holding_id"]
            holding = self.holdings.get(holding_id)
            if holding is None or not holding.open:
                self.error(event, f"unknown or closed source holding {holding_id}")
            removed = parse_exact_value(source["holding_cost_removed_usd"], "removed holding cost")
            rc_removed = parse_exact_value(source["reinvestment_capital_cost_removed_usd"], "removed RC cost")
            if removed > holding.cost or rc_removed > holding.rc_cost:
                self.error(event, f"removed cost exceeds remaining cost of {holding_id}")
            holding.cost -= removed
            holding.rc_cost -= rc_removed
            total_cost += removed
            total_rc_cost += rc_removed
            if source["closes_holding"]:
                if holding.cost != 0 or holding.rc_cost != 0:
                    self.error(event, f"closed source holding {holding_id} retains cost")
                holding.open = False
        result_cost = Fraction(0)
        result_rc_cost = Fraction(0)
        for result in event["resulting_holdings"]:
            holding_id = result["holding_id"]
            if holding_id in self.holdings:
                self.error(event, f"resulting holding ID {holding_id} already exists")
            cost = parse_exact_value(result["holding_cost_usd"], "resulting holding cost")
            rc_cost = parse_exact_value(result["reinvestment_capital_funded_cost_usd"], "resulting RC cost")
            self.holdings[holding_id] = Holding(cost=cost, rc_cost=rc_cost, open=True, public_label=result["public_label"])
            result_cost += cost
            result_rc_cost += rc_cost
        if result_cost != total_cost or result_rc_cost != total_rc_cost:
            self.error(event, "transformation does not preserve holding cost and Reinvestment Capital allocation")

    def replay_realization(self, event: dict):
        if self.commencement_event_id is None:
            self.error(event, "realization occurred before commencement")
        self.require_valuation(event)
        holding_id = event["holding_id"]
        holding = self.holdings.get(holding_id)
        if holding is None:
            self.error(event, f"unknown holding {holding_id}")
        if not holding.open and event["realization_type"] != "LATER_RECOVERY":
            self.error(event, f"closed holding {holding_id} permits only a later recovery")

        gross = parse_exact_value(event["gross_cash_proceeds_usd"], "gross cash proceeds")
        allocated_cost = parse_exact_value(event["allocated_holding_cost_usd"], "allocated holding cost")
        expenses = parse_exact_value(event["direct_transaction_expenses_usd"], "direct transaction expenses")
        taxes = parse_exact_value(event["attributable_taxes_usd"], "attributable taxes")
        if event["realization_type"] == "TERMINAL_EXIT":
            if gross != 0:
                self.error(event, "terminal exit must have zero gross cash proceeds")
        elif gross <= 0:
            self.error(event, "non-terminal realization must have positive gross cash proceeds")
        if allocated_cost > holding.cost:
            self.error(event, "allocated holding cost exceeds remaining holding cost")

        cost_before = holding.cost
        rc_cost_before = holding.rc_cost
        rc_ratio = rc_cost_before / cost_before if cost_before > 0 else Fraction(0)
        result_cost = sum(
            (parse_exact_value(item["holding_cost_usd"], "resulting holding cost") for item in event.get("resulting_holdings", [])),
            Fraction(0),
        )
        result_rc_cost = sum(
            (
                parse_exact_value(item["reinvestment_capital_funded_cost_usd"], "resulting Reinvestment Capital cost")
                for item in event.get("resulting_holdings", [])
            ),
            Fraction(0),
        )
        if allocated_cost + result_cost > holding.cost:
            self.error(event, "realization allocates more than the holding's remaining cost")
        expected_result_rc = result_cost * rc_ratio
        if result_rc_cost != expected_result_rc:
            self.error(event, "resulting holdings do not preserve proportional Reinvestment Capital cost")
        holding.cost -= allocated_cost + result_cost
        holding.rc_cost -= allocated_cost * rc_ratio + result_rc_cost
        if event["closes_holding"]:
            if holding.cost != 0 or holding.rc_cost != 0:
                self.error(event, "closed holding retains unrecovered cost")
            holding.open = False
        for result in event.get("resulting_holdings", []):
            result_id = result["holding_id"]
            if result_id in self.holdings:
                self.error(event, f"resulting holding ID {result_id} already exists")
            self.holdings[result_id] = Holding(
                cost=parse_exact_value(result["holding_cost_usd"], "resulting cost"),
                rc_cost=parse_exact_value(result["reinvestment_capital_funded_cost_usd"], "resulting RC cost"),
                open=True,
                public_label=result["public_label"],
            )

        event_value = gross - allocated_cost - expenses - taxes
        record = self.apply_realized_value(event, event_value)
        if event_value < 0 and rc_ratio > 0:
            rc_loss = min(self.reinvestment_balance, -event_value * rc_ratio)
            self.reinvestment_balance -= rc_loss
            holding.rc_loss_deficit += rc_loss
        elif event_value > 0 and holding.rc_loss_deficit > 0:
            recoverable = min(holding.rc_loss_deficit, event_value)
            governed = min(recoverable, record["non_owner_participation"])
            self.reinvestment_balance += recoverable - governed
            holding.rc_loss_deficit -= recoverable

    def replay_tax_reconciliation(self, event: dict):
        source_id = event["source_realization_event_id"]
        source = self.realization_records.get(source_id)
        if source is None:
            self.error(event, f"unknown source realization {source_id}")
        amount = parse_exact_value(event["amount_usd"], "tax reconciliation amount")
        event_value = -amount if event["reconciliation_type"] == "ADDITIONAL_TAX" else amount
        self.apply_realized_value(event, event_value)
        if event["reconciliation_type"] == "ADDITIONAL_TAX" and source["reinvest_designation"] > 0:
            adjusted_value = source["event_value"] - amount
            adjusted_cumulative = source["cumulative_before"] + adjusted_value
            adjusted_newly = max(Fraction(0), min(adjusted_value, adjusted_cumulative - source["threshold"]))
            adjusted_designation = adjusted_newly * source["non_owner_fraction"]
            total_reduction = max(Fraction(0), source["reinvest_designation"] - adjusted_designation)
            incremental_reduction = max(Fraction(0), total_reduction - source["tax_reduction"])
            reduction = min(self.reinvestment_balance, incremental_reduction)
            self.reinvestment_balance -= reduction
            source["tax_reduction"] += incremental_reduction

    def replay_reinvestment_deployed(self, event: dict):
        source_id = event["holding_event_id"]
        source = self.holding_event_rc_funding.get(source_id)
        if source is None:
            self.error(event, f"unknown holding funding event {source_id}")
        holding_id, funded_amount = source
        if holding_id != event["holding_id"]:
            self.error(event, "deployment names a different holding from its funding event")
        amount = parse_exact_value(event["amount_usd"], "deployment amount")
        if self.deployment_used[source_id] + amount > funded_amount:
            self.error(event, "deployment exceeds Reinvestment Capital funding recorded by the holding event")
        if amount > self.reinvestment_balance:
            self.error(event, "deployment exceeds the current Reinvestment Capital balance")
        self.deployment_used[source_id] += amount


def validate_document(document: Document, draft: bool, previous: Document | None = None) -> LedgerState:
    validate_header(document.header, draft)
    if draft and not document.events and previous is None:
        return LedgerState(document.header, draft)
    validate_events(document.events, draft)
    if previous is not None:
        validate_header(previous.header, draft)
        validate_events(previous.events, draft)
        validate_publication_transition(document, previous, draft)
    elif document.header["update"]["type"] == "INITIAL":
        require(
            all(event["event_type"] != "CORRECTION" for event in document.events),
            "INITIAL publication may not contain correction events",
        )
    elif document.header["update"]["type"] == "CORRECTION":
        correction_ids = document.header["update"]["correction_event_ids"]
        require(len(correction_ids) <= len(document.events), "correction_event_ids exceed the event array")
        suffix = document.events[-len(correction_ids) :]
        require(
            [event["event_id"] for event in suffix] == correction_ids
            and all(event["event_type"] == "CORRECTION" for event in suffix),
            "correction_event_ids must identify the trailing correction events",
        )
    effective_events = resolve_corrections(document.events, draft)
    state = LedgerState(document.header, draft)
    state.replay(effective_events)
    return state


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", action="store_true", help="accept the repository's explicit launch placeholders")
    parser.add_argument("--previous", type=Path, help="verify this publication against the preceding stock document")
    parser.add_argument("stock", type=Path, help="state document to validate")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        document = load_document(args.stock)
        previous = load_document(args.previous) if args.previous else None
        validate_document(document, args.draft, previous)
    except (OSError, ValidationError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
