#!/usr/bin/env python
import urllib2, json, re, base64
import artifactoryGenericCleaner

# Artifactory url
url = "http://233.27.444.555:8081/artifactory"
# Artifactory repository
repo = "sbt-local-snapshot"
# Artifactory credentials encoded in base64
base64credentials = base64.b64encode('%s:%s' % ("zzzzzz", "zzzzzzzz"))
# Number of versions that should not be deleted
num_versions = 3
# The Full name of the SNAPSHOT VERSION
main_snapshot_version = "1.0.0-SNAPSHOT"
# Artifacts tuples in the format:
# [("some.group", "artifact_name")]
artifacts = [
    ("com.xxx", "budget"),
    ("com.xxx", "strategy"),
    ("com.xxx", "key"),
    ("com.xxx", "banner"),
    ("com.xxx", "static"),
    ("com.xxx", "strategybudget")
]

for group, artifact in artifacts:
    artifactoryGenericCleaner.deleteArtifacts(url, base64credentials, repo, group, artifact, num_versions, main_snapshot_version)
