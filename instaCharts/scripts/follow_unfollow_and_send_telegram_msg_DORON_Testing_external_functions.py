import time
import schedule
from instaPy_functions import *

insta_username = 'doronshai_creative'
insta_password = 'Ilmbfvm20189'

users_i_follow = ['avital','avital_cohenlove','avital_akko','jenselter','sivanbaba','amitbetesh']

schedule.every().day.at("08:00").do(follow(insta_username,insta_password,users_i_follow))
schedule.every().day.at("12:45").do(follow(insta_username,insta_password,users_i_follow))
schedule.every().day.at("13:40").do(follow(insta_username,insta_password,users_i_follow))
schedule.every().day.at("16:30").do(follow(insta_username,insta_password,users_i_follow))
schedule.every().day.at("20:00").do(follow(insta_username,insta_password,users_i_follow))
schedule.every().day.at("22:19").do(follow(insta_username,insta_password,users_i_follow))
schedule.every().day.at("00:15").do(follow(insta_username,insta_password,users_i_follow))
schedule.every().day.at("04:15").do(follow(insta_username,insta_password,users_i_follow))

while True:
    schedule.run_pending()
    time.sleep(1)
