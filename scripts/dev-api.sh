#!/bin/sh
set -eu

cd "$(dirname "$0")/../services/api"

if [ ! -d .venv ]; then
  printf "Missing services/api/.venv. Run npm run setup:api first.\n" >&2
  exit 1
fi

. .venv/bin/activate
uvicorn app.main:app --reload
