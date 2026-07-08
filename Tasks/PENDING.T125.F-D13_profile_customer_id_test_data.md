# T125 – F-D13 Profile customer_id Test Data

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (F-D13 pipeline)  
**Issue**: F-D13  
**Branch**: `F-d13/customer`

Add **`customer_id`** back-references to sponsored mentee profiles in `Profile.0.1.0.0.json`, completing the Customer ↔ Mentee ↔ Profile relationship graph.

## User inputs (edit before running)

- **Profile dictionary**: `../configurator/dictionaries/Profile.0.1.0.yaml`
- **Profile test data**: `../configurator/test_data/Profile.0.1.0.0.json`
- **Customer test data**: `../configurator/test_data/Customer.0.1.0.0.json`
- **Mentee test data**: `../configurator/test_data/Mentee.0.1.0.0.json`

## Goal

For every Mentee listed in a Customer's `mentees` array, set the corresponding Profile's `customer_id` to that Customer's `_id`. Leave non-sponsored profiles unchanged.

## Context / Input files

- [Tasks/README.md](./README.md)
- [SHIPPED.T102.generate_profile_test_data.md](./SHIPPED.T102.generate_profile_test_data.md) — Profile EJSON conventions
- [SHIPPED.T106.mentee_collection_and_profile_schema.md](./SHIPPED.T106.mentee_collection_and_profile_schema.md) — Mentee `profile_id` linkage
- [PENDING.T124.F-D13_generate_customer_test_data.md](./PENDING.T124.F-D13_generate_customer_test_data.md)
- `../configurator/test_data/Profile.0.1.0.0.json`
- `../configurator/test_data/Customer.0.1.0.0.json`
- `../configurator/test_data/Mentee.0.1.0.0.json`

## Relationship mapping

Resolve each Customer `mentees[]` entry → Mentee document → `profile_id` → Profile document → set `customer_id`.

| Profile `name` | Profile `_id` | `customer_id` | Customer `name` |
|----------------|---------------|---------------|-----------------|
| `riley` | `A00000000000000000000010` | `DD0000000000000000000001` | `cat` |
| `daniel` | `A00000000000000000000002` | `DD0000000000000000000002` | `morgan` |
| `lucky` | `A00000000000000000000003` | `DD0000000000000000000002` | `morgan` |
| `mary` | `A00000000000000000000004` | `DD0000000000000000000002` | `morgan` |
| `luther` | `A00000000000000000000005` | `DD0000000000000000000003` | `greenfield-dev` |
| `taylor` | `A00000000000000000000014` | `DD0000000000000000000004` | `acme-startup` |
| `casey` | `A00000000000000000000015` | `DD0000000000000000000005` | `legacy-corp` |

## Requirements

### 1. Profiles to update (7 only)

Add `customer_id` **only** to the seven mentee profiles listed above.

### 2. Profiles to leave unchanged

Do **not** add `customer_id` to:

- Customer personas: `cat`, `morgan`
- Mentors: `mike`, `marti`, `jordan`
- Coordinators: `carol`, `alex`
- Admin: `sam`, `luther` (luther **is** a sponsored mentee — update luther)
- Any profile not listed in the mapping table

### 3. EJSON encoding

```json
"customer_id": { "$oid": "DD0000000000000000000002" }
```

### 4. Integrity rules

- Every Customer `mentees[]` entry must resolve: Mentee → Profile → matching `customer_id`.
- No Profile `customer_id` may reference a non-existent Customer `_id`.
- Do not modify other Profile fields (`mentor_id`, `full_name`, breadcrumbs, etc.) except adding `customer_id`.

## Testing expectations

```bash
make process
```

MongoDB cross-check script (0 errors expected):

```javascript
let errors = 0;
db.Customer.find().forEach(c => {
  (c.mentees || []).forEach(mid => {
    const mentee = db.Mentee.findOne({ _id: mid });
    if (!mentee) { print("ERROR missing Mentee", mid); errors++; return; }
    const profile = db.Profile.findOne({ _id: mentee.profile_id });
    if (!profile || !profile.customer_id || !profile.customer_id.equals(c._id)) {
      print("ERROR mismatch for Customer", c.name, "Profile", profile?.name);
      errors++;
    }
  });
});
print("cross-check errors:", errors);
db.Profile.countDocuments({ customer_id: { $exists: true } })  // 7
```

## Dependencies / Ordering

- **Requires T124** — Customer test data with `mentees` populated.
- **Requires T123** — Profile dictionary includes `customer_id`.
- **Blocks T126**.

## Change control checklist

- [ ] Reviewed all **Context / Input files**
- [ ] Added `customer_id` to 7 sponsored mentee profiles
- [ ] Cross-check script reports 0 errors
- [ ] `make process` succeeded
- [ ] Created a scoped commit referencing T125 / F-D13

## Implementation notes (to be updated by the agent)

**Summary of changes**

**Approach**

**Testing results**
