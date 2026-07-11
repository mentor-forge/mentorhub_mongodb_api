# T127 – F-D18 Remove Identity Collection

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (F-D18 pipeline)  
**Issue**: F-D18 (#40)  
**Branch**: `F-d18/profile-token-updates`

## Goal

Remove the **Identity** dictionary and related configuration/test-data files as roles move onto **Profile**.

## Requirements

- Delete `configurator/dictionaries/Identity.0.1.0.yaml`
- Delete `configurator/configurations/Identity.yaml`
- Delete `configurator/test_data/Identity.0.1.0.0.json`
- Update `Profile.0.1.0.yaml` description to remove Identity reference

## Testing expectations

- `make process` succeeds without Identity collection

## Dependencies / Ordering

- Blocks T128–T130
