# coding: utf8

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage
import requests, gspread, os, ast, httplib2, argparse
from oauth2client.client import SignedJwtAssertionCredentials


CLIENT_ID = '568464995248-7mogtrugcsb0annifq7g3agd7ncaoo2j.apps.googleusercontent.com'
CLIENT_SECRET = 'pBcI7mRsyNLU5crblbE_I2a8'
EMAIL='doronshai@gmail.com'
REFRESH_TOKEN = '1/A-1asHCzHXzEIb_lTG6tAIqOyUYFF3uopNs-Lo8hLInBactUREZofsF9C7PrpE-j'


def authenticate_google_docs():
    f = file(os.path.join('EveningShowDownloader-ea356c3a9323.p12'), 'rb')
    SIGNED_KEY = f.read()
    f.close()
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(EMAIL, SIGNED_KEY, scope)

    data = {
        'refresh_token' : REFRESH_TOKEN,
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
        'grant_type' : 'refresh_token',
        }

    r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)

    print credentials.access_token
    credentials.access_token = ast.literal_eval(r.text)['access_token']

    gc = gspread.authorize(credentials)
    return gc


flow = OAuth2WebServerFlow(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    scope = 'https://spreadsheets.google.com/feeds',
    redirect_uri = 'http://localhost:8080',
   # access_type = 'offline',
   # approval_prompt = 'auto',
    #   redirect_uri = 'http://example.com/auth_return'
)


storage = Storage('creds.data')
credentials = run(flow, storage)



gc = authenticate_google_docs()

sh = gc.open_by_key('1RP9Q6_llw64Z8v43mX1IvUxsCjvhlIiU7T2kCqHRfL0')
worksheet = sh.get_worksheet(0)
val = worksheet.acell('B3').value # With label
print val