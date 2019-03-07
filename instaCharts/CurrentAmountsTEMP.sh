#!/bin/bash 
set -x

DT="$(date +%s )"
HUMANDATE="$(date +"%d-%m-%Y-%H-%M" )"
CLIENT=${1}
SCRIPT_HOME="/home/DonkeyBites/instaCharts"

echo HUMANDATE is $HUMANDATE
