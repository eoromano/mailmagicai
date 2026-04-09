# Local Setup

## Frontend

```bash
cd apps/outlook-addin
cp .env.example .env.local
npm install
npm run dev
```

## API

```bash
cd services/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Environment Templates

- `apps/outlook-addin/.env.example`
- `services/api/.env.example`

Both apps are intentionally configured for local-only mock development.
