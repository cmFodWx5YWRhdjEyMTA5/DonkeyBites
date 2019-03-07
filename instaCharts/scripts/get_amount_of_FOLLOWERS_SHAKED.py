from instapy import InstaPy
from instapy.util import smart_run

# login credentials
insta_username = 'shaked.ohayon'
insta_password = 'sara2606'

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
