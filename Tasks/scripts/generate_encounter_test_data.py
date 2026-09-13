#!/usr/bin/env python3
"""Generate expanded Encounter test data conforming to issue #79 (F-D33).

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
    daniel_id = profiles["daniel"]      # A...02
    lucky_id = profiles["lucky"]        # A...03
    mary_id = profiles["mary"]          # A...04
    linda_id = profiles["linda"]        # A...05

    paula_id = profiles["paula"]        # A...10
    elon_id = profiles["elon"]          # A...11
    danny_id = profiles["danny"]        # A...14
    marti_id = profiles["marti"]        # A...06

    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)

    encounters: list[dict] = []
    serial = 1

    # =========================================================================
    # 1. Daniel Dissler (Persevere Mentee)
    # Mixture of completed (weeks -8 to -1) and scheduled (weeks +1 to +4).
    # Includes 1 Money Mentor session (Elon, week -4) and 1 no-show (week -2).
    # =========================================================================
    daniel_dialogues = [
        # Session 1 (week -8): FirstEncounter
        {
            "transcript": "**Paula:** Welcome Daniel to the Persevere mentoring track. In this first onboarding session, we'll map your 12-week commitment and capstone milestones.\n\n**Daniel:** I'm excited to dive in. My focus is mastering Vue 3 composition API and building a capstone dashboard.\n\n**Paula:** Excellent. We've introduced the Mentee Journey interface today so you can track your roadmap.",
            "summary": "## Summary\nPaula Persevere welcomed Daniel Dissler to the Persevere learning journey. They walked through the ALI intro, aligned on a 12-week mentoring commitment, and toured the Mentee Journey roadmap interface.",
            "tldr": "Daniel and Paula completed their initial onboarding session and agreed on 12-week capstone goals.",
        },
        # Session 2 (week -7)
        {
            "transcript": "**Paula:** Daniel, let's review your Vue component architecture sketches.\n\n**Daniel:** I started scaffolding the dashboard navigation and cards using Vue Router.\n\n**Paula:** Clean layout. Next step is extracting state into a Pinia store.",
            "summary": "## Summary\nReviewed Daniel's initial Vue Router structure and dashboard scaffolding. Paula recommended introducing Pinia for shared state.",
            "tldr": "Paula reviewed Daniel's dashboard layout and assigned Pinia store integration.",
        },
        # Session 3 (week -6)
        {
            "transcript": "**Paula:** How did the Pinia store integration go?\n\n**Daniel:** The store is working for auth state, but I'm getting TypeScript errors on the reactive getters.\n\n**Paula:** Let's inspect your type definitions. We'll define an explicit interface for the user state.",
            "summary": "## Summary\nPair-debugged TypeScript typing issues in Daniel's Pinia user store. Verified reactive getters compile without errors.",
            "tldr": "Paula helped Daniel resolve TypeScript interface typing on Pinia auth getters.",
        },
        # Session 4 (week -5)
        {
            "transcript": "**Paula:** Today we focus on composables for data fetching.\n\n**Daniel:** I wrote a `useFetch` wrapper that handles auth headers and loading states.\n\n**Paula:** Great abstraction. Make sure you test the 401 token refresh interceptor before next week.",
            "summary": "## Summary\nEvaluated Daniel's custom `useFetch` composable. Confirmed loading and error states are handled; set next step on token refresh logic.",
            "tldr": "Daniel demonstrated custom Vue fetch composable with error handling and loading indicators.",
        },
        # Session 5 (week -4): Compensated session with Elon Money
        {
            "transcript": "**Elon:** Daniel, let's pressure-test your Persevere capstone pitch — what problem does your SPA solve and who pays for it?\n\n**Daniel:** It's a cohort progress dashboard for nonprofit program managers evaluating graduate outcomes.\n\n**Elon:** Good framing. Tighten the unit economics slide and we'll mark this as a compensated money-mentor review session.",
            "summary": "## Summary\nElon Money mentored Daniel Dissler on startup pitch structure for the Persevere capstone. They refined problem framing and unit economics; this was a **compensated** money-mentor session.",
            "tldr": "Compensated money-mentor session: Elon reviewed Daniel's Persevere capstone pitch and unit economics.",
        },
        # Session 6 (week -3)
        {
            "transcript": "**Paula:** Following your session with Elon, let's wire the live API endpoints to the dashboard metrics view.\n\n**Daniel:** I connected the cohort summary endpoint and formatted the date filters.\n\n**Paula:** The layout is coming together nicely. Let's do a practice walkthrough.",
            "summary": "## Summary\nDaniel demonstrated live API data rendering in the cohort progress dashboard. Paula verified date filter responsiveness.",
            "tldr": "Paula and Daniel connected live cohort metrics API endpoints to the capstone frontend.",
        },
        # Session 7 (week -2): No-show (omitted transcript/summary/tldr)
        None,
        # Session 8 (week -1)
        {
            "transcript": "**Paula:** Glad you're feeling better after missing last week, Daniel. Let's run a full regression before cohort demo day.\n\n**Daniel:** All tests passed and error states are handled with toast notifications.\n\n**Paula:** Outstanding progress. We're ready for your cohort presentation.",
            "summary": "## Summary\nPaula and Daniel conducted a comprehensive pre-demo review of the capstone SPA, verifying end-to-end user flows and toast notifications.",
            "tldr": "Paula verified Daniel's pre-demo capstone checklist and test coverage.",
        },
    ]

    for i in range(12):
        enc_id = f"E{serial:023x}"
        serial += 1
        is_first = (i == 0)
        plan_id = FIRST_ENCOUNTER_PLAN_ID if is_first else STANDARD_PLAN_ID
        steps = FIRST_ENCOUNTER_STEPS if is_first else STANDARD_STEPS

        if i < 8:
            # Past completed sessions: weeks -8 to -1
            week_offset = i - 8
            sched_from = now + timedelta(days=7 * week_offset)
            sched_to = sched_from + timedelta(hours=1)
            is_no_show = (i == 6)  # week -2 is no-show
            mentor_id = elon_id if (i == 4) else paula_id
            mentor_user = "elon" if (i == 4) else "paula"

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
                meta = daniel_dialogues[i]
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
    # Includes 1 Money Mentor session (Elon, week -4).
    # =========================================================================
    lucky_dialogues = [
        # Session 1 (week -7): FirstEncounter
        {
            "transcript": "**Danny:** Welcome Lucky to SuperSoft engineering mentorship. In this introductory session, we'll establish your reliability and backend objectives.\n\n**Lucky:** Thanks Danny. I want to build automated deployment verification and on-call paging pipelines.\n\n**Danny:** We walked through the ALI philosophy and your 12-week roadmap in the Mentee Journey app.",
            "summary": "## Summary\nDanny Dev Lead kicked off Lucky Minyard's SuperSoft SRE apprenticeship with onboarding, roadmap orientation, and tooling setup.",
            "tldr": "Danny and Lucky completed onboarding and established SuperSoft reliability goals.",
        },
        # Session 2 (week -6)
        {
            "transcript": "**Danny:** Lucky, let's inspect your current manual deploy checklist.\n\n**Lucky:** Right now it takes 15 manual curl commands across three staging environments.\n\n**Danny:** We'll script that into a python automated health-check CLI.",
            "summary": "## Summary\nAnalyzed manual deployment verification bottlenecks; designed automated health check suite.",
            "tldr": "Danny and Lucky planned an automated health-check script to replace manual curl steps.",
        },
        # Session 3 (week -5)
        {
            "transcript": "**Danny:** How did the initial health-check script run in staging?\n\n**Lucky:** It successfully verified Mongo connectivity and flagged an expired TLS cert before promote.\n\n**Danny:** That's an immediate win. Next, add automated rollback triggering.",
            "summary": "## Summary\nReviewed staging run of health-check automation; script prevented a broken deployment due to expired TLS cert.",
            "tldr": "Lucky's deployment script blocked a bad promotion, proving SRE value.",
        },
        # Session 4 (week -4): Compensated session with Elon Money
        {
            "transcript": "**Elon:** Lucky, SuperSoft is paying for engineering depth — how do you justify the reliability work to a budget holder?\n\n**Lucky:** I can tie each health check to reduced incident minutes and faster rollback time.\n\n**Elon:** That's the story investors expect. We'll log this as a compensated money-mentor advisory on technical due diligence.",
            "summary": "## Summary\nElon Money coached Lucky Minyard on articulating SuperSoft reliability investments to budget holders. Lucky linked health checks to incident reduction; this was a **compensated** session.",
            "tldr": "Compensated money-mentor session: Elon coached Lucky on ROI framing for reliability work.",
        },
        # Session 5 (week -3)
        {
            "transcript": "**Danny:** Let's discuss Prometheus alerting thresholds for on-call paging.\n\n**Lucky:** I configured P95 latency alerts at 250ms and error rates above 1% over 5 minutes.\n\n**Danny:** Sensible thresholds to avoid alert fatigue. Let's run a chaos drill.",
            "summary": "## Summary\nConfigured Prometheus alerting rules and pager thresholds for SuperSoft core services.",
            "tldr": "Danny and Lucky tuned Prometheus latency and error alerts to avoid alert fatigue.",
        },
        # Session 6 (week -2)
        {
            "transcript": "**Danny:** Walk me through yesterday's staging chaos test.\n\n**Lucky:** We injected 5% network packet loss; the circuit breaker tripped and gracefully degraded within 2 seconds.\n\n**Danny:** Excellent resilience demonstration.",
            "summary": "## Summary\nEvaluated chaos test drill results; circuit breaker validated fault tolerance under simulated network loss.",
            "tldr": "Chaos engineering drill verified SuperSoft circuit breaker operation.",
        },
        # Session 7 (week -1)
        {
            "transcript": "**Danny:** Today we prepare for the production readiness review.\n\n**Lucky:** Runbooks are updated and grafana dashboards are grouped by SLA.\n\n**Danny:** You're ready for primary on-call rotation starting next week.",
            "summary": "## Summary\nFinal production readiness review for SuperSoft on-call transition. Verified runbook links and dashboards.",
            "tldr": "Danny approved Lucky's production readiness and on-call rotation schedule.",
        },
    ]

    for i in range(12):
        enc_id = f"E{serial:023x}"
        serial += 1
        is_first = (i == 0)
        plan_id = FIRST_ENCOUNTER_PLAN_ID if is_first else STANDARD_PLAN_ID
        steps = FIRST_ENCOUNTER_STEPS if is_first else STANDARD_STEPS

        if i < 7:
            # Past completed sessions: weeks -7 to -1
            week_offset = i - 7
            sched_from = now + timedelta(days=7 * week_offset)
            sched_to = sched_from + timedelta(hours=1)
            mentor_id = elon_id if (i == 3) else danny_id
            mentor_user = "elon" if (i == 3) else "danny"

            actual_from = sched_from + timedelta(minutes=1)
            actual_to = actual_from + timedelta(minutes=58)
            meta = lucky_dialogues[i]

            doc = {
                "_id": oid(enc_id),
                "mentor_id": oid(mentor_id),
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
                    "by_user": mentor_user,
                    "at_time": date_dict(sched_from),
                    "correlation_id": f"seed-enc-lucky-{i+1:02d}",
                },
                "saved": {
                    "from_ip": "127.0.0.1",
                    "by_user": mentor_user,
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
                "transcript": "**Danny:** Lucky, we are live in session reviewing your weekly service metrics.\n\n**Lucky:** P95 latency remained under 120ms throughout yesterday's load surge.\n\n**Danny:** Excellent. Let's finish checking the remaining agenda items.",
                "summary": "## Summary\nMid-session review of weekly service performance; meeting is currently active.",
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
    # 3. Mary Anderson (Self-funded Super Mentee)
    # ONLY future scheduled encounters (weeks +1 to +12).
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
    # Includes 1 no-show (week -6).
    # =========================================================================
    linda_dialogues = [
        # Session 1 (week -12): FirstEncounter
        {
            "transcript": "**Marti:** Welcome Linda to the Agile Learning Institute mentorship track. Today we'll set expectations for your career pivot into web development.\n\n**Linda:** I'm transitioning from administration to frontend engineering. I want to build strong fundamentals in HTML, CSS, and vanilla JS.\n\n**Marti:** Perfect alignment. We've introduced the Mentee Journey roadmap to guide your progression.",
            "summary": "## Summary\nMarti Lombardi conducted Linda Left's initial onboarding session, establishing core learning objectives and milestone timeline.",
            "tldr": "Marti and Linda completed initial ALI onboarding and established frontend learning goals.",
        },
        # Session 2 (week -11)
        {
            "transcript": "**Marti:** Let's review semantic HTML and CSS Grid layouts from your homework.\n\n**Linda:** I created responsive page layouts without relying on third-party CSS frameworks.\n\n**Marti:** Clean semantic structure. Next, let's explore JavaScript DOM manipulation.",
            "summary": "## Summary\nReviewed semantic markup and CSS grid responsive design; transitioned to DOM event listeners.",
            "tldr": "Marti verified Linda's CSS Grid homework and introduced DOM event handling.",
        },
        # Session 3 (week -10)
        {
            "transcript": "**Marti:** How did the interactive form validation exercises go?\n\n**Linda:** I added real-time validation for email and password fields using regex.\n\n**Marti:** Excellent feedback loop for users. Let's connect this form to a mock REST endpoint next.",
            "summary": "## Summary\nEvaluated Linda's client-side form validation logic and error messaging.",
            "tldr": "Linda demonstrated real-time form validation with regex pattern matching.",
        },
        # Session 4 (week -9)
        {
            "transcript": "**Marti:** Today we review fetch requests and async/await syntax.\n\n**Linda:** I replaced XMLHttpRequest callbacks with async/await and try/catch blocks.\n\n**Marti:** Much cleaner and more maintainable error handling.",
            "summary": "## Summary\nPracticed modern asynchronous JavaScript fetch patterns and error handling with try/catch.",
            "tldr": "Linda converted asynchronous data fetching to async/await syntax with robust error handling.",
        },
        # Session 5 (week -8)
        {
            "transcript": "**Marti:** Let's discuss your capstone project scope.\n\n**Linda:** I want to build a community resource directory with search and tag filtering.\n\n**Marti:** That's a great portfolio piece. Let's design the component hierarchy.",
            "summary": "## Summary\nScaffolded Linda's capstone community resource directory and established milestone targets.",
            "tldr": "Marti and Linda scoped the community resource directory capstone application.",
        },
        # Session 6 (week -7)
        {
            "transcript": "**Marti:** How is the search indexing behaving with client-side filters?\n\n**Linda:** The search filter updates instantly on keystroke with a 300ms debounce.\n\n**Marti:** Adding debounce shows mature UX consideration.",
            "summary": "## Summary\nReviewed debounced search filter implementation for the capstone directory.",
            "tldr": "Linda demonstrated debounced live search filtering for her capstone project.",
        },
        # Session 7 (week -6): No-show (omitted transcript/summary/tldr)
        None,
        # Session 8 (week -5)
        {
            "transcript": "**Marti:** Good to see you back Linda. Let's catch up on the directory details.\n\n**Linda:** I finished the card modal details and accessible keyboard navigation.\n\n**Marti:** Accessibility is essential for any public directory. Solid work.",
            "summary": "## Summary\nReviewed accessibility and keyboard navigation enhancements following Linda's excused absence.",
            "tldr": "Linda demonstrated accessible keyboard navigation and modal dialogs.",
        },
        # Session 9 (week -4)
        {
            "transcript": "**Marti:** Let's conduct a cross-browser layout inspection.\n\n**Linda:** I tested on Chrome, Firefox, and Safari on mobile viewport sizes.\n\n**Marti:** Responsive design is solid across all three rendering engines.",
            "summary": "## Summary\nValidated cross-browser rendering and responsive mobile viewports for the capstone.",
            "tldr": "Marti and Linda verified cross-browser compatibility and mobile responsiveness.",
        },
        # Session 10 (week -3)
        {
            "transcript": "**Marti:** We're approaching your graduation from the ALI program. Let's review your resume and portfolio deploy.\n\n**Linda:** The capstone is deployed to GitHub Pages with continuous deployment.\n\n**Marti:** Professional presentation. You're well prepared for job interviews.",
            "summary": "## Summary\nReviewed GitHub Pages deployment and prepared developer portfolio presentation.",
            "tldr": "Marti reviewed Linda's portfolio deployment and interview readiness.",
        },
        # Session 11 (week -2)
        {
            "transcript": "**Marti:** Let's do a practice technical interview.\n\n**Linda:** I walked through the event loop, closures, and responsive CSS strategies.\n\n**Marti:** Confident, clear explanations throughout.",
            "summary": "## Summary\nConducted mock technical interview covering core frontend and JavaScript runtime concepts.",
            "tldr": "Linda demonstrated strong conceptual grasp during mock technical interview.",
        },
        # Session 12 (week -1): Final session before archival
        {
            "transcript": "**Marti:** Linda, you're wrapping up your ALI program — let's archive your journey artifacts and capture final mentor notes.\n\n**Linda:** I've exported my capstone repo and closed the remaining homework items.\n\n**Marti:** Perfect handoff. I'll mark this session complete as you transition to alumni status.",
            "summary": "## Summary\nMarti Lombardi held the final mentoring session with Linda Left before archival. They confirmed capstone export and homework completion; all historical records retained for alumni reference.",
            "tldr": "Final session: Marti and Linda closed out Linda's ALI capstone before alumni transition.",
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

        doc = {
            "_id": oid(enc_id),
            "mentor_id": oid(marti_id),
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
            meta = linda_dialogues[i]
            doc["transcript"] = meta["transcript"]
            doc["summary"] = meta["summary"]
            doc["tldr"] = meta["tldr"]

        doc["created"] = {
            "from_ip": "127.0.0.1",
            "by_user": "marti",
            "at_time": date_dict(sched_from),
            "correlation_id": f"seed-enc-linda-{i+1:02d}",
        }
        doc["saved"] = {
            "from_ip": "127.0.0.1",
            "by_user": "marti",
            "at_time": date_dict(sched_to),
            "correlation_id": f"save-enc-linda-{i+1:02d}",
        }
        encounters.append(doc)

    return encounters


def main() -> None:
    encounters = generate_encounters()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(encounters, f, indent=2)
        f.write("\n")
    print(f"Successfully generated {len(encounters)} Encounter documents to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
