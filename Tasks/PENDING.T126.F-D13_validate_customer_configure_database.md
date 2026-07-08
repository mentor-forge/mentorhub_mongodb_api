# T126 – F-D13 Validate Customer Configure Database

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (F-D13 pipeline)  
**Issue**: F-D13  
**Branch**: `F-d13/customer`

Final validation gate for F-D13: confirm schema changes and test data load cleanly via the Configure Database pipeline and pass MongoDB integrity checks.

## User inputs (edit before running)

- **Branch name**: `F-d13/customer`
- **Configurator API port**: `8385`
- **Database name**: `mentor_hub`

## Goal

Verify the full F-D13 Customer data layer is production-ready for local Developer Edition use:

1. Container builds successfully.
2. Configure Database returns **SUCCESS**.
3. Customer, Profile, and Mentee relationship data is consistent in MongoDB.

## Context / Input files

- [Tasks/README.md](./README.md)
- [README.md](../README.md) — `make container`, `make process`
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- [PENDING.T123.F-D13_customer_profile_schema.md](./PENDING.T123.F-D13_customer_profile_schema.md)
- [PENDING.T124.F-D13_generate_customer_test_data.md](./PENDING.T124.F-D13_generate_customer_test_data.md)
- [PENDING.T125.F-D13_profile_customer_id_test_data.md](./PENDING.T125.F-D13_profile_customer_id_test_data.md)
- `artifacts/process_all_configurations.json` (output from `make process`)

## Validation checklist

### 1. Packaging

```bash
make container
```

Must complete without error.

### 2. Configure Database

```bash
make process
```

Must return HTTP 200 and top-level **SUCCESS** in `artifacts/process_all_configurations.json`.

### 3. MongoDB counts

```javascript
db.Customer.countDocuments({})                              // 5
db.Customer.countDocuments({ status: "active" })            // 4
db.Customer.countDocuments({ status: "archived" })          // 1
db.Profile.countDocuments({ customer_id: { $exists: true } })  // 7
```

### 4. Named persona spot checks

| Query | Expected |
|-------|----------|
| `db.Customer.findOne({ name: "cat" })` | 1 mentee (`CC…005` / riley) |
| `db.Customer.findOne({ name: "morgan" })` | 3 mentees (daniel, lucky, mary) |
| `db.Profile.findOne({ name: "riley" }).customer_id` | equals cat's Customer `_id` |
| `db.Profile.findOne({ name: "cat" }).customer_id` | field absent or null |

### 5. Bidirectional integrity (0 errors)

Run the cross-check from T125:

```javascript
let errors = 0;
db.Customer.find().forEach(c => {
  (c.mentees || []).forEach(mid => {
    const mentee = db.Mentee.findOne({ _id: mid });
    if (!mentee) { errors++; return; }
    const profile = db.Profile.findOne({ _id: mentee.profile_id });
    if (!profile?.customer_id?.equals(c._id)) errors++;
  });
});
print("cross-check errors:", errors);  // 0
```

### 6. No `_id` collisions

Confirm Customer `_id` values (`DD000…`) do not collide with Journey `_id` values (`D000…`) in `db.Journey`.

## Requirements

- If any check fails, stop and report the failing step; do not mark F-D13 complete.
- Do not modify Dashboard or Subscription test data in this task (out of scope for F-D13).
- Document all test command output in **Implementation notes**.

## Dependencies / Ordering

- **Requires T123, T124, and T125** to be complete.
- Final task in the F-D13 pipeline.

## Change control checklist

- [ ] `make container` succeeded
- [ ] `make process` returned SUCCESS
- [ ] All MongoDB spot checks passed
- [ ] Cross-check errors: 0
- [ ] No Customer/Journey `_id` collisions
- [ ] Created a scoped commit referencing T126 / F-D13 (or confirmed prior commits cover the branch)

## Implementation notes (to be updated by the agent)

**Summary of changes**

**Approach**

**Testing results**
