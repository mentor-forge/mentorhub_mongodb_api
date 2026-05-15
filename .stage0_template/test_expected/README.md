# Mentor Hub MongoDB configurator API

This repo contains the MongoDB database configurations for the Mentor Hub system. You can use the following commands to test, edit, and package these configurations. Note that the configuration files are just yaml files in the configurator folder - after you have made and tested changes you still need to commit your changes to a branch, and merge a PR to make them available to the other developers. 

## Prerequisites
- Mentor Hub [Developers Edition](https://github.com/agile-learning-institute/mentorhub/blob/main/CONTRIBUTING.md)

## Developer Commands
```sh
## Run the dev runtime to edit the configurations.
make dev

## Build the container for deployment
make container

## Process all configurations via the API (Configure Database)
make process

## Run the packaged configuration. (Read Only configurations)
make deploy

## Open the browser for running containers
make open

## Shut down the containers
make down

## Generate Test Data See below
make test_data COLLECTION VERSION
```

## Test Data
- Test data is just json files in the [test_data](./configurator/test_data/) folder.
- This repo includes a **Tasks framework** under the `Tasks/` folder; see `Tasks/README.md` for how to:
  - Discover and run tasks (including **Run as needed** tasks like `AS_NEEDED.T100.generate_test_data.md`).
  - Use agents to generate schema‑compliant test data from dictionaries, enumerators, and type definitions.

## Configure Database (non-interactive)

- **make process** calls the same API endpoint as the SPA **Configure Database** button (`POST /api/configurations/`) against the locally running API container (port `8385`).  
- The resulting event JSON is written to `artifacts/process_all_configurations.json` and validated with `jq` to ensure the top-level status is `"SUCCESS"`.  
- If the command fails, inspect that JSON file for detailed error information about configuration or test‑data import issues.

## Workflow
- First, create a feature branch for your work
- run ``make dev`` and use the UI to update the configurations
- When you're done making edits:
    - Check that "Drop Database" and then "Configure Database" returns all green.
    - Make sure ``make container`` runs without error.
    - Use ``make deploy`` to review that the changes made it into the container.
    - Use you source-control viewer to review source yaml changes to make sure no un-expected files were updated.
    - Commit and Push your changes on the new branch
    - Open a PR and request a review
    - When the PR is merged to main, ci will publish an updated container for use by the team.
    - After the PR is merged the branch is deleted - ``git checkout main`` and ``git pull``.
    - Don't forget to ``make down`` to shut down the containers and free the ports.