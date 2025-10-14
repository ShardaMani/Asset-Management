# Asset Management (IIT Madras) — README

<<<<<<< HEAD
This repository contains a Django backend and a React frontend (Create React App) for the Asset Management used in the UI prototype. The frontend includes a Leaflet map (`react-leaflet`) that fetches asset instances from the backend and plots them on a map. The repo layout (important folders):
=======
This repository contains a Django backend and a React frontend (Create React App) for the Asset Management POC used in the UI prototype. The frontend includes a Leaflet map (`react-leaflet`) that fetches asset instances from the backend and plots them on a map. The repo layout (important folders):
>>>>>>> f842e2e (Prepare backend for Render: env-driven settings, WhiteNoise, requirements and Procfile; update frontend API env usage)

- backend/ — Django project (API with Django REST Framework)
- frontend/dashboard/ — React app (Create React App) using `react-leaflet` and `leaflet`

This README gives quick setup, run, and troubleshooting steps so you can get the app running locally and push code to GitHub.

## Quick start (recommended)

Prerequisites
- Node.js (16+ recommended) and npm
- Python 3.8+ and pip
- Git
- PostgreSQL (if you want to run with the real DB; not required for frontend POC)

High-level steps
1. Backend: create virtualenv, install requirements, configure DB, run migrations, start Django.
2. Frontend: install npm deps, start the CRA dev server.

## Backend (Django)
Path: `backend/`

1. Create and activate virtualenv (example):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure `backend/settings.py` database and allowed hosts (if needed). The app expects API endpoints such as `/api/instances/map/`.

3. Run migrations and start the server:

```powershell
python manage.py migrate
python manage.py runserver 8000
```

4. Confirm the endpoint is reachable in your browser:

- http://localhost:8000/api/instances/map/ should return JSON (array of asset instances).

## Frontend (React + Leaflet)
Path: `frontend/dashboard/`

1. Install dependencies and start the dev server:

```powershell
cd frontend\dashboard
npm install
npm start
```

2. The CRA dev server will proxy API requests to the backend if `proxy` is set in `package.json` (this repo sets `proxy: "http://localhost:8000"`). If your backend runs on a different host/port, either update the `proxy` value or change the fetch URL inside `src/components/AssetMap.js`.

3. Open http://localhost:3000 in your browser.

## Map troubleshooting (common issues)
- Blank map tiles
  - Confirm `leaflet/dist/leaflet.css` is imported (this repo imports it in `src/index.js`).
  - Check browser Network tab for tile requests (https://a.tile.openstreetmap.org/...) and verify status 200.

- Markers not visible
  - Confirm `/api/instances/map/` returns an array of asset objects. Use the Network tab or visit the endpoint directly.
  - Check browser console for errors printed by the frontend (the app logs fetch progress and errors in `src/components/AssetMap.js`).
  - The `AssetMap` component includes a fix for Leaflet default icon paths; keep the `require('leaflet/dist/images/...')` lines intact.

- Stacked markers (many assets at same building coordinate)
  - The frontend uses a compact grid packing strategy to spread assets when explicit lat/lon aren't available; tweak `halfSide` or the packing computation in `getCoordsForAsset` inside `src/components/AssetMap.js` to change clustering tightness.

## Git / GitHub
- To add the remote and push (PowerShell examples):

```powershell
cd C:\Users\Admin\Desktop\Sharda\POC
# add remote (HTTPS)
git remote add origin https://github.com/ShardaMani/Asset-Management.git
# ensure main branch
git branch -M main
# commit and push
git add -A
git commit -m "Initial commit: frontend and backend POC"
# When prompted for password, use a GitHub Personal Access Token (PAT)
git push -u origin main
```

- If you prefer SSH (recommended for frequent use), generate an SSH key and add to your GitHub account, then set remote to `git@github.com:ShardaMani/Asset-Management.git`.

## Where to look in the code
- Frontend map: `frontend/dashboard/src/components/AssetMap.js`
- Hero banner: `frontend/dashboard/src/components/HeroBanner.js`
- Frontend entry: `frontend/dashboard/src/index.js`
- Backend API: `backend/assets/views.py` and `backend/assets/serializers.py`

## Useful debug commands
- Show remotes:
```powershell
git remote -v
```
- Show uncommitted changes:
```powershell
git status --porcelain
```
- Show recent commits:
```powershell
git log --oneline -n 10
```

## Next improvements (suggested)
- Add a backend endpoint that returns aggregated counts (assets, buildings, rooms) so the frontend doesn't need to fetch the entire `instances` list.
- Add marker clustering (e.g., react-leaflet-markercluster) for large datasets.
- Allow selecting the `SELECT_ASSET_ID` via UI or URL parameter instead of hard-coding.

---
<<<<<<< HEAD
If you want, I can paste a slightly shorter README suitable for GitHub's first look, or include contributor / license sections. Which format would you like (detailed like above or short)?
=======
If you want, I can paste a slightly shorter README suitable for GitHub's first look, or include contributor / license sections. Which format would you like (detailed like above or short)?
>>>>>>> f842e2e (Prepare backend for Render: env-driven settings, WhiteNoise, requirements and Procfile; update frontend API env usage)
