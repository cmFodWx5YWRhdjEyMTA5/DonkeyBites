#!/bin/bash

DT=$(date '+%Y%m%d%H%M%S');

python3 /home/insta/InstaPy/DORON/get_amount_of_FOLLOWERS.py > /home/DonkeyBites/instaCharts/output.log 2>&1

FOLLOWING=$(less /home/DonkeyBites/instaCharts/output.log  | grep FOLLOW | awk '{print $6}')
FOLLOWERS=$(less /home/DonkeyBites/instaCharts/output.log  | grep FOLLOW | awk '{print $10}')

echo "$DT -  $FOLLOWING" >> /home/DonkeyBites/instaCharts/FOLLOWING
echo "$DT -  $FOLLOWERS" >> /home/DonkeyBites/instaCharts/FOLLOWERS
