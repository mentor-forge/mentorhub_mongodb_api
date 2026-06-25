#!/usr/bin/env python3
"""Generate Note test data from Journey library entries (T121)."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
JOURNEY_PATH = REPO / "configurator" / "test_data" / "Journey.0.1.0.0.json"
RESOURCE_PATH = REPO / "configurator" / "test_data" / "Resource.0.1.0.0.json"
RATING_PATH = REPO / "configurator" / "test_data" / "Rating.0.1.0.0.json"
OUTPUT_PATH = REPO / "configurator" / "test_data" / "Note.0.1.0.0.json"

PROFILE_NAMES = {
    "A00000000000000000000002": "daniel",
    "A00000000000000000000003": "lucky",
    "A00000000000000000000004": "mary",
    "A00000000000000000000005": "luther",
    "A00000000000000000000010": "riley",
    "A00000000000000000000014": "taylor",
    "A00000000000000000000015": "casey",
}

NOTE_TARGETS = {
    "daniel": 3,
    "lucky": 4,
    "mary": 6,
    "luther": 12,
    "riley": 3,
    "taylor": 4,
    "casey": 3,
}


def note_oid(serial: int) -> dict[str, str]:
    return {"$oid": f"E{serial:023d}"}


def parse_date(value: dict) -> datetime:
    return datetime.fromisoformat(value["$date"].replace("Z", "+00:00"))


def format_date(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def pick_library_indices(library_len: int, count: int) -> list[int]:
    if count >= library_len:
        return list(range(library_len))
    if count == 1:
        return [library_len - 1]
    step = (library_len - 1) / (count - 1)
    indices = sorted({min(library_len - 1, round(step * index)) for index in range(count)})
    while len(indices) < count:
        for candidate in range(library_len):
            if candidate not in indices:
                indices.append(candidate)
                break
        else:
            break
    return sorted(indices[:count])


def note_text(profile_name: str, resource: dict, rating: int | None, lib_index: int) -> str:
    name = resource.get("name", "this resource")
    rtype = resource.get("type", "resource")
    topic = resource.get("description", "")[:120].strip()

    if rating is not None and rating <= 2:
        templates = [
            f"Finished **{name}** but I'm still unclear on the main takeaway. Need to revisit before I can explain it to someone else.",
            f"**{name}** felt dense for where I am. The {rtype} format helped, yet I walked away with more questions than answers.",
            f"Marked **{name}** complete, but I'm not confident I absorbed it. What part should I re-read first?",
        ]
    elif rating == 3:
        templates = [
            f"Solid intro via **{name}**. Useful context on {topic or 'the topic'}, though I want one more example before I move on.",
            f"**{name}** was worth the time — good balance of theory and practice. I'll try applying one idea this week.",
            f"Helpful {rtype} (**{name}**). I captured a few bullets; still comparing it with other EngineerKit resources.",
        ]
    else:
        templates = [
            f"**{name}** clicked for me. Clear explanation and a practical frame I can reuse on real work.",
            f"Strong {rtype}: **{name}**. I liked how it connected back to earlier modules — best completion this month.",
            f"Finished **{name}** feeling much clearer. Keeping this as a reference when I mentor others on the topic.",
        ]

    if profile_name == "luther" and lib_index >= 8:
        return (
            f"Deep dive on **{name}**. This one rewards a second pass — I added examples from recent sprint work "
            f"and tied it to our team's testing strategy."
        )
    if profile_name == "casey":
        return f"Archived note on **{name}** from earlier progress. Still a useful reference even though my journey is inactive."

    return templates[(lib_index + len(name)) % len(templates)]


def main() -> None:
    with RESOURCE_PATH.open(encoding="utf-8") as handle:
        resources = {item["_id"]["$oid"]: item for item in json.load(handle)}
    with JOURNEY_PATH.open(encoding="utf-8") as handle:
        journeys = json.load(handle)
    with RATING_PATH.open(encoding="utf-8") as handle:
        ratings = json.load(handle)

    rating_map = {
        (item["profile_id"]["$oid"], item["resource_id"]["$oid"]): item["rating"]
        for item in ratings
    }

    entries: list[dict] = []
    for journey in journeys:
        profile_id = journey.get("profile_id", {}).get("$oid")
        if not profile_id:
            continue

        profile_name = PROFILE_NAMES[profile_id]
        library = journey.get("library", [])
        target = NOTE_TARGETS[profile_name]
        indices = pick_library_indices(len(library), target)

        for lib_index in indices:
            library_entry = library[lib_index]
            resource_id = library_entry["resource_id"]["$oid"]
            resource = resources[resource_id]
            completed = parse_date(library_entry["completed"])
            created_time = completed + timedelta(minutes=30 + lib_index * 11)
            saved_time = created_time + timedelta(hours=2 + lib_index)
            rating = rating_map.get((profile_id, resource_id))

            entries.append(
                {
                    "profile_id": profile_id,
                    "profile_name": profile_name,
                    "resource_id": resource_id,
                    "note": note_text(profile_name, resource, rating, lib_index),
                    "status": "archived" if profile_name == "casey" else "active",
                    "created_time": created_time,
                    "saved_time": saved_time,
                    "lib_index": lib_index,
                }
            )

    if len(entries) < 35:
        raise SystemExit(f"Expected at least 35 notes, found {len(entries)}")

    per_mentee = Counter(entry["profile_name"] for entry in entries)
    for profile_name, minimum in [("daniel", 2), ("riley", 2), ("casey", 1)]:
        if per_mentee[profile_name] < minimum:
            raise SystemExit(f"{profile_name} has only {per_mentee[profile_name]} notes")

    entries.sort(key=lambda entry: entry["created_time"])

    documents = []
    for serial, entry in enumerate(entries, start=1):
        documents.append(
            {
                "_id": note_oid(serial),
                "resource_id": {"$oid": entry["resource_id"]},
                "profile_id": {"$oid": entry["profile_id"]},
                "note": entry["note"],
                "status": entry["status"],
                "created": {
                    "from_ip": "127.0.0.1",
                    "by_user": entry["profile_name"],
                    "at_time": {"$date": format_date(entry["created_time"])},
                    "correlation_id": f"note-{entry['profile_name']}-{serial:03d}",
                },
                "saved": {
                    "from_ip": "127.0.0.1",
                    "by_user": entry["profile_name"],
                    "at_time": {"$date": format_date(entry["saved_time"])},
                    "correlation_id": f"note-{entry['profile_name']}-{serial:03d}-saved",
                },
            }
        )

    print(f"Generated {len(documents)} notes")
    print(f"Per mentee: {dict(sorted(per_mentee.items()))}")
    print(f"Status: {dict(Counter(document['status'] for document in documents))}")

    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(documents, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
