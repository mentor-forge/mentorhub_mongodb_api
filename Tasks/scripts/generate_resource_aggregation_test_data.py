#!/usr/bin/env python3
"""Generate Resource_Aggregation test data from Journey and related collections (T122/T125)."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
JOURNEY_PATH = REPO / "configurator" / "test_data" / "Journey.0.1.0.0.json"
RESOURCE_PATH = REPO / "configurator" / "test_data" / "Resource.0.1.0.0.json"
NOTE_PATH = REPO / "configurator" / "test_data" / "Note.0.1.0.0.json"
EVENT_PATH = REPO / "configurator" / "test_data" / "Event.0.1.0.0.json"
OUTPUT_PATH = REPO / "configurator" / "test_data" / "Resource_Aggregation.0.1.0.0.json"

MIN_DURATION_MINUTES = 15
MAX_DURATION_MINUTES = 240


def seed_int(value: str, salt: str = "") -> int:
    digest = hashlib.sha256(f"{value}:{salt}".encode()).hexdigest()
    return int(digest[:12], 16)


def parse_date(value: dict) -> datetime:
    return datetime.fromisoformat(value["$date"].replace("Z", "+00:00"))


def format_date(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def duration_for(resource_id: str) -> str:
    minutes = MIN_DURATION_MINUTES + seed_int(resource_id, "duration") % (
        MAX_DURATION_MINUTES - MIN_DURATION_MINUTES + 1
    )
    hours, mins = divmod(minutes, 60)
    if hours and mins:
        return f"PT{hours}H{mins}M"
    if hours:
        return f"PT{hours}H"
    return f"PT{mins}M"


def hits_for(resource_id: str, completions: int, link_hits: int) -> int:
    base = max(link_hits, completions)
    offset = 1 + seed_int(resource_id, "hits") % 5
    hits = base + offset if base <= completions else base
    if hits <= completions:
        hits = completions + offset
    return hits


def collect_journey_resources(
    journeys: list[dict], name_to_oid: dict[str, str]
) -> tuple[set[str], Counter, Counter, defaultdict[str, int]]:
    resources: set[str] = set()
    completions: Counter = Counter()
    rating_counts: Counter = Counter()
    rating_sums: defaultdict[str, int] = defaultdict(int)

    for journey in journeys:
        if not journey.get("profile_id"):
            continue

        for item in journey.get("library", []):
            resource_id = item["resource_id"]["$oid"]
            resources.add(resource_id)
            completions[resource_id] += 1
            if "rating" in item:
                rating_counts[resource_id] += 1
                rating_sums[resource_id] += item["rating"]

        for item in journey.get("now", []):
            resource_ref = item.get("resource_id")
            if isinstance(resource_ref, str):
                resource_id = name_to_oid.get(resource_ref)
            elif isinstance(resource_ref, dict):
                resource_id = resource_ref.get("$oid")
            else:
                resource_id = None
            if resource_id:
                resources.add(resource_id)

        for module in journey.get("next", []):
            for topic in module.get("topics", []):
                for resource in topic.get("resources", []):
                    resource_ref = resource.get("resource_id")
                    if isinstance(resource_ref, dict):
                        resource_id = resource_ref.get("$oid")
                    else:
                        resource_id = resource.get("$oid")
                    if resource_id:
                        resources.add(resource_id)

    return resources, completions, rating_counts, rating_sums


def count_link_events(events: list[dict]) -> Counter:
    counts: Counter = Counter()
    for event in events:
        if event.get("type") != "link":
            continue
        resource_id = event.get("context", {}).get("resource_id", {}).get("$oid")
        if resource_id:
            counts[resource_id] += 1
    return counts


def main() -> None:
    with RESOURCE_PATH.open(encoding="utf-8") as handle:
        resources = {item["_id"]["$oid"]: item for item in json.load(handle)}
    with JOURNEY_PATH.open(encoding="utf-8") as handle:
        journeys = json.load(handle)
    with NOTE_PATH.open(encoding="utf-8") as handle:
        notes = json.load(handle)
    with EVENT_PATH.open(encoding="utf-8") as handle:
        events = json.load(handle)

    name_to_oid = {item["name"]: oid for oid, item in resources.items()}
    journey_resources, completions, rating_counts, rating_sums = collect_journey_resources(
        journeys, name_to_oid
    )
    missing = sorted(resource_id for resource_id in journey_resources if resource_id not in resources)
    if missing:
        raise SystemExit(f"Journey references unknown resources: {missing[:5]}")

    note_counts = Counter(note["resource_id"]["$oid"] for note in notes)
    link_hits = count_link_events(events)

    documents = []
    for serial, resource_id in enumerate(sorted(journey_resources), start=1):
        resource = resources[resource_id]
        resource_created = parse_date(resource["created"]["at_time"])
        created_offset_minutes = 30 + seed_int(resource_id, "created") % (72 * 60)
        created_time = resource_created + timedelta(minutes=created_offset_minutes)
        saved_offset_days = 1 + seed_int(resource_id, "saved") % 45
        last_saved_time = created_time + timedelta(days=saved_offset_days, hours=seed_int(resource_id, "saved-h") % 12)

        completion_count = completions[resource_id]
        hit_count = hits_for(resource_id, completion_count, link_hits[resource_id])
        if hit_count <= completion_count:
            raise SystemExit(f"hits must exceed completions for {resource_id}")

        rating_count = rating_counts[resource_id]
        rating_sum = rating_sums[resource_id]
        if rating_count != completion_count and completion_count > 0:
            raise SystemExit(
                f"rating_count {rating_count} != completions {completion_count} for {resource_id}"
            )

        documents.append(
            {
                "_id": {"$oid": resource_id},
                "note_count": note_counts[resource_id],
                "completions": completion_count,
                "hits": hit_count,
                "duration": duration_for(resource_id),
                "rating_count": rating_count,
                "rating_sum": rating_sum,
                "created": {
                    "from_ip": "127.0.0.1",
                    "by_user": "system",
                    "at_time": {"$date": format_date(created_time)},
                    "correlation_id": f"aggregation-{serial:04d}",
                },
                "last_saved": {
                    "from_ip": "127.0.0.1",
                    "by_user": "system",
                    "at_time": {"$date": format_date(last_saved_time)},
                    "correlation_id": f"aggregation-{serial:04d}-saved",
                },
            }
        )

    with_completions = sum(1 for document in documents if document["completions"] > 0)
    print(f"Generated {len(documents)} resource aggregations")
    print(f"With completions: {with_completions}")
    print(f"Next/now only: {len(documents) - with_completions}")
    print(f"Total note_count: {sum(document['note_count'] for document in documents)}")
    print(f"Total rating_count: {sum(document['rating_count'] for document in documents)}")

    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(documents, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
