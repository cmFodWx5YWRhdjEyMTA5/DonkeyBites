from instapy import InstaPy
from instapy.util import smart_run

# login credentials
insta_username = 'yoav.shai.2010'
insta_password = 'Ilmbfvm2018'

# get a session!
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True)

# let's go! :>
with smart_run(session):
    # settings
    session.set_user_interact(amount=3, randomize=True, percentage=100,
                              media='Photo')
