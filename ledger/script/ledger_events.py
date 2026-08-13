#!/usr/bin/env python3
"""Validate, compile, resolve, and replay personal-stock ledger event batches."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


FORMAT = "personal-stock-ledger-batch"
FORMAT_VERSION = 1
MAX_BATCH_SIZE = 100
AUTHORIZED_SHARES = 12_000_000
EVENT_HASH_DOMAIN = "0xb4b4c34e394a16f0dafa17a0c4668fdee150079904c696f0bcbdfab3d443eb2e"

ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")
HASH_RE = re.compile(r"^0x[0-9a-fA-F]{64}$")
HOLDER_RE = re.compile(r"^holder_[0-9]{6}$")
ASSET_RE = re.compile(r"^asset_[0-9]{6}$")
EVENT_TYPE_RE = re.compile(r"^[A-Z][A-Z0-9_]{0,31}$")
TIMESTAMP_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
DECIMAL_RE = re.compile(r"^(0|[1-9][0-9]*)(\.[0-9]+)?$")
SIGNED_DECIMAL_RE = re.compile(r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?$")
AGREEMENT_VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")

OVERLAY_TYPES = {
    "EVENT_SUPPLEMENT",
    "EVENT_REVISION",
    "EVENT_VOID",
    "EVENT_INSERTION",
}


class ValidationError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def exact_keys(
    value: dict[str, Any], required: set[str], optional: set[str], path: str
) -> None:
    missing = required - value.keys()
    extra = value.keys() - required - optional
    require(not missing, f"{path} missing fields: {', '.join(sorted(missing))}")
    require(not extra, f"{path} has unknown fields: {', '.join(sorted(extra))}")


def expect_object(value: Any, path: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{path} must be an object")
    return value


def expect_array(value: Any, path: str, *, nonempty: bool = False) -> list[Any]:
    require(isinstance(value, list), f"{path} must be an array")
    if nonempty:
        require(bool(value), f"{path} must not be empty")
    return value


def expect_string(value: Any, path: str, *, nonempty: bool = True) -> str:
    require(isinstance(value, str), f"{path} must be a string")
    if nonempty:
        require(bool(value), f"{path} must not be empty")
    return value


def expect_int(value: Any, path: str, *, minimum: int = 0, maximum: int | None = None) -> int:
    require(type(value) is int, f"{path} must be an integer")
    require(value >= minimum, f"{path} must be at least {minimum}")
    if maximum is not None:
        require(value <= maximum, f"{path} must be at most {maximum}")
    return value


def expect_pattern(value: Any, pattern: re.Pattern[str], path: str) -> str:
    text = expect_string(value, path)
    require(pattern.fullmatch(text) is not None, f"invalid {path}: {text}")
    return text


def expect_timestamp(value: Any, path: str) -> tuple[str, int]:
    text = expect_pattern(value, TIMESTAMP_RE, path)
    try:
        parsed = datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as error:
        raise ValidationError(f"invalid {path}: {text}") from error
    seconds = int(parsed.timestamp())
    require(0 < seconds <= (2**64 - 1), f"{path} is outside the uint64 range")
    return text, seconds


def expect_holder(value: Any, path: str) -> str:
    return expect_pattern(value, HOLDER_RE, path)


def expect_asset(value: Any, path: str) -> str:
    return expect_pattern(value, ASSET_RE, path)


def expect_hash(value: Any, path: str) -> str:
    return expect_pattern(value, HASH_RE, path)


def expect_amount(value: Any, path: str, *, positive: bool = False) -> Fraction:
    text = expect_pattern(value, DECIMAL_RE, path)
    result = Fraction(text)
    if positive:
        require(result > 0, f"{path} must be positive")
    return result


def expect_signed_amount(value: Any, path: str) -> Fraction:
    text = expect_pattern(value, SIGNED_DECIMAL_RE, path)
    result = Fraction(text)
    require(text != "-0" and not text.startswith("-0."), f"{path} must not use negative zero")
    return result


def reject_floats(value: Any, path: str = "data") -> None:
    if isinstance(value, float):
        raise ValidationError(f"{path} may not contain binary floating-point numbers")
    if isinstance(value, dict):
        for key, item in value.items():
            reject_floats(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_floats(item, f"{path}[{index}]")


@dataclass(frozen=True)
class RawEvent:
    sequence: int
    event_type: str
    schema_version: int
    effective_at: str
    effective_at_unix: int
    data: dict[str, Any]


@dataclass(frozen=True)
class Batch:
    path: Path
    chain_id: int
    stock_contract: str
    expected_event_count: int
    expected_head: str
    events: list[RawEvent]


@dataclass
class EffectiveEvent:
    logical_sequence: int
    source_sequence: int
    event_type: str
    schema_version: int
    effective_at: str
    data: dict[str, Any]
    supplements: dict[str, dict[str, Any]] = field(default_factory=dict)


@dataclass
class State:
    owner_id: str | None = None
    profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    adoptions: dict[str, tuple[str, str]] = field(default_factory=dict)
    governing_agreement: tuple[str, str] | None = None
    assets: dict[str, dict[str, Any]] = field(default_factory=dict)
    opening_items: list[dict[str, Any]] = field(default_factory=list)
    commencement_time: str | None = None
    portfolio_net_gain_usd: str | None = None
    portfolio_peak_usd: str | None = None
    cpi_2026_06: str | None = None
    balances: dict[str, int] = field(default_factory=dict)
    outstanding: int = 0
    owner_opening_issuance_recorded: bool = False

    def as_json(self) -> dict[str, Any]:
        return {
            "owner_id": self.owner_id,
            "profiles": self.profiles,
            "adoptions": {
                holder: {"agreement_version": value[0], "agreement_content_hash": value[1]}
                for holder, value in sorted(self.adoptions.items())
            },
            "governing_agreement": (
                {
                    "agreement_version": self.governing_agreement[0],
                    "agreement_content_hash": self.governing_agreement[1],
                }
                if self.governing_agreement is not None
                else None
            ),
            "assets": dict(sorted(self.assets.items())),
            "opening_items": self.opening_items,
            "commencement_time": self.commencement_time,
            "portfolio_net_gain_usd": self.portfolio_net_gain_usd,
            "portfolio_peak_usd": self.portfolio_peak_usd,
            "cpi_2026_06": self.cpi_2026_06,
            "balances": dict(sorted(self.balances.items())),
            "outstanding": self.outstanding,
        }


def load_batch(path: Path, *, allow_large_journal: bool = False) -> Batch:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValidationError(f"{path} is not valid UTF-8") from error
    try:
        source = json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except json.JSONDecodeError as error:
        raise ValidationError(f"invalid JSON: {error}") from error

    source = expect_object(source, "batch")
    exact_keys(
        source,
        {
            "format",
            "format_version",
            "chain_id",
            "stock_contract",
            "expected_event_count",
            "expected_head",
            "events",
        },
        set(),
        "batch",
    )
    require(source["format"] == FORMAT, f'batch.format must be "{FORMAT}"')
    format_version = expect_int(source["format_version"], "batch.format_version", minimum=1)
    require(format_version == FORMAT_VERSION, "unsupported format_version")
    chain_id = expect_int(source["chain_id"], "batch.chain_id", minimum=1)
    stock_contract = expect_pattern(source["stock_contract"], ADDRESS_RE, "batch.stock_contract")
    expected_count = expect_int(source["expected_event_count"], "batch.expected_event_count")
    expected_head = expect_hash(source["expected_head"], "batch.expected_head")
    if expected_count == 0:
        require(int(expected_head, 16) == 0, "an empty ledger must have a zero expected_head")
    else:
        require(int(expected_head, 16) != 0, "a nonempty ledger must have a nonzero expected_head")

    source_events = expect_array(source["events"], "batch.events", nonempty=True)
    if not allow_large_journal:
        require(len(source_events) <= MAX_BATCH_SIZE, f"a batch may contain at most {MAX_BATCH_SIZE} events")
    events: list[RawEvent] = []
    for index, source_event in enumerate(source_events):
        sequence = expected_count + index + 1
        events.append(validate_event(source_event, sequence, f"batch.events[{index}]"))

    if expected_count == 0:
        require(events[0].event_type == "FORMATION", "the first ledger event must be FORMATION")
    for event in events:
        if event.event_type == "FORMATION":
            require(event.sequence == 1, "FORMATION must be sequence 1")
    validate_overlay_references(events, expected_count)
    return Batch(path, chain_id, stock_contract, expected_count, expected_head, events)


def validate_event(value: Any, sequence: int, path: str, *, embedded: bool = False) -> RawEvent:
    event = expect_object(value, path)
    exact_keys(event, {"event_type", "schema_version", "effective_at", "data"}, set(), path)
    event_type = expect_pattern(event["event_type"], EVENT_TYPE_RE, f"{path}.event_type")
    schema_version = expect_int(
        event["schema_version"], f"{path}.schema_version", minimum=1, maximum=2**32 - 1
    )
    effective_at, effective_at_unix = expect_timestamp(event["effective_at"], f"{path}.effective_at")
    data = expect_object(event["data"], f"{path}.data")
    reject_floats(data, f"{path}.data")
    require(not embedded or event_type not in OVERLAY_TYPES, f"{path} may not embed an overlay event")
    validate_event_data(event_type, schema_version, data, sequence, f"{path}.data")
    return RawEvent(sequence, event_type, schema_version, effective_at, effective_at_unix, data)


def data_keys(
    data: dict[str, Any], required: set[str], optional: set[str], path: str
) -> None:
    exact_keys(data, required, optional | {"public_note"}, path)
    if "public_note" in data:
        expect_string(data["public_note"], f"{path}.public_note", nonempty=False)


def validate_event_data(
    event_type: str, schema_version: int, data: dict[str, Any], sequence: int, path: str
) -> None:
    require(schema_version == 1, f"unsupported {event_type} schema version {schema_version}")

    if event_type == "FORMATION":
        data_keys(
            data,
            {"owner_shareholder_id", "owner_display_name", "owner_handle"},
            set(),
            path,
        )
        expect_holder(data["owner_shareholder_id"], f"{path}.owner_shareholder_id")
        expect_string(data["owner_display_name"], f"{path}.owner_display_name")
        if data["owner_handle"] is not None:
            expect_string(data["owner_handle"], f"{path}.owner_handle")
    elif event_type == "SHAREHOLDER_REGISTERED":
        data_keys(data, {"shareholder_id", "display_name", "handle"}, set(), path)
        expect_holder(data["shareholder_id"], f"{path}.shareholder_id")
        expect_string(data["display_name"], f"{path}.display_name")
        if data["handle"] is not None:
            expect_string(data["handle"], f"{path}.handle")
    elif event_type == "AGREEMENT_ADOPTION":
        data_keys(
            data,
            {"shareholder_id", "agreement_version", "agreement_content_hash"},
            set(),
            path,
        )
        expect_holder(data["shareholder_id"], f"{path}.shareholder_id")
        expect_pattern(
            data["agreement_version"],
            AGREEMENT_VERSION_RE,
            f"{path}.agreement_version",
        )
        expect_hash(data["agreement_content_hash"], f"{path}.agreement_content_hash")
    elif event_type == "ASSET_REGISTERED":
        data_keys(
            data,
            {"asset_id", "asset_category", "description", "acquired_at", "opening_asset"},
            set(),
            path,
        )
        expect_asset(data["asset_id"], f"{path}.asset_id")
        expect_string(data["asset_category"], f"{path}.asset_category")
        if data["description"] is not None:
            expect_string(data["description"], f"{path}.description")
        expect_timestamp(data["acquired_at"], f"{path}.acquired_at")
        require(type(data["opening_asset"]) is bool, f"{path}.opening_asset must be a boolean")
    elif event_type == "OPENING_PORTFOLIO_ITEM":
        data_keys(data, {"asset_id", "item_type", "amount_usd", "occurred_at"}, set(), path)
        expect_asset(data["asset_id"], f"{path}.asset_id")
        require(
            data["item_type"] in {"ELIGIBLE_COST", "CASH_EVENT"},
            f'{path}.item_type must be "ELIGIBLE_COST" or "CASH_EVENT"',
        )
        expect_amount(data["amount_usd"], f"{path}.amount_usd", positive=True)
        expect_timestamp(data["occurred_at"], f"{path}.occurred_at")
    elif event_type == "PORTFOLIO_COMMENCEMENT":
        data_keys(
            data,
            {"opening_portfolio_net_gain_usd", "opening_item_count", "cpi_2026_06"},
            set(),
            path,
        )
        opening_balance = expect_signed_amount(
            data["opening_portfolio_net_gain_usd"],
            f"{path}.opening_portfolio_net_gain_usd",
        )
        require(opening_balance <= 0, f"{path}.opening_portfolio_net_gain_usd must not be positive")
        expect_int(data["opening_item_count"], f"{path}.opening_item_count")
        expect_amount(data["cpi_2026_06"], f"{path}.cpi_2026_06", positive=True)
    elif event_type in {"SHARE_ISSUANCE", "OWNER_TRANSFER"}:
        data_keys(data, {"recipient_shareholder_id", "shares", "actual_cash_paid_usd"}, set(), path)
        expect_holder(data["recipient_shareholder_id"], f"{path}.recipient_shareholder_id")
        expect_int(data["shares"], f"{path}.shares", minimum=1)
        expect_amount(data["actual_cash_paid_usd"], f"{path}.actual_cash_paid_usd")
    elif event_type == "BUYOUT":
        data_keys(
            data,
            {
                "seller_shareholder_id",
                "purchaser_shareholder_id",
                "shares",
                "settlement_price_usd_per_share",
            },
            set(),
            path,
        )
        expect_holder(data["seller_shareholder_id"], f"{path}.seller_shareholder_id")
        expect_holder(data["purchaser_shareholder_id"], f"{path}.purchaser_shareholder_id")
        expect_int(data["shares"], f"{path}.shares", minimum=1)
        expect_amount(
            data["settlement_price_usd_per_share"],
            f"{path}.settlement_price_usd_per_share",
            positive=True,
        )
    elif event_type == "EVENT_SUPPLEMENT":
        data_keys(
            data,
            {
                "target_sequence",
                "extension_type",
                "extension_schema_version",
                "extension_data",
                "reason",
            },
            {"supersedes_sequence"},
            path,
        )
        expect_prior_sequence(data["target_sequence"], sequence, f"{path}.target_sequence")
        expect_pattern(data["extension_type"], EVENT_TYPE_RE, f"{path}.extension_type")
        expect_int(
            data["extension_schema_version"],
            f"{path}.extension_schema_version",
            minimum=1,
            maximum=2**32 - 1,
        )
        extension = expect_object(data["extension_data"], f"{path}.extension_data")
        require(bool(extension), f"{path}.extension_data must not be empty")
        expect_string(data["reason"], f"{path}.reason")
        validate_optional_supersedes(data, sequence, path)
    elif event_type == "EVENT_REVISION":
        data_keys(
            data,
            {"target_sequence", "replacement", "reason"},
            {"supersedes_sequence", "after_sequence"},
            path,
        )
        expect_prior_sequence(data["target_sequence"], sequence, f"{path}.target_sequence")
        validate_event(data["replacement"], sequence, f"{path}.replacement", embedded=True)
        expect_string(data["reason"], f"{path}.reason")
        validate_optional_supersedes(data, sequence, path)
        if "after_sequence" in data:
            after = expect_prior_sequence(data["after_sequence"], sequence, f"{path}.after_sequence")
            require(after != data["target_sequence"], f"{path}.after_sequence may not be the target itself")
    elif event_type == "EVENT_VOID":
        data_keys(data, {"target_sequence", "reason"}, {"supersedes_sequence"}, path)
        expect_prior_sequence(data["target_sequence"], sequence, f"{path}.target_sequence")
        expect_string(data["reason"], f"{path}.reason")
        validate_optional_supersedes(data, sequence, path)
    elif event_type == "EVENT_INSERTION":
        data_keys(data, {"after_sequence", "inserted", "reason"}, set(), path)
        expect_prior_sequence(data["after_sequence"], sequence, f"{path}.after_sequence")
        validate_event(data["inserted"], sequence, f"{path}.inserted", embedded=True)
        expect_string(data["reason"], f"{path}.reason")
    else:
        raise ValidationError(f"unsupported event type: {event_type}")


def expect_prior_sequence(value: Any, sequence: int, path: str) -> int:
    result = expect_int(value, path, minimum=1)
    require(result < sequence, f"{path} must identify a prior ledger sequence")
    return result


def validate_optional_supersedes(data: dict[str, Any], sequence: int, path: str) -> None:
    if "supersedes_sequence" in data:
        expect_prior_sequence(data["supersedes_sequence"], sequence, f"{path}.supersedes_sequence")


def validate_overlay_references(events: list[RawEvent], expected_count: int) -> None:
    available_nodes: set[int] = set(range(1, expected_count + 1))
    mutation_heads: dict[int, int] = {}
    supplement_heads: dict[tuple[int, str], int] = {}

    for event in events:
        data = event.data
        if event.event_type not in OVERLAY_TYPES:
            available_nodes.add(event.sequence)
            continue
        if event.event_type == "EVENT_INSERTION":
            require(
                data["after_sequence"] in available_nodes,
                f"event {event.sequence} insertion anchor does not identify an effective event",
            )
            available_nodes.add(event.sequence)
            continue

        target = data["target_sequence"]
        require(target in available_nodes, f"event {event.sequence} target does not identify an effective event")
        supplied = data.get("supersedes_sequence")
        if event.event_type == "EVENT_SUPPLEMENT":
            key = (target, data["extension_type"])
            current = supplement_heads.get(key)
            if target > expected_count or current is not None:
                require(
                    supplied == current,
                    f"event {event.sequence} must supersede the active supplement {current}",
                )
            supplement_heads[key] = event.sequence
        else:
            current = mutation_heads.get(target)
            if target > expected_count or current is not None:
                require(
                    supplied == current,
                    f"event {event.sequence} must supersede the active revision/void {current}",
                )
            mutation_heads[target] = event.sequence


def canonical_payload(data: dict[str, Any]) -> bytes:
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def event_type_bytes32(event_type: str) -> str:
    encoded = event_type.encode("ascii")
    require(len(encoded) <= 32, f"event type is longer than 32 bytes: {event_type}")
    return "0x" + encoded.hex().ljust(64, "0")


def event_hash_preimage(
    chain_id: int,
    stock_contract: str,
    sequence: int,
    event_type: str,
    schema_version: int,
    effective_at_unix: int,
    payload_hash: str,
    previous_head: str,
) -> str:
    """Return abi.encode(...) bytes for StockLedger's event hash."""

    words = [
        EVENT_HASH_DOMAIN[2:],
        format(chain_id, "064x"),
        stock_contract[2:].lower().rjust(64, "0"),
        format(sequence, "064x"),
        event_type_bytes32(event_type)[2:],
        format(schema_version, "064x"),
        format(effective_at_unix, "064x"),
        payload_hash[2:].lower(),
        previous_head[2:].lower(),
    ]
    require(all(len(item) == 64 for item in words), "invalid event hash input width")
    return "0x" + "".join(words)


def compile_batch(batch: Batch) -> dict[str, Any]:
    return {
        "format": "personal-stock-ledger-compiled-batch",
        "format_version": 1,
        "chain_id": batch.chain_id,
        "stock_contract": batch.stock_contract,
        "expected_event_count": batch.expected_event_count,
        "expected_head": batch.expected_head,
        "event_count": len(batch.events),
        "events": [
            {
                "event_type": event_type_bytes32(event.event_type),
                "schema_version": event.schema_version,
                "effective_at": event.effective_at_unix,
                "payload": "0x" + canonical_payload(event.data).hex(),
            }
            for event in batch.events
        ],
    }


def embedded_event(value: dict[str, Any], logical_sequence: int, source_sequence: int) -> EffectiveEvent:
    timestamp, _ = expect_timestamp(value["effective_at"], "embedded.effective_at")
    return EffectiveEvent(
        logical_sequence,
        source_sequence,
        value["event_type"],
        value["schema_version"],
        timestamp,
        value["data"],
    )


def resolve_events(events: list[RawEvent]) -> list[EffectiveEvent]:
    require(bool(events) and events[0].sequence == 1, "resolution requires the complete ledger from sequence 1")
    nodes: dict[int, EffectiveEvent] = {}
    base_sequences: list[int] = []
    children: dict[int, list[int]] = {}
    parent: dict[int, int] = {}
    placement_sequence: dict[int, int] = {}
    mutations: dict[int, RawEvent] = {}
    supplements: dict[tuple[int, str], RawEvent] = {}

    for raw in events:
        if raw.event_type not in OVERLAY_TYPES:
            nodes[raw.sequence] = EffectiveEvent(
                raw.sequence,
                raw.sequence,
                raw.event_type,
                raw.schema_version,
                raw.effective_at,
                raw.data,
            )
            base_sequences.append(raw.sequence)
        elif raw.event_type == "EVENT_INSERTION":
            nodes[raw.sequence] = embedded_event(raw.data["inserted"], raw.sequence, raw.sequence)
            anchor = raw.data["after_sequence"]
            children.setdefault(anchor, []).append(raw.sequence)
            parent[raw.sequence] = anchor
            placement_sequence[raw.sequence] = raw.sequence
        elif raw.event_type == "EVENT_SUPPLEMENT":
            supplements[(raw.data["target_sequence"], raw.data["extension_type"])] = raw
        else:
            mutations[raw.data["target_sequence"]] = raw

    for target, mutation in mutations.items():
        if mutation.event_type == "EVENT_VOID":
            nodes[target].source_sequence = mutation.sequence
            nodes[target].event_type = ""
        else:
            replacement = embedded_event(mutation.data["replacement"], target, mutation.sequence)
            nodes[target] = replacement
            if "after_sequence" in mutation.data:
                if target in base_sequences:
                    base_sequences.remove(target)
                elif target in parent:
                    children[parent[target]].remove(target)
                anchor = mutation.data["after_sequence"]
                children.setdefault(anchor, []).append(target)
                parent[target] = anchor
                placement_sequence[target] = mutation.sequence

    for (target, extension_type), supplement in supplements.items():
        nodes[target].supplements[extension_type] = {
            "schema_version": supplement.data["extension_schema_version"],
            "data": supplement.data["extension_data"],
            "source_sequence": supplement.sequence,
        }

    result: list[EffectiveEvent] = []
    visiting: set[int] = set()
    visited: set[int] = set()

    def visit(sequence: int) -> None:
        require(sequence not in visiting, f"event placement cycle involving sequence {sequence}")
        require(sequence not in visited, f"event {sequence} is placed more than once")
        visiting.add(sequence)
        node = nodes[sequence]
        if node.event_type:
            result.append(node)
        for child in sorted(children.get(sequence, []), key=lambda item: placement_sequence[item]):
            visit(child)
        visiting.remove(sequence)
        visited.add(sequence)

    for sequence in base_sequences:
        visit(sequence)
    require(visited == nodes.keys(), "one or more effective events are unreachable after placement")
    effective_times = [
        expect_timestamp(event.effective_at, f"effective event {event.logical_sequence}.effective_at")[1]
        for event in result
    ]
    require(
        effective_times == sorted(effective_times),
        "effective event order is not chronological; revise the event with after_sequence",
    )
    return result


def replay(events: list[EffectiveEvent]) -> State:
    state = State()
    for event in events:
        data = event.data
        path = f"effective event {event.logical_sequence}"
        if event.event_type == "FORMATION":
            require(state.owner_id is None, f"{path}: duplicate formation")
            owner_id = data["owner_shareholder_id"]
            state.owner_id = owner_id
            state.profiles[owner_id] = {
                "display_name": data["owner_display_name"],
                "handle": data["owner_handle"],
            }
            state.balances[owner_id] = 0
        elif event.event_type == "SHAREHOLDER_REGISTERED":
            holder = data["shareholder_id"]
            require(holder not in state.profiles, f"{path}: shareholder is already registered")
            state.profiles[holder] = {"display_name": data["display_name"], "handle": data["handle"]}
            state.balances[holder] = 0
        elif event.event_type == "AGREEMENT_ADOPTION":
            holder = data["shareholder_id"]
            require(holder in state.profiles, f"{path}: shareholder is not registered")
            require(holder not in state.adoptions, f"{path}: shareholder already adopted an agreement")
            adoption = (data["agreement_version"], data["agreement_content_hash"])
            state.adoptions[holder] = adoption
            if holder == state.owner_id:
                require(
                    state.commencement_time is None,
                    f"{path}: owner's initial adoption must precede commencement",
                )
                state.governing_agreement = adoption
            else:
                require(
                    adoption == state.governing_agreement,
                    f"{path}: shareholder did not adopt the governing agreement",
                )
        elif event.event_type == "ASSET_REGISTERED":
            asset_id = data["asset_id"]
            require(asset_id not in state.assets, f"{path}: asset is already registered")
            if state.commencement_time is None:
                require(data["opening_asset"], f"{path}: a pre-commencement asset must be opening_asset")
            else:
                require(not data["opening_asset"], f"{path}: an opening asset must precede commencement")
            state.assets[asset_id] = {
                "asset_category": data["asset_category"],
                "description": data["description"],
                "acquired_at": data["acquired_at"],
                "opening_asset": data["opening_asset"],
            }
        elif event.event_type == "OPENING_PORTFOLIO_ITEM":
            require(state.commencement_time is None, f"{path}: opening item recorded after commencement")
            asset_id = data["asset_id"]
            require(asset_id in state.assets, f"{path}: opening item references an unknown asset")
            require(state.assets[asset_id]["opening_asset"], f"{path}: item asset is not an opening asset")
            if state.opening_items:
                prior_time = state.opening_items[-1]["occurred_at"]
                require(data["occurred_at"] >= prior_time, f"{path}: opening items are not chronological")
            state.opening_items.append(
                {
                    "asset_id": asset_id,
                    "item_type": data["item_type"],
                    "amount_usd": data["amount_usd"],
                    "occurred_at": data["occurred_at"],
                }
            )
        elif event.event_type == "PORTFOLIO_COMMENCEMENT":
            require(state.commencement_time is None, f"{path}: duplicate portfolio commencement")
            require(state.governing_agreement is not None, f"{path}: owner has not adopted an agreement")
            require(
                data["opening_item_count"] == len(state.opening_items),
                f"{path}: opening_item_count does not match recorded items",
            )
            for asset_id, asset in state.assets.items():
                if asset["opening_asset"]:
                    require(
                        asset["acquired_at"] <= event.effective_at,
                        f"{path}: opening asset {asset_id} was acquired after commencement",
                    )
            for item in state.opening_items:
                require(
                    item["occurred_at"] <= event.effective_at,
                    f"{path}: opening item occurred after commencement",
                )
            calculated = Fraction(0)
            for item in state.opening_items:
                amount = Fraction(item["amount_usd"])
                if item["item_type"] == "ELIGIBLE_COST":
                    calculated -= amount
                else:
                    calculated = min(Fraction(0), calculated + amount)
            declared = Fraction(data["opening_portfolio_net_gain_usd"])
            require(calculated == declared, f"{path}: opening portfolio net gain does not match items")
            state.commencement_time = event.effective_at
            state.portfolio_net_gain_usd = data["opening_portfolio_net_gain_usd"]
            state.portfolio_peak_usd = "0"
            state.cpi_2026_06 = data["cpi_2026_06"]
        elif event.event_type == "SHARE_ISSUANCE":
            recipient = data["recipient_shareholder_id"]
            require(recipient in state.profiles, f"{path}: recipient is not registered")
            require(state.governing_agreement is not None, f"{path}: owner has not adopted an agreement")
            require(state.commencement_time is not None, f"{path}: portfolio has not commenced")
            require(
                state.adoptions.get(recipient) == state.governing_agreement,
                f"{path}: recipient has not adopted the governing agreement",
            )
            if recipient == state.owner_id:
                require(state.outstanding == 0, f"{path}: owner may receive shares only at commencement")
                require(
                    event.effective_at == state.commencement_time,
                    f"{path}: owner's opening issuance must be effective at commencement",
                )
                state.owner_opening_issuance_recorded = True
            state.balances[recipient] += data["shares"]
            state.outstanding += data["shares"]
            require(state.outstanding <= AUTHORIZED_SHARES, f"{path}: authorized share count exceeded")
        elif event.event_type == "OWNER_TRANSFER":
            recipient = data["recipient_shareholder_id"]
            require(recipient in state.profiles, f"{path}: recipient is not registered")
            require(
                state.adoptions.get(recipient) == state.governing_agreement,
                f"{path}: recipient has not adopted the governing agreement",
            )
            require(state.owner_id is not None, f"{path}: missing owner")
            require(state.balances[state.owner_id] >= data["shares"], f"{path}: insufficient owner shares")
            state.balances[state.owner_id] -= data["shares"]
            state.balances[recipient] += data["shares"]
        elif event.event_type == "BUYOUT":
            seller = data["seller_shareholder_id"]
            purchaser = data["purchaser_shareholder_id"]
            require(seller != state.owner_id, f"{path}: owner cannot be bought out")
            require(purchaser != seller, f"{path}: purchaser and seller must differ")
            require(seller in state.profiles and purchaser in state.profiles, f"{path}: unknown holder")
            if purchaser != state.owner_id:
                require(
                    state.adoptions.get(purchaser) == state.governing_agreement,
                    f"{path}: purchaser has not adopted the governing agreement",
                )
            require(state.balances[seller] >= data["shares"], f"{path}: insufficient seller shares")
            state.balances[seller] -= data["shares"]
            state.balances[purchaser] += data["shares"]
        else:
            raise ValidationError(f"{path}: reducer does not support {event.event_type}")
    require(state.owner_id is not None, "effective history has no formation event")
    require(state.governing_agreement is not None, "effective history has no owner agreement adoption")
    require(state.commencement_time is not None, "effective history has no portfolio commencement")
    require(state.owner_opening_issuance_recorded, "effective history has no owner opening issuance")
    require(sum(state.balances.values()) == state.outstanding, "cap table does not equal outstanding shares")
    return state


def effective_json(event: EffectiveEvent) -> dict[str, Any]:
    return {
        "logical_sequence": event.logical_sequence,
        "source_sequence": event.source_sequence,
        "event_type": event.event_type,
        "schema_version": event.schema_version,
        "effective_at": event.effective_at,
        "data": event.data,
        "supplements": event.supplements,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--compile", dest="compiled_path", type=Path)
    parser.add_argument("--print-effective", action="store_true")
    parser.add_argument("--print-state", action="store_true")
    args = parser.parse_args(argv)

    try:
        batch = load_batch(
            args.batch,
            allow_large_journal=args.print_effective or args.print_state,
        )
        if args.compiled_path:
            args.compiled_path.write_text(
                json.dumps(compile_batch(batch), indent=2) + "\n", encoding="utf-8"
            )
        if args.print_effective or args.print_state:
            require(
                batch.expected_event_count == 0,
                "effective history and state require a complete ledger beginning at sequence 1",
            )
            effective = resolve_events(batch.events)
            if args.print_effective:
                print(json.dumps([effective_json(event) for event in effective], indent=2))
            if args.print_state:
                print(json.dumps(replay(effective).as_json(), indent=2))
        if not args.print_effective and not args.print_state:
            start = batch.expected_event_count + 1
            end = batch.expected_event_count + len(batch.events)
            print(f"valid ledger batch: sequences {start}-{end}")
        return 0
    except (OSError, ValidationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
