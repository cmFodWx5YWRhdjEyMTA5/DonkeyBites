#!/bin/bash

set -x

export oldUsedPercentage=$(df -h | grep ' 50G' | awk '{ print $4 }' | sed 's/%$//' )
export oldUsedSize=$(df -h | grep ' 50G' | awk '{ print $3 }')

if [ "$oldUsedPercentage" -ge 70 ]; then

	find /root/.jenkins/jobs/NG_Designer_ALL_QBS_Dev/modules/**/builds -type l -ctime +1 -exec rm -rf '{}' \;
	find /root/.jenkins/jobs/NG_Designer_ALL_QBS_Dev/modules/**/builds -type d -ctime +1 -exec rm -rf '{}' \;
	find /root/.jenkins/jobs/NG_Designer_QoS_10_MavenBuild/modules/**/builds -type l -ctime +1 -exec rm -rf '{}' \;
	find /root/.jenkins/jobs/NG_Designer_QoS_10_MavenBuild/modules/**/builds -type d -ctime +1 -exec rm -rf '{}' \;
	find /root/.jenkins/jobs/NG_Designer_LKG_10_MavenBuild/modules/**/builds -type l -ctime +1 -exec rm -rf '{}' \;
	find /root/.jenkins/jobs/NG_Designer_LKG_10_MavenBuild/modules/**/builds -type d -ctime +1 -exec rm -rf '{}' \;
	find /root/.jenkins/jobs/NG_Designer_Deploy_All/modules/**/builds -type l -ctime +1 -exec rm -rf '{}' \;
	find /root/.jenkins/jobs/NG_Designer_Deploy_All/modules/**/builds -type d -ctime +1 -exec rm -rf '{}' \;

	export newUsedPercentage=$(df -h | grep 50G | awk '{ print $4 }' | sed 's/%$//' )
	export newSize=$(df -h | grep 50G | awk '{ print $3 }')

	if [ "$newUsedPercentage" -lt "$oldUsedPercentage" ]; then
		echo SUCCESS = New Free disk size is greater then Old value
		exit 0;
	elif [ "$newUsedPercentage" -eq "$oldUsedPercentage" ]; then
		echo NO CHANGE = New Free disk size is the SAME as the Old value
		exit 0;
	else
	   echo ERROR - there is a problem with the script
	   exit 1;
	fi
else
	echo There is enough Space, No need for cleaner to be executed
		exit 0;
fi