#!/bin/sh
set -eu

cd "$(dirname "$0")/../services/api"

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
fi

printf "API setup complete.\n"
