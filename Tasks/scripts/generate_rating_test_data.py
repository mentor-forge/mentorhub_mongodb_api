#!/usr/bin/env python3
"""Compute and apply library ratings onto Journey documents (T120/T125).

DEPRECATED for Rating.0.1.0.0.json: ratings now live on Journey library entries.
Use apply_journey_library_ratings_from_rating.py to copy existing T120 Rating values,
or run this script to recompute ratings directly onto Journey library entries.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
JOURNEY_PATH = REPO / "configurator" / "test_data" / "Journey.0.1.0.0.json"
RESOURCE_PATH = REPO / "configurator" / "test_data" / "Resource.0.1.0.0.json"

PROFILE_NAMES = {
    "A00000000000000000000002": "daniel",
    "A00000000000000000000003": "lucky",
    "A00000000000000000000004": "mary",
    "A00000000000000000000005": "luther",
    "A00000000000000000000010": "riley",
    "A00000000000000000000014": "taylor",
    "A00000000000000000000015": "casey",
}

MENTEE_ORDER = [
    "daniel",
    "lucky",
    "mary",
    "luther",
    "riley",
    "taylor",
    "casey",
]

TIER = {
    "daniel": 0,
    "riley": 0,
    "lucky": 1,
    "taylor": 1,
    "casey": 1,
    "mary": 2,
    "luther": 3,
}

SKILL_RANK = {
    "Candidate": 0,
    "Apprentice": 1,
    "Practioneer": 2,
    "Craftsperson": 3,
    "Master": 4,
    "Distinguished": 5,
}

COST_RANK = {
    "free": 0,
    "$": 1,
    "$$": 2,
    "$$$": 3,
    "S$": 1,
    "S$$": 2,
    "S$$$": 3,
}

TYPE_RANK = {
    "article": 0,
    "video": 0,
    "tutorial": 0,
    "getting-started": 0,
    "lesson": 0,
    "book": 1,
    "membership": 2,
    "online-class": 1,
}


def rating_oid(serial: int) -> dict[str, str]:
    return {"$oid": f"D{serial + 7:023d}"}


def parse_date(value: dict) -> datetime:
    return datetime.fromisoformat(value["$date"].replace("Z", "+00:00"))


def format_date(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def resource_difficulty(resource: dict) -> int:
    skill = SKILL_RANK.get(resource.get("skill_level", "Practioneer"), 2)
    cost = COST_RANK.get(resource.get("cost", "free"), 0)
    rtype = TYPE_RANK.get(resource.get("type", "article"), 0)
    return max(0, (skill - 1) // 2 + cost // 2 + rtype)


def compute_rating(profile_name: str, resource: dict, lib_index: int) -> int:
    tier = TIER[profile_name]
    difficulty = resource_difficulty(resource)
    mentee_index = MENTEE_ORDER.index(profile_name)

    score = 2 + min(1, tier // 2)
    if difficulty <= 1 and tier >= 2:
        score += 1
    if difficulty >= 2 and tier <= 1:
        score -= 1
    if difficulty >= 3 and tier <= 2:
        score -= 1
    if resource.get("type") == "book" and tier <= 1:
        score -= 1
    if resource.get("cost") in ("$$$", "S$$$") and tier <= 1:
        score -= 1
    if tier >= 3 and lib_index >= 12:
        score += 1
    if tier <= 0 and lib_index == 0:
        score -= 1

    score += (mentee_index % 3) - 1
    return max(1, min(4, score))


def ensure_scale_coverage(entries: list[dict]) -> None:
    counts = Counter(entry["rating"] for entry in entries)
    missing = [value for value in (1, 2, 3, 4) if counts[value] == 0]
    if not missing:
        return

    adjustable = sorted(
        entries,
        key=lambda entry: (entry["profile_name"] != "daniel", entry["lib_index"]),
    )
    for needed, entry in zip(missing, adjustable):
        entry["rating"] = needed


def ensure_resource_spread(entries: list[dict]) -> None:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        grouped[entry["resource_id"]].append(entry)

    spread_pattern = [2, 3, 3, 4, 2, 3, 3]
    for resource_entries in grouped.values():
        if len(resource_entries) < 3:
            continue
        resource_entries.sort(key=lambda entry: MENTEE_ORDER.index(entry["profile_name"]))
        if len(set(entry["rating"] for entry in resource_entries)) >= 3:
            continue
        for index, entry in enumerate(resource_entries):
            entry["rating"] = spread_pattern[index % len(spread_pattern)]


def main() -> None:
    with RESOURCE_PATH.open(encoding="utf-8") as handle:
        resources = {item["_id"]["$oid"]: item for item in json.load(handle)}
    with JOURNEY_PATH.open(encoding="utf-8") as handle:
        journeys = json.load(handle)

    entries: list[dict] = []
    for journey in journeys:
        profile_id = journey.get("profile_id", {}).get("$oid")
        if not profile_id:
            continue

        profile_name = PROFILE_NAMES[profile_id]
        for lib_index, library_entry in enumerate(journey.get("library", [])):
            resource_id = library_entry["resource_id"]["$oid"]
            resource = resources[resource_id]
            completed = parse_date(library_entry["completed"])
            created_time = completed + timedelta(minutes=15 + lib_index * 7)

            entries.append(
                {
                    "profile_id": profile_id,
                    "profile_name": profile_name,
                    "resource_id": resource_id,
                    "resource_name": resource.get("name"),
                    "rating": compute_rating(profile_name, resource, lib_index),
                    "status": "archived" if profile_name == "casey" else "active",
                    "created_time": created_time,
                    "lib_index": lib_index,
                }
            )

    if len(entries) != 88:
        raise SystemExit(f"Expected 88 library ratings, found {len(entries)}")

    ensure_resource_spread(entries)
    ensure_scale_coverage(entries)

    rating_by_key = {
        (entry["profile_id"], entry["resource_id"]): entry["rating"] for entry in entries
    }

    applied = 0
    for journey in journeys:
        profile_id = journey.get("profile_id", {}).get("$oid")
        if not profile_id:
            continue
        for library_entry in journey.get("library", []):
            resource_id = library_entry["resource_id"]["$oid"]
            key = (profile_id, resource_id)
            if key not in rating_by_key:
                raise SystemExit(f"No computed rating for profile={profile_id} resource={resource_id}")
            library_entry["rating"] = rating_by_key[key]
            applied += 1

    if applied != 88:
        raise SystemExit(f"Expected 88 library ratings, applied {applied}")

    distribution = Counter(entry["rating"] for entry in entries)
    print(f"Applied {applied} ratings to Journey library entries")
    print(f"Rating distribution: {dict(sorted(distribution.items()))}")

    with JOURNEY_PATH.open("w", encoding="utf-8") as handle:
        json.dump(journeys, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
