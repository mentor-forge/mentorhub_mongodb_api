# T112 – Import Obsidian Paths Test Data

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Path.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Path.0.1.0.0.json`
- **Obsidian path source directory** `../Tasks/obsidian files/Paths/`
- **Resource cross-reference** `../configurator/test_data/Resource.0.1.0.0.json` (from T111)
- **Number of documents to generate**: One Path per Obsidian path file that represents a real learning path (see exclusions below).
- **Special requirements**
  - Import module/topic structure from Mike's Obsidian path exports.
  - Map each `[[Topic Wikilink]]` checklist item to a **topic** whose `resources` array contains the `$oid` values of all Resources harvested from that topic's markdown file in T111.
  - Map inline markdown links `[Title](url)` (as in `Paths/Python.md`) to Resources by URL lookup in T111 output.
  - Skip placeholder checklist items (`[[Topic Name]]`, empty modules titled `Segment Name`).
  - Assign deterministic Path `_id` values starting at `{ "$oid": "C00000000000000000000001" }`, sorted by path file name.
  - Set `name` using the `word` type (no spaces). Use the Obsidian path title with spaces removed (e.g. `EngineerKit`, `SiteReliabilityEngineering`, `CypressTesting`, `Odin`, `Design`, `Python`, `Databases`, `Salesforce`, `LearnApacheKafka`, `ApacheKafkaFundamentals`).
  - Put the human-readable path title (with spaces) in `description`.
  - Tag each path with appropriate `interests` and `technologies` arrays.
  - Set `status`: `active` for all imported paths except one path (e.g. `ApacheKafka101Notes`) set to `archived` so every `default_status` value appears at least once if both `active` and `archived` exist in enumerators.

## Goal

Generate Path documents whose `modules` → `topics` → `resources` hierarchy mirrors Mike's Obsidian path markdown files, with resource references wired to T111 Resource `$oid` values.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- The **Dictionary** and **Enumerators** linked in **User inputs**.
- The [type files](../configurator/types/) — especially `word.yaml`.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md).
- `../Tasks/obsidian files/Paths/*.md` — **11** path files:
  - `EngineerKit.md` — 15 modules, ~75 topics (primary path).
  - `Odin.md` — Foundations through Getting Hired.
  - `Design.md` — UI/Material Design segments.
  - `Site reliability engineering.md` — Observability, IaC, Disaster Recovery segments.
  - `Python.md` — mix of wikilinks and direct URLs.
  - `Databases.md`, `Salesforce.md`, `Cypress Testing.md`, `Learn Apache Kafka.md`, `Apache Kafka Fundamentals.md`, `Apache Kafka 101 - Notes.md`.
- `../configurator/test_data/Resource.0.1.0.0.json` — **required**; built by T111.
- Topic files under `../Tasks/obsidian files/*.md` — resolve wikilink names to topic files (handle spelling variants like `FIgma`).
- [SHIPPED.T104.generate_path_test_data.md](./SHIPPED.T104.generate_path_test_data.md) — prior EngineerKit path approach.
- [PENDING.T111.import_obsidian_resources_test_data.md](./PENDING.T111.import_obsidian_resources_test_data.md) — must be complete.

### Obsidian path file format

Path files use module headings (`## Module Name`) and checklist topic links:

```markdown
# [[EngineerKit]]
A collection of Topics...

## Architecture
- [ ] [[Common Tech Stacks]]
- [ ] [[Assembling a Tech Stack]]
```

Some paths embed direct resource URLs instead of wikilinks (see `Paths/Python.md`).

### Wikilink → topic file resolution

- Strip `[[` and `]]` from checklist items.
- Match to topic filename: `Common Tech Stacks.md`, case/spacing as exported.
- Handle known typos in filenames (e.g. wikilink `FIgma` → `FIgma.md`).

### Topic → resources mapping

For each resolved topic file, collect all Resource `$oid` values from T111 that were harvested from that topic's `## Resources` section. Populate the Path topic's `resources` array with those ids (EJSON `$oid` objects).

If a wikilink topic file has **no** resources (empty section), still include the topic with an empty `resources` array and a synthesized description from the topic file intro.

### Paths to exclude or minimize

- `Apache Kafka 101 - Notes.md` — treat as notes/supplemental; may be `archived` or include minimal structure.
- Do **not** create Practitioner SRE or Practitioner UI/UX paths here — those are T113 and T114.

## Requirements

1. **EJSON encoding** — same rules as T111 for `_id`, dates, and nested `$oid` references in `resources` arrays.

2. **Schema structure**

```json
{
  "_id": { "$oid": "C00000000000000000000001" },
  "name": "EngineerKit",
  "description": "A collection of engineering topics compiled by Enok Collective.",
  "technologies": ["Other"],
  "interests": ["api", "sre", "data", "design"],
  "modules": [
    {
      "name": "Architecture",
      "description": "Tech stack selection, ramping, and living documentation.",
      "topics": [
        {
          "name": "CommonTechStacks",
          "description": "...",
          "resources": [{ "$oid": "B000000000000000000000XX" }]
        }
      ]
    }
  ],
  "status": "active",
  "created": { ... },
  "saved": { ... }
}
```

3. **Validation**
   - Every `$oid` in `resources` arrays must exist in `Resource.0.1.0.0.json`.
   - Log any unmatched wikilinks or URLs in **Implementation notes**; aim for zero unmatched links on real (non-placeholder) topics.

4. **Enum coverage**
   - Across all Path documents, ensure `interests` and `technologies` enum arrays collectively cover all enumerator values at least once (same pattern as T103/T104).

5. **Do not overwrite T113/T114 paths**
   - T113 and T114 append additional Path documents after this task. Leave room in the `$oid` sequence or append after the Obsidian-import paths.

## Testing expectations

- **Processing test**
  - `curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"`
  - `curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"`
  - Validate `SUCCESS`.
- **Packaging test**
  - `make container` → SUCCESS.
  - `make process` → SUCCESS.

## Dependencies / Ordering

- **Depends on** [PENDING.T110](./PENDING.T110.clear_resource_and_path_test_data.md) and [PENDING.T111](./PENDING.T111.import_obsidian_resources_test_data.md).
- **Blocks** [PENDING.T113](./PENDING.T113.practitioner_sre_membership_path.md) and [PENDING.T114](./PENDING.T114.practitioner_uiux_path.md) — those tasks **append** to Path test data; run T112 first.

## Change control checklist

- [x] Reviewed Obsidian path files and T111 Resource output.
- [x] Generated Path test data with valid resource cross-references.
- [x] Documented unmatched wikilinks/URLs (if any).
- [x] Ran `make container` successfully.
- [x] Ran `make process` successfully.
- [ ] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Generated **11** Obsidian-import Path documents in `configurator/test_data/Path.0.1.0.0.json` (T113/T114 append 2 practitioner paths for **13** total).

**Approach**

- Parsed all markdown files in `Tasks/obsidian files/Paths/`.
- Built `modules` → `topics` → `resources` hierarchy from `##` module headings and `- [ ] [[Topic]]` checklist items.
- Resolved wikilinks to topic files and wired `resources` arrays to T111 `$oid` values.
- Handled `Paths/Python.md` direct URL links via URL lookup.
- Skipped placeholder `Topic Name` / `Segment Name` entries.
- Set `Apache Kafka 101 - Notes` path to `archived` status.
- EngineerKit path: 15 modules, 74 topics, 463 resource references.

**Cross-reference validation**

- **0** unmatched resource `$oid` references across all paths.

**Testing results**

- `make container` → SUCCESS.
- `POST /api/configurations/` → SUCCESS.
