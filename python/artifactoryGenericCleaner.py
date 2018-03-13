#!/usr/bin/env python

import urllib2, json, re, base64, requests
from lxml import html 
from bs4 import BeautifulSoup

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def deleteArtifacts(url, base64credentials, repo, group, artifact, num_versions, main_snapshot_version):
    versions = []
    paths = []
    point = re.compile("\.")    
    group = group.replace(".","/")
    uri = url + "/" + repo + "/" + group + "/" + artifact + "/" +  main_snapshot_version

    # print ('----- uri - ' + uri)
    
    raw  = requests.get(uri)
    data = raw.text
    soup = BeautifulSoup(data, "lxml")
    for link in soup.find_all('a'):
        versions.append(link.get('href'))
        # print (link.get('href'))
    # print ('------------------------------------------------------')

    versions = unique(versions)
    versions.sort()
    versions.sort(key=lambda s: map(str, s.split('-')))

    print("Going to leave these %s/%s artifacts untouched: %s" %
          (re.sub(point, "/", group), artifact, versions[-num_versions:]))
    # Leave the latest n versions

    del versions[0]    
    del versions[-num_versions:]

    for version in versions:
        paths.append(uri + "/"  + version)
        # print (uri + "/"  + version)

    for path in paths:
        try:
            request = urllib2.Request(path)
            request.add_header("Authorization", "Basic %s" % base64credentials)
            request.get_method = lambda: 'DELETE'
            result = urllib2.urlopen(request)
            print "Artifact %s was deleted" % path
            # print "Path is -> %s" % path

        except Exception as e:
            print("Couldn't delete artifact %s. Error: %s" % (path, e))
