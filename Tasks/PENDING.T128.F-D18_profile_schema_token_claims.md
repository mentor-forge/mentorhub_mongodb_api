# T128 – F-D18 Profile Schema Token Claim Fields

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (F-D18 pipeline)  
**Issue**: F-D18 (#40)  
**Branch**: `F-d18/profile-token-updates`

## Goal

Extend **Profile** schema for JWT token claims: `roles` and `full_name` index.

## Requirements

- Add `roles` as `enum_array` of `user_roles` to `Profile.0.1.0.yaml`
- Change `Profile.yaml` unique index from `name` to `full_name`

## Testing expectations

- `make process` succeeds

## Dependencies / Ordering

- Requires T127
