#!/bin/bash
set -x

#mount iltlvp01:/vol/nrvol4/DEV_P_HPS /mnt/DEV_P_HPS/ -O username=kmcadm,password=Gauss2004,domain=global
my_time=`date +"%T" |tr ":" _`
my_date=`date +'%d_%m_%Y'`
my_date="$my_date"_
export bu_filename=Jenkins_Backup_$my_date$my_time.zip
echo 'Backup file name is: '$bu_filename

zip -9 -r /mnt/DEV_P_HPS/backup/panda_backup/$bu_filename /root/.jenkins -x root/.jenkins/tools/* root/.jenkins/jobs/**/builds/* root/.jenkins/cache/* root/.jenkins/plugins/* root/**/*.war root/.jenkins/workspace/**/.git/* root/.jenkins/jobs/**/log root/.jenkins/backup/* 


rm -rf /tmp/*.zip