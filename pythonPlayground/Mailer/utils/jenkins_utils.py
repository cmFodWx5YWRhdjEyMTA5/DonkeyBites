#!/usr/bin/python
import urllib, urllib2
import sys, os, time, optparse, re
import jenkins

import logging 
from datetime import datetime

JENKINS_SERVER_URL = "jenkins.url"
JENKINS_JOB = "jenkins.job"
JENKINS_USER = "jenkins.user"
JENKINS_PASSWORD = "jenkins.password"
JENKINS_SANDBOX_JOB_UI = "jenkins.sandbox-job-ui"
JENKINS_SANDBOX_JOB_SERVER = "jenkins.sandbox-job-server"
JENKINS_TESTBOX_JOB = "jenkins.testbox-job"



class Job():
    def __init__(self, jenkinsUrl, job, token, buildWithParams=False):
        self.jenkinsUrl = jenkinsUrl
        self.jenkinsJob = "/job/" + job + "/"
        if buildWithParams:
            self.buildWith = "buildWithParameters?"
        else:
            self.buildWith = "build?"
        self.token = "token=" + token
        self.job = self.jenkinsUrl + self.jenkinsJob
        self.status = self.job + "api/python"
        self.logger = logging.getLogger()

    def waitForJob(self, timeout=1200):
        buildStatus = self.job + self.buildNumber + "/api/python"
        self.logger.debug("using url: " + buildStatus)
        response = eval(urllib2.urlopen(buildStatus).read())
        building = response['building']
        consLine = 0
        while building and timeout >= 0:
            response = eval(urllib2.urlopen(buildStatus).read())
            consLine = self.printConsole(consLine)
            time.sleep(10)
            timeout -= 10
            building = response['building']
            if timeout <= 0:
                self.logger.error("Job timeout. Job may still be running on Jenkins")
                sys.exit(1)
        if response['result'] == 'FAILURE':
                self.logger.error("Job failed!")
                sys.exit(1)
        else:
            return response['result']

    def getLastBuildNumber(self):
        return str(eval(urllib2.urlopen(self.status).read())['lastBuild']['number'])

    def isJobRunning(self):
        lastBuild = self.getLastBuildNumber()
        buildStatus = self.job + lastBuild + "/api/python"
        self.logger.debug("using url: " + buildStatus)
        return eval(urllib2.urlopen(buildStatus).read())['building']

    def isJobQueued(self):
        return eval(urllib2.urlopen(self.status).read())['inQueue']
        
    def getJobUrl(self):
        return self.job

    def getLastSuccefulBuild(self):
        return str(eval(urllib2.urlopen(self.status).read())['lastSuccessfulBuild']['number'])

    def runJob(self, params=None):
        #if self.isJobRunning():
        #    self.logger.error("job was taken by another user. Exiting")
        #    sys.exit(1)
            
        url = self.job + self.buildWith + self.token
        if params:
            url += "&" + urllib.urlencode(params)

        self.logger.debug("running job: " + self.jenkinsJob)
        self.logger.debug("using url: " + url)
        resp = urllib2.urlopen(url)
        self.logger.debug(resp)
        #self.logger.debug("sleeping 10 seconds...")
        #time.sleep(10)
        if self.isJobQueued():
            self.logger.debug("job was queued, waiting for executer")
            #while self.isJobQueued():
            #    time.sleep(10)

        self.buildNumber = self.getLastBuildNumber()
        #self.logger.debug("job run with build number " + self.buildNumber)

    def printConsole(self, fromLine):
        currText = self.getConsole().read().splitlines()
        for line in currText[fromLine:]:
            self.logger.debug(line)
        return len(currText)

    def getConsole(self):
        console = self.job + self.buildNumber + '/consoleText'
        return urllib2.urlopen(console)

def get_jenkins_url( git_config_get ):
    jenkins_url = git_config_get("jenkins.url")
    if jenkins_url == None or jenkins_url == "":
        logging.error("Jenkins URL is not set. Please use 'git config jenkins.url <actual-jenkins-url> to set it'")
        return None

    return jenkins_url


def runJob( jenkinsUrl , jobName , branch, mergeBranch , version, userMail ):
    logging.debug("run job %s, for branch %s" %(jobName , branch) )
    params={'CLOUDBAND_VERSION':version, "BRANCH":branch, "MERGE_BRANCH":mergeBranch, "USER_EMAIL": userMail}
    token = "build-cbsandbox"
    logging.debug("Job Token: %s" %token )
	
    job = Job(jenkinsUrl, jobName, token , True )

    logging.debug("Run Job..." )
    job.runJob(params)    
    number = int(job.getLastBuildNumber())+1
    logging.debug("Running Job number: %s" %number )
    return number
    '''
    if job.waitForJob(timeout=20*60) == 'SUCCESS':
        logging.debug("job finished successfuly")
    else:
        logging.error("job failed! exiting")
    '''

def disableJob(jenkinsUrl , jenkinsUser, jenkinsPassword, jobName ):

    logging.debug("Disabling job %s..." %jobName )
    j = jenkins.Jenkins(jenkinsUrl, jenkinsUser, jenkinsPassword)
    j.disable_job(jobName)

def enableJob(jenkinsUrl , jenkinsUser, jenkinsPassword, jobName ):

    logging.debug("Enabling job %s..." %jobName )
    j = jenkins.Jenkins(jenkinsUrl, jenkinsUser, jenkinsPassword)
    j.enable_job(jobName)



def main():
    try:
        loglevel=logging.DEBUG
        logging.basicConfig(level=loglevel, format="%(levelname)s: %(message)s" )
        #runJob( "http://172.29.36.7" , "test_hook" , "tiers_feature" , "tiers_test", "1.4.0" , "hanan.moiseyev@gmail.com")
        
    except Exception,e:
        print e
    

if __name__ == '__main__':
    main()
    
