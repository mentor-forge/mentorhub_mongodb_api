# T114 – Practitioner UI/UX Engineer Path and Vue Mastery Resources

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
  - Add **Vue Mastery** membership Resource and **2–4 additional UI/UX-appropriate resources** not already in T111 (synthesized from web research; e.g. Interaction Design Foundation, Refactoring UI, or similar — agent chooses with brief rationale in notes).
  - Add one **Practitioner UI/UX Engineer** Path weaving Vue Mastery with Obsidian Design-path topics and T111 resources.
  - Use web-researched descriptions (summarized below).

## Goal

Extend Resource and Path test data with a practitioner-grade UI/UX engineering path centered on Vue.js craft (Vue Mastery) plus design fundamentals, Figma, and Material Design topics from Mike's Obsidian vault.

## Context / Input files

- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- Resource and Path dictionaries and enumerators.
- `../configurator/test_data/Resource.0.1.0.0.json` — T111 + T113 resources (append).
- `../configurator/test_data/Path.0.1.0.0.json` — T112 + T113 paths (append).
- `../Tasks/obsidian files/Paths/Design.md` — primary path structure reference.
- Related topic files (T111 harvest):
  - `Design Fundamentals.md`, `Introduction to Design Thinking.md`, `Design Systems.md`, `Accessibility and Universal Design Fundamentals.md`, `Working with Digital Product Designers.md`
  - `FIgma.md`
  - `Material Design Foundations.md`, `Material Design Styles.md`, `Components Actions.md`, `Communication.md`, `Containment.md`, `Navigation.md`, `Selection.md`, `Text Inputs.md`
  - `Responsive Design.md`, `Intermediate CSS Concepts.md`, `CSS Grid.md`, `CSS Flexbox.md`
- [PENDING.T111](./PENDING.T111.import_obsidian_resources_test_data.md), [PENDING.T112](./PENDING.T112.import_obsidian_paths_test_data.md), and preferably [PENDING.T113](./PENDING.T113.practitioner_sre_membership_path.md) — T113 should complete first to avoid JSON merge conflicts.

### Primary membership resource: Vue Mastery

| Field | Value |
| --- | --- |
| `name` | `VueMasteryMembership` |
| `url` | `https://www.vuemastery.com/pricing/` |
| `type` | `membership` |
| `cost` | `S$$$` (~$300/year billed yearly; ~$25/month monthly option) |
| `skill_level` | `Practioneer` |
| `interests` | `["ux", "design"]` |
| `technologies` | `["Other"]` (Vue not yet in technologies enum — use `Other`; note in implementation notes) |
| `status` | `active` |
| `description` | Vue Mastery all-access subscription — premium Vue 3 video courses, learning paths for beginner through advanced, exclusive Evan You content, cheat sheets, progress tracking, and contributions to the Vue.js open-source project. |

**Research notes**: Annual ~$300/yr; monthly ~$25/mo; team plans via team@vuemastery.com; courses include Intro to Vue 3, Real World Vue 3 (Composition API), Vue Router, Pinia, TypeScript, Vite, and Nuxt 3 ([vuemastery.com/pricing](https://www.vuemastery.com/pricing/)).

### Additional UI/UX resources to add (agent selects 2–4)

Choose resources that complement the Obsidian Design topics and are **not** duplicates of T111 URLs. Examples (verify URLs at implementation time):

| Candidate | `name` | `type` | `cost` | Rationale |
| --- | --- | --- | --- | --- |
| Interaction Design Foundation | `InteractionDesignFoundation` | `membership` | `S$$` | UX research, design thinking courses |
| Refactoring UI (book/course) | `RefactoringUI` | `book` or `online-class` | `$$` | Practical visual design for developers |
| Google Material Design docs | `MaterialDesignDocs` | `manual` | `free` | Official Material 3 reference (if not already in T111) |
| Nielsen Norman Group articles | Already in `Design Fundamentals.md` T111 harvest — **do not duplicate** |

Ensure new resources vary `type` and `cost` enums and include at least one `free` resource if not already covered.

### Practitioner UI/UX Engineer Path

| Field | Value |
| --- | --- |
| `_id` | Next available `C000…` after T113 |
| `name` | `PractitionerUIUXEngineer` |
| `description` | Practitioner-level UI and UX engineering path covering design fundamentals, Figma prototyping, Material Design systems, responsive CSS, and Vue.js front-end mastery. |
| `interests` | `["ux", "design"]` |
| `technologies` | `["HTML", "CSS", "Other"]` |
| `status` | `active` |

**Suggested module structure** (from `Paths/Design.md` + frontend craft):

| Module | Topics | Key resources |
| --- | --- | --- |
| `DesignFoundations` | Design Fundamentals, Introduction to Design Thinking, Design Systems, Accessibility and Universal Design | T111 topic resources + any new UX membership |
| `UIDesignTools` | Figma | T111 Figma topic resources |
| `MaterialDesign` | Material Design Foundations, Material Design Styles, Components Actions, Communication, Containment, Navigation, Selection, Text Inputs | T111 topic resources |
| `ResponsiveFrontEnd` | Responsive Design, CSS Flexbox, CSS Grid, Intermediate CSS Concepts | T111 topic resources |
| `VueEngineering` | Dedicated topic `VueMasteryLearningPath` | `VueMasteryMembership` + synthesized description of recommended Vue Mastery course sequence (Intro → Real World Vue 3 → Router → Pinia → Vite/Nuxt as aspirational resources or notes in topic description) |

Each topic's `resources` array uses `$oid` references from Resource test data. The Vue module topic should include the Vue Mastery membership `$oid` plus any free Vue getting-started resources already harvested (if any).

## Requirements

1. **Append only** — preserve all T111/T112/T113 documents.
2. **EJSON encoding** — same rules as prior tasks.
3. **`name` fields** — `word` pattern (e.g. `PractitionerUIUXEngineer`, `VueMasteryMembership`).
4. **No duplicate URLs** — skip creating a Resource if the same URL already exists in test data; reference the existing `$oid` in the Path instead.
5. **Cross-reference integrity** — all Path resource refs must resolve.
6. **Human-readable path title** — "Practitioner UI/UX Engineer" belongs in `description`, not `name`.

## Testing expectations

- **Processing test** — drop database, configure on port **8385**, validate `SUCCESS`.
- **Packaging test** — `make container` and `make process` → SUCCESS.

## Dependencies / Ordering

- **Depends on** [PENDING.T111](./PENDING.T111.import_obsidian_resources_test_data.md) and [PENDING.T112](./PENDING.T112.import_obsidian_paths_test_data.md).
- **Run after** [PENDING.T113](./PENDING.T113.practitioner_sre_membership_path.md) to avoid concurrent edits to the same JSON files.

## Change control checklist

- [x] Added Vue Mastery membership and 2–4 complementary UI/UX resources.
- [x] Added PractitionerUIUXEngineer Path with modules/topics wired to resources.
- [x] Ran `make container` successfully.
- [x] Ran `make process` successfully.
- [ ] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Appended four UI/UX Resources and the `PractitionerUIUXEngineer` Path document.

**Resources added**

| name | type | cost |
| --- | --- | --- |
| `VueMasteryMembership` | membership | S$$$ |
| `InteractionDesignFoundation` | membership | S$$ |
| `RefactoringUI` | book | $$ |
| `MaterialDesign3Docs` | manual | free |

**PractitionerUIUXEngineer path**

- 5 modules: DesignFoundations, UIDesignTools, MaterialDesign, ResponsiveFrontEnd, VueEngineering.
- Figma, Material Design, and Design Obsidian topics wired from T111.
- VueEngineering module centers on Vue Mastery membership with recommended course progression in topic description.

**Testing results**

- `make container` → SUCCESS.
- `POST /api/configurations/` → SUCCESS.
