#!/bin/sh
# Query JSON files containing the URLs of images

LENGTH=50
DIR="./data/raw"

rm "$DIR/response.txt"

for i in {0..50}
do
    START=$((1 + $i * $LENGTH))
    echo "Request URls $START through $(($START + $LENGTH - 1))..."
    curl "https://www.earthcam.com/cams/common/gethofitems.php?camera=empirestatebuilding&start=$START&length=$LENGTH" >> "$DIR/response.txt"
    printf "\n" >> "$DIR/response.txt"
done
