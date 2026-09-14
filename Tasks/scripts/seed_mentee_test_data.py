#!/usr/bin/env python3
"""Seed new mentee Profile and Mentee records for T258."""

from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROFILE_PATH = REPO / "configurator" / "test_data" / "Profile.0.1.0.0.json"
MENTEE_PATH = REPO / "configurator" / "test_data" / "Mentee.0.1.0.0.json"
PERSONA_IDS_PATH = REPO / "Tasks" / "scripts" / "persona_ids.json"

new_profiles = [
    {
        "_id": {"$oid": "A00000000000000000000022"},
        "status": "active",
        "display_name": "Jordan Persevere",
        "description": "Persevere apprentice specializing in responsive web applications and component accessibility.",
        "email": "jordan.persevere@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Master responsive CSS layout", "Build accessible UI components"],
        "interests": ["ux", "design"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000010"},
        "customer_id": {"$oid": "D00000000000000000000002"},
        "experience": [
            {
                "company": "Persevere Now",
                "roles": [
                    {
                        "title": "Frontend Apprentice",
                        "start": {"$date": "2025-01-10T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Developing responsive UI components and accessible design patterns.",
                        "technologies": ["HTML", "CSS", "React"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-01-15T10:00:00.000Z"},
            "correlation_id": "seed-profile-22",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "jordan",
            "at_time": {"$date": "2025-06-01T12:00:00.000Z"},
            "correlation_id": "save-profile-22",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000023"},
        "status": "active",
        "display_name": "Taylor Persevere",
        "description": "Frontend developer transitioning to full-stack Vue and API integration.",
        "email": "taylor.persevere@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Implement secure API endpoints", "Ship full-stack capstone project"],
        "interests": ["ux", "api"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000010"},
        "customer_id": {"$oid": "D00000000000000000000002"},
        "experience": [
            {
                "company": "Persevere Now",
                "roles": [
                    {
                        "title": "Software Apprentice",
                        "start": {"$date": "2025-02-01T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Building full-stack Vue SPA features and connecting backend APIs.",
                        "technologies": ["TypeScript", "HTML", "CSS"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-05T11:00:00.000Z"},
            "correlation_id": "seed-profile-23",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "taylor",
            "at_time": {"$date": "2025-06-02T13:30:00.000Z"},
            "correlation_id": "save-profile-23",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000024"},
        "status": "active",
        "display_name": "Casey SuperSoft",
        "description": "SuperSoft junior engineer advancing backend microservice development and automated CI.",
        "email": "casey.supersoft@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Containerize Python microservices", "Deploy automated release pipelines"],
        "interests": ["api", "sre"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000014"},
        "customer_id": {"$oid": "D00000000000000000000007"},
        "experience": [
            {
                "company": "SuperSoft",
                "roles": [
                    {
                        "title": "Junior Backend Engineer",
                        "start": {"$date": "2025-01-15T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Developing REST APIs and pipeline automation with Danny.",
                        "technologies": ["Python", "MongoDB"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-01-20T14:00:00.000Z"},
            "correlation_id": "seed-profile-24",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "casey",
            "at_time": {"$date": "2025-06-03T10:15:00.000Z"},
            "correlation_id": "save-profile-24",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000025"},
        "status": "active",
        "display_name": "Morgan SuperSoft",
        "description": "Infrastructure apprentice focused on observability, metrics aggregation, and uptime monitoring.",
        "email": "morgan.supersoft@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Set up Prometheus telemetry", "Improve incident response workflows"],
        "interests": ["sre", "data"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000014"},
        "customer_id": {"$oid": "D00000000000000000000007"},
        "experience": [
            {
                "company": "SuperSoft",
                "roles": [
                    {
                        "title": "SRE Apprentice",
                        "start": {"$date": "2025-02-10T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Configuring metrics scrapers, dashboards, and alerting rules.",
                        "technologies": ["Python", "TypeScript"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-12T09:30:00.000Z"},
            "correlation_id": "seed-profile-25",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "morgan",
            "at_time": {"$date": "2025-06-04T15:45:00.000Z"},
            "correlation_id": "save-profile-25",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000026"},
        "status": "active",
        "display_name": "Alex SuperSoft",
        "description": "SuperSoft cloud platform apprentice learning container clustering and deployment reliability.",
        "email": "alex.supersoft@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Configure Kubernetes deployments", "Implement zero-downtime rolling updates"],
        "interests": ["sre", "api"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000014"},
        "customer_id": {"$oid": "D00000000000000000000007"},
        "experience": [
            {
                "company": "SuperSoft",
                "roles": [
                    {
                        "title": "DevOps Intern",
                        "start": {"$date": "2025-03-01T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Assisting on deployment pipelines and container orchestration checks.",
                        "technologies": ["Python"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-03-05T16:00:00.000Z"},
            "correlation_id": "seed-profile-26",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "alex",
            "at_time": {"$date": "2025-06-05T11:20:00.000Z"},
            "correlation_id": "save-profile-26",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000027"},
        "status": "active",
        "display_name": "Sam Startup",
        "description": "Technical founder preparing product roadmap and pre-seed venture pitch.",
        "email": "sam.startup@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Prepare financial forecast model", "Refine investor deck"],
        "interests": ["api", "ux"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000011"},
        "customer_id": {"$oid": "D00000000000000000000006"},
        "experience": [
            {
                "company": "Agile Learning Institute",
                "roles": [
                    {
                        "title": "Startup Fellow",
                        "start": {"$date": "2025-01-01T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Building MVP prototype and business model with Elon Money.",
                        "technologies": ["TypeScript", "Python"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-01-10T10:00:00.000Z"},
            "correlation_id": "seed-profile-27",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "sam",
            "at_time": {"$date": "2025-06-06T14:10:00.000Z"},
            "correlation_id": "save-profile-27",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000028"},
        "status": "active",
        "display_name": "Riley Revenue",
        "description": "SaaS founder exploring unit economics, pricing models, and stripe billing integration.",
        "email": "riley.revenue@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Model customer acquisition cost", "Design recurring subscription tiers"],
        "interests": ["data", "api"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000011"},
        "customer_id": {"$oid": "D00000000000000000000006"},
        "experience": [
            {
                "company": "Agile Learning Institute",
                "roles": [
                    {
                        "title": "Venture Apprentice",
                        "start": {"$date": "2025-02-01T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Designing monetized API architectures and financial runways.",
                        "technologies": ["Python", "TypeScript"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-15T15:30:00.000Z"},
            "correlation_id": "seed-profile-28",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "riley",
            "at_time": {"$date": "2025-06-07T09:40:00.000Z"},
            "correlation_id": "save-profile-28",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000029"},
        "status": "active",
        "display_name": "Quinn Capital",
        "description": "Fintech apprentice studying capital allocation, risk modeling, and regulatory compliance.",
        "email": "quinn.capital@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Implement ledger reconciliation", "Audit transaction security"],
        "interests": ["data", "api"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000011"},
        "customer_id": {"$oid": "D00000000000000000000006"},
        "experience": [
            {
                "company": "Agile Learning Institute",
                "roles": [
                    {
                        "title": "Fintech Fellow",
                        "start": {"$date": "2025-01-20T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Implementing data verification pipelines and compliance safeguards.",
                        "technologies": ["Python", "MongoDB"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-01-25T11:45:00.000Z"},
            "correlation_id": "seed-profile-29",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "quinn",
            "at_time": {"$date": "2025-06-08T16:00:00.000Z"},
            "correlation_id": "save-profile-29",
        },
    },
    {
        "_id": {"$oid": "A0000000000000000000002a"},
        "status": "active",
        "display_name": "Avery Design",
        "description": "Product designer deepening design system architecture and user research methodologies.",
        "email": "avery.design@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Build multi-brand token system", "Conduct usability testing sessions"],
        "interests": ["design", "ux"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000015"},
        "customer_id": {"$oid": "D00000000000000000000006"},
        "experience": [
            {
                "company": "Agile Learning Institute",
                "roles": [
                    {
                        "title": "Product Design Apprentice",
                        "start": {"$date": "2025-02-01T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Standardizing cross-platform component tokens and UI patterns with Melinda.",
                        "technologies": ["HTML", "CSS"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-05T13:00:00.000Z"},
            "correlation_id": "seed-profile-2a",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "avery",
            "at_time": {"$date": "2025-06-09T10:50:00.000Z"},
            "correlation_id": "save-profile-2a",
        },
    },
    {
        "_id": {"$oid": "A0000000000000000000002b"},
        "status": "active",
        "display_name": "Devon Interface",
        "description": "UI engineer mastering state management, micro-frontends, and animation choreography.",
        "email": "devon.interface@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Optimize render performance", "Implement fluid interactive transitions"],
        "interests": ["ux", "api"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000015"},
        "customer_id": {"$oid": "D00000000000000000000006"},
        "experience": [
            {
                "company": "Agile Learning Institute",
                "roles": [
                    {
                        "title": "Frontend Apprentice",
                        "start": {"$date": "2025-02-15T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Crafting micro-interactions and client state management for web apps.",
                        "technologies": ["React", "TypeScript", "HTML"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-20T10:15:00.000Z"},
            "correlation_id": "seed-profile-2b",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "devon",
            "at_time": {"$date": "2025-06-10T12:30:00.000Z"},
            "correlation_id": "save-profile-2b",
        },
    },
    {
        "_id": {"$oid": "A0000000000000000000002c"},
        "status": "active",
        "display_name": "Harper Fullstack",
        "description": "Full-stack apprentice balancing MongoDB query design with polished frontend presentation.",
        "email": "harper.fullstack@mentor-forge.dev",
        "email_verified": True,
        "goals": ["Design normalized document schemas", "Ship full-stack feature end-to-end"],
        "interests": ["ux", "data"],
        "roles": ["mentee"],
        "mentor_id": {"$oid": "A00000000000000000000015"},
        "customer_id": {"$oid": "D00000000000000000000006"},
        "experience": [
            {
                "company": "Agile Learning Institute",
                "roles": [
                    {
                        "title": "Fullstack Apprentice",
                        "start": {"$date": "2025-03-01T09:00:00.000Z"},
                        "end": {"$date": "2025-12-31T00:00:00.000Z"},
                        "description": "Integrating document database persistence with interactive user interfaces.",
                        "technologies": ["MongoDB", "Python", "TypeScript"],
                    }
                ],
            }
        ],
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-03-05T09:00:00.000Z"},
            "correlation_id": "seed-profile-2c",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "harper",
            "at_time": {"$date": "2025-06-11T14:20:00.000Z"},
            "correlation_id": "save-profile-2c",
        },
    },
]

new_mentees = [
    {
        "_id": {"$oid": "A00000000000000000000022"},
        "summary": "Jordan is a Persevere apprentice mastering responsive UI components and accessibility with Paula.",
        "notes": "## Progress\nExceptional grasp of semantic HTML and accessibility guidelines; building accessible component library.\n\n## Observations\nApplies feedback immediately during pairing sessions.\n\n## Mentor (paula)\nPersevere mentor; reinforce component composition and automated accessibility testing.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-01-15T10:00:00.000Z"},
            "correlation_id": "seed-profile-22",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "paula",
            "at_time": {"$date": "2025-06-01T12:00:00.000Z"},
            "correlation_id": "save-profile-22",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000023"},
        "summary": "Taylor is a Persevere mentee advancing full-stack Vue patterns and API integrations with Paula.",
        "notes": "## Progress\nConsistent progress on state management and asynchronous data fetching in Vue.\n\n## Observations\nLearns best with hands-on live coding exercises.\n\n## Mentor (paula)\nPersevere mentor; emphasize reactive store patterns and API error handling.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-05T11:00:00.000Z"},
            "correlation_id": "seed-profile-23",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "paula",
            "at_time": {"$date": "2025-06-02T13:30:00.000Z"},
            "correlation_id": "save-profile-23",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000024"},
        "summary": "Casey is a SuperSoft junior engineer building backend service reliability and CI pipelines with Danny.",
        "notes": "## Progress\nImplemented clean REST endpoints with robust schema validation in Python.\n\n## Observations\nQuickly debugs container build failures.\n\n## Mentor (danny)\nSuperSoft coordinator-mentor; deepen Docker multi-stage builds and automated test coverage.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-01-20T14:00:00.000Z"},
            "correlation_id": "seed-profile-24",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "danny",
            "at_time": {"$date": "2025-06-03T10:15:00.000Z"},
            "correlation_id": "save-profile-24",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000025"},
        "summary": "Morgan is a SuperSoft SRE apprentice establishing metrics collection and alert automation with Danny.",
        "notes": "## Progress\nSuccessfully instrumented key service endpoints with Prometheus metrics.\n\n## Observations\nMethodical approach to incident investigation and telemetry aggregation.\n\n## Mentor (danny)\nSuperSoft mentor; focus on SLO definition and alert threshold tuning.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-12T09:30:00.000Z"},
            "correlation_id": "seed-profile-25",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "danny",
            "at_time": {"$date": "2025-06-04T15:45:00.000Z"},
            "correlation_id": "save-profile-25",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000026"},
        "summary": "Alex is a SuperSoft cloud platform apprentice learning cluster deployment and rolling updates with Danny.",
        "notes": "## Progress\nOnboarded to SuperSoft staging environments; reviewing cluster manifests.\n\n## Observations\nHigh enthusiasm for cloud infrastructure automation.\n\n## Mentor (danny)\nSuperSoft mentor; prepare for upcoming onboarding session on rollout strategies.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-03-05T16:00:00.000Z"},
            "correlation_id": "seed-profile-26",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "danny",
            "at_time": {"$date": "2025-06-05T11:20:00.000Z"},
            "correlation_id": "save-profile-26",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000027"},
        "summary": "Sam is a startup founder refining financial modeling and pitch preparation with Elon.",
        "notes": "## Progress\nCompleted initial revenue model; articulating TAM and value proposition clearly.\n\n## Observations\nValues Elon sharp commercial feedback and stress-testing of unit economics.\n\n## Mentor (elon)\nMoney mentor; continue pitch deck polish and valuation sensitivity analysis.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-01-10T10:00:00.000Z"},
            "correlation_id": "seed-profile-27",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "elon",
            "at_time": {"$date": "2025-06-06T14:10:00.000Z"},
            "correlation_id": "save-profile-27",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000028"},
        "summary": "Riley is a SaaS founder modeling subscription pricing tiers and customer acquisition metrics with Elon.",
        "notes": "## Progress\nDefined three-tier pricing model; mapped churn risk factors across subscription cohorts.\n\n## Observations\nAnalytical mindset; eager to validate pricing assumptions with real cohort data.\n\n## Mentor (elon)\nMoney mentor; focus on net revenue retention and billing engine integration.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-15T15:30:00.000Z"},
            "correlation_id": "seed-profile-28",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "elon",
            "at_time": {"$date": "2025-06-07T09:40:00.000Z"},
            "correlation_id": "save-profile-28",
        },
    },
    {
        "_id": {"$oid": "A00000000000000000000029"},
        "summary": "Quinn completed the ALI fintech apprenticeship focused on capital ledger systems and risk audit with Elon.",
        "notes": "## Progress\nFinalized capstone risk model and audit reconciliation reports with Elon.\n\n## Observations\nSuccessfully graduated from the specialized fintech cohort; archive record retained.\n\n## Mentor (elon)\nConcluded coaching program with final milestone sign-off.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-01-25T11:45:00.000Z"},
            "correlation_id": "seed-profile-29",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "elon",
            "at_time": {"$date": "2025-06-08T16:00:00.000Z"},
            "correlation_id": "save-profile-29",
        },
    },
    {
        "_id": {"$oid": "A0000000000000000000002a"},
        "summary": "Avery is an ALI product design mentee developing design system tokens and user test protocols with Melinda.",
        "notes": "## Progress\nStandardized token taxonomy across web and mobile Figma libraries.\n\n## Observations\nDeep user empathy and strong cross-functional communication.\n\n## Mentor (melinda)\nALI multi-mentor; guide token export automation into CSS variables.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-05T13:00:00.000Z"},
            "correlation_id": "seed-profile-2a",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "melinda",
            "at_time": {"$date": "2025-06-09T10:50:00.000Z"},
            "correlation_id": "save-profile-2a",
        },
    },
    {
        "_id": {"$oid": "A0000000000000000000002b"},
        "summary": "Devon is an ALI frontend mentee crafting UI micro-interactions and performant animations with Melinda.",
        "notes": "## Progress\nBuilt reusable modal and drawer components with spring-based motion physics.\n\n## Observations\nExcels at polishing micro-interactions and optimizing 60fps animations.\n\n## Mentor (melinda)\nALI multi-mentor; pair on accessibility considerations for reduced-motion users.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-02-20T10:15:00.000Z"},
            "correlation_id": "seed-profile-2b",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "melinda",
            "at_time": {"$date": "2025-06-10T12:30:00.000Z"},
            "correlation_id": "save-profile-2b",
        },
    },
    {
        "_id": {"$oid": "A0000000000000000000002c"},
        "summary": "Harper is an ALI full-stack mentee learning MongoDB data modeling and backend API design with Melinda.",
        "notes": "## Progress\nEnrolled in ALI full-stack cohort; completed initial environment setup.\n\n## Observations\nStrong foundational programming skills, eager to bridge frontend and database layers.\n\n## Mentor (melinda)\nALI multi-mentor; schedule upcoming onboarding session to define capstone milestones.",
        "status": "active",
        "created": {
            "from_ip": "127.0.0.1",
            "by_user": "system",
            "at_time": {"$date": "2025-03-05T09:00:00.000Z"},
            "correlation_id": "seed-profile-2c",
        },
        "saved": {
            "from_ip": "127.0.0.1",
            "by_user": "melinda",
            "at_time": {"$date": "2025-06-11T14:20:00.000Z"},
            "correlation_id": "save-profile-2c",
        },
    },
]


def main():
    # 1. Update Profile
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    existing_ids = {p["_id"]["$oid"] for p in profiles}
    for p in new_profiles:
        oid_val = p["_id"]["$oid"]
        if oid_val not in existing_ids:
            profiles.append(p)
            existing_ids.add(oid_val)

    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)
        f.write("\n")

    # 2. Update Mentee
    with open(MENTEE_PATH, "r", encoding="utf-8") as f:
        mentees = json.load(f)

    existing_mentee_ids = {m["_id"]["$oid"] for m in mentees}
    for m in new_mentees:
        oid_val = m["_id"]["$oid"]
        if oid_val not in existing_mentee_ids:
            mentees.append(m)
            existing_mentee_ids.add(oid_val)

    with open(MENTEE_PATH, "w", encoding="utf-8") as f:
        json.dump(mentees, f, indent=2)
        f.write("\n")

    # 3. Update persona_ids.json
    with open(PERSONA_IDS_PATH, "r", encoding="utf-8") as f:
        persona_ids = json.load(f)

    slug_map = {
        "A00000000000000000000022": "jordan",
        "A00000000000000000000023": "taylor-persevere",
        "A00000000000000000000024": "casey",
        "A00000000000000000000025": "morgan",
        "A00000000000000000000026": "alex",
        "A00000000000000000000027": "sam-startup",
        "A00000000000000000000028": "riley-revenue",
        "A00000000000000000000029": "quinn-capital",
        "A0000000000000000000002a": "avery",
        "A0000000000000000000002b": "devon",
        "A0000000000000000000002c": "harper",
    }

    for p in new_profiles:
        oid_val = p["_id"]["$oid"]
        slug = slug_map[oid_val]
        persona_ids["profiles"][slug] = oid_val
        persona_ids["mentees"][slug] = oid_val

    with open(PERSONA_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(persona_ids, f, indent=2)
        f.write("\n")

    print(f"Updated Profile: {len(profiles)} total documents")
    print(f"Updated Mentee: {len(mentees)} total documents")
    print("persona_ids.json updated.")


if __name__ == "__main__":
    main()
