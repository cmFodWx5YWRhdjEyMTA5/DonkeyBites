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

# login credentials
insta_username = 'shaked.ohayon'
insta_password = 'sara2606'

users_i_follow = ['omershapira_','gostylemagazine','israel_bidur','noakirel_','rotemhanan','wearebeautiful.de','tlvagency','taylor_hill','maya.keyy','kedemstudio','shelly_shwartz','nisrinasbia','mishelgerzig','idophelmakeup','fashionnova','shaharyaacobi_','nicoledanino']

#users_i_follow = ['jastookes','taylor_hill','hoskelsa','imgmodels','modelsdiscovery','ayalasinai_18','omer_hazan']


#users_i_follow = ['barzomer','the_romi_frenkel','reefneeman','annazak12','edenfines ','naomieliav','adela_hock','romakeren','_omernudelman_','yeela_frumkin','yaelshelbia','jastookes','taylor_hill','hoskelsa','imgmodels','modelsdiscovery','ayalasinai_18','omer_hazan']


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
    sendTelegram("Follower Started")
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
                # activity
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
schedule.every(10).minutes.do(follow)
#schedule.every().day.at("09:30").do(follow)
#schedule.every().day.at("12:00").do(follow)
#schedule.every().day.at("13:26").do(follow)
#schedule.every().day.at("15:00").do(follow)
#schedule.every().day.at("18:00").do(follow)
#schedule.every().day.at("21:00").do(follow)
#schedule.every().day.at("00:00").do(follow)

while True:
    schedule.run_pending()
    time.sleep(1)
