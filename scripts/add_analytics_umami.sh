#!/bin/bash

WORK_DIR="$(pwd)"
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"


if [ -z "$UMAMI_TRACE_ID" ] || [ -z "$UMAMI_TRACE_URL" ]; then
    echo "Missing required environment variables. Exiting..."
    exit
fi

if grep -q 'umami' "$WORK_DIR/docusaurus.config.js"; then
  echo "umami analytics is found. Exiting."
  exit
fi

cp "$SCRIPT_DIR/umami-analytics.template.js" "$SCRIPT_DIR/umami-analytics.js"
sed -i 's/UMAMI_TRACE_ID/'"$UMAMI_TRACE_ID"'/' "$SCRIPT_DIR/umami-analytics.js"
sed -i 's#UMAMI_TRACE_URL#'"$UMAMI_TRACE_URL"'#' "$SCRIPT_DIR/umami-analytics.js"

sed -i "s/plugins: \[/plugins: \[require('.\/scripts\/umami-analytics'), /" "$WORK_DIR/docusaurus.config.js"
echo "done."