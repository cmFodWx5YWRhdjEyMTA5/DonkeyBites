#!/usr/bin/env python
import urllib2, json, re, base64
import artifactoryCleaner

# Artifactory url
url = "http://222.222.222.222:8081/artifactory"
# Artifactory repository
repo = "libs-snapshot-local"
# Artifactory credentials encoded in base64
base64credentials = base64.b64encode('%s:%s' % ("zzzzzzzz", "zzzzzzz"))
# Number of versions that should not be deleted
num_versions = 10 #(2 * 5) 2 is since for each version there are 1 jar and 1 pom
# The Full name of the SNAPSHOT VERSION
main_snapshot_version = "0.0.1-SNAPSHOT"
# Artifacts tuples in the format:
# [("some.group", "artifact_name")]
artifacts = [
    ("com.xxx.aaa", "host"),
    ("com.xxx.aaa", "fraux"),
    ("com.xxx.aaa", "tracking"),
    ("com.xxx.aaa", "retarget")
]

for group, artifact in artifacts:
    artifactoryCleaner.deleteArtifacts(url, base64credentials, repo, group, artifact, num_versions, main_snapshot_version)
