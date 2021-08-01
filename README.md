## Introduction

This project fetches the latest forex prices from the alphavantage API every hour and saves them to the database. 
Once saved the user can fetch the latest quote via the provided API endpoint or trigger a refresh before the hour is up

## Postman Collection

You can try out various API calls via Postman (or Insomnia) using [this link](https://www.getpostman.com/collections/85efa8a64f4cc52d70dd)

## Recommended Requirements

- docker and docker compose if using the docker approach for local development (recommended)
- The environment variables `API_KEY` and `ALPHAVANTAGE_API_KEY` setup in the project's environment

## Quickstart (With Docker)

Ensure you have docker and docker compose installed.  Once both are available, you can start the project with

```bash
docker-compose up
```

## Endpoints

| HTTP Verb  | Endpoint  |  Usage |
|---|---|---|
| POST | http://localhost:8000/api/v1/quotes | trigger a refresh of the BTC/USD price (still via celery for responsiveness)  |
| GET  | http://localhost:8000/api/v1/quotes  | fetch the latest BTC/USD quote based on the date created for the available quotes |

## Shell

To open an interactive shell, run the following command

```bash
docker-compose run web python manage.py shell
```

## Migrations

Django's migration mechanisms are used for managing changes to the tables to make DB changes easy.

To generate a migration from changes you've made locally, run the following commands:

```bash
docker-compose run web python manage.py makemigrations
```

Then you can apply the migration to the database:

```bash
docker-compose run web python manage.py migrate
```

Then each time the database models change repeat the `makemigrations` and `migrate` commands.

To sync the database in another system just pull the latest changes and run the `migrate` command (this is always done automatically when Docker is starting up).

## Git Hooks

To make githooks easy enough to manage, we're making use of the [pre-commit](https://pre-commit.com/) project.

To configure the githooks, just run `pre-commit install` and thereafter pre-commit will run on every commit.

Refer to [this guide](https://pre-commit.com/#2-add-a-pre-commit-configuration) for configuration options should you want to tweak it

## API Authentication

The API expects each incoming request to have a valid API key as configured in the application settings.  This API should be added as the environment variable `API_KEY'
