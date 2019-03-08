#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
import sys


def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers


if __name__ == "__main__":
    api = InstagramAPI("yoav.shai.2010", "Ilmbfvm2018")
    api.login()

    # user_id = '1461295173'
    user_id = api.username_id

    # List of all followers
    followers = api.getTotalFollowers(user_id)
    following = api.getTotalFollowings(user_id)
    user_feed = api.getTotalUserFeed(user_id)
    print(len(followers))
    print(len(following))
    print(len(user_feed))


    orig_stdout = sys.stdout
    f = open('out.txt', 'w')
    sys.stdout = f

#    print('Number of followers:', len(followers))
    print(followers)
#    with open('output.txt', 'w') as f:
#        print >> f, 'Number of followers:', len(followers) 
#        print >> f, 'The followers are:', followers 

    sys.stdout = orig_stdout
    f.close()

    # Alternatively, use the code below
    # (check evaluation.evaluate_user_followers for further details).
    #followers = api.getTotalFollowers(user_id)
    #print('Number of followers:', len(followers))
