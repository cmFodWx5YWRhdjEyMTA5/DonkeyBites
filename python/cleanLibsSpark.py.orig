#!/usr/bin/env python

import urllib2, json, re, base64

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def deleteArtifacts(url, base64credentials, repo, group, artifact, num_versions, main_snapshot_version):
    versions = []
    paths = []
    point = re.compile("\.")
    uri = url + "/api/search/gavc?g=" + group + "&a=" \
        + artifact + "&repos=" + repo
    print ('----- uri - ' + uri)
    try:
        request = urllib2.Request(uri)
        base64string = base64.b64encode('%s:%s' % ("admin", "password"))
        request.add_header("Authorization", "Basic %s" % base64credentials)
        output = urllib2.urlopen(request)
    except Exception as e:
        print e
        return "The connection wasn't successful. Error: %s" % e

    result = output.read()
    print ('---- result' + result)
    if not result:
        return "There are no %s/%s artifacts" % \
               (re.sub(point, "/", group), artifact)

    result_json = json.loads(result)
    for path in result_json["results"]:
        artifact_path = path["uri"].split("/")
        print ('----- artifact_path     ' + str(artifact_path))
        print ('----- artifact_path[-1] ' + artifact_path[-1])
        versions.append(artifact_path[-1])

    versions = unique(versions)
    versions.sort()
    versions.sort(key=lambda s: map(str, s.split('-')))

    print("Going to leave these %s/%s artifacts untouched: %s" %
          (re.sub(point, "/", group), artifact, versions[-num_versions:]))
    # Leave the latest n versions
    del versions[-num_versions:]

    for version in versions:
        print ('---- artifact - ' + artifact)
        paths.append(url + "/" + repo + "/" + re.sub(point, "/", group) +
                     "/" + artifact + "/" + main_snapshot_version + "/"  + version)

    for path in paths:
        try:
            request = urllib2.Request(path)
            request.add_header("Authorization", "Basic %s" % base64credentials)
            request.get_method = lambda: 'DELETE'
            result = urllib2.urlopen(request)
            print "Artifact %s was deleted" % path
        except Exception as e:
            print("Couldn't delete artifact %s. Error: %s" % (path, e))
