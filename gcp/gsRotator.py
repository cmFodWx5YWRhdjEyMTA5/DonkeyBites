#!/usr/bin/python

# Take the credentials of the storage and put them using gsutils config -a
# If configuration exists it can be deleted by delete .boto file
#    GOOGFKUTD7EGUKER3TIE
#    Qv5b/outIULq4UAiAk4CFIWyugjT6qkLF7brhiM9

import boto
from operator import itemgetter

ROTATOR_QUOTA=20
BUCKET='ensilobackup'
GOOGLE_STORAGE = 'gs'
LOCAL_FILE = 'file'

d = {}

uri = boto.storage_uri(BUCKET, GOOGLE_STORAGE)
for obj in uri.get_bucket():
  print '%s://%s/%s' % (uri.scheme, uri.bucket_name, obj.name)
  object_uri = boto.storage_uri(BUCKET + '/' + obj.name, GOOGLE_STORAGE)
  key = object_uri.get_key()
  date = key.last_modified
  print ' Last mod:\t%s' % date
  id = key.etag.strip('"\'') #Remove surrounding quotes
  print ' MD5:\t%s' % id
  d[id] = date

print '------------------------------'

print sorted(d.items(),key=itemgetter(1),reverse=False)[0]

print len(d)

files_to_delete = 0

if len(d) <= ROTATOR_QUOTA:
  print "Amount of backup files is %d, which is ok. Limit is %d" % (len(d),ROTATOR_QUOTA)
  exit(0)
else:
  files_to_delete = len(d) - ROTATOR_QUOTA

print "files to delete - " + str(files_to_delete)

for x in range(0, files_to_delete):
  print "x is " + str(x)
  print "Delete item " + str(sorted(d.items(),key=itemgetter(1),reverse=False)[x])

  uri = boto.storage_uri(BUCKET, GOOGLE_STORAGE)
  for obj in uri.get_bucket():

    object_uri = boto.storage_uri(BUCKET + '/' + obj.name, GOOGLE_STORAGE)
    key = object_uri.get_key()
    id = key.etag.strip('"\'')  # Remove surrounding quotes

    if id == sorted(d.items(),key=itemgetter(1),reverse=False)[x]:
      print 'Deleting object: %s...' % obj.name
      # obj.delete()
