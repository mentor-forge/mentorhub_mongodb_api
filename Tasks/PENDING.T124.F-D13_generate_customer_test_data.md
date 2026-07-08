# T124 – F-D13 Generate Customer Test Data

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (F-D13 pipeline)  
**Issue**: F-D13  
**Branch**: `F-d13/customer`

Generate EJSON test data for the **Customer** collection, linking sponsoring customers to existing **Mentee** documents.

## User inputs (edit before running)

- **Dictionary file**: `../configurator/dictionaries/Customer.0.1.0.yaml`
- **Enumerators file**: `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file**: `../configurator/test_data/Customer.0.1.0.0.json`
- **Number of documents to generate**: `5`
- **Customer `_id` prefix**: `DD000000000000000000000` (avoid collision with Journey `D000…` IDs in `Journey.0.1.0.0.json`)

## Goal

Populate `Customer.0.1.0.0.json` with realistic sponsoring-customer records that reference existing Mentee documents and support Customer SPA list/search scenarios.

## Context / Input files

- [Tasks/README.md](./README.md)
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- [Customer workshop](../../mentorhub/Workshops/customer_workshop.md)
- [SHIPPED.T101.generate_identity_test_data.md](./SHIPPED.T101.generate_identity_test_data.md) — `cat` and `morgan` customer identities
- [SHIPPED.T106.mentee_collection_and_profile_schema.md](./SHIPPED.T106.mentee_collection_and_profile_schema.md) — Mentee `_id` conventions
- `../configurator/test_data/Identity.0.1.0.0.json`
- `../configurator/test_data/Profile.0.1.0.0.json`
- `../configurator/test_data/Mentee.0.1.0.0.json`
- `../configurator/types/`
- [PENDING.T123.F-D13_customer_profile_schema.md](./PENDING.T123.F-D13_customer_profile_schema.md)

## Requirements

### 1. EJSON encoding

- Every `_id` and `mentees[]` entry: `{ "$oid": "<24-byte hex>" }`
- Breadcrumb `at_time`: `{ "$date": "<ISO-8601>" }`

### 2. Document set (5 records)

| # | `name` | Status | Persona / purpose | `mentees` (Mentee `_id`) | Mentee profile |
|---|--------|--------|-------------------|--------------------------|----------------|
| 1 | `cat` | active | Cat the Customer — family sponsorship | `CC0000000000000000000005` | riley |
| 2 | `morgan` | active | Morgan Customer — small business team | `CC…001`, `CC…002`, `CC…003` | daniel, lucky, mary |
| 3 | `greenfield-dev` | active | Synthetic enterprise sponsor | `CC0000000000000000000004` | luther |
| 4 | `acme-startup` | active | Synthetic startup sponsor | `CC0000000000000000000006` | taylor |
| 5 | `legacy-corp` | archived | Completed pilot (enum coverage) | `CC0000000000000000000007` | casey |

Deterministic Customer `_id` values:

- `DD0000000000000000000001` → `cat`
- `DD0000000000000000000002` → `morgan`
- `DD0000000000000000000003` → `greenfield-dev`
- `DD0000000000000000000004` → `acme-startup`
- `DD0000000000000000000005` → `legacy-corp`

### 3. Field rules

- `name` matches Identity username for personas (`cat`, `morgan`); synthetic customers use kebab-case names.
- `description` — realistic sentence aligned with workshop themes (ROI, team sponsorship, family learning).
- `status` — both `active` and `archived` must appear (via `legacy-corp`).
- `created` / `saved` breadcrumbs — align timestamps with matching Identity/Profile records where personas exist; use varied IPs and correlation IDs (`seed-customer-00N`, `save-customer-00N`).

### 4. Enum coverage

- Every `default_status` value (`active`, `archived`) appears at least once.

## Testing expectations

```bash
make container
make process
```

Expect **SUCCESS**. MongoDB spot check:

```javascript
db.Customer.countDocuments({})  // 5
db.Customer.countDocuments({ status: "archived" })  // 1
```

## Dependencies / Ordering

- **Requires T123** — Customer dictionary includes `mentees` array.
- **Requires** existing Mentee test data (T106).
- **Blocks T125**.

## Change control checklist

- [ ] Reviewed all **Context / Input files**
- [ ] Generated 5 EJSON Customer documents in `Customer.0.1.0.0.json`
- [ ] Used `DD000…` prefix (no Journey `_id` collision)
- [ ] `make container` and `make process` succeeded
- [ ] Created a scoped commit referencing T124 / F-D13

## Implementation notes (to be updated by the agent)

**Summary of changes**

**Approach**

**Testing results**
