#!/usr/bin/python

import gdata.spreadsheet.service
import logging
import socket



email = 'doronshai@gmail.com'
password = 'Ilmbfvm2015'
weight = '180'
# Find this value in the url with 'key=XXX' and copy XXX below
spreadsheet_key = '1kqdYBt8NraGpsJ-9u-etFIsQi9CMCqy_gpUi8F-lvaY'
# All spreadsheets have worksheets. I think worksheet #1 by default always
# has a value of 'od6'
worksheet_id = 'od6'

spr_client = gdata.spreadsheet.service.SpreadsheetsService()
spr_client.email = email
spr_client.password = password
spr_client.source = 'Example Spreadsheet Writing Application'
spr_client.ProgrammaticLogin()
print"aaa"
try:
    print"bbb"
    feed = spr_client.GetListFeed(spreadsheet_key, worksheet_id)
    print"ccc"
except gdata.service.RequestError, e:
    logging.error('Spreadsheet gdata.service.RequestError: ' + str(e))
except socket.sslerror, e:
    logging.error('Spreadsheet socket.sslerror: ' + str(e))

for row_entry in feed.entry:
    record = gdata.spreadsheet.text_db.Record(row_entry=row_entry)
    print "%s,%s,%s" % (record.content['firstname'], record.content['lastname'], record.content['telephone'])


# Prepare the dictionary to write
#dict = {}
#dict['date'] = time.strftime('%m/%d/%Y')
#dict['time'] = time.strftime('%H:%M:%S')
#dict['weight'] = weight
#print dict

#entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
#if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
#    print "Insert row succeeded."
#else:
#    print "Insert row failed."