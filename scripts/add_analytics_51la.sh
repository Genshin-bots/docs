#!/bin/bash

WORK_DIR="$(pwd)"
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"


if [ -z "$LA51_TRACE_ID" ] || [ -z "$LA51_TRACE_CK" ]; then
    echo "Missing required environment variables. Exiting..."
    exit
fi

if grep -q '51la' "$WORK_DIR/docusaurus.config.js"; then
  echo "51la analytics is found. Exiting."
  exit
fi

cp "$SCRIPT_DIR/51la-analytics.template.js" "$SCRIPT_DIR/51la-analytics.js"
sed -i 's/LA51_TRACE_ID/'"$LA51_TRACE_ID"'/' "$SCRIPT_DIR/51la-analytics.js"
sed -i 's#LA51_TRACE_CK#'"$LA51_TRACE_CK"'#' "$SCRIPT_DIR/51la-analytics.js"

sed -i "s/plugins: \[/plugins: \[require('.\/scripts\/51la-analytics'), /" "$WORK_DIR/docusaurus.config.js"
echo "done."