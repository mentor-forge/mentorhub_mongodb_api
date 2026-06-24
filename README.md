# Mentor Hub MongoDB configurator API

This repo contains the MongoDB database configurations for the Mentor Hub system. You can use the following commands to test, edit, and package these configurations. Note that the configuration files are just yaml files in the configurator folder - after you have made and tested changes you still need to commit your changes to a branch, and merge a PR to make them available to the other developers. 

## Prerequisites

- Mentor Hub [Developers Edition](https://github.com/mentor-forge/mentorhub/blob/main/CONTRIBUTING.md)

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
```

## Test Data

- Test data is just json files in the [test_data](./configurator/test_data/) folder.
- This repo includes a **Tasks framework** under the `Tasks/` folder; see `Tasks/README.md` for instructions on how to discover and run tasks, and use agents to generate schema‑compliant test data from dictionaries, enumerators, and type definitions.

## Configure Database (non-interactive)

- **make process** calls the same API endpoint as the SPA **Configure Database** button (`POST /api/configurations/`) against the locally running API container (port `8385`).  
- The resulting event JSON is written to `artifacts/process_all_configurations.json` and validated with `jq` to ensure the top-level status is `"SUCCESS"`.  
- If the command fails, inspect that JSON file for detailed error information about configuration or test‑data import issues.

## Testing 
- When working on a feature you can use the `make dev` to start the [WebUI](http://localhost:8386)
- To test your changes in the WebUI, from the Admin page, click "Drop Database" and then return to the Admin page and click "Configure Database". It should return all green checks.
- To test your changes from the cli you can use the ``make process`` command to drop and configure the database. 
- When you are finished working with the tool, don't forget to `make down` to shut down the containers and free the ports. 

