# -*- coding: UTF-8 -*-
import time
from datetime import datetime
import schedule
import traceback
import requests
import sys
import pickle

from instapy import InstaPy
from instapy.util import smart_run

#client = sys.argv[1]
#from details.DORON import client
#client = sys.argv[1]
#__import__ (client)

#file = open('variables.pickle', 'rb')
#externalVars = pickle.load(file)

#print ("insta_username is " + externalVars.insta_username)
#sys.exit()


insta_username = 'doronshai_creative'
insta_password = 'Ilmbfvm20189'

users_i_follow = ['omershapira_','gostylemagazine','israel_bidur','noakirel_','rotemhanan','wearebeautiful.de','tlvagency','taylor_hill','maya.keyy','kedemstudio','shelly_shwartz','nisrinasbia','mishelgerzig','idophelmakeup','fashionnova','shaharyaacobi_','nicoledanino','romakeren','elinor_shahar_pm','shaharyaacobi','libarbalilti','maytagar','kaiagerber','edenfines','robertomodels','israel_bidur']

#users_i_follow = ['avital','avital_cohenlove','avital_akko','jenselter','sivanbaba','amitbetesh']
#users_i_follow = ['saarpesach','tonivisualartist','segal_studio','pergament','batizoz','fashionphotographerss','gilbertosouzaphoto']

#users_i_follow = ['natalia_tellez','lajosa','verge','thrillist','olyria_roy','edenfines','avital_akko','coral.sharon','sapir_elgrabli','noharbatit','yarden3ardity','roni_brachel1','moran.titanchi','max164','diana_tre','sapir_perez','moran_dvoskin','moran_aroch','sapirmichaeli_','shir_tikozky','sky_buskila','adi_edri9','shirrrrrraaa_elbaz','madlen_tequila','danigozlan5397','yael_ovadia','djtristanofficial','12sivan12','koral_shmuel11','dana_vyun','itssany']


def get_session():
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True,
                      nogui=True)
    return session

def sendTelegram (message):
    requests.get(
        "https://api.telegram.org/bot730982013:AAHjGc7kf3csMAY680TZTn80WFnb-dcdzOs/sendMessage?chat_id=387986068&text={} InstaPy {} @ {}".format(insta_username, message, datetime.now().strftime("%H:%M:%S")))

def follow():
    sendTelegram(":smile::sunglasses::smile: Follower Started")
    session = get_session()
    with smart_run(session):
        counter = 0
        while counter < 3:
            counter += 1
            sendTelegram("Follower part " + str(counter) + "/3 Started")
            try:
                # settings
                session.set_relationship_bounds(enabled=True,
                                               delimit_by_numbers=True,
                                               max_followers=30000)
                session.set_skip_users(skip_private=False)
                session.set_do_follow(enabled=True, percentage=100, times=1)
  
                # activity
                #session.like_by_tags(['photographerfashion'], amount=150)
                session.follow_user_followers(users_i_follow, amount=150,
                                              randomize=False, interact=False)
                session.unfollow_users(amount=120, InstapyFollowed=(True, "nonfollowers"),
                                       style="FIFO", unfollow_after=4*60*60, sleep_delay=600)

            except Exception:
                print(traceback.format_exc())
                sendTelegram("Follower Exploded")

            sendTelegram("Follower part " + str(counter) + "/3 Finished")
 
    sendTelegram("Follower Stopped")

def unfollow():
    sendTelegram("UnFollower Started")
    session = get_session()
    with smart_run(session):
        try:
            # actions
            session.unfollow_users(amount=400, InstapyFollowed=(True, "all"),
                                   style="FIFO", unfollow_after=8*60*60,
                                   sleep_delay=600)

        except Exception:
            print(traceback.format_exc())
            sendTelegram("UnFollower Exploded")

        sendTelegram("UnFollower Stopped")    

#follow()
#unfollow()
# schedulers
#schedule.every(15).minutes.do(follow)


hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
minutes = ["00","15","30","45"]

for hour in hours:
    for minute in minutes:
#        time = '"' + str(hour) + ':' + str(minute) + '"'
        currentTime = str(hour) + ":" + str(minute)
        schedule.every().day.at(currentTime).do(follow)

#schedule.every().day.at("09:00").do(follow)
#schedule.every().day.at("10:00").do(follow)
#schedule.every().day.at("11:00").do(follow)
#schedule.every().day.at("12:00").do(follow)
#schedule.every().day.at("13:00").do(follow)
#schedule.every().day.at("14:00").do(follow)
#schedule.every().day.at("15:00").do(follow)
#schedule.every().day.at("16:00").do(follow)
#schedule.every().day.at("17:00").do(follow)
#schedule.every().day.at("18:00").do(follow)
#schedule.every().day.at("19:00").do(follow)
#schedule.every().day.at("20:00").do(follow)
#schedule.every().day.at("21:00").do(follow)
#schedule.every().day.at("22:00").do(follow)
#schedule.every().day.at("23:00").do(follow)
#schedule.every().day.at("00:00").do(follow)
#schedule.every().day.at("01:00").do(follow)

while True:
    schedule.run_pending()
    time.sleep(1)
