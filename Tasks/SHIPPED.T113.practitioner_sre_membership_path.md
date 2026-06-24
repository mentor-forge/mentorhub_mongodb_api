# T113 – Practitioner SRE Path and Membership Resources

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary files** `../configurator/dictionaries/Resource.0.1.0.yaml`, `../configurator/dictionaries/Path.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data files**
  - Append to `../configurator/test_data/Resource.0.1.0.0.json`
  - Append to `../configurator/test_data/Path.0.1.0.0.json`
- **Special requirements**
  - Add **three membership Resource** documents (Real Python, Cantrill.io, More Than Certified).
  - Add one **Practitioner SRE** Path document that weaves these memberships together with relevant Obsidian SRE/ops/infrastructure topics and their T111 resources.
  - Use web-researched descriptions (summarized below); verify URLs at implementation time.

## Goal

Extend Resource and Path test data with practitioner-grade SRE membership subscriptions and a curated **Practitioner SRE** learning path suitable for a Practioneer-level engineer.

## Context / Input files

- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- Resource and Path dictionaries and enumerators (see **User inputs**).
- `../configurator/test_data/Resource.0.1.0.0.json` — existing T111 resources (append, do not replace).
- `../configurator/test_data/Path.0.1.0.0.json` — existing T112 paths (append).
- `../Tasks/obsidian files/Paths/Site reliability engineering.md` — seed module structure.
- Related topic files for SRE path modules (from T111 harvest):
  - Monitoring: `Collecting Logs, Errors, Metrics, and Traces.md`, `The Golden Signals.md`, `Effective Alerting.md`, `Debugging.md`, `Improving Performance.md`, `elastic search (ELK).md`
  - Operations: `Managing Incidents.md`, `Managing Releases.md`, `Continuous Integration and Deployment.md`, `Performance Testing.md`, `Working with Site Reliability Engineers.md`
  - Infrastructure: `Cloud Providers.md`, `Infrastructure as Code.md`, `Backing Services.md`, `Managing Multiple Environments.md`, `Working with Cloud Engineers.md`
  - Security/ops overlap: `Managing Secrets.md`, `Continuous Security.md`
  - Python automation (Real Python tie-in): any Python topic resources already harvested
- [PENDING.T111](./PENDING.T111.import_obsidian_resources_test_data.md) and [PENDING.T112](./PENDING.T112.import_obsidian_paths_test_data.md) — must be complete.

### Membership resources to create

Assign the next available `B000…` `$oid` values after T111's last id.

#### 1. Real Python Membership

| Field | Value |
| --- | --- |
| `name` | `RealPythonMembership` |
| `url` | `https://realpython.com/account/join/` |
| `type` | `membership` |
| `cost` | `S$$` (annual ~$360/yr individual; monthly also available) |
| `skill_level` | `Practioneer` |
| `interests` | `["data", "api"]` |
| `technologies` | `["Python"]` |
| `status` | `active` |
| `description` | All-access Real Python membership with unlimited video courses, written tutorials, learning paths, quizzes, member Slack community, weekly live office hours, completion certificates, and downloadable source code. |

**Research notes**: Individual and team plans; no long-term contract; PayPal/credit card; yearly discount vs monthly ([realpython.com/account/join](https://realpython.com/account/join/)).

#### 2. Cantrill.io Membership (All The Things Plus)

| Field | Value |
| --- | --- |
| `name` | `CantrillAllTheThingsPlus` |
| `url` | `https://learn.cantrill.io/p/all-the-things-plus` |
| `type` | `membership` |
| `cost` | `S$$` (~$29/month or ~$299/year; tiered plans from $8–$29/month) |
| `skill_level` | `Practioneer` |
| `interests` | `["sre", "api"]` |
| `technologies` | `["Other"]` |
| `status` | `active` |
| `description` | Adrian Cantrill's All The Things Plus subscription — monthly or annual access to all AWS and Azure certification courses on learn.cantrill.io plus guest creator content, with hands-on labs in your own cloud accounts. |

**Research notes**: Flexible tiers (Associate $8/mo, All AWS ~$18–20/mo, All Courses $29/mo); one-time purchase options also exist but this resource represents the **subscription/membership** model ([learn.cantrill.io/p/all-the-things-plus](https://learn.cantrill.io/p/all-the-things-plus)).

#### 3. More Than Certified (MTC) — DevOps Deployment Expert Bundle

| Field | Value |
| --- | --- |
| `name` | `MTCDevOpsDeploymentExpert` |
| `url` | `https://www.morethancertified.com/program/all-the-terraform` |
| `type` | `membership` |
| `cost` | `S$$$` (lifetime bundle purchase; treat as high-value platform access) |
| `skill_level` | `Practioneer` |
| `interests` | `["sre", "data"]` |
| `technologies` | `["Other"]` |
| `status` | `active` |
| `description` | More Than Certified DevOps Deployment Expert bundle by Derek Morgan — lifetime access to project-based Terraform, Ansible, Jenkins, GitHub Actions, and multi-cloud IaC courses with hands-on labs and certification prep. |

**Research notes**: MTC primarily sells lifetime course bundles rather than recurring subscriptions; model as `membership` for platform-wide access. Flagship Terraform bundle includes 10+ hands-on courses ([morethancertified.com/program/all-the-terraform](https://www.morethancertified.com/program/all-the-terraform)).

### Practitioner SRE Path to create

| Field | Value |
| --- | --- |
| `_id` | Next available `C000…` after T112 paths |
| `name` | `PractitionerSRE` |
| `description` | Practitioner-level Site Reliability Engineering path combining cloud platform memberships with observability, operations, and infrastructure-as-code topics. |
| `interests` | `["sre", "api", "data"]` |
| `technologies` | `["Python", "Other"]` |
| `status` | `active` |

**Suggested module structure** (adapt based on T111 resource availability):

| Module | Topics | Membership tie-in |
| --- | --- | --- |
| `CloudPlatformMastery` | Cloud Providers, Infrastructure as Code, Backing Services, Managing Multiple Environments | Include `CantrillAllTheThingsPlus` resource id in module intro topic or dedicated `CantrillMembership` topic |
| `Observability` | Collecting Logs/Metrics/Traces, Golden Signals, Effective Alerting, ELK stack | Topic resources from T111 |
| `ReliabilityOperations` | Managing Incidents, Managing Releases, CI/CD, Performance Testing, Working with SREs | Topic resources from T111 |
| `AutomationAndIaC` | Managing Secrets, Continuous Security | Include `MTCDevOpsDeploymentExpert` + `RealPythonMembership` where Python scripting supports automation |

Each topic's `resources` array must reference valid `$oid` values from Resource test data (T111 topic resources + the three new membership resources).

## Requirements

1. **Append only** — do not remove or rewrite T111/T112 documents.
2. **EJSON encoding** — same rules as prior tasks.
3. **`name` fields** — satisfy `word` pattern (no spaces).
4. **Cross-reference integrity** — every `$oid` in the new Path must exist in Resource test data.
5. **Enum variety** — membership resources should use distinct `cost` tiers (`S$$`, `S$$$`) and complementary `interests`/`technologies` tags.
6. **Breadcrumbs** — include `created` and `saved` on all new documents.

## Testing expectations

- **Processing test** — drop database, configure, validate `SUCCESS` (port **8385**).
- **Packaging test** — `make container` and `make process` → SUCCESS.

## Dependencies / Ordering

- **Depends on** [PENDING.T111](./PENDING.T111.import_obsidian_resources_test_data.md) and [PENDING.T112](./PENDING.T112.import_obsidian_paths_test_data.md).
- **Independent of** [PENDING.T114](./PENDING.T114.practitioner_uiux_path.md) — may run in parallel after T112 if orchestrator supports it, but both append to the same JSON files; **recommend sequential T113 then T114** to avoid merge conflicts.

## Change control checklist

- [x] Added three membership Resource documents with researched descriptions.
- [x] Added PractitionerSRE Path with modules/topics wired to resources.
- [x] Ran `make container` successfully.
- [x] Ran `make process` successfully.
- [ ] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Appended three membership Resources and the `PractitionerSRE` Path document.

**Membership resources added**

| name | url | cost |
| --- | --- | --- |
| `RealPythonMembership` | realpython.com/account/join/ | S$$ |
| `CantrillAllTheThingsPlus` | learn.cantrill.io/p/all-the-things-plus | S$$ |
| `MTCDevOpsDeploymentExpert` | morethancertified.com/program/all-the-terraform | S$$$ |

**PractitionerSRE path**

- 4 modules: CloudPlatformMastery, Observability, ReliabilityOperations, AutomationAndIaC.
- Cantrill membership in CloudPlatformMastery; MTC + Real Python in AutomationAndIaC.
- Topics wired to Obsidian SRE/monitoring/infrastructure topic resources from T111.

**Testing results**

- `make container` → SUCCESS.
- `POST /api/configurations/` → SUCCESS.
