#!/usr/bin/env python3
"""Generate expanded Encounter test data conforming to issue #79 (F-D33)
and reflecting authentic Obsidian encounter transcripts, summaries, and TLDRs.

Generates at least 12 weekly encounter records per Mentee with relative Now() +/- days
schedules, actual appointment times, no-show handling, FirstEncounter vs Standard plans,
and persona status distributions.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO / "configurator" / "test_data" / "Encounter.0.1.0.0.json"
PERSONA_IDS_PATH = REPO / "Tasks" / "scripts" / "persona_ids.json"

STANDARD_PLAN_ID = "f00000000000000000000001"
FIRST_ENCOUNTER_PLAN_ID = "f00000000000000000000002"

FIRST_ENCOUNTER_STEPS = [
    "Start Whisper Recording",
    "Introduction - The Agile Learning Institute",
    "Introduction - Mentor / Mentee",
    "How many weeks are you commiting to?",
    "What do you want to be able to say at the end of that time?",
    "Introduce Mentee Journey interface.",
    "Stop Recording, Transcribe, and Paste Updates",
]

STANDARD_STEPS = [
    "Start Whisper Recording",
    "What do you want to focus on today?",
    "How would you describe what's happening now?",
    "During our time together, what would you like to accomplish?",
    "What would you like to be able to share next time?",
    "How are your discoveries making a difference?",
    "How do you want to wrap up today?",
    "Stop Recording, Transcribe and Paste Updates",
]


def oid(hex_str: str) -> dict[str, str]:
    return {"$oid": hex_str}


def date_dict(dt: datetime) -> dict[str, str]:
    return {"$date": dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")}


def build_agenda(steps: list[str], status: str, no_show: bool) -> list[dict]:
    if status == "scheduled" or no_show:
        return [{"step": step, "checked": False} for step in steps]
    if status == "active":
        # First 3 steps checked, remaining in progress/unchecked
        return [
            {"step": step, "checked": i < 3}
            for i, step in enumerate(steps)
        ]
    # Complete and attended
    return [{"step": step, "checked": True} for step in steps]


def generate_encounters() -> list[dict]:
    with open(PERSONA_IDS_PATH, encoding="utf-8") as f:
        personas = json.load(f)

    profiles = personas["profiles"]
    mike_id = profiles["mike"]          # A...01
    daniel_id = profiles["daniel"]      # A...02
    lucky_id = profiles["lucky"]        # A...03
    mary_id = profiles["mary"]          # A...04
    linda_id = profiles["linda"]        # A...05
    marti_id = profiles["marti"]        # A...06
    paula_id = profiles["paula"]        # A...10
    elon_id = profiles["elon"]          # A...11
    danny_id = profiles["danny"]        # A...14
    pat_id = profiles["pat"]            # A...19

    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)

    encounters: list[dict] = []
    serial = 1

    # =========================================================================
    # 1. Daniel Dissler (Persevere Mentee)
    # Mixture of completed (weeks -8 to -1) and scheduled (weeks +1 to +4).
    # Includes authentic flood / SPA utils 5.5 / Pokemon API encounter (week -3).
    # Includes Money Mentor session (Elon, week -5) and no-show (week -2).
    # =========================================================================
    daniel_dialogues = [
        # Session 1 (week -8): FirstEncounter
        {
            "mentor_id": paula_id,
            "by_user": "paula",
            "tldr": "Daniel and Paula completed initial Persevere onboarding and agreed on 12-week capstone goals.",
            "summary": "## Summary\n**Summary:** Paula Persevere welcomed Daniel Dissler to the Persevere learning journey. They walked through the ALI intro, aligned on a 12-week mentoring commitment, and toured the Mentee Journey roadmap interface.",
            "transcript": "#### Paula\nWelcome Daniel. This hour is Persevere capstone onboarding time—Vue patterns and API integration for your portfolio SPA.\n\n#### Daniel\nI'm excited to get started. I've been sketching components, but I want to make sure my project structure follows best practices.\n\n#### Paula\nWe'll map your capstone routes first, then extract a composable for authenticated API calls.",
        },
        # Session 2 (week -7): Standard
        {
            "mentor_id": paula_id,
            "by_user": "paula",
            "tldr": "Paula reviewed Daniel's dashboard layout and assigned Pinia store integration for auth state.",
            "summary": "## Summary\n**Summary:** Reviewed Daniel's initial Vue Router structure and dashboard scaffolding. Paula recommended introducing Pinia for shared authentication state.",
            "transcript": "#### Paula\nDaniel, let's review your Vue component architecture sketches.\n\n#### Daniel\nI started scaffolding the dashboard navigation and cards using Vue Router.\n\n#### Paula\nClean layout. Next step is extracting state into a Pinia store so auth tokens are accessible globally.",
        },
        # Session 3 (week -6): Standard
        {
            "mentor_id": paula_id,
            "by_user": "paula",
            "tldr": "Paula helped Daniel resolve TypeScript interface typing on Pinia auth getters.",
            "summary": "## Summary\n**Summary:** Pair-debugged TypeScript typing issues in Daniel's Pinia user store. Verified reactive getters compile without errors.",
            "transcript": "#### Paula\nHow did the Pinia store integration go?\n\n#### Daniel\nThe store is working for auth state, but I'm getting TypeScript errors on the reactive getters.\n\n#### Paula\nLet's inspect your type definitions. We'll define an explicit interface for the user state.",
        },
        # Session 4 (week -5): Compensated Money Mentor session with Elon Money
        {
            "mentor_id": elon_id,
            "by_user": "elon",
            "tldr": "Compensated money-mentor session: Elon reviewed Daniel's Persevere capstone pitch and unit economics.",
            "summary": "## Summary\n**Summary:** Elon Money mentored Daniel Dissler on startup pitch structure for the Persevere capstone. They refined problem framing and unit economics; this was a **compensated** money-mentor review session.",
            "transcript": "#### Elon\nDaniel, let's pressure-test your Persevere capstone pitch—what problem does your SPA solve and who pays for it?\n\n#### Daniel\nIt's a cohort progress dashboard for nonprofit program managers evaluating graduate outcomes.\n\n#### Elon\nGood framing. Tighten the unit economics slide and we'll mark this as a compensated money-mentor review session.",
        },
        # Session 5 (week -4): Standard
        {
            "mentor_id": paula_id,
            "by_user": "paula",
            "tldr": "Daniel demonstrated custom Vue fetch composable with error handling and loading indicators.",
            "summary": "## Summary\n**Summary:** Evaluated Daniel's custom `useFetch` composable. Confirmed loading and error states are handled; set next step on token refresh logic.",
            "transcript": "#### Paula\nToday we focus on composables for data fetching.\n\n#### Daniel\nI wrote a `useFetch` wrapper that handles auth headers and loading states.\n\n#### Paula\nGreat abstraction. Make sure you test the 401 token refresh interceptor before next week.",
        },
        # Session 6 (week -3): Authentic sample with Mike Storey (flood, SPA utils 5.5, Pokemon API, draft PR)
        {
            "mentor_id": mike_id,
            "by_user": "mike",
            "tldr": "Daniel vented recent personal setbacks, then with Mike debugged and updated their SPA project, cleaned up tasks, reviewed the API, and set up a draft PR.",
            "summary": "## Summary\n**Summary:** Daniel opened the chat describing a series of personal stresses—a recent flood that soaked his garage, the death of his cousin, a dog’s accidental overdose, and a close call on the highway—before shifting focus to work. He and Mike walked through updating the SPA utils to version 5.5, using MH commands (pull-all, down/up), handling cursor sandbox restrictions, cleaning up pending tasks, committing changes, and preparing a draft pull request. They then explored the local API via localhost:8080, discussed how the API shapes data for the UI (comparing it to a Pokémon API), and planned next steps for reviewing UI components and finalizing the PR.",
            "transcript": "#### Daniel\nI'm here.\n\n#### Mike\nHey, Daniel. How are you doing today?\n\n#### Daniel\nOh, it's rough. We had a flood last night. Whole garage got washed out. Just had to spend some time cleaning that up.\n\n#### Mike\nOh no, that's no fun. If it got up to the walls, you really need to take it all the way back to the studs. Well, what would you like to focus on today?\n\n#### Daniel\nI want to get this ticket done today. The bump to SPA utils 0.5.5.\n\n#### Mike\nDo an MH down, an MH pull all, and an MH up all, and then go to localhost:8080. Pull all pulls the latest version of all the containers so you get Lucky's API updates.\n\n#### Daniel\nOkay, it's done. I'm looking at localhost:8080. Oh, it's clean.\n\n#### Mike\nLook at the Mentee SPA because it's using all the shared components from the new SPA utils. Your update to 5.5 is going to make your app look a lot like the Mentee app.\n\n#### Daniel\nCollapse Single Page Applications, open API Explorer, and choose Mentor API. This is almost the same as the Pokemon layout. It was an app for Pokemon, but when you have a category of all the different Pokemon, they have all these different abilities. This basically is the layout of each one.\n\n#### Mike\nYes, exactly like the Pokemon API. The API reaches out to the database and makes the data the correct shape for how you want to use it. These API definitions are the contract between you on your SPA and Lucky on the API.\n\n#### Daniel\nI'll get to reviewing the tasks and open a draft PR for review.\n\n#### Mike\nSounds good. I look forward to the PR review. Peace.",
        },
        # Session 7 (week -2): No-show (omitted transcript/summary/tldr)
        None,
        # Session 8 (week -1): Standard
        {
            "mentor_id": paula_id,
            "by_user": "paula",
            "tldr": "Paula verified Daniel's pre-demo capstone checklist and test coverage.",
            "summary": "## Summary\n**Summary:** Paula and Daniel conducted a comprehensive pre-demo review of the capstone SPA, verifying end-to-end user flows and toast notifications.",
            "transcript": "#### Paula\nGlad you're feeling better after missing last week, Daniel. Let's run a full regression before cohort demo day.\n\n#### Daniel\nAll tests passed and error states are handled with toast notifications.\n\n#### Paula\nOutstanding progress. We're ready for your cohort presentation.",
        },
    ]

    for i in range(12):
        enc_id = f"E{serial:023x}"
        serial += 1
        is_first = (i == 0)
        plan_id = FIRST_ENCOUNTER_PLAN_ID if is_first else STANDARD_PLAN_ID
        steps = FIRST_ENCOUNTER_STEPS if is_first else STANDARD_STEPS

        if i < 8:
            week_offset = i - 8
            sched_from = now + timedelta(days=7 * week_offset)
            sched_to = sched_from + timedelta(hours=1)
            is_no_show = (i == 6)  # week -2 is no-show

            meta = daniel_dialogues[i]
            mentor_id = paula_id if is_no_show else meta["mentor_id"]
            mentor_user = "paula" if is_no_show else meta["by_user"]

            doc: dict = {
                "_id": oid(enc_id),
                "mentor_id": oid(mentor_id),
                "mentee_id": oid(daniel_id),
                "appointment": {
                    "from": date_dict(sched_from),
                    "to": date_dict(sched_to),
                },
                "plan_id": oid(plan_id),
                "agenda": build_agenda(steps, "complete", is_no_show),
                "status": "complete",
                "no_show": is_no_show,
            }

            if not is_no_show:
                actual_from = sched_from + timedelta(minutes=2)
                actual_to = actual_from + timedelta(minutes=55)
                doc["actual"] = {
                    "from": date_dict(actual_from),
                    "to": date_dict(actual_to),
                }
                doc["transcript"] = meta["transcript"]
                doc["summary"] = meta["summary"]
                doc["tldr"] = meta["tldr"]

            doc["created"] = {
                "from_ip": "127.0.0.1",
                "by_user": mentor_user,
                "at_time": date_dict(sched_from),
                "correlation_id": f"seed-enc-daniel-{i+1:02d}",
            }
            doc["saved"] = {
                "from_ip": "127.0.0.1",
                "by_user": mentor_user,
                "at_time": date_dict(sched_to),
                "correlation_id": f"save-enc-daniel-{i+1:02d}",
            }
            encounters.append(doc)
        else:
            # Future scheduled sessions: weeks +1 to +4
            week_offset = (i - 8) + 1
            sched_from = now + timedelta(days=7 * week_offset)
            sched_to = sched_from + timedelta(hours=1)
            doc = {
                "_id": oid(enc_id),
                "mentor_id": oid(paula_id),
                "mentee_id": oid(daniel_id),
                "appointment": {
                    "from": date_dict(sched_from),
                    "to": date_dict(sched_to),
                },
                "plan_id": oid(plan_id),
                "agenda": build_agenda(steps, "scheduled", False),
                "status": "scheduled",
                "created": {
                    "from_ip": "127.0.0.1",
                    "by_user": "paula",
                    "at_time": date_dict(now),
                    "correlation_id": f"seed-enc-daniel-{i+1:02d}",
                },
                "saved": {
                    "from_ip": "127.0.0.1",
                    "by_user": "paula",
                    "at_time": date_dict(now),
                    "correlation_id": f"save-enc-daniel-{i+1:02d}",
                },
            }
            encounters.append(doc)

    # =========================================================================
    # 2. Lucky Minyard (SuperSoft Mentee)
    # Mixture of completed (weeks -7 to -1), 1 active (week 0), scheduled (+1 to +4).
    # Includes authentic PR review / slump / T-shaped engineer encounter (week -3).
    # Includes Money Mentor session (Elon, week -4).
    # =========================================================================
    lucky_dialogues = [
        # Session 1 (week -7): FirstEncounter
        {
            "mentor_id": danny_id,
            "by_user": "danny",
            "tldr": "Danny and Lucky completed onboarding and established SuperSoft reliability goals.",
            "summary": "## Summary\n**Summary:** Danny Dev Lead kicked off Lucky Minyard's SuperSoft SRE apprenticeship with onboarding, roadmap orientation, and tooling setup.",
            "transcript": "#### Danny\nWelcome Lucky to SuperSoft engineering mentorship. In this introductory session, we'll establish your reliability and backend objectives.\n\n#### Lucky\nThanks Danny. I want to build automated deployment verification and on-call paging pipelines.\n\n#### Danny\nWe walked through the ALI philosophy and your 12-week roadmap in the Mentee Journey app.",
        },
        # Session 2 (week -6): Standard
        {
            "mentor_id": danny_id,
            "by_user": "danny",
            "tldr": "Danny and Lucky planned an automated health-check script to replace manual curl steps.",
            "summary": "## Summary\n**Summary:** Analyzed manual deployment verification bottlenecks; designed automated health check suite.",
            "transcript": "#### Danny\nLucky, let's inspect your current manual deploy checklist.\n\n#### Lucky\nRight now it takes 15 manual curl commands across three staging environments.\n\n#### Danny\nWe'll script that into a python automated health-check CLI.",
        },
        # Session 3 (week -5): Standard
        {
            "mentor_id": danny_id,
            "by_user": "danny",
            "tldr": "Lucky's deployment script blocked a bad promotion, proving SRE value.",
            "summary": "## Summary\n**Summary:** Reviewed staging run of health-check automation; script prevented a broken deployment due to expired TLS cert.",
            "transcript": "#### Danny\nHow did the initial health-check script run in staging?\n\n#### Lucky\nIt successfully verified Mongo connectivity and flagged an expired TLS cert before promote.\n\n#### Danny\nThat's an immediate win. Next, add automated rollback triggering.",
        },
        # Session 4 (week -4): Compensated Money Mentor session with Elon Money
        {
            "mentor_id": elon_id,
            "by_user": "elon",
            "tldr": "Compensated money-mentor session: Elon coached Lucky on ROI framing for reliability work.",
            "summary": "## Summary\n**Summary:** Elon Money coached Lucky Minyard on articulating SuperSoft reliability investments to budget holders. Lucky linked health checks to incident reduction; this was a **compensated** session.",
            "transcript": "#### Elon\nLucky, SuperSoft is paying for engineering depth—how do you justify the reliability work to a budget holder?\n\n#### Lucky\nI can tie each health check to reduced incident minutes and faster rollback time.\n\n#### Elon\nThat's the story investors expect. We'll log this as a compensated money-mentor advisory on technical due diligence.",
        },
        # Session 5 (week -3): Authentic sample with Mike Storey (PR review, slump, T-shaped engineer, Clean Code, bank issue)
        {
            "mentor_id": mike_id,
            "by_user": "mike",
            "tldr": "Mike helped Lucky clarify his pull request, offered productivity and career guidance (focus on one ticket, become T-shaped via Engineer Kit), and gave practical advice on resolving a stuck bank/check issue.",
            "summary": "## Summary\n**Summary:** Lucky and Mike discussed a pending pull request that Lucky had pushed on Friday but hadn't requested review for, leading to some confusion about its status. Mike clarified the PR's details (API utils version bumps, new filters, pagination changes) and outlined upcoming work items such as resource list implementation and API utils updates. The conversation then shifted to Lucky's feeling of burnout and lack of focus. Mike advised using the Kanban board to limit work to one ticket at a time, emphasized the value of becoming a T-shaped engineer rather than trying to master everything, and suggested progressing through the 'Engineer Kit' learning modules (starting with the Clean Code section). Finally, they addressed Lucky's personal issue with an unresolved bank/check problem, with Mike recommending concrete steps: set deadlines, follow up persistently with the bank, and keep documentation. They concluded by setting a short-term goal for Lucky to review the clean-code material this week and for Mike to get the PR reviewed.",
            "transcript": "#### Lucky\nOver the weekend and this morning I wanted to read over a lot of the tasks to understand them better. Did you get a chance to look at what I committed and pushed on Friday?\n\n#### Mike\nThere is a PR on mentor API. You went to 0.5.0, and 0.5.1 added new filter options to the list composable. So you're backing that up with filters by URL, interests, technologies, and skill level.\n\n#### Lucky\nI need to focus on getting some enthusiasm back. I've been in a slump for a few days. I feel like I just cannot keep up.\n\n#### Mike\nThe Kanban board is meant to deal with that overwhelming feeling. Pick up one ticket; the only thing you're supposed to work on is that ticket. When that ticket's done, you go bang out the next one.\n\n#### Lucky\nI want to learn everything, but I'm kind of scatterbrained. I know a little bit about this and a little bit about that.\n\n#### Mike\nDid you read the article on the Agile Learning Institute's webpage about the T-shaped engineer? Employers are looking for T-shaped engineers. They're looking for someone with deep expertise in a skill set that they need, who can work with the entire team because they understand what everybody else does.\n\n#### Lucky\nRight.\n\n#### Mike\nIn your curriculum, we have a tool called the Engineer Kit. If you work your way through the Engineer Kit modules, you will establish that top of the T, and then you can decide on your specialty.\n\n#### Lucky\nI think I want to start with the Clean Code section. I'll go through some of that this week.\n\n#### Mike\nClean Code is a really good topic. How we implement separation of concerns, routes, services, utilities, and single intent. That's clean code. I'll get that PR reviewed for you this morning. Peace.",
        },
        # Session 6 (week -2): Standard
        {
            "mentor_id": danny_id,
            "by_user": "danny",
            "tldr": "Danny and Lucky tuned Prometheus latency and error alerts to avoid alert fatigue.",
            "summary": "## Summary\n**Summary:** Configured Prometheus alerting rules and pager thresholds for SuperSoft core services.",
            "transcript": "#### Danny\nLet's discuss Prometheus alerting thresholds for on-call paging.\n\n#### Lucky\nI configured P95 latency alerts at 250ms and error rates above 1% over 5 minutes.\n\n#### Danny\nSensible thresholds to avoid alert fatigue. Let's run a chaos drill.",
        },
        # Session 7 (week -1): Standard
        {
            "mentor_id": danny_id,
            "by_user": "danny",
            "tldr": "Danny approved Lucky's production readiness and on-call rotation schedule.",
            "summary": "## Summary\n**Summary:** Final production readiness review for SuperSoft on-call transition. Verified runbook links and dashboards.",
            "transcript": "#### Danny\nToday we prepare for the production readiness review.\n\n#### Lucky\nRunbooks are updated and grafana dashboards are grouped by SLA.\n\n#### Danny\nYou're ready for primary on-call rotation starting next week.",
        },
    ]

    for i in range(12):
        enc_id = f"E{serial:023x}"
        serial += 1
        is_first = (i == 0)
        plan_id = FIRST_ENCOUNTER_PLAN_ID if is_first else STANDARD_PLAN_ID
        steps = FIRST_ENCOUNTER_STEPS if is_first else STANDARD_STEPS

        if i < 7:
            week_offset = i - 7
            sched_from = now + timedelta(days=7 * week_offset)
            sched_to = sched_from + timedelta(hours=1)
            meta = lucky_dialogues[i]

            actual_from = sched_from + timedelta(minutes=1)
            actual_to = actual_from + timedelta(minutes=58)

            doc = {
                "_id": oid(enc_id),
                "mentor_id": oid(meta["mentor_id"]),
                "mentee_id": oid(lucky_id),
                "appointment": {
                    "from": date_dict(sched_from),
                    "to": date_dict(sched_to),
                },
                "actual": {
                    "from": date_dict(actual_from),
                    "to": date_dict(actual_to),
                },
                "plan_id": oid(plan_id),
                "agenda": build_agenda(steps, "complete", False),
                "status": "complete",
                "no_show": False,
                "transcript": meta["transcript"],
                "summary": meta["summary"],
                "tldr": meta["tldr"],
                "created": {
                    "from_ip": "127.0.0.1",
                    "by_user": meta["by_user"],
                    "at_time": date_dict(sched_from),
                    "correlation_id": f"seed-enc-lucky-{i+1:02d}",
                },
                "saved": {
                    "from_ip": "127.0.0.1",
                    "by_user": meta["by_user"],
                    "at_time": date_dict(sched_to),
                    "correlation_id": f"save-enc-lucky-{i+1:02d}",
                },
            }
            encounters.append(doc)
        elif i == 7:
            # Week 0: 1 active encounter in progress right now
            sched_from = now - timedelta(minutes=15)
            sched_to = sched_from + timedelta(hours=1)
            actual_from = sched_from + timedelta(minutes=2)
            doc = {
                "_id": oid(enc_id),
                "mentor_id": oid(danny_id),
                "mentee_id": oid(lucky_id),
                "appointment": {
                    "from": date_dict(sched_from),
                    "to": date_dict(sched_to),
                },
                "actual": {
                    "from": date_dict(actual_from),
                    "to": date_dict(sched_to),
                },
                "plan_id": oid(plan_id),
                "agenda": build_agenda(steps, "active", False),
                "status": "active",
                "no_show": False,
                "transcript": "#### Danny\nLucky, we are live in session reviewing your weekly service metrics.\n\n#### Lucky\nP95 latency remained under 120ms throughout yesterday's load surge.\n\n#### Danny\nExcellent. Let's finish checking the remaining agenda items.",
                "summary": "## Summary\n**Summary:** Mid-session review of weekly service performance; meeting is currently active.",
                "tldr": "Active session: Danny and Lucky reviewing SuperSoft weekly latency metrics in progress.",
                "created": {
                    "from_ip": "127.0.0.1",
                    "by_user": "danny",
                    "at_time": date_dict(sched_from),
                    "correlation_id": f"seed-enc-lucky-{i+1:02d}",
                },
                "saved": {
                    "from_ip": "127.0.0.1",
                    "by_user": "danny",
                    "at_time": date_dict(now),
                    "correlation_id": f"save-enc-lucky-{i+1:02d}",
                },
            }
            encounters.append(doc)
        else:
            # Future scheduled sessions: weeks +1 to +4
            week_offset = (i - 7)
            sched_from = now + timedelta(days=7 * week_offset)
            sched_to = sched_from + timedelta(hours=1)
            doc = {
                "_id": oid(enc_id),
                "mentor_id": oid(danny_id),
                "mentee_id": oid(lucky_id),
                "appointment": {
                    "from": date_dict(sched_from),
                    "to": date_dict(sched_to),
                },
                "plan_id": oid(plan_id),
                "agenda": build_agenda(steps, "scheduled", False),
                "status": "scheduled",
                "created": {
                    "from_ip": "127.0.0.1",
                    "by_user": "danny",
                    "at_time": date_dict(now),
                    "correlation_id": f"seed-enc-lucky-{i+1:02d}",
                },
                "saved": {
                    "from_ip": "127.0.0.1",
                    "by_user": "danny",
                    "at_time": date_dict(now),
                    "correlation_id": f"save-enc-lucky-{i+1:02d}",
                },
            }
            encounters.append(doc)

    # =========================================================================
    # 3. Mary Anderson (Self-funded Apprentice Mentee)
    # Mixture of completed (weeks -8 to -1) and scheduled (weeks +1 to +4).
    # Includes authentic cold / GitHub staff job / microservices encounter (week -3)
    # and authentic Stripe research / ERD data model session (week -5).
    # =========================================================================
    mary_dialogues = [
        # Session 1 (week -8): FirstEncounter
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Marti Lombardi conducted Mary Anderson's initial ALI apprenticeship onboarding session.",
            "summary": "## Summary\n**Summary:** Marti Lombardi welcomed Mary Anderson to her self-funded engineering apprenticeship. They reviewed Mary's career transition goals, established bi-weekly meeting rhythms, and toured the Mentee Journey roadmap.",
            "transcript": "#### Marti\nMary, you self-funded this apprenticeship—what outcome do you want from our bi-weekly sessions?\n\n#### Mary\nI need confidence designing REST endpoints for my capstone without over-scoping the database layer.\n\n#### Marti\nLet's sketch the ER diagram together and map each entity to a minimal OpenAPI path set.",
        },
        # Session 2 (week -7): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Marti helped Mary scope REST endpoints and entity relationship design for her capstone.",
            "summary": "## Summary\n**Summary:** Marti Lombardi and Mary Anderson aligned on self-funded capstone goals. They sketched domain entities for Mary's REST API and agreed on a minimal OpenAPI surface.",
            "transcript": "#### Marti\nLet's examine your entity model drafts.\n\n#### Mary\nI split the user profile from the authentication credentials, but I'm wondering if subscriptions belong on the customer.\n\n#### Marti\nEmbedding subscriptions on the customer document is much cleaner for document databases.",
        },
        # Session 3 (week -6): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Mary showed OpenAPI pagination work; Marti assigned 404 and 422 error schema tasks.",
            "summary": "## Summary\n**Summary:** Mary reviewed her OpenAPI progress with Marti, covering collection versus singleton routes and pagination parameters. Marti confirmed strong API design momentum and assigned error-response schema work.",
            "transcript": "#### Marti\nWalk me through the OpenAPI paths you added since our last session.\n\n#### Mary\nI split collection routes from singleton routes and documented pagination query params.\n\n#### Marti\nSolid API design progress. Before next week, add error response schemas for 404 and 422 cases.",
        },
        # Session 4 (week -5): Authentic sample with Mike Storey (Stripe, webhooks, payments, subscriptions)
        {
            "mentor_id": mike_id,
            "by_user": "mike",
            "tldr": "They decided to simplify the data model by removing card and dashboard collections, embedding subscriptions in the customer entity, and adding payments for Stripe webhooks.",
            "summary": "## Summary\n**Summary:** Mike and Mary start with casual chat about noisy landscaping outside Mike’s house, then move into a work session focused on the MentorHub project. Mary wants help finishing the FWO2 tickets, and Mike walks her through his mental model for breaking down UI pages, APIs, and data structures. They agree that storing credit-card data in Stripe is preferable, so they plan to drop the 'card' collection, eliminate the customizable dashboard for the MVP, and move subscription information into the customer document. Mike suggests adding a new collection ('payments') to capture Stripe webhook events.",
            "transcript": "#### Mike\nLandscaping is going on outside my door today, so it might be a little noisy. But all those trees blocking my view are coming down! So what would you like to focus on today?\n\n#### Mary\nFinishing FWO2 and the tickets that follow behind it, so you don't have to look over my shoulder all the time.\n\n#### Mike\nOur approach to credit card is probably not appropriate. If we avoid storing credit card information and let it persist in Stripe, we avoid regulatory compliance issues.\n\n#### Mary\nRight, basic form on our end with name and email, and a button to connect to Stripe so we don't store it.\n\n#### Mike\nExactly. In our customer schema, we'll have an array of subscriptions. When Stripe processes payment, they notify our webhook, and we persist the webhook receipt in a payments collection.\n\n#### Mary\nSo we delete card, delete dashboard, and move subscriptions into customer?\n\n#### Mike\nRight! We simplify the data structure significantly. Let's research the exact webhook payloads and document them before making schema edits.\n\n#### Mary\nSounds great, I'll document the research in Markdown.",
        },
        # Session 5 (week -4): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Marti reviewed Mary's webhook payload documentation and approved the payments collection design.",
            "summary": "## Summary\n**Summary:** Marti and Mary reviewed research findings on Stripe checkout sessions and payment webhooks. Confirmed database structures align with external webhook events.",
            "transcript": "#### Marti\nHow did your research on the Stripe webhook structures turn out?\n\n#### Mary\nI documented the payment_intent.succeeded and invoice.payment_failed payloads in Markdown.\n\n#### Marti\nVery thorough research. That will make implementing the payments collection schema straightforward.",
        },
        # Session 6 (week -3): Authentic sample with Mike Storey (Cold, GitHub job listing, microservices, asynchronous bus)
        {
            "mentor_id": mike_id,
            "by_user": "mike",
            "tldr": "Mary is dealing with a cold but can work later; Mike outlined the GitHub job's heavy technical demands and mapped them to experiences Mary will gain through Mentor Hub, recommending she finish Python training before tackling architecture topics next week.",
            "summary": "## Summary\n**Summary:** Mary and Mike discussed Mary’s cold and upcoming work schedule, then shifted focus to a GitHub staff software engineer job listing that requires extensive experience in large-scale system architecture, cloud deployment, microservices, DevOps practices (including on-call responsibilities), scripting languages (Bash/Python), GraphQL, asynchronous messaging systems (Kafka/RabbitMQ), CI/CD pipelines, and familiarity with AWS/Azure services. Mike explained how the Mentor Hub project aligns with many of these requirements—providing Mary hands-on experience with cloud architecture, microservices, event-driven design, and API development—and suggested she complete a Python course first before diving deeper into architectural concepts during upcoming sessions. Both agreed to continue building relevant skills step-by-step.",
            "transcript": "#### Mary\nHey Mike.\n\n#### Mike\nHey, Mary. How are you today?\n\n#### Mary\nI have a cold, but I still wanted to meet. I have my assignments to do.\n\n#### Mike\nI glanced at those different job offerings you sent. Which one sounded like the one you believed in?\n\n#### Mary\nI thought about GitHub. We're already working in GitHub, so I feel like we could work on whatever I'm missing.\n\n#### Mike\nStaff software engineer for GitHub. They want demonstrated experience with large-scale system architecture and design in cloud-based environments with microservices. Guess what MentorHub is? It's a cloud-based microservice architecture.\n\n#### Mary\nThose are the environments I've been training on. I want more experience.\n\n#### Mike\nAll of our APIs are written in Python, and the MH command line utility is a Bash script. And for asynchronous messaging, webhooks receive inbound data, but at scale you use message queuing like Kafka or RabbitMQ. It's like a mailbox: you drop an event in, and subscribers process it independently.\n\n#### Mary\nRight, so the services stay completely independent.\n\n#### Mike\nExactly. Finish that introductory Python course first, and next week when we do architectural reviews, pay special attention to how MentorHub maps to these cloud patterns.\n\n#### Mary\nI'm ready to tackle this. Thank you, Mike. Peace.",
        },
        # Session 7 (week -2): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Mary completed her Python introductory modules and verified Flask route decorators.",
            "summary": "## Summary\n**Summary:** Mary demonstrated completion of the Python course exercises. Marti verified Flask route decorators and blueprint structuring.",
            "transcript": "#### Marti\nMary, congratulations on finishing the introductory Python course.\n\n#### Mary\nThanks Marti. Understanding functions, dictionaries, and blueprints made the API code so much clearer.\n\n#### Marti\nNow you're equipped to build domain routes directly against MongoIO.",
        },
        # Session 8 (week -1): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Marti and Mary planned architectural review checkpoints for the MentorHub cloud deployment.",
            "summary": "## Summary\n**Summary:** Final pre-architecture session reviewing Docker containerization and AWS ECS deployment patterns.",
            "transcript": "#### Marti\nNext week begins the cloud architecture series Mike mentioned. Ready to dive in?\n\n#### Mary\nYes, I'm ready to connect my Python API work to the broader cloud infrastructure.\n\n#### Marti\nSolid foundation. See you at stand-up.",
        },
    ]

    for i in range(12):
        enc_id = f"E{serial:023x}"
        serial += 1
        is_first = (i == 0)
        plan_id = FIRST_ENCOUNTER_PLAN_ID if is_first else STANDARD_PLAN_ID
        steps = FIRST_ENCOUNTER_STEPS if is_first else STANDARD_STEPS

        if i < 8:
            week_offset = i - 8
            sched_from = now + timedelta(days=7 * week_offset)
            sched_to = sched_from + timedelta(hours=1)
            meta = mary_dialogues[i]

            actual_from = sched_from + timedelta(minutes=2)
            actual_to = actual_from + timedelta(minutes=56)

            doc = {
                "_id": oid(enc_id),
                "mentor_id": oid(meta["mentor_id"]),
                "mentee_id": oid(mary_id),
                "appointment": {
                    "from": date_dict(sched_from),
                    "to": date_dict(sched_to),
                },
                "actual": {
                    "from": date_dict(actual_from),
                    "to": date_dict(actual_to),
                },
                "plan_id": oid(plan_id),
                "agenda": build_agenda(steps, "complete", False),
                "status": "complete",
                "no_show": False,
                "transcript": meta["transcript"],
                "summary": meta["summary"],
                "tldr": meta["tldr"],
                "created": {
                    "from_ip": "127.0.0.1",
                    "by_user": meta["by_user"],
                    "at_time": date_dict(sched_from),
                    "correlation_id": f"seed-enc-mary-{i+1:02d}",
                },
                "saved": {
                    "from_ip": "127.0.0.1",
                    "by_user": meta["by_user"],
                    "at_time": date_dict(sched_to),
                    "correlation_id": f"save-enc-mary-{i+1:02d}",
                },
            }
            encounters.append(doc)
        else:
            # Future scheduled sessions: weeks +1 to +4
            week_offset = (i - 8) + 1
            sched_from = now + timedelta(days=7 * week_offset)
            sched_to = sched_from + timedelta(hours=1)
            doc = {
                "_id": oid(enc_id),
                "mentor_id": oid(marti_id),
                "mentee_id": oid(mary_id),
                "appointment": {
                    "from": date_dict(sched_from),
                    "to": date_dict(sched_to),
                },
                "plan_id": oid(plan_id),
                "agenda": build_agenda(steps, "scheduled", False),
                "status": "scheduled",
                "created": {
                    "from_ip": "127.0.0.1",
                    "by_user": "marti",
                    "at_time": date_dict(now),
                    "correlation_id": f"seed-enc-mary-{i+1:02d}",
                },
                "saved": {
                    "from_ip": "127.0.0.1",
                    "by_user": "marti",
                    "at_time": date_dict(now),
                    "correlation_id": f"save-enc-mary-{i+1:02d}",
                },
            }
            encounters.append(doc)

    # =========================================================================
    # 4. Linda Left (Archived ALI Mentee)
    # ONLY historical completed encounters (weeks -12 to -1).
    # Includes authentic Jillian/Linda & Mike onboarding session (week -12).
    # Includes 1 no-show (week -6).
    # =========================================================================
    linda_dialogues = [
        # Session 1 (week -12): Authentic sample with Mike Storey (Data engineering roadmap, MongoDB, PostgreSQL, Mac)
        {
            "mentor_id": mike_id,
            "by_user": "mike",
            "tldr": "Linda got a roadmap to transition into data engineering—starting with MongoDB training, then PostgreSQL—plus help setting up her Mac, accounts, and daily stand-up logistics.",
            "summary": "## Summary\n**Summary:** Linda asked Mike for professional advice on re-entering the tech workforce after a five-year gap, wondering whether to focus on data engineering or data analysis. Mike highlighted that Linda already knows JavaScript/Node.js and has experience with MongoDB and Mongoose, and suggested starting with free MongoDB developer courses (≈20 hours) that lead to a certification discount. He explained the basics of document vs. relational databases, recommending later study of PostgreSQL, and introduced concepts like indexing and data modeling. They also discussed practical setup: Linda's Mac purchase, accessories, configuring Discord backgrounds, and linking work Google calendar for daily stand-up meetings. Finally, they coordinated future onboarding steps and scheduled regular stand-ups.",
            "transcript": "#### Mike\nAll right. So what would you like to focus on today?\n\n#### Linda\nI really want to get a professional opinion from you. I've been out of the game for five years. What focus should I invest in? I keep hearing data engineer or data analysis.\n\n#### Mike\nYou already know JavaScript and Node.js. If you want to pursue data engineering, let's start with document databases like MongoDB and ODM tools like Mongoose.\n\n#### Linda\nYes, Mongoose seemed very straightforward and simple.\n\n#### Mike\nThere's a free 20-hour developer course from Mongo with a 50% certification discount. After that, we'll look at relational databases like PostgreSQL, which store tables with rows and columns.\n\n#### Linda\nI have experience with Excel, so rows and columns make sense to me.\n\n#### Mike\nAnd when you get your Mac set up, we'll install the MentorHub developer environment so you can clone the source code and run the whole stack locally.\n\n#### Linda\nThat's awesome. I can't wait to get my Mac and start setting up the local environment.\n\n#### Mike\nCheck your calendar for the stand-up invite every morning Monday through Friday.\n\n#### Linda\nI see the calendar invite now. Thank you, Mike! Talk to you tomorrow for stand-up. Peace.",
        },
        # Session 2 (week -11): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Marti verified Linda's CSS Grid homework and introduced DOM event handling.",
            "summary": "## Summary\n**Summary:** Reviewed semantic markup and CSS grid responsive design; transitioned to DOM event listeners.",
            "transcript": "#### Marti\nLet's review semantic HTML and CSS Grid layouts from your homework.\n\n#### Linda\nI created responsive page layouts without relying on third-party CSS frameworks.\n\n#### Marti\nClean semantic structure. Next, let's explore JavaScript DOM manipulation.",
        },
        # Session 3 (week -10): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Linda demonstrated real-time form validation with regex pattern matching.",
            "summary": "## Summary\n**Summary:** Evaluated Linda's client-side form validation logic and error messaging.",
            "transcript": "#### Marti\nHow did the interactive form validation exercises go?\n\n#### Linda\nI added real-time validation for email and password fields using regex.\n\n#### Marti\nExcellent feedback loop for users. Let's connect this form to a mock REST endpoint next.",
        },
        # Session 4 (week -9): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Linda converted asynchronous data fetching to async/await syntax with robust error handling.",
            "summary": "## Summary\n**Summary:** Practiced modern asynchronous JavaScript fetch patterns and error handling with try/catch.",
            "transcript": "#### Marti\nToday we review fetch requests and async/await syntax.\n\n#### Linda\nI replaced XMLHttpRequest callbacks with async/await and try/catch blocks.\n\n#### Marti\nMuch cleaner and more maintainable error handling.",
        },
        # Session 5 (week -8): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Marti and Linda scoped the community resource directory capstone application.",
            "summary": "## Summary\n**Summary:** Scaffolded Linda's capstone community resource directory and established milestone targets.",
            "transcript": "#### Marti\nLet's discuss your capstone project scope.\n\n#### Linda\nI want to build a community resource directory with search and tag filtering.\n\n#### Marti\nThat's a great portfolio piece. Let's design the component hierarchy.",
        },
        # Session 6 (week -7): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Linda demonstrated debounced live search filtering for her capstone project.",
            "summary": "## Summary\n**Summary:** Reviewed debounced search filter implementation for the capstone directory.",
            "transcript": "#### Marti\nHow is the search indexing behaving with client-side filters?\n\n#### Linda\nThe search filter updates instantly on keystroke with a 300ms debounce.\n\n#### Marti\nAdding debounce shows mature UX consideration.",
        },
        # Session 7 (week -6): No-show (omitted transcript/summary/tldr)
        None,
        # Session 8 (week -5): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Linda demonstrated accessible keyboard navigation and modal dialogs.",
            "summary": "## Summary\n**Summary:** Reviewed accessibility and keyboard navigation enhancements following Linda's excused absence.",
            "transcript": "#### Marti\nGood to see you back Linda. Let's catch up on the directory details.\n\n#### Linda\nI finished the card modal details and accessible keyboard navigation.\n\n#### Marti\nAccessibility is essential for any public directory. Solid work.",
        },
        # Session 9 (week -4): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Marti and Linda verified cross-browser compatibility and mobile responsiveness.",
            "summary": "## Summary\n**Summary:** Validated cross-browser rendering and responsive mobile viewports for the capstone.",
            "transcript": "#### Marti\nLet's conduct a cross-browser layout inspection.\n\n#### Linda\nI tested on Chrome, Firefox, and Safari on mobile viewport sizes.\n\n#### Marti\nResponsive design is solid across all three rendering engines.",
        },
        # Session 10 (week -3): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Marti reviewed Linda's portfolio deployment and interview readiness.",
            "summary": "## Summary\n**Summary:** Reviewed GitHub Pages deployment and prepared developer portfolio presentation.",
            "transcript": "#### Marti\nWe're approaching your graduation from the ALI program. Let's review your resume and portfolio deploy.\n\n#### Linda\nThe capstone is deployed to GitHub Pages with continuous deployment.\n\n#### Marti\nProfessional presentation. You're well prepared for job interviews.",
        },
        # Session 11 (week -2): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Linda demonstrated strong conceptual grasp during mock technical interview.",
            "summary": "## Summary\n**Summary:** Conducted mock technical interview covering core frontend and JavaScript runtime concepts.",
            "transcript": "#### Marti\nLet's do a practice technical interview.\n\n#### Linda\nI walked through the event loop, closures, and responsive CSS strategies.\n\n#### Marti\nConfident, clear explanations throughout.",
        },
        # Session 12 (week -1): Standard
        {
            "mentor_id": marti_id,
            "by_user": "marti",
            "tldr": "Final session: Marti and Linda closed out Linda's ALI capstone before alumni transition.",
            "summary": "## Summary\n**Summary:** Marti Lombardi held the final mentoring session with Linda Left before archival. They confirmed capstone export and homework completion; all historical records retained for alumni reference.",
            "transcript": "#### Marti\nLinda, you're wrapping up your ALI program—let's archive your journey artifacts and capture final mentor notes.\n\n#### Linda\nI've exported my capstone repo and closed the remaining homework items.\n\n#### Marti\nPerfect handoff. I'll mark this session complete as you transition to alumni status.",
        },
    ]

    for i in range(12):
        enc_id = f"E{serial:023x}"
        serial += 1
        is_first = (i == 0)
        plan_id = FIRST_ENCOUNTER_PLAN_ID if is_first else STANDARD_PLAN_ID
        steps = FIRST_ENCOUNTER_STEPS if is_first else STANDARD_STEPS

        week_offset = i - 12
        sched_from = now + timedelta(days=7 * week_offset)
        sched_to = sched_from + timedelta(hours=1)
        is_no_show = (i == 6)  # week -6 is no-show

        meta = linda_dialogues[i]
        mentor_id = marti_id if is_no_show else meta["mentor_id"]
        mentor_user = "marti" if is_no_show else meta["by_user"]

        doc = {
            "_id": oid(enc_id),
            "mentor_id": oid(mentor_id),
            "mentee_id": oid(linda_id),
            "appointment": {
                "from": date_dict(sched_from),
                "to": date_dict(sched_to),
            },
            "plan_id": oid(plan_id),
            "agenda": build_agenda(steps, "complete", is_no_show),
            "status": "complete",
            "no_show": is_no_show,
        }

        if not is_no_show:
            actual_from = sched_from + timedelta(minutes=3)
            actual_to = actual_from + timedelta(minutes=53)
            doc["actual"] = {
                "from": date_dict(actual_from),
                "to": date_dict(actual_to),
            }
            doc["transcript"] = meta["transcript"]
            doc["summary"] = meta["summary"]
            doc["tldr"] = meta["tldr"]

        doc["created"] = {
            "from_ip": "127.0.0.1",
            "by_user": mentor_user,
            "at_time": date_dict(sched_from),
            "correlation_id": f"seed-enc-linda-{i+1:02d}",
        }
        doc["saved"] = {
            "from_ip": "127.0.0.1",
            "by_user": mentor_user,
            "at_time": date_dict(sched_to),
            "correlation_id": f"save-enc-linda-{i+1:02d}",
        }
        encounters.append(doc)

    # =========================================================================
    # 5. Pat Persevere (Roster Mentee pending first session)
    # ONLY future scheduled encounters (weeks +1 to +12).
    # Mentee has booked sessions on the Persevere track with Paula, but has not
    # started any encounters yet.
    # =========================================================================
    for i in range(12):
        enc_id = f"E{serial:023x}"
        serial += 1
        is_first = (i == 0)
        plan_id = FIRST_ENCOUNTER_PLAN_ID if is_first else STANDARD_PLAN_ID
        steps = FIRST_ENCOUNTER_STEPS if is_first else STANDARD_STEPS

        week_offset = i + 1
        sched_from = now + timedelta(days=7 * week_offset)
        sched_to = sched_from + timedelta(hours=1)

        doc = {
            "_id": oid(enc_id),
            "mentor_id": oid(paula_id),
            "mentee_id": oid(pat_id),
            "appointment": {
                "from": date_dict(sched_from),
                "to": date_dict(sched_to),
            },
            "plan_id": oid(plan_id),
            "agenda": build_agenda(steps, "scheduled", False),
            "status": "scheduled",
            "created": {
                "from_ip": "127.0.0.1",
                "by_user": "paula",
                "at_time": date_dict(now),
                "correlation_id": f"seed-enc-pat-{i+1:02d}",
            },
            "saved": {
                "from_ip": "127.0.0.1",
                "by_user": "paula",
                "at_time": date_dict(now),
                "correlation_id": f"save-enc-pat-{i+1:02d}",
            },
        }
        encounters.append(doc)

    return encounters


def main() -> None:
    encounters = generate_encounters()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Validate constraints
    for doc in encounters:
        if "tldr" in doc:
            tldr = doc["tldr"]
            assert len(tldr) <= 255, f"tldr too long: {len(tldr)}"
            assert "\n" not in tldr and "\t" not in tldr, "tldr has newline/tab"
        if "summary" in doc:
            summary = doc["summary"]
            assert len(summary) <= 4096, f"summary too long: {len(summary)}"
        if "transcript" in doc:
            transcript = doc["transcript"]
            assert len(transcript) <= 4096, f"transcript too long: {len(transcript)}"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(encounters, f, indent=2)
        f.write("\n")
    print(f"Successfully generated {len(encounters)} Encounter documents to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
