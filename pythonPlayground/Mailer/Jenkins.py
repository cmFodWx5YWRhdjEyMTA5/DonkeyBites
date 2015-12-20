__author__ = 'dshai'

import sys
import os

sys.path.append("utils")


import git_utils
import jenkins_utils

from jenkinsapi.jenkins import Jenkins

def get_server_instance():
    jenkins_url = 'http://jenkins.tlv.c7d.net'
    server = Jenkins(jenkins_url, username = 'dshai', password = '@Ilmfvm2015')


    jenkins_url = git_utils.git_config_get(jenkins_utils.JENKINS_SERVER_URL)

    return server

if __name__ == '__main__':
    print get_server_instance().version

