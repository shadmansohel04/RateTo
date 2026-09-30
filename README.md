# RateTO

RateTO is a Toronto neighborhood exploration app. Enter an address to view a map and location score based on nearby city data, including parks, schools, transit, emergency services, traffic, and crime. The repository contains a React/Vite frontend and a Flask API.

## Repository Layout

| Path | Description |
| --- | --- |
| [`frontend/`](frontend/README-RateTO.md) | React application and map interface |
| [`backend/`](backend/README.md) | Flask API, scoring logic, and city-data files |

See the linked component READMEs for installation, configuration, and run instructions.

## Quick Start

Start the frontend:

```sh
cd frontend
npm ci
npm run dev
```

The frontend currently calls the deployed API at `https://rateto-backend.onrender.com`; running a local backend does not change that target. The backend setup also requires its private `jennifer` package, which is not included in this repository, and PostgreSQL configuration for account/session endpoints. See [`backend/README.md`](backend/README.md) before attempting a local API run.

## Notes

- Frontend production assets are built with `npm run build` and written to `frontend/dist/`.
- Do not commit credentials, database passwords, JWT secrets, or SMTP credentials.
- The backend currently contains an embedded SMTP credential. Rotate it and move mail configuration to environment variables before deploying or publishing the backend.
