# T130 – F-D18 Profile Test Data Token Updates

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (F-D18 pipeline)  
**Issue**: F-D18 (#40)  
**Branch**: `F-d18/profile-token-updates`

## Goal

Update **Profile** test data with `roles` and `customer_id` for JWT claims.

## Requirements

- Migrate `roles` from former Identity test data onto each Profile
- `mike` and `sam`: all `user_roles` values
- Admin/coordinator profiles: `customer_id` → Agile Learning Institute (`D...006`)
- Mentees daniel, lucky, mary, luther: `customer_id` → Persevere Now (`D...002`)
- Update remaining customer/mentee/coordinator `customer_id` mappings consistently

## Testing expectations

- `make process` succeeds
- MongoDB: no Identity collection; Profiles have `roles` and expected `customer_id`

## Dependencies / Ordering

- Requires T129
