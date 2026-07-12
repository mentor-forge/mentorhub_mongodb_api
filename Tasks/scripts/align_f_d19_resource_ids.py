#!/usr/bin/env python3
"""F-D19: align Journey resource_id values and Journey/Event id references."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEST_DATA = REPO_ROOT / "configurator" / "test_data"

JOURNEY_ID_MAP = {
    "D00000000000000000000001": "A00000000000000000000002",
    "D00000000000000000000002": "A00000000000000000000003",
    "D00000000000000000000003": "A00000000000000000000004",
    "D00000000000000000000004": "A00000000000000000000005",
    "D00000000000000000000006": "A00000000000000000000014",
}

REMOVED_JOURNEY_IDS = {
    "D00000000000000000000005",
    "D00000000000000000000007",
}


def load_json(path: Path) -> list | dict:
    return json.loads(path.read_text())


def save_json(path: Path, data: list | dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")


def resource_name_lookup() -> dict[str, str]:
    resources = load_json(TEST_DATA / "Resource.0.1.0.0.json")
    return {item["name"]: item["_id"]["$oid"] for item in resources if item.get("name")}


def to_oid(value: str, by_name: dict[str, str]) -> dict[str, str]:
    if re.fullmatch(r"[A-Fa-f0-9]{24}", value):
        return {"$oid": value.upper()}
    if value not in by_name:
        raise KeyError(f"Unknown resource name: {value}")
    return {"$oid": by_name[value]}


def migrate_journeys(by_name: dict[str, str]) -> list[dict]:
    journeys = load_json(TEST_DATA / "Journey.0.1.0.0.json")
    updated: list[dict] = []

    for journey in journeys:
        journey_id = journey["_id"]["$oid"].upper()
        if journey_id in REMOVED_JOURNEY_IDS:
            continue

        profile_id = journey.get("profile_id", {}).get("$oid", "").upper()
        if profile_id:
            new_id = profile_id
            journey["_id"] = {"$oid": new_id}
            journey["profile_id"] = {"$oid": new_id}
        else:
            new_id = journey_id

        for item in journey.get("now", []):
            resource_id = item.get("resource_id")
            if isinstance(resource_id, str):
                item["resource_id"] = to_oid(resource_id, by_name)
            elif isinstance(resource_id, dict) and "$oid" in resource_id:
                resource_id["$oid"] = resource_id["$oid"].upper()

        updated.append(journey)

    return updated


def replace_oid_values(node: object, id_map: dict[str, str]) -> object:
    if isinstance(node, dict):
        if set(node.keys()) == {"$oid"}:
            oid = node["$oid"].upper()
            if oid in id_map:
                return {"$oid": id_map[oid]}
            return node
        return {key: replace_oid_values(value, id_map) for key, value in node.items()}
    if isinstance(node, list):
        return [replace_oid_values(item, id_map) for item in node]
    return node


def journey_id_in_event(event: dict) -> str | None:
    context = event.get("context", {})
    journey_id = context.get("journey_id")
    if isinstance(journey_id, dict):
        return journey_id.get("$oid", "").upper()
    return None


def migrate_events() -> list[dict]:
    events = load_json(TEST_DATA / "Event.0.1.0.0.json")
    filtered: list[dict] = []

    for event in events:
        journey_id = journey_id_in_event(event)
        if journey_id in REMOVED_JOURNEY_IDS:
            continue
        filtered.append(replace_oid_values(event, JOURNEY_ID_MAP))

    return filtered


def main() -> None:
    by_name = resource_name_lookup()
    journeys = migrate_journeys(by_name)
    save_json(TEST_DATA / "Journey.0.1.0.0.json", journeys)

    events = migrate_events()
    save_json(TEST_DATA / "Event.0.1.0.0.json", events)

    print(f"Journey documents: {len(journeys)}")
    print(f"Event documents: {len(events)}")


if __name__ == "__main__":
    main()
