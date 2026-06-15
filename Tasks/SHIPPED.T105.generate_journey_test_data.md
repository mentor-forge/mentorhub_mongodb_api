# T105 – Generate Journey Test Data

**Status**: Shipped
**Task Type**: Feature  
**Run Mode**: As Needed 

This is a reusable, parameterized task. A human should:

- Edit the **User inputs** section below to point at the desired dictionary, enumerators, and target test‑data file.
- Update `Status` from `As Needed` → `Pending`.
- Ask the agent/orchestrator to execute **pending** tasks.

## User inputs (edit before running)

- **Dictionary file** ../configurator/dictionaries/Journey.0.1.0.yaml
- **Enumerators file** ../configurator/enumerators/enumerations.0.yaml
- **Target test‑data file** ../configurator/test_data/Journey.0.1.0.0.json`
- **Number of documents to generate**: `4`
- **Special requirements** Create journey documents for Luther, Daniel, Mary, and Lucky. Use the resources in the EngineerKit Learning Path. Place some resources in the library indicating they are complete, place one or two resources in the Now section, and the remaining topics and resources in the Next section.

## Goal

Given a **dictionary**, its **enumerators**, and the supporting **type files**, generate a set of EJSON documents that conform to the effective schema and write them to the configured test‑data file.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- The **Dictionary** and **Enumerators** linked in the **User inputs** section.
- The [type files](../configurator/types/) that map dictionary field types to JSON/BSON Schema fragments.

The agent may also consult:

- Existing test data in `../configurator/test_data/` for style and structure.

## Requirements

For the configured dictionary + enumerators (which together describe a single document type), generate test data into the configured test‑data JSON file. Each document should conform to the inferred schema and obey the following rules:

1. **EJSON encoding** for use with MongoDB  
   - Every `_id` type value (identifier type) must be wrapped as `{ "$oid": "<24-byte hex>" }`.  
   - Every `date-time` value must be wrapped as `{ "$date": "<ISO-8601>" }`.  
   - Reference IDs that are not the primary `_id` but still use the identifier type must also be encoded with `$oid`.

2. **Schema‑driven generation**  
   - Use the dictionary plus its referenced type definitions in `../configurator/types/` to infer:
     - Field names, data types, enum membership, and required vs optional fields.
   - Generate values that are valid for each field type (e.g., strings, numbers, enums, nested objects, arrays) and consistent with any constraints expressed in the simplified schema.

3. **Enum values**  
   - When a property is an enum, assign values at random **but ensure that every listed enum value appears at least once** across the generated documents.  
   - If special instructions mention specific enum values, obey those rules (for example, “use only `active` and `archived`”).

4. **Document count and variability**  
   - Generate exactly the number of documents specified in **User inputs** (default: `15`).  
   - Vary field values so the documents are realistic and cover diverse paths (different enum values, dates, and combinations where appropriate).

5. **Special instructions**  
   - Follow any additional constraints or preferences listed in the **Special requirements** bullet(s) above (for example, distributions, required relationships between fields, or edge cases to include).

## Testing expectations

- **Processing test**
  - Use `curl -X DELETE "http://localhost:8383/api/database/" -H "accept: application/json"` to drop the MongoDB database so it can be re-configured.
  - Use `curl -X POST "http://localhost:8383/api/configurations/" -H "accept: application/json"` to Configure the Database 
  - Validate the configure result passed with a `SUCCESS` status; if it fails, inspect the JSON Error message for details and update the test data accordingly. 

## Dependencies / Ordering

- **Verify** – Before executing this task, first drop the database and configure the database using the curl commands listed above to ensure that we are starting from a clean configuration. If this test fails, stop execution and report an error message.

## Change control checklist

- [x] Reviewed all **Context / Input files**.
- [x] Captured concrete values in **User inputs (edit before running)**.
- [x] Designed and documented the solution approach in this file.
- [x] Implemented code or scripts to generate test data.
- [x] Ran `make container` successfully.
- [x] Ran curl commands to drop and configure database successfully.
- [ ] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Generated **4** EJSON Journey documents in `configurator/test_data/Journey.0.1.0.0.json` for Daniel, Lucky, Mary, and Luther.

**Approach**

- Linked each journey to the corresponding Profile `$oid` (`A000...002`–`005`).
- Used the EngineerKit path (`Path.0.1.0.0.json`, `engineerkit`) as the ordered source of topics and resource references.
- Split each mentee's progress sequentially along the path:
  - **library** — completed resources with `resource_id` `$oid`, `started`, and `completed` timestamps.
  - **now** — 1–2 in-progress resources using Resource `name` values (schema type `word` for `now.resource_id`).
  - **next** — remaining topics with only resources not already in library/now.
- Varied progress depth per mentee (Daniel: 5+2, Lucky: 8+1, Mary: 10+2, Luther: 12+2).
- Assigned deterministic Journey `_id` values (`D0000000000000000000001`–`4`).
- Set Luther's journey to `archived` status for `default_status` enum coverage; others are `active`.

**Testing results**

- Baseline verify: `DELETE /api/database/` → SUCCESS; `POST /api/configurations/` → SUCCESS.
- With full test data (Identity, Profile, Resource, Path, Journey): `DELETE /api/database/` → SUCCESS; `POST /api/configurations/` → SUCCESS.
- `make container` → SUCCESS.
- Note: local dev compose exposes the configurator API on port **8385** (not 8383 as listed in this task).
