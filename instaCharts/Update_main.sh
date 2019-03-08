#!/bin/bash 
set -x

SCRIPTS_HOME="/home/DonkeyBites/instaCharts/main_html"
HTML_HOME="/var/www/html"

cp ${SCRIPTS_HOME}/TEMPLATE_main.html ${SCRIPTS_HOME}/INITIAL_main.html

for PROFILE in {1..4};
do
  FOLLOWERS=$(sqlite3 /root/InstaPy/db/instapy.db "SELECT MAX(followers) FROM 'accountsProgress' WHERE strftime('%s', 'now') AND profile_id is $PROFILE")
  FOLLOWING=$(sqlite3 /root/InstaPy/db/instapy.db "SELECT MAX(following) FROM 'accountsProgress' WHERE strftime('%s', 'now') AND profile_id is $PROFILE")
  POSTS=$(sqlite3 /root/InstaPy/db/instapy.db "SELECT MAX(total_posts) FROM 'accountsProgress' WHERE strftime('%s', 'now') AND profile_id is $PROFILE")

  case $PROFILE in
    1 )
      CLIENT=doron
      sed -i "s/__doron_FOLLOWERS__/${FOLLOWERS}/" ${SCRIPTS_HOME}/INITIAL_main.html;;
    2 )
      CLIENT=SHAKED
      sed -i "s/__SHAKED_FOLLOWERS__/${FOLLOWERS}/" ${SCRIPTS_HOME}/INITIAL_main.html;;
    3 )
      CLIENT=YOAV
      sed -i "s/__YOAV_FOLLOWERS__/${FOLLOWERS}/" ${SCRIPTS_HOME}/INITIAL_main.html;;
    4 )
      CLIENT=ofek
      sed -i "s/__ofek_FOLLOWERS__/${FOLLOWERS}/" ${SCRIPTS_HOME}/INITIAL_main.html;;
  esac

done

rm -rf ${HTML_HOME}/main.html
mv ${SCRIPTS_HOME}/INITIAL_main.html ${HTML_HOME}/main.html


