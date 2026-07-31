# T227 – Add Product catalog collection (F-D22)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T225  
**Description:** Create **Product** Configuration, Dictionary, and empty/minimal test data for the E2 plan catalog (Admin SPA CRUD; Customer SPA reads via API later). Prefer create over rename. Locked business fields + `stripe_price_id`.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/configurations/`, `configurator/dictionaries/`, `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — Product locked shape + `stripe_price_id`
- GitHub: [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- `configurator/api_config/templates/default_new_dictionary.yaml` / `default_new_configuration.yaml` — starters
- **External:** Product catalog CRUD UI is Admin SPA (**F-AS01** ProductsListPage / F-US09) — see `Tasks/ISSUE.mentorhub_admin_spa.products_catalog_crud.md`; not Customer SPA
- **Out of scope:** Discount / Payment / Customer subscription seeds (T228–T230); Admin SPA implementation.

### Locked Product fields (+ standard dictionary metadata)

| Field | Role |
| --- | --- |
| Standard | `_id`, `name`, `description`, `created`, `saved`, `status` (`default_status` unless a product-specific enum is required) |
| `minimum_members` | Floor for cart `quantity` |
| `subscription` | Plan identifier (key/name for the offering) |
| `unit_price` | Display / checkout unit price |
| `stripe_price_id` | Stripe Checkout `line_items[].price` |

Indexes: unique on `subscription` and/or `stripe_price_id` as appropriate; document in Execution Notes.  
**Stable `_id` prefix for seeds (T230):** e.g. `P0…` — record chosen prefix in Execution Notes.

## Goals

- Create `configurator/dictionaries/Product.0.1.0.yaml`.
- Create `configurator/configurations/Product.yaml` version `0.1.0.0`.
- Create `configurator/test_data/Product.0.1.0.0.json` as `[]` until T230 (or minimal placeholders if configure requires).
- Prefer **create** (not rename of unrelated collections). Confirm configure **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Configurations list includes `Product.yaml`.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Product.0.1.0.yaml` — **create**
- `configurator/configurations/Product.yaml` — **create**
- `configurator/test_data/Product.0.1.0.0.json` — **create** (`[]` acceptable)
- `Tasks/PENDING.T227.add_product_collection.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
