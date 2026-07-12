# T206 – Fix Journey now.resource_id Schema

**Status**: Shipped  
**Type**: Feature  
**Depends On**: none  
**Description**: Change `now[].resource_id` from `word` to `identifier` so Journey schema requires valid Resource `$oid` values.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/dictionaries/Journey.0.1.0.yaml` — `library[].resource_id` is `identifier`; `now[].resource_id` is incorrectly `word`
- GitHub issue **#45** (F-D19: resource_id test data)

## Goals

- Update `now[].resource_id` property type from `word` to `identifier` in `Journey.0.1.0.yaml`.
- Pre-release: edit **0.1.0** dictionary in place; no version bump.

## Testing Expectations

```sh
make container
```

- Build succeeds.
- Configure-database may **fail** until T207 migrates Journey test data (`now.resource_id` still uses Resource names). Confirm failures are test-data related.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Journey.0.1.0.yaml`

## Execution Notes

- Updated `now[].resource_id` type to `identifier` in `Journey.0.1.0.yaml`.
- `POST /api/configurations/` succeeded after T207 migrated Journey test data.
