# coding: utf8
import urllib2

# ON ENV THE LANG VARIABLE NEED TO BE UTF-8

response = urllib2.urlopen('http://pod.icast.co.il/1ab9a811-5b99-4512-a42f-21023817fb1e.icast.mp3')
html = response.read()

file="מיכה פורטוגלי - בקלפיות לקראת הבחירות, סבתא מוגזת.mp3"

CHUNK = 16 * 1024
with open(file, 'wb') as f:
    while True:
        chunk = response.read(CHUNK)
        if not chunk: break
        f.write(chunk)