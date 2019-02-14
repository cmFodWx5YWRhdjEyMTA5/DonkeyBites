#!/bin/bash 
set -x


CLIENT=${1}
SCRIPT_HOME="/home/DonkeyBites/instaCharts"


cp -f ${SCRIPT_HOME}/${CLIENT}_followers.json /var/www/html/$CLINET/followers.json
