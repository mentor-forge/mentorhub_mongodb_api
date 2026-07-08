#!/usr/bin/env python3
"""Apply library ratings from Rating.0.1.0.0.json onto Journey library entries (T125)."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
JOURNEY_PATH = REPO / "configurator" / "test_data" / "Journey.0.1.0.0.json"
RATING_PATH = REPO / "configurator" / "test_data" / "Rating.0.1.0.0.json"


def main() -> None:
    with RATING_PATH.open(encoding="utf-8") as handle:
        ratings = json.load(handle)
    with JOURNEY_PATH.open(encoding="utf-8") as handle:
        journeys = json.load(handle)

    rating_map = {
        (rating["profile_id"]["$oid"], rating["resource_id"]["$oid"]): rating["rating"]
        for rating in ratings
    }

    applied = 0
    for journey in journeys:
        profile_id = journey.get("profile_id", {}).get("$oid")
        if not profile_id:
            continue
        for library_entry in journey.get("library", []):
            resource_id = library_entry["resource_id"]["$oid"]
            key = (profile_id, resource_id)
            if key not in rating_map:
                raise SystemExit(f"No rating for profile={profile_id} resource={resource_id}")
            library_entry["rating"] = rating_map[key]
            applied += 1

    if applied != 88:
        raise SystemExit(f"Expected 88 library ratings, applied {applied}")

    with JOURNEY_PATH.open("w", encoding="utf-8") as handle:
        json.dump(journeys, handle, indent=2)
        handle.write("\n")

    print(f"Applied {applied} ratings to Journey library entries")


if __name__ == "__main__":
    main()
