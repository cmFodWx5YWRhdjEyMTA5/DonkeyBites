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

insta_username = 'yoav.shai.2010'
insta_password = 'Ilmbfvm2018'

users_i_follow = ['brawl_stars_isr','brawl.stars.israel','funny.il.1','fortnite_il','srutonim','game_israel','reala10n']


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
schedule.every().day.at("08:00").do(follow)
schedule.every().day.at("12:45").do(follow)
schedule.every().day.at("13:26").do(follow)
schedule.every().day.at("16:00").do(follow)
schedule.every().day.at("18:00").do(follow)
schedule.every().day.at("20:00").do(follow)
schedule.every().day.at("21:17").do(follow)
schedule.every().day.at("00:00").do(follow)
#schedule.every().wednesday.at("03:00").do(unfollow)

while True:
    schedule.run_pending()
    time.sleep(1)
