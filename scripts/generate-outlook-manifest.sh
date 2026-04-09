#!/bin/sh
set -eu

if [ "${1:-}" = "" ]; then
  printf "Usage: ./scripts/generate-outlook-manifest.sh https://your-https-url\n" >&2
  exit 1
fi

BASE_URL="${1%/}"

case "$BASE_URL" in
  https://*)
    ;;
  *)
    printf "Manifest generation requires an HTTPS base URL for Outlook on the web.\n" >&2
    exit 1
    ;;
esac

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)

ORIGIN=$(printf "%s" "$BASE_URL" | sed -E 's#(https://[^/]+).*#\1#')
TEMPLATE_PATH="$REPO_ROOT/apps/outlook-addin/manifest/threadsense.template.xml"
OUTPUT_DIR="$REPO_ROOT/apps/outlook-addin/manifest/dist"
OUTPUT_PATH="$OUTPUT_DIR/threadsense-manifest.xml"

mkdir -p "$OUTPUT_DIR"

sed \
  -e "s#__BASE_URL__#$BASE_URL#g" \
  -e "s#__ORIGIN__#$ORIGIN#g" \
  "$TEMPLATE_PATH" > "$OUTPUT_PATH"

printf "Generated Outlook manifest:\n%s\n" "$OUTPUT_PATH"
