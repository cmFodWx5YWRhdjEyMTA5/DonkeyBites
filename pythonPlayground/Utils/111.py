import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
json_key = json.load(open('client_secret_568464995248-7mogtrugcsb0annifq7g3agd7ncaoo2j.apps.googleusercontent.com.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email']
                                            , bytes(json_key['private_key']
                                                    , 'utf-8')
                                            , scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('1RP9Q6_llw64Z8v43mX1IvUxsCjvhlIiU7T2kCqHRfL0')
worksheet = sh.get_worksheet(0)
val = worksheet.acell('B3').value # With label
print val