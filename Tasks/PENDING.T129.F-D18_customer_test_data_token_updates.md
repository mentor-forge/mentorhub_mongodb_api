# T129 – F-D18 Customer Test Data for Token Claims

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (F-D18 pipeline)  
**Issue**: F-D18 (#40)  
**Branch**: `F-d18/profile-token-updates`

## Goal

Update **Customer** test data for sponsoring organizations used in JWT `customer_id` claims.

## Requirements

- Rename `morgan` customer to `persevere-now` with description about justice-involved graduates
- Add `agile-learning-institute` customer at `D00000000000000000000006`
- Keep mentee arrays aligned with Persevere Now (daniel, lucky, mary, luther)

## Testing expectations

- `make process` succeeds

## Dependencies / Ordering

- Requires T128
