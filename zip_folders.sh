#!/bin/bash

for dir in */; do
    dir="${dir%/}"
    zip -r "${dir}.zip" "${dir}"
    echo "✓ ${dir}.zip"
done
