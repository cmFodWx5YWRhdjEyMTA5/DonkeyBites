"""
This template is written by @Tachenz

What does this quickstart script aim to do?
- Interact with user followers, liking 3 pictures, doing 1-2 comment - and
25% chance of follow (ratios which work the best for my account)

NOTES:
- This is used in combination with putting a 40 sec sleep delay after every
like the script does. It runs 24/7 at rather slower speed, but without
problems (so far).
"""

from instapy import InstaPy
from instapy.util import smart_run

# login credentials
insta_username = 'doronshai_creative'
insta_password = 'Ilmbfvm20189'

# get a session!
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True,
                  bypass_suspicious_attempt=True)

# let's go! :>
with smart_run(session):
    # settings
    session.set_user_interact(amount=3, randomize=True, percentage=100,
                              media='Photo')
    session.set_relationship_bounds(enabled=True,
                                    potency_ratio=None,
                                    delimit_by_numbers=True,
                                    max_followers=3000,
                                    max_following=900,
                                    min_followers=50,
                                    min_following=50)
    session.set_simulation(enabled=False)
    session.set_do_like(enabled=True, percentage=100)
    session.set_ignore_users([])
    session.set_do_comment(enabled=True, percentage=35)
    session.set_do_follow(enabled=True, percentage=25, times=1)
    session.set_comments([])
    session.set_comments(['Nice shot! @{}', 
         'I love your profile! @{}',
         '@{} Love it!',
         '@{} Must do more of this oneI :sunglasses::sunglasses::sunglasses:',
         '@{} :heart::heart:',
         '@{}:revolving_hearts::revolving_hearts:',
         '@{}:fire::fire::fire:'])
    session.set_ignore_if_contains([])
    session.set_action_delays(enabled=True, like=40)

    # activity
    session.interact_user_followers(['shir_tikozky','sky_buskila','adi_edri9','shirrrrrraaa_elbaz','madlen_tequila','danigozlan5397','yael_ovadia','djtristanofficial','12sivan12','koral_shmuel11'], amount=340)

"""
-- REVIEWS --

@Andercorp:
- This would probably be the best temp for new accounts to start slowly and 
gently and then as your account gather IG authority, you could put some more 
power to your temp/bot...

@uluQulu:
- @Tachenz, the values in your script took my attention, it will be very 
good for new starters, as @Andercorp said. Stunning!

"""
