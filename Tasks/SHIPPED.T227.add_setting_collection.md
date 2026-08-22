# T227 – Add Setting polymorphic collection (Product + Discount variants) (F-D22)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T225  
**Description:** Create a single persisted **Setting** collection for small Admin/reference documents. Use root **`one_of`** with **`type` constant** discriminators (Card-style), but version **`0.1.0.0`** so documents **are** stored in Mongo. MVP variants: **Product** and **Discount**. Do **not** create separate Product or Discount collections (fewer collection names for api_utils). Prefer create over rename. Name is **Setting** (not Configuration) to avoid clashing with configurator Configuration YAML.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/configurations/`, `configurator/dictionaries/`, `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — locked Product + Discount shapes; `stripe_price_id`
- GitHub: [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- Decision: polymorphic **Setting** bag (Product | Discount now; future websocket / non-secret admin knobs may add variants) — fewer collection names than separate Product + Discount
- `configurator/dictionaries/Card.0.0.0.yaml` — `one_of` + `constant` `type` pattern (**Card is non-persisted `0.0.0.0`**; Setting is **persisted `0.1.0.0`**)
- `Tasks/PENDING.T225.add_commerce_enumerators.md` — `discount_status`
- **External:** Admin SPA CRUD filters Setting by `type` — `Tasks/ISSUE.mentorhub_admin_spa.products_catalog_crud.md`
- **Out of scope:** Payment (T229 — stays its own collection); Customer.subscriptions[] (T226); seeds (T230); implementing future websocket variants in this task (document extension point only).

### Locked F-D22 collection names (api_utils)

| Collection | Notes |
| --- | --- |
| **Setting** | Polymorphic bag — variants below |
| **Payment** | Separate transactional collection (T229) |

Do **not** introduce `Product` or `Discount` as Mongo collection names.

### Variants (constant `type`)

**Product** (`type: Product`) — catalog / plan picker:

| Field | Role |
| --- | --- |
| Shared | `_id`, `type` (constant `Product`), `name`, `description`, `created`, `saved`, `status` as appropriate |
| `minimum_members` | Floor for cart `quantity` |
| `subscription` | Plan identifier |
| `unit_price` | Display / checkout unit price |
| `stripe_price_id` | Stripe Checkout `line_items[].price` |

**Discount** (`type: Discount`) — free-encounter codes:

| Field | Role |
| --- | --- |
| Shared | `_id`, `type` (constant `Discount`), `name`/`description` as needed, `created`, `saved` |
| `code` | unique among Discount variants |
| `free_encounters` | integer ≥ 0 |
| `status` | enum `discount_status`: `active` \| `inactive` |
| `expires_at` | optional date-time |
| `max_redemptions` | optional integer |
| Optional | `redemption_count` — document if included |

Indexes (document choices in Execution Notes): e.g. compound unique partial indexes where supported (`type` + `subscription`, `type` + `code`, `type` + `stripe_price_id`), or application-enforced uniqueness if configurator indexes are limited.

**Stable `_id` prefixes for seeds (T230):** e.g. Product `P0…`, Discount `K0…` — record in Execution Notes (valid hex).

## Goals

- Create `configurator/dictionaries/Setting.0.1.0.yaml` with root `one_of` of Product and Discount object variants (`type` constants).
- Create `configurator/configurations/Setting.yaml` version **`0.1.0.0`** (persisted — not `0.0.0.0`).
- Create `configurator/test_data/Setting.0.1.0.0.json` as `[]` until T230.
- Do **not** create Product.yaml / Discount.yaml collections.
- Confirm configure **SUCCESS**; Setting collection exists in Mongo after configure.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Configurations list includes `Setting.yaml`; does **not** list `Product.yaml` or `Discount.yaml`.
- After configure, Mongo has a **Setting** collection (unlike Card).

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Setting.0.1.0.yaml` — **create**
- `configurator/configurations/Setting.yaml` — **create**
- `configurator/test_data/Setting.0.1.0.0.json` — **create** (`[]` acceptable)
- `Tasks/PENDING.T227.add_setting_collection.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Create Card-style root `one_of` Setting dictionary (Product + Discount, constant `type`) at version `0.1.0` with persisted Configuration `0.1.0.0` (not `0.0.0.0`). Empty test_data until T230. Use compound unique **sparse** indexes on `type`+variant key fields (configurator supports `sparse`/`unique`; no `partialFilterExpression`). Verify via existing orchestrator stack on `:8385` only (no docker compose down/up).

**Indexes**

- `Type Subscription` — `{ type: 1, subscription: 1 }` unique + sparse (Product; Discount omitted — missing `subscription`)
- `Type Code` — `{ type: 1, code: 1 }` unique + sparse (Discount; Product omitted — missing `code`)
- `Type Stripe Price Id` — `{ type: 1, stripe_price_id: 1 }` unique + sparse (Product)
- `Created` — `{ created.at_time: -1 }`

Sparse compound uniqueness avoids cross-variant null collisions without partial indexes. Application still owns business rules (e.g. code normalize uppercase).

**Stable `_id` prefixes for T230 seeds** (valid 24-hex ObjectId prefixes):

- Product: `P0…` (e.g. `P00000000000000000000001`)
- Discount: `K0…` (e.g. `K00000000000000000000001`)

**Changes**

- Created `Setting.0.1.0.yaml`: root `one_of` with Product (`type` constant Product; `name`/`description` sentence; `created`/`saved`; `status` `default_status`; `minimum_members` count; `subscription` word; `unit_price` count; `stripe_price_id` sentence) and Discount (`type` constant Discount; `name`/`description` sentence; `created`/`saved`; `code` word; `free_encounters` count; `status` `discount_status`; optional `expires_at`, `max_redemptions`, `redemption_count`). Root description notes future variant extension point.
- Created `Setting.yaml` version `0.1.0.0` with indexes above; `test_data` → `Setting.0.1.0.0.json`.
- Created `Setting.0.1.0.0.json` as `[]` (seeds deferred to T230).
- Did **not** create `Product.yaml` / `Discount.yaml`.

**Testing results**

- Orchestrator stack `:8385`: `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; `CFG-05-Setting.yaml` SUCCESS; `PROCESS_VERSION-0.1.0.0` SUCCESS; indexes `PRO-04-Type Subscription`, `PRO-04-Type Code`, `PRO-04-Type Stripe Price Id`, `PRO-04-Created` present; zero non-SUCCESS events.
- `GET /api/configurations/` lists `Setting.yaml`; does **not** list `Product.yaml` or `Discount.yaml`.
- Packaging (`make container` / `mh up`) skipped — orchestrator owns the live stack; INPUT_FOLDER mount already serves `./configurator`.
