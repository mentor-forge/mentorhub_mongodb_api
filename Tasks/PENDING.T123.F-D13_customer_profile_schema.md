# T123 – F-D13 Customer and Profile Schema Updates

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (F-D13 pipeline — not “Run as needed”)  
**Issue**: F-D13  
**Branch**: `F-d13/customer`

This task wires the **Customer** collection to **Mentee** and **Profile** documents for the Customer user journey. We are **pre-release**, so edit the existing **0.1.0** dictionaries directly — **no version bumps and no migrations**.

## User inputs (edit before running)

- **Branch name**: `F-d13/customer`
- **Customer dictionary**: `../configurator/dictionaries/Customer.0.1.0.yaml`
- **Profile dictionary**: `../configurator/dictionaries/Profile.0.1.0.yaml`
- **Customer configuration**: `../configurator/configurations/Customer.yaml` (stays at version 0.1.0.0)
- **Profile configuration**: `../configurator/configurations/Profile.yaml` (stays at version 0.1.0.0)
- **Enumerators file**: `../configurator/enumerators/enumerations.0.yaml`

## Goal

1. Extend **Customer** so a sponsoring customer can reference the **Mentee** documents they pay for.
2. Extend **Profile** so sponsored mentee profiles can reference their **Customer** document.
3. Keep schemas at **0.1.0** and verify configure-database still succeeds before test-data tasks run.

## Design decisions

| Concept | Decision |
|--------|----------|
| **Pre-release** | Edit `Customer.0.1.0.yaml` and `Profile.0.1.0.yaml` in place. Do **not** add 0.2.0 versions or migration pipelines. |
| **Customer → Mentee** | `Customer.mentees` is an array of **Mentee collection `_id`** values (`CC000…`), not Profile `_id`s. |
| **Profile → Customer** | `Profile.customer_id` points to **Customer `_id`**. Set only on **sponsored mentee** profiles — not on customer personas (`cat`, `morgan`) or mentors/coordinators. |
| **Customer `name`** | Use type **`word`** (searchable IdP-style key such as `cat`, `morgan`), consistent with [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md). |
| **Bidirectional integrity** | If Customer `cat` lists Mentee `CC…005` (riley), then riley's Profile must have `customer_id` pointing at `cat`'s Customer `_id`. Enforced in T125. |

## Context / Input files

- [Tasks/README.md](./README.md)
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- [Customer workshop](../../mentorhub/Workshops/customer_workshop.md) — Cat the Customer sponsors mentees and tracks ROI
- [SHIPPED.T106.mentee_collection_and_profile_schema.md](./SHIPPED.T106.mentee_collection_and_profile_schema.md) — Mentee collection and Profile conventions
- `../configurator/dictionaries/Customer.0.1.0.yaml`
- `../configurator/dictionaries/Profile.0.1.0.yaml`
- `../configurator/dictionaries/Mentee.0.1.0.yaml`
- `../configurator/configurations/Customer.yaml`
- `../configurator/test_data/Mentee.0.1.0.0.json` — Mentee `_id` values for reference

## Implementation plan

### Step 1 — Update Customer.0.1.0.yaml

Ensure **Customer** includes standard document properties plus sponsorship linkage:

| Property | Type | Notes |
|----------|------|-------|
| `_id` | identifier | |
| `name` | **word** | Searchable; unique index in Customer.yaml |
| `description` | sentence | |
| `status` | enum (`default_status`) | Include `active` and `archived` |
| `created`, `saved` | breadcrumb | |
| `mentees` | array of identifier | Mentee `_id` values this customer sponsors |

Use dictionary formatting consistent with other 0.1.0 dictionaries (`_locked`, `additional_properties: false`, property `description`/`name`/`required` ordering).

### Step 2 — Update Profile.0.1.0.yaml

**Add** after `saved`:

```yaml
- description: the customer this profile is associated with
  name: customer_id
  required: false
  type: identifier
```

Do **not** remove existing Profile fields. `Profile.yaml` stays at **0.1.0.0**.

### Step 3 — Verify configurations unchanged

- `Customer.yaml` — version 0.1.0.0, test data file `Customer.0.1.0.0.json`, unique index on `name`.
- `Profile.yaml` — version 0.1.0.0, test data file `Profile.0.1.0.0.json`.

No configuration version bumps required for this task.

## Requirements

1. **Schema conformance** — dictionaries validate against existing type files in `../configurator/types/`.
2. **No version bumps** — do not add Customer 0.2.0, Profile 0.2.0, or migration files.
3. **Out of scope for this task** — test data edits (T124, T125), Dashboard/Subscription collections, ERD/catalog updates.

## Testing expectations

With **existing** test data (empty Customer array is acceptable for schema-only pass):

```bash
make container
make process
```

Expect top-level **SUCCESS**. Local configurator API port is **8385**.

## Dependencies / Ordering

- Requires **T106** (Mentee collection and Profile schema) to be shipped.
- **Blocks** T124 and T125.

## Change control checklist

- [ ] Reviewed all **Context / Input files**
- [ ] Updated Customer.0.1.0.yaml (`mentees` array; `name` as `word`)
- [ ] Updated Profile.0.1.0.yaml (`customer_id` added)
- [ ] `make container` and `make process` succeeded
- [ ] Created a scoped commit referencing T123 / F-D13

## Implementation notes (to be updated by the agent)

**Summary of changes**

**Approach**

**Testing results**
