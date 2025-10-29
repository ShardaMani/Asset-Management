# Asset Management (IIT Madras) — README

This repository contains a Django backend and a React frontend (Create React App) for the Asset Management used in the UI prototype. The frontend includes a Leaflet map (`react-leaflet`) that fetches asset instances from the backend and plots them on a map. The repo layout (important folders):

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
