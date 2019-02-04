#!/bin/bash

DT="$(date '+%Y-%m-%d %H:%M:%S')"

BASE_FOLDER=${1}

python3 ${BASE_FOLDER}/get_amount_of_FOLLOWERS.py > ${BASE_FOLDER}/output.log 2>&1

FOLLOWING=$(less ${BASE_FOLDER}/output.log  | grep FOLLOW | awk '{print $6}')
FOLLOWERS=$(less ${BASE_FOLDER}/output.log  | grep FOLLOW | awk '{print $10}')

jq --arg DT "$DT" --arg FOLLOWERS "$FOLLOWERS" --arg FOLLOWING "$FOLLOWING" '.data.entries[.data.entries| length] |= . + {"Date": $DT, "Followers": $FOLLOWERS, "Following": $FOLLOWING }' ${BASE_FOLDER}/followers.json > ${BASE_FOLDER}/followers_temp.json

rm -rf ${BASE_FOLDER}/followers.json
mv ${BASE_FOLDER}/followers_temp.json ${BASE_FOLDER}/followers.json

cp -f ${BASE_FOLDER}/followers.json /var/www/html/followers.json
