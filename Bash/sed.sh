SED
Change all <disabled>false</disabled> TO <disabled>true</disabled>
On all config.xml files
only on current level and next folder levels

find . -maxdepth 2 -name "doron.xml" -type f -exec sed -i 's/<disabled>false<\/disabled>/<disabled>true<\/disabled>/g' {} +
