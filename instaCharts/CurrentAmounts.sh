#!/bin/bash 
set -x

DT="$(date +%s )"
HUMANDATE="$(date +"%d-%m-%Y-%H-%M" )"
CLIENT=${1}
SCRIPT_HOME="/home/DonkeyBites/instaCharts"

#if [ -f ${SCRIPT_HOME}/${CLIENT}_output.log ]; then
#  rm -rf ${SCRIPT_HOME}/${CLIENT}_output.log
#fi

#touch ${SCRIPT_HOME}/${CLIENT}_output.log

#python3 /home/InstaPy/get_amount_of_FOLLOWERS_${CLIENT}.py > ${SCRIPT_HOME}/${CLIENT}_output.log 2>&1

#FOLLOWING=$(less ${SCRIPT_HOME}/${CLIENT}_output.log  | grep FOLLOW | awk '{print $6}')
#FOLLOWERS=$(less ${SCRIPT_HOME}/${CLIENT}_output.log  | grep FOLLOW | awk '{print $10}')

case $CLIENT in
  doron )
    ACOUNT=1;;
  SHAKED )
    ACOUNT=2;;
  YOAV )
    ACOUNT=3;;
  ofek )
    ACOUNT=4;;
esac

FOLLOWERS=$(sqlite3 /root/InstaPy/db/instapy.db "SELECT MAX(followers) FROM 'accountsProgress' WHERE strftime('%s', 'now') AND profile_id is $ACOUNT")
FOLLOWING=$(sqlite3 /root/InstaPy/db/instapy.db "SELECT MAX(following) FROM 'accountsProgress' WHERE strftime('%s', 'now') AND profile_id is $ACOUNT")
POSTS=$(sqlite3 /root/InstaPy/db/instapy.db "SELECT MAX(total_posts) FROM 'accountsProgress' WHERE strftime('%s', 'now') AND profile_id is $ACOUNT")

jq --arg DT "$DT" --arg HUMANDATE "$HUMANDATE" --arg FOLLOWERS "$FOLLOWERS" --arg FOLLOWING "$FOLLOWING" '.data.entries[.data.entries| length] |= . + {"Date": $DT, "HumanDate": $HUMANDATE, "Followers": $FOLLOWERS, "Following": $FOLLOWING }' ${SCRIPT_HOME}/${CLIENT}_followers.json > ${SCRIPT_HOME}/${CLIENT}_followers_temp.json

rm -rf ${SCRIPT_HOME}/${CLIENT}_followers.json
mv ${SCRIPT_HOME}/${CLIENT}_followers_temp.json ${SCRIPT_HOME}/${CLIENT}_followers.json

rm -rf ${CLIENT}_index.html
sed -e "s/__CLIENT__/${CLIENT}/" ${SCRIPT_HOME}/INITIAL_index.html > ${SCRIPT_HOME}/${CLIENT}_index.html
mkdir -p /var/www/html/${CLIENT}/
cp -f ${SCRIPT_HOME}/${CLIENT}_index.html /var/www/html/${CLIENT}/index.html

cp -f ${SCRIPT_HOME}/${CLIENT}_followers.json /var/www/html/${CLIENT}/followers.json
