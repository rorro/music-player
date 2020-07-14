#!/bin/bash

IFS=$'\n'; set -f
for f in $(find music/ -type f); do
    path="$(dirname "$f")"/
    file="$(basename "$f")"
    echo $path$file
    mv $path$file $path$(echo $file | sed -e 's/[^][A-Za-z0-9'\''\(\).,+& _=-]//g');
done
unset IFS; set +f
