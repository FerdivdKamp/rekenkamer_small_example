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

## Frontend

Start the backend on port 8000, then run from `frontend`:

```sh
npm install
npm run dev
```

Open the URL printed by Vite (normally `http://localhost:5173`). Enter a name to call `GET /v1/begroetingen/{naam}`. The development server proxies `/v1` to the backend. For a production build, run `npm run build` and serve `frontend/dist` from the same origin as the API, or proxy `/v1` to the backend.


## GibHub Actions

Linter
OpenAPI stadnard validation
