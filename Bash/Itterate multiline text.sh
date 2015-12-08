#!/bin/bash


# What is it?
# when we have many java process and we want to kill all expect the Jenkinsslave proccesses then we need such a script



set +x

ps aux | grep [j]ava > JavaProccessList

cat JavaProccessList | while read line
do
    #currentJava[i]="$line"
	if [[ "$line" != *"slave"* ]]
	then
		currentJava[i]="$line"
		echo "${currentJava[i]}"
    	echo -e "\n"
   	fi
    let i++
done

#######  OR DO THIS #######

processesToKill=$(ps aux | grep  -v "slave" | grep [j]ava |  awk '{print $2}')

if [[ -z "${processesToKill// }" ]]
then
    echo "Nothing to Kill"
else
	kill $(ps aux | grep  -v "slave" | grep [j]ava |  awk '{print $2}')
fi




### OLD 
IFS=', ' read -a currentJavaArray <<< "$currentJava"
echo "${currentJavaArray[0]}"



ps aux | grep  -v "slave" | grep [j]ava |  awk '{print $2}' 

ps axo pid,cmd,etime