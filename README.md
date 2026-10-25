## Introduction

Simple project that has a pyton openapi rest api (fastapi) and a react + typescript frontend

For the API it follows these design rules: https://developer.overheid.nl/kennisbank/api-ontwikkeling/standaarden/api-design-rules/cheat-sheet


We also need a small CI/CD example 
 
automated testing using github actions
starting for this we'll use docker compose 




## Backend
Updated the hello world example with hello name matching the ADR design rules.

poetry run uvicorn app.main:app --reload


### Pytest

poetry run python -m pytest tests/test_main.py -q -p no:cacheprovider


## GibHub Actions

Linter
OpenAPI stadnard validation
