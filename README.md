# Bannerlord matchmaker

Matchmaker api for bannerlord matchmaking

One of the core parts of our bannerlord matchmaking infrastructure. It splits players
into teams using its own (kinda complex) algorighms, chooses player roles, IGLs,
maps, factions and so on

Matchmaker uses dynamic configuration that can be changed in a runtime via an api endpoints

It's a recreation of our old matchmaker that was integrated into the matchmaking discord bot.
Since TaleWorlds have released their custom servers and we are looking into making a 
website, matchmaker functinality had to be segregated into its own service


**Work in progress, the project is not production ready yet**

## Requirements

Requirements to run locally:
1. Python3.10+
1. Poetry

Production requirements:
1. Docker

## Set up locally

Setup process for local testing, api docs checking, development etc.

1. Install dependencies `poetry install --only main` from inside repos' root dir
1. Install dev dependencies if needed `poetry install --with dev`
1. Set all required environment variables. Check `EnvVarNames` enum inside `enums.py` for the list of required variables
1. Activate poetry venv `poetry shell`
1. Run locally via `python main.py` from inside an `app` directory

## Development and testing

Project uses `pytest` for testing. Tests dir is separated from the project's
source to avoid writing painstaking Dockerfile to pull out all the 
unused files in prod

For testing install dev dependencies via `poetry install --with dev`,
then run `pytest` from inside the project's root
Add tests into the `tests` folder. It's structure mirrors the project's source

TODO: set up a CI pipeline

## Tools

There are a bunch tools used in development, some of them have their config specified
in `pyproject.toml`

1. `pyright` as a main lsp and linter
1. `mypy` for static type checking
1. `black` for code formatting
1. `pytest` for testing
1. `poetry` as a package and environment manager
1. `docker` for an image building and deployment
