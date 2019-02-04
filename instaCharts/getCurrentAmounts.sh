#!/bin/bash

DT="$(date '+%Y-%m-%d %H:%M:%S')"

python3 /home/InstaPy/get_amount_of_FOLLOWERS.py > /home/InstaPy/output.log 2>&1

FOLLOWING=$(less /home/InstaPy/output.log  | grep FOLLOW | awk '{print $6}')
FOLLOWERS=$(less /home/InstaPy/output.log  | grep FOLLOW | awk '{print $10}')

jq --arg DT "$DT" --arg FOLLOWERS "$FOLLOWERS" --arg FOLLOWING "$FOLLOWING" '.data.entries[.data.entries| length] |= . + {"Date": $DT, "Followers": $FOLLOWERS, "Following": $FOLLOWING }' followers.json > followers_temp.json

rm -rf /home/InstaPy/followers.json
mv /home/InstaPy/followers_temp.json /home/InstaPy/followers.json

cp -f /home/InstaPy/followers.json /var/www/html/followers.json
