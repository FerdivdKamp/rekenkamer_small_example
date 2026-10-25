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

### Run both services with Docker Compose

From the repository root, run `docker compose up`. On startup, Compose installs dependencies from `backend/poetry.lock` and `frontend/package-lock.json`. Open `http://localhost:5173` for the frontend and `http://localhost:8000/v1/docs` for the API documentation. Source changes reload both services. Run `docker compose down` to stop them.

This Compose setup uses the standard Python and Node images for local development.

### Published images

The production Dockerfiles are in `backend/` and `frontend/`. The frontend image serves the built React app through Nginx and proxies `/v1/` to the backend service. To build and run the images locally, run:

```sh
docker compose -f compose.prod.yaml up --build
```

Open `http://localhost:8080`. To use the published images, run `docker compose -f compose.prod.yaml pull` and then `docker compose -f compose.prod.yaml up`. Set `IMAGE_TAG` to select a release tag instead of `latest`.

The [image publishing workflow](.github/workflows/publish-images.yml) builds both images on pull requests and publishes them to GitHub Container Registry on pushes to `master`, version tags (`v*`), or manual runs. The workflow uses the repository's `GITHUB_TOKEN` with package write permission. It publishes `latest` from `master`, a version tag without its leading `v`, and a short commit SHA tag. The package visibility can be set in GitHub Packages after its first publication.

Start the backend on port 8000, then run from `frontend`:

```sh
npm install
npm run dev
```

Open the URL printed by Vite (normally `http://localhost:5173`). Enter a name to call `GET /v1/begroetingen/{naam}`. The development server proxies `/v1` to the backend. For a production build, run `npm run build` and serve `frontend/dist` from the same origin as the API, or proxy `/v1` to the backend.


## GibHub Actions

Linter
OpenAPI stadnard validation
