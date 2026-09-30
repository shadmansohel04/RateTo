# RateTO Frontend

RateTO's frontend is a React single-page application built with Vite. It lets users enter a Toronto address and explore a map with nearby neighborhood data, including schools, parks, transit, emergency services, traffic, and crime information.

## Requirements

- Node.js 18 or newer
- npm

## Run Locally

From the `frontend/` directory:

```sh
npm ci
npm run dev
```

Vite prints the development URL, usually `http://localhost:5173`.

## Scripts

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the Vite development server |
| `npm run build` | Create a production build in `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint |

## API

The map and contact form currently send requests directly to `https://rateto-backend.onrender.com`. Running the backend locally does not automatically redirect these requests; update the API URLs in the frontend source when developing against a local backend.

## Source Layout

- `src/pages/` contains the page-level views and routes.
- `src/components/` contains the map, address form, header, and contact form.
- `src/styles/` and the component CSS files contain the application styles.
