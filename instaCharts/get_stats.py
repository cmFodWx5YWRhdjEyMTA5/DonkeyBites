#!/usr/bin/env python

from InstagramAPI import InstagramAPI
import sys, os, uuid, calendar, json
import sqlite3, logging, requests
from os.path import exists as path_exists
from os.path import isfile as file_exists
from os.path import sep as native_slash
from datetime import datetime

from database_engine import get_database
from settings import Settings
from exceptions import InstaPyError


def direct_message(text, recipients):
    if type(recipients) != type([]):
        recipients = [str(recipients)]
    recipient_users = '"",""'.join(str(r) for r in recipients)
    endpoint = 'direct_v2/threads/broadcast/text/'
    boundary = uuid
    bodies   = [
        {
            'type' : 'form-data',
            'name' : 'recipient_users',
            'data' : '[["{}"]]'.format(recipient_users),
        },
        {
            'type' : 'form-data',
            'name' : 'client_context',
            'data' : uuid,
        },
        {
            'type' : 'form-data',
            'name' : 'thread',
            'data' : '["0"]',
        },
        {
            'type' : 'form-data',
            'name' : 'text',
            'data' : text or '',
        },
    ]
    data = buildBody(bodies,boundary)
    s.headers.update (
        {
            'User-Agent' : USER_AGENT,
            'Proxy-Connection' : 'keep-alive',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'multipart/form-data; boundary={}'.format(boundary),
            'Accept-Language': 'en-en',
        }
    )
    #self.SendRequest(endpoint,post=data) #overwrites 'Content-type' header and boundary is missed
    response = s.post(API_URL + endpoint, data=data)
    
    if response.status_code == 200:
        LastResponse = response
        LastJson = json.loads(response.text)
        return True
    else:
        print ("Request return " + str(response.status_code) + " error!")
        # for debugging
        try:
            LastResponse = response
            LastJson = json.loads(response.text)
        except:
            pass
        return False
    
def buildBody(bodies, boundary):
    body = u''
    for b in bodies:
        body += u'--{boundary}\r\n'.format(boundary=boundary)
        body += u'Content-Disposition: {b_type}; name="{b_name}"'.format(b_type=b['type'], b_name=b['name'])
        _filename = b.get('filename', None)
        _headers = b.get('headers', None)
        if _filename:
            _filename, ext = os.path.splitext(_filename)
            _body += u'; filename="pending_media_{uid}.{ext}"'.format(uid=generateUploadId(), ext=ext)
        if _headers and isinstance(_headers, list):
            for h in _headers:
                _body += u'\r\n{header}'.format(header=h)
        body += u'\r\n\r\n{data}\r\n'.format(data=b['data'])
    body += u'--{boundary}--'.format(boundary=boundary)
    return body

def generateUploadId(self):
    return str(calendar.timegm(datetime.utcnow().utctimetuple()))
    
def save_account_progress(username, followers, following, posts, logger):
    """
    Check account current progress and update database

    Args:
        :username: Account to be updated
        :logger: library to log actions
    """
    logger.info('Saving account progress...')

    try:
        # DB instance
        db, id = get_database()
        conn = sqlite3.connect(db)
        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            sql = ("INSERT INTO accountsProgress (profile_id, followers, "
                   "following, total_posts, created, modified) "
                   "VALUES (?, ?, ?, ?, strftime('%Y-%m-%d %H:%M:%S'), "
                   "strftime('%Y-%m-%d %H:%M:%S'))")
            cur.execute(sql, (id, str(followers), str(following), str(posts)))
            conn.commit()
    except Exception:
        logger.exception('message')

def get_instapy_logger(show_logs):
    """
    Handles the creation and retrieval of loggers to avoid
    re-instantiation.
    """

    existing_logger = Settings.loggers.get(username)
    if existing_logger is not None:
        return existing_logger
    else:
        # initialize and setup logging system for the InstaPy object
        logger = logging.getLogger(username)
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(
            '{}general.log'.format(logfolder))
        file_handler.setLevel(logging.DEBUG)
        extra = {"username": username}
        logger_formatter = logging.Formatter(
            '%(levelname)s [%(asctime)s] [%(username)s]  %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(logger_formatter)
        logger.addHandler(file_handler)

        if show_logs is True:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(logger_formatter)
            logger.addHandler(console_handler)

        logger = logging.LoggerAdapter(logger, extra)

        Settings.loggers[username] = logger
        Settings.logger = logger
        return logger

def get_logfolder(username, multi_logs):
    if multi_logs:
        logfolder = "{0}{1}{2}{1}".format(Settings.log_location,
                                          native_slash,
                                          username)
    else:
        logfolder = (Settings.log_location + native_slash)

    validate_path(logfolder)
    return logfolder

def validate_path(path):
    """ Make sure the given path exists """

    if not path_exists(path):
        try:
            os.makedirs(path)

        except OSError as exc:
            exc_name = type(exc).__name__
            msg = ("{} occured while making \"{}\" path!"
                   "\n\t{}".format(exc_name,
                                   path,
                                   str(exc).encode("utf-8")))
            raise InstaPyError(msg)

if __name__ == "__main__":

    API_URL = 'https://i.instagram.com/api/v1/'
    USER_AGENT = 'Instagram 10.26.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**DEVICE_SETTINTS)

    s = requests.Session()

    # usersdetails = [(1111,'aaaaaa'), (22222,'bbbbb'), (33333,'ccccc'), (44444,'ddddd')]
    ___USERS___
    for username, profile_id, password in usersdetails:
        Settings.profile["name"] = username
        Settings.profile["id"] = profile_id

        api = InstagramAPI(username,password)
        api.login()

        multi_logs=True
        show_logs=True
        logfolder = get_logfolder(username, multi_logs)
        logger = get_instapy_logger(show_logs)

        # user_id = '1461295173'
        user_id = api.username_id

        followers = api.getTotalFollowers(user_id)
        following = api.getTotalFollowings(user_id)
        posts = api.getTotalUserFeed(user_id)
        print(len(followers))
        print(len(following))
        print(len(posts))
        
        message = "text text text"
        user_id = 19478691
        direct_message(message, user_id)
        
        save_account_progress(username, len(followers), len(following), len(posts), logger)

        orig_stdout = sys.stdout
        f = open( username + '.out.txt', 'w')
        sys.stdout = f
        for line in followers:
            print(line)
        sys.stdout = orig_stdout
        f.close()