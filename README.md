# Netsuite Interview Secret Vault

This project contains a very very very secure secret vault, which is currently in use in production.
This vault can be used to generate, persist and retrieve secrets.
Interaction with the vault is only possible via the `/secret` endpoint.

## Before You Begin

- Tasks are of varying difficulty, and completing all of them is ideal, but not required.
- Don't be afraid to start working on a tasks and abandon it when you are stuck.
This can be further discussed on the followup interview.
- Treat this as if you were contributing to an active project.

## Setting Up

For the project, you will need git, docker and poetry.

You have received an archive. Set up this project as a git repository and use is as such.

## Tasks:

- We need to add support for the following secrets:
   - Passwords - user should be able to specify length, and group of symbols
   - GPG key - no need to validate sensible combinations of arguments
- Check out if anything can be done to reduce the docker image size, even if by a little.
Implement these changes.
- Check if there are any security issues with the way we generate the secrets.
Make a list and suggest some remediation, so that we can construct a backlog.

## How to submit:

Bundle your git repository as an archive, with your name included.
This will be your submission. You may consider this the contents of your merge request.
```
git bundle create nsi_secret_vault_${CANDIDATE_NAME}.bundle --all
```
