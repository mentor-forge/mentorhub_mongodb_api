#!/usr/bin/env python3
"""Generate Resource and Path test data from Obsidian exports (T111-T114)."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OBS = REPO / "Tasks" / "obsidian files"
RESOURCE_OUT = REPO / "configurator" / "test_data" / "Resource.0.1.0.0.json"
PATH_OUT = REPO / "configurator" / "test_data" / "Path.0.1.0.0.json"

RESOURCE_TYPES = [
    "article", "video", "book", "audio", "manual", "membership", "tutorial",
    "lesson", "getting-started", "online-class", "online-instructor", "in-person",
]
COSTS = ["free", "$", "$$", "$$$", "S$", "S$$", "S$$$"]
SKILLS = ["Candidate", "Apprentice", "Practioneer", "Craftsperson", "Master", "Distinguished"]
INTERESTS = ["ux", "api", "sre", "data", "design", "games", "iot", "robot"]
TECHS = ["React", "MongoDB", "Python", "TypeScript", "Java", "HTML", "CSS", "Other"]

LINK_TYPED = re.compile(r"\[([^\]]+?)\s*`([^`]+)`\]\(([^)]+)\)")
LINK_CHECKLIST = re.compile(r"-\s*\[\s*\]\s*\[([^\]]+)\]\(([^)]+)\)")
LINK_BULLET = re.compile(r"^\s*[-*]\s*\[([^\]]+)\]\(([^)]+)\)\s*$", re.MULTILINE)
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
TOPIC_HEADING = re.compile(r"^#\s+(?:Topic\s+)?\[\[([^\]]+)\]\]|^#\s+\[\[([^\]]+)\]\]", re.MULTILINE)
MODULE_HEADING = re.compile(r"^##\s+(.+)$", re.MULTILINE)

PLACEHOLDER_TOPICS = {"topic name", "segment name"}


def oid(n: int) -> dict:
    return {"$oid": f"B{n:023d}"}


def path_oid(n: int) -> dict:
    return {"$oid": f"C{n:023d}"}


def date_iso() -> dict:
    return {"$date": "2025-06-01T14:30:00.000Z"}


def breadcrumb(prefix: str, user: str = "system") -> dict:
    cid = re.sub(r"\s+", "", prefix)[:40]
    return {
        "at_time": date_iso(),
        "by_user": user,
        "correlation_id": cid,
        "from_ip": "127.0.0.1",
    }


def word_name(title: str, used: set[str]) -> str:
    raw = unicodedata.normalize("NFKD", title)
    raw = re.sub(r"[^A-Za-z0-9]+", "", raw)
    if not raw:
        raw = "Resource"
    base = raw[:40]
    name = base
    i = 1
    while name in used:
        suffix = str(i)
        name = (base[: 40 - len(suffix)] + suffix)[:40]
        i += 1
    used.add(name)
    return name


def infer_type(hint: str | None, url: str, title: str) -> str:
    h = (hint or "").lower()
    u = url.lower()
    t = title.lower()
    if "membership" in h or "subscription" in h:
        return "membership"
    if "video" in h or "youtube.com" in u or "youtu.be" in u or "vimeo.com" in u:
        return "video"
    if "book" in h or "amazon.com" in u or "audible.com" in u:
        return "book"
    if "audio" in h:
        return "audio"
    if "manual" in h or "docs." in u or "/docs/" in u or "documentation" in t:
        return "manual"
    if "tutorial" in h or "tool" in h:
        return "tutorial"
    if "lesson" in h:
        return "lesson"
    if "getting started" in h or "getting-started" in u:
        return "getting-started"
    if "class" in h or "course" in h or "udemy" in u or "coursera" in u:
        return "online-class"
    if "instructor" in h and "online" in h:
        return "online-instructor"
    if "in-person" in h or "in person" in h:
        return "in-person"
    if "thread" in h or "stackoverflow" in u:
        return "article"
    return "article"


def infer_cost(hint: str | None, url: str, rtype: str) -> str:
    h = (hint or "").lower()
    if rtype == "membership":
        if "mastery" in url.lower() or "300" in h:
            return "S$$$"
        return "S$$"
    if "book ($" in h or "($)" in h or "$$$" in h:
        return "$$$"
    if "($)" in h or " paid" in h:
        return "$$"
    if "$" in h and "free" not in h:
        return "$"
    if any(x in url.lower() for x in ("realpython.com/account", "cantrill", "morethancertified")):
        return "S$$"
    return "free"


def infer_interests(topic: str, url: str, title: str) -> list[str]:
    blob = f"{topic} {url} {title}".lower()
    tags: list[str] = []
    rules = [
        (["sre", "reliability", "incident", "monitor", "alert", "golden signal", "elk", "datadog", "grafana", "opentelemetry"], "sre"),
        (["design", "figma", "material design", "ux", "usability", "accessibility", "heuristic"], "design"),
        (["ux", "user experience", "ui design"], "ux"),
        (["python", "data wrang", "data engineer", "pandas"], "data"),
        (["api", "express", "rest", "graphql", "node"], "api"),
        (["game", "unity", "godot"], "games"),
        (["iot", "arduino", "raspberry"], "iot"),
        (["robot", "ros"], "robot"),
    ]
    for keys, val in rules:
        if any(k in blob for k in keys):
            tags.append(val)
    if not tags:
        tags.append("api")
    # dedupe preserve order
    seen = set()
    out = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out[:3]


def infer_technologies(topic: str, url: str, title: str) -> list[str]:
    blob = f"{topic} {url} {title}".lower()
    rules = [
        ("react", "React"), ("mongodb", "MongoDB"), ("mongoose", "MongoDB"),
        ("python", "Python"), ("typescript", "TypeScript"), (" java", "Java"),
        ("html", "HTML"), ("css", "CSS"), ("node", "Other"), ("vue", "Other"),
        ("cypress", "Other"), ("terraform", "Other"), ("aws", "Other"),
        ("kafka", "Other"), ("salesforce", "Other"), ("figma", "Other"),
    ]
    tags = []
    for key, val in rules:
        if key in blob and val not in tags:
            tags.append(val)
    if not tags:
        tags.append("Other")
    return tags[:3]


def infer_skill(topic: str, title: str) -> str:
    blob = f"{topic} {title}".lower()
    if any(x in blob for x in ("advanced", "specialty", "professional", "master")):
        return "Master"
    if any(x in blob for x in ("intermediate", "practitioner", "practioneer")):
        return "Practioneer"
    if any(x in blob for x in ("introduction", "intro", "basic", "foundation", "getting started", "beginner")):
        return "Apprentice"
    if any(x in blob for x in ("history", "overview")):
        return "Candidate"
    if any(x in blob for x in ("refactor", "pattern", "architecture")):
        return "Craftsperson"
    return "Practioneer"


def parse_topic_file(path: Path) -> tuple[str, str, list[tuple[str, str | None, str]]]:
    text = path.read_text(encoding="utf-8")
    title = path.stem
    m = TOPIC_HEADING.search(text)
    if m:
        title = (m.group(1) or m.group(2) or path.stem).strip()

    desc = ""
    lines = text.splitlines()
    started = False
    for line in lines:
        if line.startswith("#"):
            started = True
            continue
        if started and line.strip() and not line.startswith("##"):
            desc = line.strip()
            break
    if not desc:
        desc = f"Learning resources for {title}."

    resources: list[tuple[str, str | None, str]] = []
    if "## Resources" not in text:
        return title, desc, resources

    section = text.split("## Resources", 1)[1]
    section = re.split(r"\n##\s+", section, maxsplit=1)[0]

    seen_urls: set[str] = set()
    for m in LINK_TYPED.finditer(section):
        t, hint, url = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if url.startswith("http") and url not in seen_urls:
            seen_urls.add(url)
            resources.append((t, hint, url))
    for m in LINK_CHECKLIST.finditer(section):
        t, url = m.group(1).strip(), m.group(2).strip()
        if url.startswith("http") and url not in seen_urls:
            seen_urls.add(url)
            resources.append((t, None, url))
    for m in LINK_BULLET.finditer(section):
        t, url = m.group(1).strip(), m.group(2).strip()
        if url.startswith("http") and url not in seen_urls:
            seen_urls.add(url)
            resources.append((t, None, url))

    return title, desc, resources


def build_topic_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    for p in OBS.glob("*.md"):
        index[p.stem.lower()] = p
        title, _, _ = parse_topic_file(p)
        index[title.lower()] = p
    return index


def resolve_topic(name: str, index: dict[str, Path]) -> Path | None:
    key = name.strip().lower()
    if key in PLACEHOLDER_TOPICS:
        return None
    if key in index:
        return index[key]
    # fuzzy: remove punctuation
    norm = re.sub(r"[^a-z0-9]+", "", key)
    for k, p in index.items():
        if re.sub(r"[^a-z0-9]+", "", k) == norm:
            return p
    return None


def generate_resources() -> tuple[list[dict], dict[str, str], dict[str, list[str]]]:
    """Returns resources, url->oid map, topic stem -> list of oids."""
    used_names: set[str] = set()
    url_to_oid: dict[str, str] = {}
    topic_resources: dict[str, list[str]] = {}
    resources: list[dict] = []
    seq = 1

    topic_files = sorted(OBS.glob("*.md"))
    for tf in topic_files:
        topic_title, topic_desc, links = parse_topic_file(tf)
        topic_oids: list[str] = []
        for title, hint, url in links:
            if url in url_to_oid:
                topic_oids.append(url_to_oid[url])
                continue
            rtype = infer_type(hint, url, title)
            cost = infer_cost(hint, url, rtype)
            interests = infer_interests(topic_title, url, title)
            technologies = infer_technologies(topic_title, url, title)
            skill = infer_skill(topic_title, title)
            name = word_name(title, used_names)
            desc = f"{title} — supports learning in {topic_title}."
            oid_str = f"B{seq:023d}"
            seq += 1
            url_to_oid[url] = oid_str
            topic_oids.append(oid_str)
            resources.append({
                "_id": {"$oid": oid_str},
                "name": name,
                "description": desc[:500],
                "url": url,
                "type": rtype,
                "cost": cost,
                "skill_level": skill,
                "interests": interests,
                "technologies": technologies,
                "last_verified": date_iso(),
                "status": "active",
                "created": breadcrumb(f"seed-resource-{seq:04d}"),
                "saved": breadcrumb("save-resource-batch", "mike"),
            })
        topic_resources[tf.stem] = topic_oids
        topic_resources[topic_title] = topic_oids

    # enum coverage patches on last resources
    patches = [
        (0, {"type": "audio", "cost": "$", "skill_level": "Candidate", "interests": ["games"], "technologies": ["Java"], "status": "active"}),
        (1, {"type": "in-person", "cost": "$$", "skill_level": "Apprentice", "interests": ["iot"], "technologies": ["TypeScript"], "status": "active"}),
        (2, {"type": "online-instructor", "cost": "$$$", "skill_level": "Craftsperson", "interests": ["robot"], "technologies": ["React"], "status": "failed"}),
        (3, {"type": "lesson", "cost": "S$", "skill_level": "Distinguished", "interests": ["ux"], "technologies": ["MongoDB"], "status": "active"}),
        (4, {"type": "getting-started", "cost": "S$$$", "skill_level": "Master", "interests": ["design"], "technologies": ["HTML"], "status": "active"}),
        (5, {"type": "online-class", "cost": "S$$", "skill_level": "Practioneer", "interests": ["sre"], "technologies": ["CSS"], "status": "failed"}),
        (6, {"type": "manual", "cost": "free", "skill_level": "Candidate", "interests": ["data"], "technologies": ["Python"], "status": "failed"}),
    ]
    for i, patch in patches:
        if i < len(resources):
            resources[-(i + 1)].update(patch)

    # ensure all enum values present
    def ensure(field, values, idx=-1):
        present = {r[field] if not isinstance(r.get(field), list) else tuple(r[field]) for r in resources}
        for v in values:
            key = v if not isinstance(v, list) else tuple(v)
            if field == "type" and v not in {r["type"] for r in resources}:
                resources[idx]["type"] = v
                idx -= 1
            elif field == "cost" and v not in {r["cost"] for r in resources}:
                resources[idx]["cost"] = v
                idx -= 1
            elif field == "skill_level" and v not in {r["skill_level"] for r in resources}:
                resources[idx]["skill_level"] = v
                idx -= 1

    idx = -1
    for v in RESOURCE_TYPES:
        if v not in {r["type"] for r in resources}:
            resources[idx]["type"] = v
            idx -= 1
    for v in COSTS:
        if v not in {r["cost"] for r in resources}:
            resources[idx]["cost"] = v
            idx -= 1
    for v in SKILLS:
        if v not in {r["skill_level"] for r in resources}:
            resources[idx]["skill_level"] = v
            idx -= 1
    for v in INTERESTS:
        if not any(v in r["interests"] for r in resources):
            resources[idx]["interests"] = [v] + resources[idx]["interests"][:2]
            idx -= 1
    for v in TECHS:
        if not any(v in r["technologies"] for r in resources):
            resources[idx]["technologies"] = [v] + resources[idx]["technologies"][:2]
            idx -= 1
    if not any(r["status"] == "failed" for r in resources):
        resources[0]["status"] = "failed"
    if "audio" not in {r["type"] for r in resources}:
        resources[-7]["type"] = "audio"

    return resources, url_to_oid, topic_resources


def fix_sentence(s: str, max_len: int = 255) -> str:
    s = re.sub(r"[\t\n]+", " ", s or "").strip()
    if len(s) > max_len:
        s = s[: max_len - 3].rstrip() + "..."
    return s


def topic_entry(name: str, desc: str, oids: list[str]) -> dict:
    used: set[str] = set()
    wname = word_name(name, used)
    return {
        "name": wname,
        "description": fix_sentence(desc or f"Topic covering {name}."),
        "resources": [{"$oid": o} for o in oids],
    }


def parse_path_file(path: Path, index: dict[str, Path], topic_resources: dict[str, list[str]], url_to_oid: dict[str, str]) -> dict | None:
    text = path.read_text(encoding="utf-8")
    title = path.stem
    m = re.search(r"^#\s+\[\[([^\]]+)\]\]|^#\s+(.+)$", text, re.MULTILINE)
    if m:
        title = (m.group(1) or m.group(2) or path.stem).strip()

    desc_lines = []
    for line in text.splitlines()[1:]:
        if line.startswith("#"):
            break
        if line.strip() and not line.startswith("tags::"):
            desc_lines.append(line.strip())
    desc = " ".join(desc_lines) or f"Learning path for {title}."

    modules = []
    current_module = None
    for line in text.splitlines():
        if line.startswith("## "):
            mod_name = line[3:].strip()
            if mod_name.lower() in PLACEHOLDER_TOPICS:
                current_module = None
                continue
            current_module = {"name": word_name(mod_name, set()), "description": f"Module covering {mod_name}.", "topics": []}
            modules.append(current_module)
        elif current_module and line.strip().startswith("- [ ]"):
            # wikilink or url
            wm = WIKILINK.search(line)
            if wm:
                wname = wm.group(1).strip()
                if wname.lower() in PLACEHOLDER_TOPICS:
                    continue
                tp = resolve_topic(wname, index)
                if tp:
                    t_title, t_desc, _ = parse_topic_file(tp)
                    oids = topic_resources.get(tp.stem, topic_resources.get(t_title, []))
                    current_module["topics"].append(topic_entry(t_title, t_desc, oids))
            else:
                lm = LINK_BULLET.search(line) or LINK_CHECKLIST.search(line.replace("- [ ]", "-"))
                if lm:
                    t_title = lm.group(1).strip()
                    url = lm.group(2).strip()
                    oid = url_to_oid.get(url)
                    oids = [oid] if oid else []
                    current_module["topics"].append(topic_entry(t_title, f"Resource for {t_title}.", oids))

    if not modules:
        return None

    used_path_names: set[str] = set()
    pname = word_name(re.sub(r"[^A-Za-z0-9]+", "", title) or path.stem.replace(" ", ""), used_path_names)
    interests = infer_interests(title, "", desc)
    technologies = infer_technologies(title, "", desc)
    return {
        "name": pname,
        "description": desc[:500],
        "technologies": technologies,
        "interests": interests,
        "modules": modules,
    }


def append_membership(resources: list[dict], start_seq: int, specs: list[dict]) -> tuple[list[dict], dict[str, str], int]:
    used: set[str] = {r["name"] for r in resources}
    name_to_oid: dict[str, str] = {}
    seq = start_seq
    for spec in specs:
        # skip if url exists
        existing = next((r for r in resources if r.get("url") == spec["url"]), None)
        if existing:
            name_to_oid[spec["name"]] = existing["_id"]["$oid"]
            continue
        oid_str = f"B{seq:023d}"
        seq += 1
        doc = {
            "_id": {"$oid": oid_str},
            "name": spec["name"],
            "description": spec["description"],
            "url": spec["url"],
            "type": spec.get("type", "membership"),
            "cost": spec["cost"],
            "skill_level": spec.get("skill_level", "Practioneer"),
            "interests": spec["interests"],
            "technologies": spec["technologies"],
            "last_verified": date_iso(),
            "status": "active",
            "created": breadcrumb(f"seed-membership-{spec['name']}"),
            "saved": breadcrumb("save-membership-batch", "mike"),
        }
        resources.append(doc)
        name_to_oid[spec["name"]] = oid_str
        used.add(spec["name"])
    return resources, name_to_oid, seq


def main() -> None:
    # T110
    for f in [
        REPO / "configurator/test_data/Resource_Aggregation.0.1.0.0.json",
        RESOURCE_OUT,
        PATH_OUT,
    ]:
        f.write_text("[]\n", encoding="utf-8")

    resources, url_to_oid, topic_resources = generate_resources()
    index = build_topic_index()

    paths: list[dict] = []
    pseq = 1
    path_files = sorted((OBS / "Paths").glob("*.md"))
    for pf in path_files:
        parsed = parse_path_file(pf, index, topic_resources, url_to_oid)
        if not parsed:
            continue
        status = "archived" if "101 - Notes" in pf.name else "active"
        paths.append({
            "_id": path_oid(pseq),
            "name": parsed["name"],
            "description": parsed["description"],
            "technologies": parsed["technologies"],
            "interests": parsed["interests"],
            "modules": parsed["modules"],
            "status": status,
            "created": breadcrumb(f"seed-path-{pseq:03d}"),
            "saved": breadcrumb("save-path-batch", "mike"),
        })
        pseq += 1

    # enum coverage for paths
    for i, interest in enumerate(INTERESTS):
        if i < len(paths) and interest not in paths[i]["interests"]:
            paths[i]["interests"].append(interest)
    for i, tech in enumerate(TECHS):
        if i < len(paths) and tech not in paths[i]["technologies"]:
            paths[i]["technologies"].append(tech)

    next_resource_seq = len(resources) + 1

    # T113 memberships + PractitionerSRE
    sre_memberships = [
        {
            "name": "RealPythonMembership",
            "url": "https://realpython.com/account/join/",
            "cost": "S$$",
            "interests": ["data", "api"],
            "technologies": ["Python"],
            "description": "All-access Real Python membership with unlimited video courses, written tutorials, learning paths, quizzes, member Slack community, weekly live office hours, completion certificates, and downloadable source code.",
        },
        {
            "name": "CantrillAllTheThingsPlus",
            "url": "https://learn.cantrill.io/p/all-the-things-plus",
            "cost": "S$$",
            "interests": ["sre", "api"],
            "technologies": ["Other"],
            "description": "Adrian Cantrill All The Things Plus subscription with monthly or annual access to all AWS and Azure certification courses on learn.cantrill.io plus guest creator content and hands-on cloud labs.",
        },
        {
            "name": "MTCDevOpsDeploymentExpert",
            "url": "https://www.morethancertified.com/program/all-the-terraform",
            "cost": "S$$$",
            "interests": ["sre", "data"],
            "technologies": ["Other"],
            "description": "More Than Certified DevOps Deployment Expert bundle by Derek Morgan with lifetime access to project-based Terraform, Ansible, Jenkins, GitHub Actions, and multi-cloud IaC courses.",
        },
    ]
    resources, mem_oids, next_resource_seq = append_membership(resources, next_resource_seq, sre_memberships)

    def topic_oids_for(*names: str) -> list[str]:
        oids: list[str] = []
        for n in names:
            tp = resolve_topic(n, index)
            if tp:
                oids.extend(topic_resources.get(tp.stem, []))
        # dedupe preserve order
        seen = set()
        out = []
        for o in oids:
            if o not in seen:
                seen.add(o)
                out.append(o)
        return out

    sre_modules = [
        ("CloudPlatformMastery", "Cloud infrastructure and platform engineering foundations.", [
            ("CloudProviders", "Cloud Providers"),
            ("InfrastructureAsCode", "Infrastructure as Code"),
            ("BackingServices", "Backing Services"),
            ("ManagingMultipleEnvironments", "Managing Multiple Environments"),
        ], [mem_oids["CantrillAllTheThingsPlus"]]),
        ("Observability", "Monitoring, logging, metrics, and alerting practices.", [
            ("CollectingTelemetry", "Collecting Logs, Errors, Metrics, and Traces"),
            ("GoldenSignals", "The Golden Signals"),
            ("EffectiveAlerting", "Effective Alerting"),
            ("ELKStack", "elastic search (ELK)"),
            ("Debugging", "Debugging"),
        ], []),
        ("ReliabilityOperations", "Release engineering, incidents, and SRE collaboration.", [
            ("ManagingIncidents", "Managing Incidents"),
            ("ManagingReleases", "Managing Releases"),
            ("CICD", "Continuous Integration and Deployment"),
            ("PerformanceTesting", "Performance Testing"),
            ("WorkingWithSREs", "Working with Site Reliability Engineers"),
        ], []),
        ("AutomationAndIaC", "Secrets, security automation, Python tooling, and IaC practice.", [
            ("ManagingSecrets", "Managing Secrets"),
            ("ContinuousSecurity", "Continuous Security"),
        ], [mem_oids["MTCDevOpsDeploymentExpert"], mem_oids["RealPythonMembership"]]),
    ]

    sre_path_modules = []
    for mod_name, mod_desc, topics, extra_oids in sre_modules:
        topics_out = []
        for tname, wikilink in topics:
            tp = resolve_topic(wikilink, index)
            t_title, t_desc, _ = parse_topic_file(tp) if tp else (wikilink, f"Topic {wikilink}.", [])
            oids = topic_oids_for(wikilink)
            topics_out.append(topic_entry(t_title, t_desc, oids))
        # membership topic
        if extra_oids:
            topics_out.insert(0, topic_entry(
                f"{mod_name}Memberships",
                f"Platform memberships supporting {mod_name}.",
                extra_oids,
            ))
        sre_path_modules.append({
            "name": mod_name,
            "description": mod_desc,
            "topics": topics_out,
        })

    paths.append({
        "_id": path_oid(pseq),
        "name": "PractitionerSRE",
        "description": "Practitioner-level Site Reliability Engineering path combining cloud platform memberships with observability, operations, and infrastructure-as-code topics.",
        "technologies": ["Python", "Other"],
        "interests": ["sre", "api", "data"],
        "modules": sre_path_modules,
        "status": "active",
        "created": breadcrumb("seed-path-practitioner-sre"),
        "saved": breadcrumb("save-path-practitioner-sre", "mike"),
    })
    pseq += 1

    # T114 Vue Mastery + UI/UX
    uiux_resources = [
        {
            "name": "VueMasteryMembership",
            "url": "https://www.vuemastery.com/pricing/",
            "cost": "S$$$",
            "interests": ["ux", "design"],
            "technologies": ["Other"],
            "description": "Vue Mastery all-access subscription with premium Vue 3 video courses, learning paths, exclusive Evan You content, cheat sheets, progress tracking, and contributions to the Vue.js open-source project.",
        },
        {
            "name": "InteractionDesignFoundation",
            "url": "https://www.interaction-design.org/",
            "cost": "S$$",
            "interests": ["ux", "design"],
            "technologies": ["Other"],
            "description": "Interaction Design Foundation membership with self-paced UX courses on design thinking, user research, interaction design, and accessibility.",
            "type": "membership",
        },
        {
            "name": "RefactoringUI",
            "url": "https://www.refactoringui.com/",
            "cost": "$$",
            "interests": ["design", "ux"],
            "technologies": ["CSS", "HTML"],
            "description": "Refactoring UI book and course by Adam Wathan and Steve Schoger teaching practical visual design techniques for developers building interfaces.",
            "type": "book",
        },
        {
            "name": "MaterialDesign3Docs",
            "url": "https://m3.material.io/",
            "cost": "free",
            "interests": ["design", "ux"],
            "technologies": ["Other"],
            "description": "Official Google Material Design 3 documentation and guidelines for building adaptive, accessible product UI systems.",
            "type": "manual",
        },
    ]
    resources, ui_oids, next_resource_seq = append_membership(resources, next_resource_seq, uiux_resources)

    uiux_modules = [
        ("DesignFoundations", "Human-centered design principles and UX fundamentals.", [
            "Design Fundamentals", "Introduction to Design Thinking", "Design Systems",
            "Accessibility and Universal Design Fundamentals", "Working with Digital Product Designers",
        ], [ui_oids.get("InteractionDesignFoundation", "")]),
        ("UIDesignTools", "Prototyping and visual design tooling.", ["FIgma"], []),
        ("MaterialDesign", "Google Material Design system components and patterns.", [
            "Material Design Foundations", "Material Design Styles", "Components Actions",
            "Communication", "Containment", "Navigation", "Selection", "Text Inputs",
        ], [ui_oids.get("MaterialDesign3Docs", "")]),
        ("ResponsiveFrontEnd", "Layout, responsiveness, and CSS craft.", [
            "Responsive Design", "CSS Flexbox", "CSS Grid", "Intermediate CSS Concepts",
        ], [ui_oids.get("RefactoringUI", "")]),
        ("VueEngineering", "Vue.js front-end engineering with structured course progression.", [], [ui_oids["VueMasteryMembership"]]),
    ]

    ui_path_modules = []
    for mod_name, mod_desc, wikilinks, extra_oids in uiux_modules:
        topics_out = []
        extra_oids = [o for o in extra_oids if o]
        if mod_name == "VueEngineering":
            topics_out.append(topic_entry(
                "VueMasteryLearningPath",
                "Vue Mastery subscription with Intro to Vue 3, Real World Vue 3, Vue Router, Pinia, TypeScript, Vite, and Nuxt 3 courses.",
                extra_oids,
            ))
        else:
            if extra_oids:
                topics_out.append(topic_entry(f"{mod_name}Resources", f"Curated resources for {mod_name}.", extra_oids))
            for wl in wikilinks:
                tp = resolve_topic(wl, index)
                if not tp:
                    continue
                t_title, t_desc, _ = parse_topic_file(tp)
                oids = topic_oids_for(wl)
                topics_out.append(topic_entry(t_title, t_desc, oids))
        ui_path_modules.append({"name": mod_name, "description": mod_desc, "topics": topics_out})

    paths.append({
        "_id": path_oid(pseq),
        "name": "PractitionerUIUXEngineer",
        "description": "Practitioner-level UI and UX engineering path covering design fundamentals, Figma prototyping, Material Design systems, responsive CSS, and Vue.js front-end mastery.",
        "technologies": ["HTML", "CSS", "Other"],
        "interests": ["ux", "design"],
        "modules": ui_path_modules,
        "status": "active",
        "created": breadcrumb("seed-path-practitioner-uiux"),
        "saved": breadcrumb("save-path-practitioner-uiux", "mike"),
    })

    RESOURCE_OUT.write_text(json.dumps(resources, indent=2) + "\n", encoding="utf-8")
    PATH_OUT.write_text(json.dumps(paths, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {len(resources)} resources -> {RESOURCE_OUT}")
    print(f"Wrote {len(paths)} paths -> {PATH_OUT}")


if __name__ == "__main__":
    main()
