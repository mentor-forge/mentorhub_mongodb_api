#!/usr/bin/env python3
"""Regenerate Event test data from Journey and Encounter personas (T215)."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PERSONA_IDS_PATH = REPO / "Tasks" / "scripts" / "persona_ids.json"
JOURNEY_PATH = REPO / "configurator" / "test_data" / "Journey.0.1.0.0.json"
ENCOUNTER_PATH = REPO / "configurator" / "test_data" / "Encounter.0.1.0.0.json"
RESOURCE_PATH = REPO / "configurator" / "test_data" / "Resource.0.1.0.0.json"
PROFILE_PATH = REPO / "configurator" / "test_data" / "Profile.0.1.0.0.json"
OUTPUT_PATH = REPO / "configurator" / "test_data" / "Event.0.1.0.0.json"

EVENT_TYPES = [
    "login",
    "logout",
    "fail",
    "arrived",
    "completed",
    "started",
    "encounter",
    "note",
    "link",
    "advanced",
]

MENTEES = ["daniel", "lucky", "mary", "linda"]

LOGIN_TARGETS = {
    "mary": 10,
    "daniel": 3,
    "lucky": 3,
    "linda": 1,
    "emma": 4,
    "danny": 4,
    "margaret": 2,
    "stacey": 3,
    "eddy": 3,
    "marti": 2,
    "paula": 1,
    "elon": 1,
}


def event_oid(serial: int) -> dict[str, str]:
    return {"$oid": f"F{serial:023d}"}


def oid(value: str) -> dict[str, str]:
    return {"$oid": value}


def parse_date(value: dict | str) -> datetime:
    if isinstance(value, dict):
        value = value["$date"]
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def format_date(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def breadcrumb(
    profile_name: str,
    at_time: datetime,
    correlation_id: str,
) -> dict:
    return {
        "from_ip": "127.0.0.1",
        "by_user": profile_name,
        "at_time": {"$date": format_date(at_time)},
        "correlation_id": correlation_id,
    }


class EventBuilder:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def add(
        self,
        event_type: str,
        profile_id: str,
        profile_name: str,
        at_time: datetime,
        correlation_id: str,
        **context: object,
    ) -> None:
        context_obj: dict = {"profile_id": oid(profile_id)}
        context_obj.update(context)
        self.events.append(
            {
                "type": event_type,
                "context": context_obj,
                "created": breadcrumb(profile_name, at_time, correlation_id),
            }
        )

    def finalize(self) -> list[dict]:
        self.events.sort(key=lambda event: parse_date(event["created"]["at_time"]))
        documents = []
        for serial, event in enumerate(self.events, start=1):
            documents.append(
                {
                    "_id": event_oid(serial),
                    "type": event["type"],
                    "context": event["context"],
                    "created": event["created"],
                }
            )
        return documents


def spread_logins(
    builder: EventBuilder,
    profile_id: str,
    profile_name: str,
    count: int,
    start: datetime,
    end: datetime,
    prefix: str,
) -> None:
    if count <= 0:
        return
    if count == 1:
        times = [end - timedelta(days=7)]
    else:
        span = (end - start).total_seconds()
        step = span / (count - 1)
        times = [start + timedelta(seconds=step * index) for index in range(count)]
    for index, at_time in enumerate(times, start=1):
        builder.add(
            "login",
            profile_id,
            profile_name,
            at_time,
            f"{prefix}-login-{index:02d}",
        )


def journey_events(
    builder: EventBuilder,
    journey: dict,
    profile_id: str,
    profile_name: str,
    resources: dict[str, dict],
) -> None:
    journey_id = journey["_id"]["$oid"]
    library = journey.get("library", [])

    for index, entry in enumerate(library):
        resource_id = entry["resource_id"]["$oid"]
        started = parse_date(entry["started"])
        completed = parse_date(entry["completed"])
        builder.add(
            "link",
            profile_id,
            profile_name,
            started - timedelta(minutes=5),
            f"evt-{profile_name}-link-{index}",
            journey_id=oid(journey_id),
            resource_id=oid(resource_id),
        )
        builder.add(
            "started",
            profile_id,
            profile_name,
            started,
            f"evt-{profile_name}-start-{index}",
            journey_id=oid(journey_id),
            resource_id=oid(resource_id),
        )
        builder.add(
            "completed",
            profile_id,
            profile_name,
            completed,
            f"evt-{profile_name}-done-{index}",
            journey_id=oid(journey_id),
            resource_id=oid(resource_id),
        )

    if library:
        last = library[-1]
        builder.add(
            "note",
            profile_id,
            profile_name,
            parse_date(last["completed"]) + timedelta(minutes=30),
            f"evt-{profile_name}-note",
            journey_id=oid(journey_id),
            resource_id=last["resource_id"],
        )

    for index, entry in enumerate(journey.get("now", [])):
        added = parse_date(entry["added"])
        resource_id = entry["resource_id"]["$oid"]
        resource_name = resources[resource_id]["name"]
        builder.add(
            "advanced",
            profile_id,
            profile_name,
            added,
            f"evt-{profile_name}-adv-{index}",
            journey_id=oid(journey_id),
            resource_id=oid(resource_id),
            resource_name=resource_name,
        )
        if "started" in entry:
            builder.add(
                "started",
                profile_id,
                profile_name,
                parse_date(entry["started"]),
                f"evt-{profile_name}-now-start-{index}",
                journey_id=oid(journey_id),
                resource_id=oid(resource_id),
                resource_name=resource_name,
            )


def main() -> None:
    with PERSONA_IDS_PATH.open(encoding="utf-8") as handle:
        persona_ids = json.load(handle)
    profiles = persona_ids["profiles"]
    valid_profile_ids = set(profiles.values())
    profile_names = {value: key for key, value in profiles.items()}
    removed_names = {"luther", "sam", "carol", "cat", "taylor", "riley", "casey"}

    with RESOURCE_PATH.open(encoding="utf-8") as handle:
        resources = {item["_id"]["$oid"]: item for item in json.load(handle)}
    with JOURNEY_PATH.open(encoding="utf-8") as handle:
        journeys = {
            item["_id"]["$oid"]: item
            for item in json.load(handle)
            if item.get("profile_id")
        }
    with ENCOUNTER_PATH.open(encoding="utf-8") as handle:
        encounters = json.load(handle)
    with PROFILE_PATH.open(encoding="utf-8") as handle:
        profile_docs = {item["_id"]["$oid"]: item for item in json.load(handle)}

    builder = EventBuilder()
    window_end = datetime(2026, 6, 22, 12, 0, tzinfo=timezone.utc)
    window_start = window_end - timedelta(days=183)

    for name in MENTEES:
        profile_id = profiles[name]
        journey = journeys[profile_id]
        journey_events(builder, journey, profile_id, name, resources)
        spread_logins(
            builder,
            profile_id,
            name,
            LOGIN_TARGETS[name],
            window_start,
            window_end,
            f"seed-auth-{name}",
        )

    mentor_by_mentee = {
        profiles["mary"]: "marti",
        profiles["daniel"]: "marti",
        profiles["lucky"]: "marti",
        profiles["linda"]: "marti",
    }
    for encounter in encounters:
        mentee_id = encounter["mentee_id"]["$oid"]
        if mentee_id not in valid_profile_ids:
            continue
        mentee_name = profile_names[mentee_id]
        mentor_name = mentor_by_mentee.get(mentee_id, "marti")
        builder.add(
            "encounter",
            mentee_id,
            mentor_name,
            parse_date(encounter["date"]),
            f"evt-enc-{mentee_name}-{encounter['_id']['$oid'][-2:]}",
            encounter_id=encounter["_id"],
        )

    arrived_targets = [
        "emma",
        "danny",
        "margaret",
        "stacey",
        "eddy",
        "mary",
        "marti",
        "paula",
        "elon",
    ]
    for name in arrived_targets:
        profile_id = profiles[name]
        created = parse_date(profile_docs[profile_id]["created"]["at_time"])
        builder.add(
            "arrived",
            profile_id,
            name,
            created,
            f"seed-arrived-{name}",
        )

    for name in ["emma", "danny", "margaret", "stacey", "eddy", "marti", "paula", "elon"]:
        spread_logins(
            builder,
            profiles[name],
            name,
            LOGIN_TARGETS[name],
            window_start,
            window_end,
            f"seed-auth-{name}",
        )

    builder.add(
        "fail",
        profiles["margaret"],
        "margaret",
        datetime(2026, 4, 10, 8, 15, tzinfo=window_end.tzinfo),
        "seed-auth-fail-margaret",
    )
    builder.add(
        "logout",
        profiles["daniel"],
        "daniel",
        datetime(2026, 5, 1, 17, 30, tzinfo=window_end.tzinfo),
        "seed-auth-logout-daniel",
    )

    documents = builder.finalize()

    referenced_profiles = {
        event["context"]["profile_id"]["$oid"] for event in documents
    }
    bad_refs = referenced_profiles - valid_profile_ids
    if bad_refs:
        raise SystemExit(f"Events reference unknown profiles: {bad_refs}")

    bad_users = {
        event["created"]["by_user"]
        for event in documents
        if event["created"]["by_user"] in removed_names
    }
    if bad_users:
        raise SystemExit(f"Events reference removed personas: {bad_users}")

    by_type = Counter(document["type"] for document in documents)
    missing_types = set(EVENT_TYPES) - set(by_type)
    if missing_types:
        raise SystemExit(f"Missing event types: {sorted(missing_types)}")

    by_profile = Counter(
        profile_names.get(document["context"]["profile_id"]["$oid"], "?")
        for document in documents
    )

    mentee_counts = {name: by_profile[name] for name in MENTEES}
    if not (
        mentee_counts["mary"] > mentee_counts["lucky"]
        and mentee_counts["lucky"] > mentee_counts["linda"]
        and mentee_counts["daniel"] > mentee_counts["linda"]
    ):
        raise SystemExit(f"Density order wrong: {mentee_counts}")

    print(f"Generated {len(documents)} events")
    print(f"By type: {dict(sorted(by_type.items()))}")
    print(f"By profile: {dict(sorted(by_profile.items(), key=lambda item: (-item[1], item[0])))}")
    print(f"Mentee density: {mentee_counts}")

    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(documents, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
