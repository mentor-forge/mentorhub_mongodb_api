# Mentor Hub MongoDB configurator API

This repo contains the MongoDB database configurations for the Mentor Hub system. You can use the following commands to test, edit, and package these configurations. Note that the configuration files are just yaml files in the configurator folder - after you have made and tested changes you still need to commit your changes to a branch, and merge a PR to make them available to the other developers.

## Pre-release

This project is in **pre-release**. Dictionary and configuration work stays on the existing **0.1.0** versions:

- Edit `configurator/dictionaries/*.0.1.0.yaml`, matching `configurator/configurations/*.yaml`, and `configurator/test_data/*.0.1.0.0.json` **in place**.
- Do **not** bump dictionary or configuration version numbers.
- Do **not** add configurator migration pipelines or multi-version upgrade paths.

When schema or seed data needs to change, update the current 0.1.0 artifacts and test data together. After GA, version bumps and migrations will follow the release process documented in platform standards.

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
- This repo includes a **Tasks framework** under the `Tasks/` folder; see `Tasks/_PLANNING.md` and `Tasks/_ORCHESTRATE.md` for instructions on planning and orchestrating schema‑compliant test data work.

## Test Personas

Persistent **Developer Edition personas** in seed data support manual SPA testing and JWT claims on [`login.html`](https://github.com/mentor-forge/mentorhub/blob/main/login.html) (synced via `welcome-auth.js` in the `mentorhub` repo — see `Tasks/ISSUE.mentorhub.login_html_persona_alignment.md`).

**Path A self-registration fixtures** (`patha-owner` provisioned / `nora` enriched) are primary-owner Customer + Profile pairs for Cognito Path A. They are **not** Sign-in personas until Developer Edition `login.html` is aligned — see `Tasks/ISSUE.mentorhub.login_html_e3_roster_personas.md`. Northstar is unsubscribed (`subscriptions: []`) for Choose-a-plan + empty mentee roster.

**Path B invite fixtures** (`riley` pending / `quinn` revoked) are org-invite Profiles under Persevere, invited by Stacey. They are **not** Sign-in personas until accepted. Invitation state is `profile_status` only (`provisioned` / `active` / `archived`) — reuse **emma** as the accepted member.

### Customer organizations

| `_id` | Slug | Display name | Sponsored personas |
| --- | --- | --- | --- |
| `D00000000000000000000001` | `mary` | Mary | Mary (self-funded) |
| `D00000000000000000000002` | `persevere` | Persevere Now | Stacey, Emma, Margaret, Daniel, Pat, Riley, Quinn |
| `D00000000000000000000006` | `ali` | Agile Learning Institute | Mike, Marti, Paula, Elon, Melinda, Linda |
| `D00000000000000000000007` | `supersoft` | SuperSoft | Eddy, Danny, Lucky |
| `D00000000000000000000008` | `scamsoft` | ScamSoft | Donny |
| `D00000000000000000000009` | `provisioned-org-path-a` | (provisioned stub) | Path A Owner |
| `D00000000000000000000010` | `northstar` | Northstar Labs | Nora |
| `D00000000000000000000011` | `harbor` | Harbor | Helen |

### Persona matrix

 | Persona | Slug | `display_name` | Profile `_id` | Roles | Customer | Mentor |
| --- | --- | --- | --- | --- | --- | --- |
| Mike the Admin | `mike` | Mike Storey | `A00000000000000000000001` | admin | ALI | — |
| Daniel the Mentee | `daniel` | Daniel Dissler | `A00000000000000000000002` | mentee | Persevere | Paula |
| Lucky the Mentee | `lucky` | Lucky Minyard | `A00000000000000000000003` | mentee | SuperSoft | Danny |
| Mary the Super Mentee | `mary` | Mary Anderson | `A00000000000000000000004` | customer, coordinator, mentee | Mary | Marti |
| Linda the Archived Mentee | `linda` | Linda Left | `A00000000000000000000005` | mentee (archived) | ALI | Marti |
| Marti the Mentor | `marti` | Marti Lombardi | `A00000000000000000000006` | mentor | — | — |
| Emma the Coordinator | `emma` | Emma Coordinator | `A00000000000000000000007` | coordinator | Persevere | — |
| Stacey the CEO | `stacey` | Stacey CEO | `A00000000000000000000008` | customer | Persevere | — |
| Margaret the Coordinator | `margaret` | Margaret Coordinator | `A00000000000000000000009` | coordinator (suspended) | Persevere | — |
| Paula the Persevere Mentor | `paula` | Paula Persevere | `A00000000000000000000010` | mentor | ALI | — |
| Elon the Money Mentor | `elon` | Elon Money | `A00000000000000000000011` | mentor | ALI | — |
| Eddy the Entrepreneur | `eddy` | Eddy Entrepreneur | `A00000000000000000000012` | customer | SuperSoft | — |
| Donny the Deadbeat | `donny` | Donny Deadbeat | `A00000000000000000000013` | customer | ScamSoft | — |
| Danny the Dev Lead | `danny` | Danny Dev Lead | `A00000000000000000000014` | coordinator, mentor | SuperSoft | — |
| Melinda the Multi Customer Mentor | `melinda` | Melinda Multi | `A00000000000000000000015` | mentor | ALI | — |
| Path A Owner | `patha-owner` | Path A Owner | `A00000000000000000000016` | customer (provisioned) | Path A stub | — |
| Nora the Northstar Owner | `nora` | Nora Northstar | `A00000000000000000000017` | customer | Northstar | — |
| Helen the Harbor Owner | `helen` | Helen Harbor | `A00000000000000000000018` | customer | Harbor | — |
| Pat the Empty-Activity Mentee | `pat` | Pat Persevere | `A00000000000000000000019` | mentee | Persevere | Paula |
| Riley the Pending Invitee | `riley` | Riley Invitee | `A00000000000000000000020` | customer (provisioned) | Persevere | — |
| Quinn the Revoked Invitee | `quinn` | Quinn Revoked | `A00000000000000000000021` | customer (archived) | Persevere | — |

### Mentor–mentee relationships

| Mentee | Primary mentor | Notes |
| --- | --- | --- |
| Daniel | Paula | Persevere-exclusive mentoring |
| Lucky | Danny | SuperSoft coordinator-mentor |
| Mary | Marti | Self-funded apprentice |
| Linda | Marti | Archived; historical sessions only |

| Mentor | Mentees | Notes |
| --- | --- | --- |
| Elon | Daniel, Lucky | Compensated encounters (noted in encounter narrative) |
| Melinda | Persevere + compensated cases | Multi-customer mentor persona |

**Stable ID policy:** Profile and Customer `_id` values are fixtures. Changing them requires updating Journey, Encounter, Event, Note, Rating seed data and `welcome-auth.js` in the `mentorhub` repo.

## Configure Database (non-interactive)

- **make process** calls the same API endpoint as the SPA **Configure Database** button (`POST /api/configurations/`) against the locally running API container (port `8385`).  
- The resulting event JSON is written to `artifacts/process_all_configurations.json` and validated with `jq` to ensure the top-level status is `"SUCCESS"`.  
- If the command fails, inspect that JSON file for detailed error information about configuration or test‑data import issues.

## Testing 
- When working on a feature you can use the `make dev` to start the [WebUI](http://localhost:8386)
- To test your changes in the WebUI, from the Admin page, click "Drop Database" and then return to the Admin page and click "Configure Database". It should return all green checks.
- To test your changes from the cli you can use the ``make process`` command to drop and configure the database. 
- When you are finished working with the tool, don't forget to `make down` to shut down the containers and free the ports. 

