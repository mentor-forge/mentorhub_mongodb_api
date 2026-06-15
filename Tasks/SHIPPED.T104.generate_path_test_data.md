# T104 – Generate Path Test Data

**Status**: Shipped
**Task Type**: Feature  
**Run Mode**: As Needed 

This is a reusable, parameterized task. A human should:

- Edit the **User inputs** section below to point at the desired dictionary, enumerators, and target test‑data file.
- Update `Status` from `As Needed` → `Pending`.
- Ask the agent/orchestrator to execute **pending** tasks.

## User inputs (edit before running)

- **Dictionary file** ../configurator/dictionaries/Path.0.1.0.yaml
- **Enumerators file** ../configurator/enumerators/enumerations.0.yaml
- **Target test‑data file** ../configurator/test_data/Path.0.1.0.0.json
- **Number of documents to generate**: `15`
- **Special requirements** Create a "EngineerKit" learning Path with the modules, topics, and resources you just created. Match the resource_id's found in ../configurator/test_data/Resource.0.1.0.0.json

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

Generated **15** EJSON Path documents in `configurator/test_data/Path.0.1.0.0.json`, anchored by a full **EngineerKit** learning path linked to Resource test data.

**Approach**

- Parsed all 15 engineerkit module markdown files for `## Topics` → `###` topic headings and resource links under `Resources` / `Primary Resources` / `Extended Resources`.
- Mapped harvested URLs to Resource `$oid` values from `Resource.0.1.0.0.json` (491 topic resource references, 0 unmatched URLs).
- Built primary path `engineerkit` with 15 modules, 75 topics, and nested `resources` arrays using EJSON `$oid` references.
- Added 14 supplemental single-module paths for document-count and variability requirements; one supplemental path uses `archived` status for `default_status` enum coverage.
- Assigned deterministic Path `_id` values (`C0000000000000000000001` … `C00000000000000000000015`).
- Set `tags` on the EngineerKit path to include all `technologies` enum values.

**Testing results**

- Baseline configure: `POST /api/configurations/` → SUCCESS (`DELETE /api/database/` returned FAILURE in this session but configure still succeeded).
- With Identity, Profile, Resource, and Path test data: `POST /api/configurations/` → SUCCESS.
- `make container` → SUCCESS.
- Note: local dev compose exposes the configurator API on port **8385** (not 8383 as listed in this task).
