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
    #session.set_relationship_bounds(enabled=True,
     #                               delimit_by_numbers=True,
      #                              max_followers=15000,
       #                             min_followers=45,
        #                            min_following=77)

    session.set_relationship_bounds(enabled=True,
                                    delimit_by_numbers=True,
                                    max_followers=2000000)
    session.set_skip_users(skip_private=False)

    #session.set_dont_include(["friend1", "friend2", "friend3"])
    #session.set_dont_like(["pizza", "#store"])

    # activities

    users_i_follow = ['barzomer','the_romi_frenkel','reefneeman','annazak12','edenfines ','naomieliav','adela_hock','romakeren','_omernudelman_','yeela_frumkin','yaelshelbia','jastookes','taylor_hill','hoskelsa','imgmodels','modelsdiscovery','ayalasinai_18','omer_hazan']


    """ Massive Follow of users followers (I suggest to follow not less than
    3500/4000 users for better results)...
    """
    session.follow_user_followers(users_i_follow, amount=1000,
                                  randomize=False, interact=False)

    """ First step of Unfollow action - Unfollow not follower users...
    """
    session.unfollow_users(amount=700, InstapyFollowed=(True, "all"),
                           style="FIFO",
                           unfollow_after=12*60*60, sleep_delay=601)

    """ Second step of Massive Follow...
    """
    session.follow_user_followers(users_i_follow, amount=1000,
                                  randomize=False, interact=False)

    """ Second step of Unfollow action - Unfollow not follower users...
    """
    session.unfollow_users(amount=700, InstapyFollowed=(True, "all"),
                           style="FIFO",
                           unfollow_after=12*60*60, sleep_delay=601)