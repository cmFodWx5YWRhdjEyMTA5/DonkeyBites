# -*- coding: UTF-8 -*-
import time
from datetime import datetime
import traceback
import requests
import sys
#import pickle

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


def get_session(insta_username,insta_password):
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True,
                      nogui=True)
    return session

def sendTelegram (message,insta_username):
    requests.get(
        "https://api.telegram.org/bot730982013:AAHjGc7kf3csMAY680TZTn80WFnb-dcdzOs/sendMessage?chat_id=387986068&text={} InstaPy {} @ {}".format(insta_username, message, datetime.now().strftime("%H:%M:%S")))

def follow(user,password,user_list):
    sendTelegram("Follower Started",user)
    session = get_session(user,password)
    with smart_run(session):
        counter = 0
        while counter < 3:
            counter += 1
            sendTelegram("Follower part " + str(counter) + "/3 Started",user)
            try:
                # settings
                session.set_relationship_bounds(enabled=True,
                                               delimit_by_numbers=True,
                                               max_followers=30000,
                                               min_followers=100,
                                               min_posts=30)
                session.set_skip_users(skip_private=False)
                session.set_do_follow(enabled=True, percentage=100, times=1)
  
                # activity
                #session.like_by_tags(['photographerfashion'], amount=150)
                session.follow_user_followers(user_list, amount=150,
                                              randomize=False, interact=False)
                session.unfollow_users(amount=120, InstapyFollowed=(True, "nonfollowers"),
                                       style="FIFO", unfollow_after=4*60*60, sleep_delay=600)

            except Exception:
                print(traceback.format_exc())
                sendTelegram("Follower Exploded",user)

            sendTelegram("Follower part " + str(counter) + "/3 Finished",user)
 
    sendTelegram("Follower Stopped",user)

def unfollow(user,password):
    sendTelegram("UnFollower Started",user)
    session = get_session()
    with smart_run(session):
        try:
            # actions
            session.unfollow_users(amount=400, InstapyFollowed=(True, "all"),
                                   style="FIFO", unfollow_after=8*60*60,
                                   sleep_delay=600)

        except Exception:
            print(traceback.format_exc())
            sendTelegram("UnFollower Exploded",user)

        sendTelegram("UnFollower Stopped",user)    
