# T100 – Generate Test Data

**Status**: As Needed  
**Task Type**: Feature  
**Run Mode**: As Needed 

This is a reusable, parameterized task. A human should:

- Edit the **User inputs** section below to point at the desired dictionary, enumerators, and target test‑data file.
- Update `Status` from `As Needed` → `Pending`.
- Ask the agent/orchestrator to execute **pending** tasks.

## User inputs (edit before running)

- **Dictionary file** (single‑document schema to generate data for):  
  - Example: `../configurator/dictionaries/CHANGEME.1.0.0.yaml`
- **Enumerators file** (enum definitions used by the dictionary):  
  - Default: `../configurator/enumerators/enumerations.0.yaml`
- **Target test‑data file** (output, JSON array of documents):  
  - Example: `../configurator/test_data/CHANGEME.1.0.0.0.json`
- **Number of documents to generate**: `15`
- **Special requirements** (free‑form notes for the agent/generator):  
  - Example: “Cover every `status` enum value at least once; bias heavily toward `active`.”

## Goal

Given a **dictionary**, its **enumerators**, and the supporting **type files**, generate a set of EJSON documents that conform to the effective schema and write them to the configured test‑data file.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- The **Dictionary** and **Enumerators** linked in the **User inputs** section.
- The [type files](../configurator/types/) that map dictionary field types to JSON Schema fragments.

The agent may also consult:

- Existing test data in `../configurator/test_data/` for style and structure.

## Requirements

For the configured dictionary + enumerators (which together describe a single document type), generate test data into the configured test‑data JSON file. Each document should conform to the inferred schema and obey the following rules:

1. **EJSON encoding** for use with MongoDB  
   - Every `_id` value (identifier type) must be wrapped as `{ "$oid": "<24-byte hex>" }`.  
   - Every `date` value must be wrapped as `{ "$date": "<ISO-8601>" }`.  
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
  - Run `make container` to verify that the MongoDB Configurator API container builds successfully.
  - Run `make process` to call the Configure Database API (`POST /api/configurations/`) and validate the resulting event JSON with `jq`. The command should succeed with a `SUCCESS` status; if it fails, inspect the JSON for test‑data or configuration errors.

## Dependencies / Ordering

- **None** – this task can be run whenever a dictionary + enumerators pair is ready for test‑data generation.

## Change control checklist

- [ ] Reviewed all **Context / Input files**.
- [ ] Captured concrete values in **User inputs (edit before running)**.
- [ ] Designed and documented the solution approach in this file.
- [ ] Implemented code or scripts to generate test data.
- [ ] Ran `make container` and `make process`; both succeeded.
- [ ] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**
