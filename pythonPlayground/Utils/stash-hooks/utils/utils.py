#!/usr/local/bin/python2.7

from __future__ import with_statement

import re
import smtplib
import subprocess
import sys
import time
import traceback
import logging
from collections import defaultdict
from email.mime.text import MIMEText
from StringIO import StringIO

import git_utils
import jenkins_utils

class Mailer(object):
    def __init__(self, smtp_host, smtp_port,
                 sender, sender_password, recipients, replay_to):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender = sender
        self.sender_password = sender_password
        self.recipients = recipients
        self.replay_to  = replay_to

    def send(self, subject, send_to, message):
        if not self.recipients:
            return

        mime_text = MIMEText(message, _charset='utf-8')
        mime_text['From'] = self.sender
        mime_text['Reply-To'] = self.replay_to
        mime_text['To'] = send_to
        mime_text['Cc'] =  ",".join(self.recipients)
        mime_text['Subject'] = subject
        
        all_recipients = [send_to] + self.recipients 

        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.sendmail(self.sender, all_recipients, 
                        mime_text.as_string())
        #server.rset()
        server.quit()


def init_mailer():
    
    # Get mail configuration
    config = git_utils.get_config_variables()
    mailer = Mailer(config[git_utils.SMTP_HOST], config[git_utils.SMTP_PORT],config[git_utils.SMTP_SENDER], config[git_utils.SMTP_SENDER_PASSWORD],config[git_utils.MAILINGLIST], config[git_utils.SMTP_REPLY_TO])
    
    return mailer


     
def init_logger():    
    log_file_path = git_utils.git_config_get(git_utils.SANDBOX_LOGFILE)
    log_level = logging.DEBUG 
    
    logging.basicConfig(level = log_level)
    formatter = logging.Formatter("%(levelname)s %(asctime)s (%(module)s)  - %(message)s")
    handler = logging.FileHandler( filename=log_file_path )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler( handler )
    logging.getLogger().handlers[0].setLevel( logging.ERROR )

def run( lines , version , old_rev , new_rev , user ,ref_name , test ):

    # Create mail message
    mailer = init_mailer()
    gitMessage = git_utils.git_get_commit_msg( new_rev )
    
    jenkins_url = git_utils.git_config_get(jenkins_utils.JENKINS_SERVER_URL)
    jenkins_job = git_utils.git_config_get(jenkins_utils.JENKINS_JOB)
   
    branches = git_utils.git_config_get(git_utils.SANDBOX_HOOK_BRANCHES)
    branch_src_pattern = git_utils.git_config_get(git_utils.SANDBOX_HOOK_BRANCH_PATTERN)
    branch_test_pattern = git_utils.git_config_get(git_utils.SANDBOX_HOOK_BRANCH_TEST_PATTERN)
    logging.debug("Branches: [%s], branch_src_pattern:[%s], branch_test_pattern:[%s]" %(branches, branch_src_pattern, branch_test_pattern) )

    if branch_src_pattern == None or branch_src_pattern == "" or branch_test_pattern == "" or branch_test_pattern == None:
	logging.error( "Missing configuration parameter for branch suffix [_stg_] or [_test_]")
	return
#    user = git_utils.get_push_user()
    super_users = git_utils.git_config_get(git_utils.SANDBOX_HOOK_SUPER_USERS).split(",")    	
    curBranchName = git_utils.get_branch_name(ref_name)
    logging.debug("Current branch name:[%s]" %curBranchName )
    for branch in branches.split(','):
    	if (curBranchName.find(branch+branch_src_pattern) == 0 or curBranchName.find(branch+branch_test_pattern) == 0) and curBranchName != branch :
		logging.debug("In branches branch name:%s" %curBranchName )
		send_to = gitMessage.fields[git_utils.FLD_EMAIL]
		if curBranchName.find(branch+branch_test_pattern) == 0:
			jenkins_job = "testbox"
			jobNumer = jenkins_utils.runJob( jenkins_url , jenkins_job , curBranchName ,branch , curBranchName, send_to )
			logging.debug( "Job started running. %s/job/%s/%s/" %(jenkins_url,jenkins_job,jobNumber))
			mailer.send(subject, send_to, message)
			break
		if test == "true":
			break
			# Check which component this is
		comps=[]
		for commitID in git_utils.get_commit_list_in_branch_not_in(curBranchName,branch).split("\n"):
			comps.append(git_utils.get_commit_component_name(commitID))
			logging.debug("The commitId:[%s]" %commitID )
		logging.debug("The org commitId:[%s]" %new_rev )
		comp_name  = set(comps)
		logging.debug("The component:[%s]" %comp_name )
		if len(comp_name)==1 and "ui" in comp_name :
			jenkins_job = "sandbox-ui"
		elif len(comp_name)==1 and "server" in comp_name:
			jenkins_job = "sandbox-server"
		elif len(comp_name)==2 or "error" in comp_name :
			if user in super_users:
				comp_name.remove("error")
				comp_name.add("super_user")
				jenkins_jobs = ["sandbox-server","sandbox-ui"]
			else:
				jenkins_job = ""
		if branch != "dev":
			jenkins_job = "branch-" + jenkins_job
			# Prepare the mail fields
		subject = "[git sandbox] branch %s build queued" %(curBranchName)
		message = "Git commit message:"
		for field,value in gitMessage.fields.items():
			message += "\n\t%s: %s" %(field,value)
		message += "\n\nHook info"
		message += "\n\tVersion: %s" %version
		message += "\n\tlines:%s" %lines
		logging.debug("The jenkins_job:[%s]" %jenkins_job )

		if jenkins_job != "" and "error" not in comp_name :
			jobNumber = jenkins_utils.runJob( jenkins_url , jenkins_job , curBranchName , branch , curBranchName, send_to )
			logging.debug( "Job started running. %s/job/%s/%s/" %(jenkins_url,jenkins_job,jobNumber) )
		if "super_user" in comp_name:
			for jenkins_job in jenkins_jobs:
				jobNumber = jenkins_utils.runJob(jenkins_url, jenkins_job, curBranchName, branch, curBranchName, send_to)
				logging.debug("Job started running. %s/job/%s/%s/" % (jenkins_url, jenkins_job, jobNumber))
		if "error" in comp_name :
			subject = "[git sandbox] Your commit includes changes to both Server and UI"
			message = "Your commit is rejected"
			# send mail
		mailer.send(subject, send_to, message)
		break

