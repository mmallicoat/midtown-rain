#!/bin/sh
# Query JSON files containing the URLs of images

DIR="./data/raw"
URLS="./data/raw/combined_urls.txt"

wget -i $URLS -P $DIR
