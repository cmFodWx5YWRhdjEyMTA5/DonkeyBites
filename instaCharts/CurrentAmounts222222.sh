#!/bin/bash 
set -x


CLIENT=${1}
SCRIPT_HOME="/home/DonkeyBites/instaCharts"

sed -e "s/__CLIENT__/${CLIENT}/" index.html > ${CLIENT}_index.html
cp -f ${SCRIPT_HOME}/${CLIENT}_index.html /var/www/html/${CLIENT}/index.html
