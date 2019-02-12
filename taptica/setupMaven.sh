#!/bin/bash
cd /tmp
if [ -d /tmp/parent-project ]; then
    echo "repo already exists, git pull for changes"
    cd parent-project
    git pull origin master
else
    git clone https://bitbucket.org/taptica/parent-project.git
fi
cd parent-project
chmod +x build.sh
./build.sh
