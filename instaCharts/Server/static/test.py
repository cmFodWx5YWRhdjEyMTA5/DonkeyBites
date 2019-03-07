# -*- coding: UTF-8 -*-
import requests


def sendTelegram (message):
    requests.get(
        "https://api.telegram.org/bot730982013:AAHjGc7kf3csMAY680TZTn80WFnb-dcdzOs/sendMessage?chat_id=387986068&text=InstaPy {} @ {}".format(message, datetime.now().strftime("%H:%M:%S")))

def follow():
    print("aaa")
    sendTelegram("WORKING")
    print("bbbb")

follow()
