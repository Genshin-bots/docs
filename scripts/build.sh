#!/bin/bash

# Trying to add analytics plugins
for file in scripts/add_analytics_*.sh; do
  bash "$file"
done

# build
yarn build