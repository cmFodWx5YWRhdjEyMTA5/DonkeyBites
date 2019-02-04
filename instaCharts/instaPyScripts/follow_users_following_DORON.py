""" Quickstart script for InstaPy usage """
# imports
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

with smart_run(session):
    """ Activity flow """
    # general settings
    session.set_dont_unfollow_active_users(enabled=True, posts=5)

    session.set_relationship_bounds(enabled=True,
                                    delimit_by_numbers=True,
                                    potency_ratio=None,
                                    max_followers=50000,
                                    min_followers=45,
                                    min_following=77)

    session.set_skip_users(skip_private=True,
                           private_percentage=100,
                           skip_no_profile_pic=False,
                           no_profile_pic_percentage=100,
                           skip_business=False,
                           business_percentage=100,
                           skip_business_categories=[],
                           dont_skip_business_categories=[])
    
    session.set_dont_include(["emelybs1", "friend2", "friend3"])
    
    session.set_dont_like(["pizza", "#store","sex"])

    session.set_user_interact(amount=5, randomize=True, percentage=50, media='Photo')
    session.set_do_follow(enabled=False, percentage=70)
    session.set_do_like(enabled=False, percentage=70)
    session.set_comments(["Great one", "Amazing :)", "Cool", "Super!"])
    session.set_do_comment(enabled=True, percentage=80)

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
    session.like_by_tags(["telaviv","fashion","party","photography"], amount=30)

    
    accs = ['marthahigaredaoficial','natalia_tellez','lajosa','verge','thrillist','olyria_roy','edenfines','avital_akko','coral.sharon','sapir_elgrabli','noharbatit','yarden3ardity','roni_brachel1','moran.titanchi','max164','diana_tre','sapir_perez','moran_dvoskin','moran_aroch','sapirmichaeli_','shir_tikozky','sky_buskila','adi_edri9','shirrrrrraaa_elbaz','madlen_tequila','danigozlan5397','yael_ovadia','djtristanofficial','12sivan12','koral_shmuel11','dana_vyun','itssany']
    
    #session.follow_by_list(accs, times=1, sleep_delay=600, interact=True)


    #session.interact_user_followers(['liyanadi', 'liora_kramarov06', 'max164'], amount=20, randomize=True)

    session.follow_user_followers(accs, amount=20, randomize=False)
