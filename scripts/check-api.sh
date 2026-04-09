#!/bin/sh
set -eu

cd "$(dirname "$0")/../services/api"
python3 -m compileall app
