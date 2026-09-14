#!/usr/bin/env python3
"""Module to generate encounters for 11 new mentees and integrate with generate_encounter_test_data.py."""

from __future__ import annotations
import json
from datetime import datetime, timedelta
from typing import Any

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
    return [{"step": step, "checked": True} for step in steps]


# Dialogue specs for each new mentee
NEW_MENTEE_CONFIGS = [
    # 1. Jordan Persevere (Paula): 6 completed, 3 scheduled
    {
        "mentee_slug": "jordan",
        "mentor_slug": "paula",
        "user_name": "paula",
        "next_offset_days": 2,
        "completed_count": 6,
        "scheduled_count": 3,
        "no_show_indices": [],
        "dialogues": [
            {
                "tldr": "Paula and Jordan aligned on Persevere accessibility milestones and component standards.",
                "summary": "## Summary\n**Summary:** Paula Persevere welcomed Jordan to the Persevere UI engineering track. They reviewed WCAG 2.1 AA requirements and planned a 12-week accessible component library roadmap.",
                "transcript": "#### Paula\nWelcome Jordan! Today we kick off your Persevere UI engineering track with a focus on accessible design.\n\n#### Jordan\nI'm ready to dive in. Accessibility is often treated as an afterthought, but I want to build it into every component from day one.\n\n#### Paula\nExactly. We'll start with semantics and keyboard interactions for common navigation patterns.",
            },
            {
                "tldr": "Paula reviewed Jordan's semantic landmark structure and keyboard focus management.",
                "summary": "## Summary\n**Summary:** Jordan demonstrated keyboard tab sequencing and skip links across the layout. Paula advised adding ARIA landmarks for landmark-based navigation.",
                "transcript": "#### Paula\nHow is the keyboard navigation prototype behaving?\n\n#### Jordan\nTab order is natural, but screen reader users might get lost without explicit ARIA landmark roles.\n\n#### Paula\nGood observation. Let's add main, nav, and complementary landmarks to clarify layout regions.",
            },
            {
                "tldr": "Jordan implemented accessible modal focus trapping with Paula's guidance.",
                "summary": "## Summary\n**Summary:** Paired on building a reusable accessible dialog component. Jordan implemented focus trapping and escape-key dismissal.",
                "transcript": "#### Paula\nModals are notoriously tricky for screen readers. What's your focus trap strategy?\n\n#### Jordan\nI'm listening for keydown events and cycling focus between the first and last focusable elements in the modal container.\n\n#### Paula\nThat works nicely. Don't forget to restore focus to the triggering element when the modal unmounts.",
            },
            {
                "tldr": "Paula and Jordan verified color contrast ratios and responsive typography scales.",
                "summary": "## Summary\n**Summary:** Evaluated design tokens for dark and light themes against contrast formulas. Jordan adjusted button hover contrast to exceed 4.5:1 ratio.",
                "transcript": "#### Paula\nLet's run color contrast checks across your theme tokens.\n\n#### Jordan\nThe primary button hover state was dipping below 4.2:1 contrast. I darkened the background tint.\n\n#### Paula\nConfirmed, that now reaches 4.7:1 and passes AA compliance comfortably.",
            },
            {
                "tldr": "Jordan integrated automated axe-core accessibility checks into the Vitest test suite.",
                "summary": "## Summary\n**Summary:** Automated CI accessibility testing by integrating `axe-core`. Jordan demonstrated zero violations across all rendered components.",
                "transcript": "#### Paula\nAutomating accessibility audits in CI prevents regressions from slipping into production.\n\n#### Jordan\nI configured axe-core in Vitest to run on every component test. We're at zero accessibility violations.\n\n#### Paula\nImpressive rigor. That gives us great confidence heading into cohort presentations.",
            },
            {
                "tldr": "Paula and Jordan conducted a dry run of the accessible component showcase.",
                "summary": "## Summary\n**Summary:** Final dry run of Jordan's component library showcase. Paula praised the interactive documentation and clear keyboard usage guidelines.",
                "transcript": "#### Paula\nWalk me through your component showcase demo before the cohort review.\n\n#### Jordan\nI have the keyboard shortcuts overlay ready, plus voiceover audio demos for each component.\n\n#### Paula\nYou're in great shape. Next session we will explore screen reader compatibility nuances.",
            },
        ],
    },
    # 2. Taylor Persevere (Paula): 4 completed, 4 scheduled
    {
        "mentee_slug": "taylor-persevere",
        "mentor_slug": "paula",
        "user_name": "paula",
        "next_offset_days": 4,
        "completed_count": 4,
        "scheduled_count": 4,
        "no_show_indices": [],
        "dialogues": [
            {
                "tldr": "Paula and Taylor established full-stack Vue learning milestones and capstone scope.",
                "summary": "## Summary\n**Summary:** Onboarding session aligning Taylor's full-stack goals. Paula outlined composables architecture and API integration patterns.",
                "transcript": "#### Paula\nWelcome Taylor! Over the next 12 weeks we'll connect your frontend Vue skills with robust backend API services.\n\n#### Taylor\nI'm excited to move beyond static mock data and handle real async server communication.\n\n#### Paula\nWe'll build custom composables that abstract HTTP calls and manage loading and error state cleanly.",
            },
            {
                "tldr": "Taylor demonstrated custom Vue composables with loading states and reactive ref binding.",
                "summary": "## Summary\n**Summary:** Taylor walked through `useAsyncData` composable implementation. Paula recommended adding abort controller support for unmounted components.",
                "transcript": "#### Paula\nLet's inspect how your data-fetching composable handles component unmounting.\n\n#### Taylor\nI hadn't considered that. If a user navigates away mid-request, it could update unmounted state.\n\n#### Paula\nPass an AbortController signal to the fetch call and cancel pending requests on cleanup.",
            },
            {
                "tldr": "Paula guided Taylor through Pinia store integration with token refresh middleware.",
                "summary": "## Summary\n**Summary:** Pair-programmed Pinia auth store with automatic token refresh on 401 Unauthorized responses. Verified session recovery works seamlessly.",
                "transcript": "#### Paula\nWhat happens in your auth store when an access token expires?\n\n#### Taylor\nCurrently the app throws an unhandled error and forces a redirect to login.\n\n#### Paula\nLet's intercept the 401, call the refresh endpoint, and replay the original request transparently.",
            },
            {
                "tldr": "Taylor built resilient error boundaries and user-friendly toast notifications.",
                "summary": "## Summary\n**Summary:** Taylor showcased global error boundary handling and toast feedback for failed network requests. Paula confirmed edge case coverage.",
                "transcript": "#### Paula\nHow are API network failures displayed to the user?\n\n#### Taylor\nI built a global toast notification service with retry action buttons for transient failures.\n\n#### Paula\nClean user experience. Next week we will look into form validation and optimistic UI updates.",
            },
        ],
    },
    # 3. Casey SuperSoft (Danny): 8 completed (session 3 no-show), 2 scheduled
    {
        "mentee_slug": "casey",
        "mentor_slug": "danny",
        "user_name": "danny",
        "next_offset_days": 1,
        "completed_count": 8,
        "scheduled_count": 2,
        "no_show_indices": [2],  # session 3 is no-show
        "dialogues": [
            {
                "tldr": "Danny introduced Casey to SuperSoft backend services, FastAPI patterns, and container setups.",
                "summary": "## Summary\n**Summary:** Onboarding session reviewing SuperSoft backend service architecture. Danny oriented Casey on local container stacks and endpoint routing.",
                "transcript": "#### Danny\nWelcome to the SuperSoft team Casey! We'll be ramping you up on backend API microservices.\n\n#### Casey\nGlad to be here Danny. I've worked with Python before but want to master production-grade FastAPI services.\n\n#### Danny\nWe'll start with our domain architecture and containerized dev environments.",
            },
            {
                "tldr": "Danny reviewed Casey's initial endpoint schemas and Pydantic v2 data models.",
                "summary": "## Summary\n**Summary:** Code review of Casey's REST endpoint models. Danny recommended strict field validation and custom validator methods for business rules.",
                "transcript": "#### Danny\nLet's check your Pydantic request models for the roster service.\n\n#### Casey\nI defined standard type hints, but haven't added regex validations for IDs yet.\n\n#### Danny\nAdd Field constraints with custom validator decorators to catch malformed inputs early.",
            },
            # Session 3: No-show (handled automatically)
            None,
            {
                "tldr": "Casey and Danny synced after the missed session, implementing MongoDB connection pooling.",
                "summary": "## Summary\n**Summary:** Quick check-in after last week's absence. Danny helped Casey optimize MongoDB connection pool sizing and client lifecycles.",
                "transcript": "#### Danny\nGood to have you back Casey, hope everything settled down from last week.\n\n#### Casey\nThanks Danny, all good now. Ready to tackle the database connection issues.\n\n#### Danny\nLet's inspect how the Mongo client is instantiated across worker threads and tune pool sizes.",
            },
            {
                "tldr": "Casey built decorator-based retry logic for transient MongoDB network drops.",
                "summary": "## Summary\n**Summary:** Demonstrated exponential backoff retry decorator for database operations. Danny approved the implementation for production use.",
                "transcript": "#### Danny\nHow did the retry wrapper turn out for transient connection blips?\n\n#### Casey\nI used an exponential backoff with jitter up to three attempts before bubbling the exception.\n\n#### Danny\nSolid error resilience. That will prevent spurious alerting during rolling restarts.",
            },
            {
                "tldr": "Danny and Casey reviewed JWT claim extraction and role-based route dependencies.",
                "summary": "## Summary\n**Summary:** Evaluated auth security layer. Casey implemented dependency injection for role checks, protecting admin and coordinator routes.",
                "transcript": "#### Danny\nLet's walk through your RBAC dependency function.\n\n#### Casey\nIt unpacks the JWT claims, verifies the expiration and audience, and checks if user_roles contains the required permission.\n\n#### Danny\nExactly right. Clean and decoupled from the business logic handlers.",
            },
            {
                "tldr": "Casey increased test suite coverage to 92% with pytest and mock database fixtures.",
                "summary": "## Summary\n**Summary:** Review of test coverage metrics. Casey added integration tests covering error handlers and mock database failures.",
                "transcript": "#### Danny\nTest coverage report looks great Casey—over 90% across the domain handlers.\n\n#### Casey\nMocking the database client allowed me to simulate replica set failovers and 500 scenarios.\n\n#### Danny\nThorough tests make deploying on Fridays much less stressful.",
            },
            {
                "tldr": "Danny verified Casey's CI pipeline GitHub Actions workflow for container builds.",
                "summary": "## Summary\n**Summary:** Inspected Casey's automated CI workflow. Verified automated linting, pytest matrix runs, and Docker multi-stage image packaging.",
                "transcript": "#### Danny\nWalk me through the GitHub Actions workflow you configured.\n\n#### Casey\nOn pull request, it runs ruff linting, executes pytest in parallel, and verifies the Docker container builds cleanly.\n\n#### Danny\nOutstanding milestone Casey. Next session we'll focus on deployment strategies.",
            },
        ],
    },
    # 4. Morgan SuperSoft (Danny): 5 completed, 3 scheduled
    {
        "mentee_slug": "morgan",
        "mentor_slug": "danny",
        "user_name": "danny",
        "next_offset_days": 5,
        "completed_count": 5,
        "scheduled_count": 3,
        "no_show_indices": [],
        "dialogues": [
            {
                "tldr": "Danny and Morgan launched SuperSoft SRE track focusing on Prometheus observability.",
                "summary": "## Summary\n**Summary:** SRE apprenticeship kickoff. Danny and Morgan aligned on service level objectives (SLOs), latency histograms, and alert hygiene.",
                "transcript": "#### Danny\nWelcome Morgan! In this track we'll turn reactive troubleshooting into proactive system observability.\n\n#### Morgan\nExcited to work with you Danny. I want to build monitoring that gives engineers actionable context during incidents.\n\n#### Danny\nWe'll start by instrumenting our core services with Prometheus metrics.",
            },
            {
                "tldr": "Morgan instrumented HTTP middleware with custom Prometheus latency histograms.",
                "summary": "## Summary\n**Summary:** Reviewed Morgan's `/metrics` exporter. Configured latency buckets tuned for API response times and error rate counters.",
                "transcript": "#### Danny\nLet's check the latency bucket distribution on your HTTP middleware.\n\n#### Morgan\nI tuned the histogram buckets from 5ms up to 2 seconds so we capture the p95 and p99 tails accurately.\n\n#### Danny\nGood choice. That will highlight database stalls without muddying normal requests.",
            },
            {
                "tldr": "Danny reviewed Morgan's Grafana dashboard with RED method visualizations.",
                "summary": "## Summary\n**Summary:** Evaluated Grafana dashboard implementing Rate, Errors, and Duration (RED) panels. Danny approved the layout for team operations.",
                "transcript": "#### Danny\nShow me the operational dashboard you drafted.\n\n#### Morgan\nHere is the top row: request rate, 5xx error percentage, and p50/p90/p99 duration timelines.\n\n#### Danny\nClean visual hierarchy. Anyone on call can assess service health in five seconds.",
            },
            {
                "tldr": "Morgan configured Alertmanager routing and severity thresholds for service degradations.",
                "summary": "## Summary\n**Summary:** Pair-configured alert routing rules. Established warning thresholds for latency trends and critical alerts for elevated error rates.",
                "transcript": "#### Danny\nHow are alert severities partitioned in Alertmanager?\n\n#### Morgan\nWarnings go to Slack for gradual resource trends; critical 5xx spikes trigger high-priority alerts with runbook links.\n\n#### Danny\nAlways linking the runbook in the alert payload is a great SRE habit.",
            },
            {
                "tldr": "Danny and Morgan conducted a tabletop post-mortem exercise on database connection exhaustion.",
                "summary": "## Summary\n**Summary:** Simulated incident post-mortem. Morgan drafted timeline, root-cause analysis, and preventative action items for connection pool exhaustion.",
                "transcript": "#### Danny\nLet's run through an incident retrospective: connection pool saturation during peak ingress.\n\n#### Morgan\nTimeline shows thread contention starting at 14:02. Immediate mitigation was scaling replicas; permanent fix is adding connection limits.\n\n#### Danny\nClear blameless analysis Morgan. Next session we'll practice automated chaos testing.",
            },
        ],
    },
    # 5. Alex SuperSoft (Danny): 0 completed, 5 scheduled
    {
        "mentee_slug": "alex",
        "mentor_slug": "danny",
        "user_name": "danny",
        "next_offset_days": 3,
        "completed_count": 0,
        "scheduled_count": 5,
        "no_show_indices": [],
        "dialogues": [],
    },
    # 6. Sam Startup (Elon): 6 completed, 3 scheduled
    {
        "mentee_slug": "sam-startup",
        "mentor_slug": "elon",
        "user_name": "elon",
        "next_offset_days": 6,
        "completed_count": 6,
        "scheduled_count": 3,
        "no_show_indices": [],
        "dialogues": [
            {
                "tldr": "Elon and Sam kicked off startup founder mentoring, clarifying customer persona and problem scope.",
                "summary": "## Summary\n**Summary:** Kickoff session for technical founder Sam. Elon evaluated the core problem hypothesis and aligned on pre-seed milestones.",
                "transcript": "#### Elon\nWelcome Sam. Let's cut straight to the core: what painful problem does your software solve that someone will write a check for today?\n\n#### Sam\nWe automate data pipeline audits for mid-market fintechs who currently spend days doing manual reconciliation.\n\n#### Elon\nStrong wedge. We'll quantify that pain into unit economics over our sessions.",
            },
            {
                "tldr": "Elon stress-tested Sam's bottom-up market sizing and enterprise pricing model.",
                "summary": "## Summary\n**Summary:** Market sizing review. Sam presented TAM/SAM/SOM calculations; Elon guided the transition from top-down estimates to bottom-up pipeline metrics.",
                "transcript": "#### Elon\nWalk me through how you arrived at your $500M market estimate.\n\n#### Sam\nI counted total mid-market financial institutions and multiplied by an estimated $25k annual contract value.\n\n#### Elon\nMuch better than top-down industry reports. Now let's calculate customer acquisition costs.",
            },
            {
                "tldr": "Sam modeled CAC payback periods and net revenue retention curves with Elon.",
                "summary": "## Summary\n**Summary:** Financial modeling review. Elon validated Sam's payback period assumptions and recommended targeting under 12-month CAC recovery.",
                "transcript": "#### Elon\nWhat's your projected CAC payback period on direct sales?\n\n#### Sam\nCurrently 14 months based on outbound SDR lead costs and pilot conversion rates.\n\n#### Elon\nTighten the sales cycle by offering self-serve evaluation tiers to pull that under 10 months.",
            },
            {
                "tldr": "Elon reviewed Sam's 10-slide pre-seed pitch deck and narrative flow.",
                "summary": "## Summary\n**Summary:** Pitch deck surgery. Elon restructured the opening slides to lead with proprietary data advantage and technical defensibility.",
                "transcript": "#### Elon\nSlide three is burying your biggest advantage: your automated parsing engine is 10x faster than legacy tools.\n\n#### Sam\nI had that under technical architecture on slide seven.\n\n#### Elon\nMove it up front. Investors care about unfair technical advantages before team bios.",
            },
            {
                "tldr": "Sam executed a mock investor pitch and handled aggressive diligence questioning.",
                "summary": "## Summary\n**Summary:** Simulated partner pitch. Elon tested Sam on competitive moats, churn risks, and gross margin sustainability.",
                "transcript": "#### Elon\nSuppose Snowflake launches a native feature duplicating your core audit hook—what is your defense?\n\n#### Sam\nOur value is multi-cloud cross-reconciliation across heterogeneous datastores, which single-cloud vendors won't support.\n\n#### Elon\nDecisive answer. Keep that conviction during partner meetings.",
            },
            {
                "tldr": "Elon and Sam finalized term sheet negotiation priorities and cap table models.",
                "summary": "## Summary\n**Summary:** Pre-round preparation. Reviewed SAFE note valuation caps, dilution scenarios, and board governance expectations.",
                "transcript": "#### Elon\nReview your cap table model after the pre-seed round.\n\n#### Sam\nWith the standard post-money SAFE at a $6M cap, we preserve 80% founder equity going into seed.\n\n#### Elon\nHealthy balance. Next session we'll tackle hiring executive technical talent.",
            },
        ],
    },
    # 7. Riley Revenue (Elon): 4 completed, 4 scheduled
    {
        "mentee_slug": "riley-revenue",
        "mentor_slug": "elon",
        "user_name": "elon",
        "next_offset_days": 2,
        "completed_count": 4,
        "scheduled_count": 4,
        "no_show_indices": [],
        "dialogues": [
            {
                "tldr": "Elon and Riley established SaaS revenue architecture and pricing strategy milestones.",
                "summary": "## Summary\n**Summary:** Revenue mentoring kickoff. Elon and Riley evaluated subscription packaging, tier differentiators, and annual upfront discounting.",
                "transcript": "#### Elon\nRiley, monetization is a product feature, not an afterthought. What is your primary value metric?\n\n#### Riley\nWe're deciding between active tracked entities and seat-based licensing.\n\n#### Elon\nSeat licenses punish customer growth. Charge based on tracked entities so your revenue expands as your customer succeeds.",
            },
            {
                "tldr": "Riley presented three-tier pricing model with usage-based expansion levers.",
                "summary": "## Summary\n**Summary:** Pricing model review. Elon refined tier boundaries to encourage frictionless self-service upgrades to the mid-tier plan.",
                "transcript": "#### Elon\nWhere is the cliff between your Starter and Growth tiers?\n\n#### Riley\nStarter caps at 10,000 monthly events; Growth unlocks 100,000 events and team collaboration features.\n\n#### Elon\nWell-placed boundary. Companies will naturally cross that threshold in month three.",
            },
            {
                "tldr": "Elon guided Riley through automated billing recovery and smart dunning workflows.",
                "summary": "## Summary\n**Summary:** Involuntary churn mitigation. Riley demonstrated webhook handlers for failed invoice notifications and automated card update emails.",
                "transcript": "#### Elon\nInvoluntary churn from expired cards silently kills SaaS cash flow. What is your dunning schedule?\n\n#### Riley\nWe retry payments on days 1, 3, and 7, while triggering in-app banners and transactional emails.\n\n#### Elon\nStandard best practice. That recovers up to 60% of failed subscription renewals.",
            },
            {
                "tldr": "Riley modeled cohort retention curves and expansion revenue metrics with Elon.",
                "summary": "## Summary\n**Summary:** Revenue retention analysis. Evaluated net revenue retention (NRR) targets and modeled annual prepayment incentives.",
                "transcript": "#### Elon\nLet's inspect your revenue retention waterfall.\n\n#### Riley\nOur gross churn is 2% monthly, but expansion revenue from growing customers pushes NRR to 108%.\n\n#### Elon\nNRR above 100% is what gives venture investors confidence. Next week we'll model sales team commissions.",
            },
        ],
    },
    # 8. Quinn Capital (Elon): 8 completed (alumni / only completed), 0 scheduled
    {
        "mentee_slug": "quinn-capital",
        "mentor_slug": "elon",
        "user_name": "elon",
        "next_offset_days": None,
        "completed_count": 8,
        "scheduled_count": 0,
        "no_show_indices": [],
        "dialogues": [
            {
                "tldr": "Elon and Quinn launched fintech capital ledger apprenticeship and compliance roadmap.",
                "summary": "## Summary\n**Summary:** Apprenticeship orientation. Elon reviewed immutable ledger double-entry principles and regulatory compliance standards with Quinn.",
                "transcript": "#### Elon\nWelcome Quinn. In financial software, every cent must balance across immutable ledger accounts.\n\n#### Quinn\nUnderstood Elon. My goal is mastering double-entry accounting engines and automated reconciliation.\n\n#### Elon\nWe'll construct a production-ready ledger engine from the ground up.",
            },
            {
                "tldr": "Quinn implemented double-entry debit/credit ledger constraints with Elon's guidance.",
                "summary": "## Summary\n**Summary:** Core ledger implementation. Quinn verified transaction balance invariants where sum of debits strictly equals sum of credits.",
                "transcript": "#### Elon\nHow does your ledger enforce transaction atomicity?\n\n#### Quinn\nDatabase transactions wrap the dual ledger entries; if debits don't equal credits, the entire batch rolls back.\n\n#### Elon\nFundamental financial safeguard. Always assert zero-sum balance before committing.",
            },
            {
                "tldr": "Elon verified Quinn's idempotent payment ingestion pipeline and replay protection.",
                "summary": "## Summary\n**Summary:** Idempotency architecture. Quinn demonstrated unique idempotency key caching preventing duplicate charge processing.",
                "transcript": "#### Elon\nWhat happens when a webhook delivers duplicate payment event payloads?\n\n#### Quinn\nWe hash the payload with the idempotency key and return the cached receipt without re-processing.\n\n#### Elon\nFlawless. Double-charging a customer is an instant regulatory violation.",
            },
            {
                "tldr": "Quinn built automated bank statement reconciliation and discrepancy detection.",
                "summary": "## Summary\n**Summary:** Statement reconciliation. Quinn demonstrated automated parser matching clearinghouse records against internal ledger entries.",
                "transcript": "#### Elon\nHow fast does your reconciliation job flag settlement discrepancies?\n\n#### Quinn\nWithin 30 seconds of statement upload, flagging any rounding mismatch greater than $0.001.\n\n#### Elon\nPrecision is everything in fintech.",
            },
            {
                "tldr": "Elon and Quinn reviewed PCI DSS data boundary isolation and tokenization.",
                "summary": "## Summary\n**Summary:** Security boundary review. Quinn verified cardholder data is never persisted locally, isolating tokenized identifiers.",
                "transcript": "#### Elon\nWalk me through our PCI audit scope.\n\n#### Quinn\nCard data goes directly to the payment gateway; our database only handles customer tokens and payment IDs.\n\n#### Elon\nStrict isolation keeps our compliance overhead minimal.",
            },
            {
                "tldr": "Quinn demonstrated audit trail exports with cryptographic tamper evidence.",
                "summary": "## Summary\n**Summary:** Audit compliance. Quinn implemented SHA-256 hash chaining across ledger blocks ensuring immutable audit logs.",
                "transcript": "#### Elon\nShow me the tamper-evident hash chaining on the audit table.\n\n#### Quinn\nEach ledger block includes the previous block's SHA-256 hash. Any retroactive row edit invalidates the chain.\n\n#### Elon\nBank examiners will appreciate that level of cryptographic integrity.",
            },
            {
                "tldr": "Elon conducted final capstone review of Quinn's financial ledger platform.",
                "summary": "## Summary\n**Summary:** Comprehensive capstone review. Elon evaluated performance, security penetration results, and system uptime.",
                "transcript": "#### Elon\nAll stress-test benchmarks passed with sub-10ms ledger write latencies.\n\n#### Quinn\nWe verified zero data loss across simulated cluster dropouts.\n\n#### Elon\nExceptional engineering Quinn. You are ready for lead fintech roles.",
            },
            {
                "tldr": "Elon signed off on Quinn's completed fintech fellowship and milestone portfolio.",
                "summary": "## Summary\n**Summary:** Final graduation sync. Elon signed off on Quinn's completed fellowship dossier and archived the active coaching schedule.",
                "transcript": "#### Elon\nQuinn, today marks the completion of your intensive financial engineering fellowship with ALI.\n\n#### Quinn\nThank you Elon. The depth of architectural and commercial feedback has been transformative.\n\n#### Elon\nStay rigorous, keep ledger balances exact, and best of luck in your next venture.",
            },
        ],
    },
    # 9. Avery Design (Melinda): 7 completed, 3 scheduled
    {
        "mentee_slug": "avery",
        "mentor_slug": "melinda",
        "user_name": "melinda",
        "next_offset_days": 4,
        "completed_count": 7,
        "scheduled_count": 3,
        "no_show_indices": [],
        "dialogues": [
            {
                "tldr": "Melinda and Avery aligned on ALI design system token architecture and component guidelines.",
                "summary": "## Summary\n**Summary:** Design track orientation. Melinda and Avery reviewed token hierarchy (global, semantic, component-specific) and Figma-to-code workflows.",
                "transcript": "#### Melinda\nWelcome Avery! In this track we will bridge the gap between design tokens and production UI components.\n\n#### Avery\nExcited to learn from you Melinda. I want our design system to be intuitive for designers and effortless for engineers.\n\n#### Melinda\nWe'll establish a three-tier token taxonomy starting with primitive colors and spacing scales.",
            },
            {
                "tldr": "Avery mapped primitive color scales and semantic aliases across Figma libraries.",
                "summary": "## Summary\n**Summary:** Semantic token mapping. Avery demonstrated light and dark mode mappings using semantic tokens like `surface-primary` and `content-subtle`.",
                "transcript": "#### Melinda\nShow me how your semantic aliases map to underlying primitive palettes.\n\n#### Avery\n`surface-card` maps to Neutral-50 in light mode and Neutral-900 in dark mode, decoupling components from hardcoded hex values.\n\n#### Melinda\nClean abstraction. That makes theming effortless.",
            },
            {
                "tldr": "Melinda reviewed Avery's automated GitHub Action exporting Figma tokens to CSS variables.",
                "summary": "## Summary\n**Summary:** Token export pipeline. Avery demonstrated automated sync pulling JSON tokens from Figma REST API and generating CSS variables.",
                "transcript": "#### Melinda\nHow does the token export pipeline handle breaking changes?\n\n#### Avery\nThe script runs schema validation and opens an automated pull request with visual diff screenshots.\n\n#### Melinda\nAutomating the PR generation keeps designers and developers in continuous alignment.",
            },
            {
                "tldr": "Avery built accessible button and badge components with micro-interaction states.",
                "summary": "## Summary\n**Summary:** Component construction. Avery showcased button variants with clear hover, active, focus-visible, and disabled states.",
                "transcript": "#### Melinda\nLet's review the focus-visible indicator on your secondary buttons.\n\n#### Avery\nI used a 2px offset ring that inherits high-contrast accent colors without clipping border-radii.\n\n#### Melinda\nCrisp and accessible. It looks polished across both bright and dark backgrounds.",
            },
            {
                "tldr": "Melinda guided Avery through Storybook documentation and accessibility add-ons.",
                "summary": "## Summary\n**Summary:** Component catalog setup. Avery configured Storybook with interactive props tables and automated a11y inspection panels.",
                "transcript": "#### Melinda\nHow are component props documented in your Storybook catalog?\n\n#### Avery\nAll TypeScript interfaces auto-generate prop controls, and the a11y tab flags contrast or role issues live.\n\n#### Melinda\nHaving automated accessibility feedback right in the design workspace accelerates reviews.",
            },
            {
                "tldr": "Avery conducted qualitative usability testing on navigation drawer interactions.",
                "summary": "## Summary\n**Summary:** User research findings. Avery summarized findings from 5 user testing sessions on mobile drawer gesture navigation.",
                "transcript": "#### Melinda\nWhat did users struggle with most during the mobile drawer tests?\n\n#### Avery\nSeveral users expected swipe-down gesture dismissal rather than only tapping the backdrop overlay.\n\n#### Melinda\nGreat insight. Let's incorporate touch drag gestures into the next component release.",
            },
            {
                "tldr": "Melinda and Avery prioritized design system roadmap items for upcoming sprint.",
                "summary": "## Summary\n**Summary:** Roadmap planning. Synthesized user research feedback into component updates and planned table component tokens.",
                "transcript": "#### Melinda\nLet's prioritize the next component sprint.\n\n#### Avery\nWe'll deliver touch swipe gestures for drawers, then begin tokens for complex tabular data layouts.\n\n#### Melinda\nGreat plan. Next session we'll refine dark mode contrast ratios.",
            },
        ],
    },
    # 10. Devon Interface (Melinda): 5 completed (session 4 no-show), 3 scheduled
    {
        "mentee_slug": "devon",
        "mentor_slug": "melinda",
        "user_name": "melinda",
        "next_offset_days": 1,
        "completed_count": 5,
        "scheduled_count": 3,
        "no_show_indices": [3],  # session 4 is no-show
        "dialogues": [
            {
                "tldr": "Melinda and Devon kicked off UI animation choreography and micro-interaction track.",
                "summary": "## Summary\n**Summary:** UI engineering kickoff. Melinda and Devon discussed 60fps performance budgets, CSS transforms, and purposeful interaction motion.",
                "transcript": "#### Melinda\nWelcome Devon! Great interaction design feels alive without distracting users from their tasks.\n\n#### Devon\nThrilled to work with you Melinda. I want to build fluid animations that communicate system state changes clearly.\n\n#### Melinda\nWe'll stick to GPU-composited properties like transform and opacity to keep frame rates buttery smooth.",
            },
            {
                "tldr": "Devon demonstrated layout transitions using FLIP technique and GPU acceleration.",
                "summary": "## Summary\n**Summary:** Animation performance. Devon showed First, Last, Invert, Play (FLIP) layout animations achieving 60fps during DOM reordering.",
                "transcript": "#### Melinda\nShow me the performance profile during grid item reordering.\n\n#### Devon\nUsing the FLIP technique, there is zero layout thrashing—only composited matrix transforms running on the GPU.\n\n#### Melinda\nFlawless 60fps timeline. That feels snappy and modern.",
            },
            {
                "tldr": "Melinda guided Devon through micro-frontend event bus and isolated state dispatch.",
                "summary": "## Summary\n**Summary:** Micro-frontend communication. Devon implemented a lightweight event emitter coordinating route transitions across micro-apps.",
                "transcript": "#### Melinda\nHow do isolated micro-frontends signal page transitions without direct coupling?\n\n#### Devon\nI instantiated a typed CustomEvent dispatcher on window, passing route payload and transition timing cues.\n\n#### Melinda\nClean decoupling. Each app remains independently deployable.",
            },
            # Session 4: No-show (handled automatically)
            None,
            {
                "tldr": "Melinda and Devon synced after absence, debugging virtualized list frame drops.",
                "summary": "## Summary\n**Summary:** Post-absence check-in. Melinda helped Devon profile and eliminate frame drops during high-speed list virtualization scrolling.",
                "transcript": "#### Melinda\nGood to see you Devon. Let's look at the scroll stuttering you mentioned on large datasets.\n\n#### Devon\nThanks Melinda. Rendering 10,000 items was triggering garbage collection spikes during rapid scrolling.\n\n#### Melinda\nWe'll pool DOM nodes with a virtualized window so only visible rows mount in the tree.",
            },
        ],
    },
    # 11. Harper Fullstack (Melinda): 0 completed, 4 scheduled
    {
        "mentee_slug": "harper",
        "mentor_slug": "melinda",
        "user_name": "melinda",
        "next_offset_days": 5,
        "completed_count": 0,
        "scheduled_count": 4,
        "no_show_indices": [],
        "dialogues": [],
    },
]


def generate_new_encounters(serial_start: int, now: datetime, profiles: dict[str, str]) -> tuple[list[dict], int]:
    encounters: list[dict] = []
    serial = serial_start

    for cfg in NEW_MENTEE_CONFIGS:
        mentee_id = profiles[cfg["mentee_slug"]]
        mentor_id = profiles[cfg["mentor_slug"]]
        mentor_user = cfg["user_name"]
        next_offset_days = cfg["next_offset_days"]
        comp_count = cfg["completed_count"]
        sched_count = cfg["scheduled_count"]
        no_show_indices = set(cfg["no_show_indices"])
        dialogues = cfg["dialogues"]

        # Calculate next_dt if mentee has scheduled sessions
        if next_offset_days is not None:
            next_dt = (now + timedelta(days=next_offset_days)).replace(hour=14, minute=0, second=0, microsecond=0)
        else:
            next_dt = None

        # 1. Generate Completed Sessions (chronological order)
        for i in range(comp_count):
            enc_id = f"E{serial:023x}"
            serial += 1
            is_first = (i == 0)
            plan_id = FIRST_ENCOUNTER_PLAN_ID if is_first else STANDARD_PLAN_ID
            steps = FIRST_ENCOUNTER_STEPS if is_first else STANDARD_STEPS
            is_no_show = (i in no_show_indices)

            # Scheduled timestamp in the past
            if next_dt is not None:
                # Weeks before the next scheduled encounter
                weeks_before = comp_count - i
                sched_from = next_dt - timedelta(days=7 * weeks_before)
            else:
                # Concluded alumni (Quinn): ending 2 weeks ago
                weeks_ago = (comp_count - i) + 1
                sched_from = now - timedelta(days=7 * weeks_ago)
            sched_to = sched_from + timedelta(hours=1)

            doc: dict[str, Any] = {
                "_id": oid(enc_id),
                "mentor_id": oid(mentor_id),
                "mentee_id": oid(mentee_id),
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
                meta = dialogues[i]
                actual_from = sched_from + timedelta(minutes=3)
                actual_to = actual_from + timedelta(minutes=52)
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
                "correlation_id": f"seed-enc-{cfg['mentee_slug']}-{i+1:02d}",
            }
            doc["saved"] = {
                "from_ip": "127.0.0.1",
                "by_user": mentor_user,
                "at_time": date_dict(sched_to),
                "correlation_id": f"save-enc-{cfg['mentee_slug']}-{i+1:02d}",
            }
            encounters.append(doc)

        # 2. Generate Scheduled Sessions (chronological order starting at next_dt)
        if next_dt is not None:
            for j in range(sched_count):
                enc_id = f"E{serial:023x}"
                serial += 1
                is_first = (comp_count == 0 and j == 0)
                plan_id = FIRST_ENCOUNTER_PLAN_ID if is_first else STANDARD_PLAN_ID
                steps = FIRST_ENCOUNTER_STEPS if is_first else STANDARD_STEPS

                sched_from = next_dt + timedelta(days=7 * j)
                sched_to = sched_from + timedelta(hours=1)

                doc = {
                    "_id": oid(enc_id),
                    "mentor_id": oid(mentor_id),
                    "mentee_id": oid(mentee_id),
                    "appointment": {
                        "from": date_dict(sched_from),
                        "to": date_dict(sched_to),
                    },
                    "plan_id": oid(plan_id),
                    "agenda": build_agenda(steps, "scheduled", False),
                    "status": "scheduled",
                    "created": {
                        "from_ip": "127.0.0.1",
                        "by_user": mentor_user,
                        "at_time": date_dict(now),
                        "correlation_id": f"seed-enc-{cfg['mentee_slug']}-{comp_count+j+1:02d}",
                    },
                    "saved": {
                        "from_ip": "127.0.0.1",
                        "by_user": mentor_user,
                        "at_time": date_dict(now),
                        "correlation_id": f"save-enc-{cfg['mentee_slug']}-{comp_count+j+1:02d}",
                    },
                }
                encounters.append(doc)

    return encounters, serial


if __name__ == "__main__":
    now = datetime.now()
    with open("Tasks/scripts/persona_ids.json") as f:
        p = json.load(f)["profiles"]
    encs, end_serial = generate_new_encounters(61, now, p)
    print(f"Generated {len(encs)} encounters for new mentees. End serial: {end_serial}")
