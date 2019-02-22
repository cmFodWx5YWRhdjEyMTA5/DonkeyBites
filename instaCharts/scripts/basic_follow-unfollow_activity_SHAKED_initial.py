"""
This template is written by @cormo1990

What does this quickstart script aim to do?
- Basic follow/unfollow activity.

NOTES:
- I don't want to automate comment and too much likes because I want to do
this only for post that I really like the content so at the moment I only
use the function follow/unfollow.
- I use two files "quickstart", one for follow and one for unfollow.
- I noticed that the most important thing is that the account from where I
get followers has similar contents to mine in order to be sure that my
content could be appreciated. After the following step, I start unfollowing
the user that don't followed me back.
- At the end I clean my account unfollowing all the users followed with
InstaPy.
"""

# imports
from instapy import InstaPy
from instapy.util import smart_run

# login credentials
insta_username = 'shaked.ohayon'
insta_password = 'sara2606'

# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True,
                  bypass_suspicious_attempt=True)

with smart_run(session):
    """ Activity flow """
    # general settings
    session.set_relationship_bounds(enabled=False)
    session.set_skip_users(skip_private=False)

    #session.set_dont_include(["friend1", "friend2", "friend3"])
    #session.set_dont_like(["pizza", "#store"])

    # activities
    #users_i_follow = ['Barzomer','The_romi_frenkel','Reefneeman','Annazak12','Edenfines ','Naomieliav','Adela_hock','Romakeren','_omernudelman_','Yeela_frumkin','Yaelshelbia','Jastookes','Taylor_hill','Hoskelsa','Imgmodels','Modelsdicovery','Ayalasinai_18','Omer_hazan']

    #users_i_follow = ['Adela_hock','Romakeren','_omernudelman_','Yeela_frumkin','Yaelshelbia','Jastookes','Taylor_hill','Hoskelsa','Imgmodels','modelsdiscovery','Ayalasinai_18','Omer_hazan']
    #session.follow_by_list(users_i_follow, times=2, sleep_delay=600, interact=False)
