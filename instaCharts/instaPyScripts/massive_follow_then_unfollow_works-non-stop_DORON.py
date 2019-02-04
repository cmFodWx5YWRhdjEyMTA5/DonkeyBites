"""
This template is written by @loopypanda

What does this quickstart script aim to do?
- My settings is for running InstaPY 24/7 with approximately 1400
follows/day - 1400 unfollows/day running follow until reaches 7500 and than
switch to unfollow until reaches 0.
"""

from instapy import InstaPy
from instapy.util import smart_run

# login credentials
insta_username = 'doronshai_creative'
insta_password = 'Ilmbfvm20189'

# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True,
                  bypass_suspicious_attempt=True)

# let's go! :>
with smart_run(session):
    # general settings

    session.set_relationship_bounds(enabled=True,
                                    delimit_by_numbers=False,
                                    max_followers=12000000,
                                    max_following=45000,
                                    min_followers=35,
                                    min_following=35)
    session.set_user_interact(amount=2, randomize=True, percentage=100, media='Photo')
    session.set_do_follow(enabled=True, percentage=100)
    session.set_do_like(enabled=True, percentage=100)
    session.set_comments(["Superb shot! :sunglasses:", "Really liked that one", "LIKE!!! :+1::+1::+1:", "this is a hot one :fire::fire::fire:"])
    session.set_do_comment(enabled=False, percentage=80)
    session.set_quota_supervisor(enabled=True,
                                 sleep_after=["likes", "comments_d", "follows", "unfollows", "server_calls_h"],
                                 sleepyhead=True,
                                 stochastic_flow=True,
                                 notify_me=True,
                                 peak_likes=(57, 585),
                                 peak_comments=(21, 182),
                                 peak_follows=(48, None),
                                 peak_unfollows=(35, 402),
                                 peak_server_calls=(None, 4700))
    # activity

    # session.interact_user_followers(['user1', 'user2', 'user3'],
    # amount=8000, randomize=True)
    users_i_follow = ['natalia_tellez','lajosa','verge','thrillist','olyria_roy','edenfines','avital_akko','coral.sharon','sapir_elgrabli','noharbatit','yarden3ardity','roni_brachel1','moran.titanchi','max164','diana_tre','sapir_perez','moran_dvoskin','moran_aroch','sapirmichaeli_','shir_tikozky','sky_buskila','adi_edri9','shirrrrrraaa_elbaz','madlen_tequila','danigozlan5397','yael_ovadia','djtristanofficial','12sivan12','koral_shmuel11','dana_vyun','itssany']

    #session.follow_user_followers(users_i_follow, amount=200, randomize=False, interact=True)
    session.unfollow_users(amount=5, nonFollowers=True, style="FIFO", unfollow_after=12*60*60, sleep_delay=30)
    #session.like_by_tags(['???'], amount=8000)
