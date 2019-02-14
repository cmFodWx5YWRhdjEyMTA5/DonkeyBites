#!/bin/bash 
set -x

DT="$(date +%s )"

CLIENT=${1}
SCRIPT_HOME="/home/DonkeyBites/instaCharts"

if [ ! -f ${SCRIPT_HOME}/${CLIENT}_output.log ]; then
  touch ${SCRIPT_HOME}/${CLIENT}_output.log
fi

python3 /home/InstaPy/get_amount_of_FOLLOWERS_${CLIENT}.py > ${SCRIPT_HOME}/${CLIENT}_output.log 2>&1

FOLLOWING=$(less ${SCRIPT_HOME}/${CLIENT}_output.log  | grep FOLLOW | awk '{print $6}')
FOLLOWERS=$(less ${SCRIPT_HOME}/${CLIENT}_output.log  | grep FOLLOW | awk '{print $10}')

jq --arg DT "$DT" --arg FOLLOWERS "$FOLLOWERS" --arg FOLLOWING "$FOLLOWING" '.data.entries[.data.entries| length] |= . + {"Date": $DT, "Followers": $FOLLOWERS, "Following": $FOLLOWING }' ${SCRIPT_HOME}/${CLIENT}_followers.json > ${SCRIPT_HOME}/${CLIENT}_followers_temp.json

rm -rf ${SCRIPT_HOME}/${CLIENT}_followers.json
mv ${SCRIPT_HOME}/${CLIENT}_followers_temp.json ${SCRIPT_HOME}/${CLIENT}_followers.json

cp -f ${SCRIPT_HOME}/${CLIENT}_followers.json /var/www/html/${CLINET}/followers.json
