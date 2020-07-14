#!/bin/bash

while read p; do
    echo $p
    cp -i "$p" carmusic/
done <upvotes.txt
