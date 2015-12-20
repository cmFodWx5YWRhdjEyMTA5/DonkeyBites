import sys
import os
import subprocess
import time
import traceback
import re
import logging

COMMITS_LIMIT = 'hook.max.commits'
MAILINGLIST = 'hooks.mailinglist'
EMAILPREFIX = 'hooks.emailprefix'
SMTP_SUBJECT = 'hooks.smtp-subject'
SMTP_HOST = 'hooks.smtp-host'
SMTP_PORT = 'hooks.smtp-port'
SMTP_SENDER = 'hooks.smtp-sender'
SMTP_REPLY_TO = 'hooks.smtp-replay'
SMTP_SENDER_PASSWORD = 'hooks.smtp-sender-password'
SANDBOX_LOGFILE = 'hooks.sandbox-logfile'
SANDBOX_HOOK_BRANCHES = 'hook.branches'
SANDBOX_HOOK_BLOCKEDBRANCHES = 'hook.blockedbranches'
SANDBOX_HOOK_BRANCH_PATTERN = "hook.branch.src.pattern"
SANDBOX_HOOK_BRANCH_TEST_PATTERN = "hook.branch.test.pattern"
SANDBOX_HOOK_SUPER_USERS = "hook.super.users"
SANDBOX_VERSION = "hook.sandbox.version"

FLD_EMAIL="Email"
FLD_AUTHOR="Author"
FLD_JIRA="Jira"
FLD_COMMENT="Comment"
    

class GitMessage(object):
    
    raw_msg=""
    fields = dict()
    def __init__(self, msg ):
        raw_msg = msg
        msgLines = msg.split('\n')
        logging.debug("Git message:%s" %msgLines )
        self.fields[FLD_AUTHOR] = self.extractField( 'Author:\s+(.+) <' , msg)
        self.fields[FLD_EMAIL] = self.extractField( 'Author: .+<(.+)>' , msg )
        self.fields[FLD_JIRA] = self.extractField( 'Jira:\s*(.+)' , msg )
        if len(self.fields.get(FLD_JIRA)) == 0:
            self.fields[FLD_JIRA] = self.extractField( '(DEV-[0-9]+)' , msg )
            if len(self.fields.get(FLD_JIRA)) == 0:
                self.fields[FLD_JIRA] = self.extractField( '([A-Z]+-[0-9]+)' , msg )
                
        # Message breadown by lines for improved fields extraction
        content=""
        msg_raw_fields = msg.split("\n")
        for raw_field in msg_raw_fields:
            field_name = self.extractField( '([a-zA-Z0-9]+):' , raw_field )
            if field_name != None and len(field_name)>0 and self.fields.get(field_name) == None:
                self.fields[field_name.lower().title()] = self.extractField( ':\s*(.+)' , raw_field )
            else:
                content += self.extractField( '\b(.+)' , raw_field )
        
        if len(content) > 0 :
            self.fields[FLD_COMMENT] = content  
        #self.fields['reviewer'] = self.extractField( 'Reviewer: (.+)' , msg )
        #self.fields['changes'] = self.extractField( 'Changes: (.+)' , msg )
        #self.fields['tests'] = self.extractField( 'Tests: (.+)' , msg )
        


    def extractField( self , charset , inText ):
        match = re.search(charset, inText)
        if match == None:
            #logging.debug("did not find " + charset)
            return ""

        return match.group(1)


    def field( self,name):
        return self.fields[name]

    def __str__( self ):
        msg_str = 'GitMessage['
        msg_str += str(self.fields)
        msg_str += ']'
        return msg_str

def git_rev_parse(hash, short=False):
    args = ['git', 'rev-parse']
    if short:
        args.append('--short')
    args.append(hash)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    # Cut off the last \n character.
    return p.stdout.read()[:-1]
    
##This function will list the files modified in a given commit
def get_files_list_in_commit(commit_id):
    p = subprocess.Popen(['git','show', '--pretty=oneline' , '--name-only' , commit_id ], stdout=subprocess.PIPE)
    # Cut off the last \n character.
    return p.stdout.read()[:-1]

## This Function will return the component name involved in a given commit
## The results are: ui, server, error
def get_commit_component_name(commit_id):
    files_list = get_files_list_in_commit(commit_id)
    logging.debug("files_list: "+str(files_list))
    ui_flag = 0
    server_flag = 0
    ui_string = "al-portal"
    html_string = "al-html"
    commit_component_name = "Empty"
    for l in files_list.split("\n"):
        ##Check that the line is a path - See that there is no spaces
        if not " " in l:
            ##Check if it's UI_string
            if ui_string in l or html_string in l:
                ui_flag = 1
            else:
                server_flag = 1
    if ui_flag == 1 and server_flag ==0:
        return "ui"
    if ui_flag == 0 and server_flag ==1:
        return "server"
    if ui_flag == server_flag:
        return "error"
        
def get_commit_info(hash):
    p = subprocess.Popen(['git', 'show', '--pretty=format:%s%n%h', '-s', hash], 
                         stdout=subprocess.PIPE)
    s = StringIO(p.stdout.read())
    def undefined(): 
        return 'undefined'
    info = defaultdict(undefined)
    for k in ['message', 'hash']:
        info[k] = s.readline().strip()
    return info

def get_branch_name(ref_name):
    proc = subprocess.Popen(['git','rev-parse','--symbolic','--abbrev-ref',ref_name], stdout=subprocess.PIPE)
    name = proc.stdout.read()
    name = name.rstrip('//')
    name = os.path.basename(name)
    name = name.rstrip()
    #return name[:-1]
    return name

def get_push_user():
    return os.environ['GL_USER'] or ""

def parse_receive_line(l):
    return l.split()
    
# given a string, executes it as an executable, and returns the STDOUT
# as a string
def get_shell_cmd_output(cmd):
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        msg = GitMessage(proc.stdout.read())
        return msg
    except KeyboardInterrupt:
        print "... interrupted"

    except Exception, e:
        print "Failed trying to execute ", cmd, e


def git_get_commit_msg(commit_id):
    #'--format="Author: %an%n Email: %ae%n Subject: %s"'
    return get_shell_cmd_output(['git','rev-list', '--pretty=medium' , '--max-count=1' , commit_id ])
    

def git_config_get(name):
    p = subprocess.Popen(['git', 'config', '--get', name], 
                         stdout=subprocess.PIPE)
    # Cut off the last \n character.
    return p.stdout.read()[:-1]

def git_show(hash):
    p = subprocess.Popen(['git', 'show', hash], stdout=subprocess.PIPE)
    return p.stdout.read()


def get_config_variables():
    def optional(variable):
        config[variable] = git_config_get(variable)
    def required(variable, type_=str):
        v = git_config_get(variable)
        if not v:
            raise RuntimeError('This script needs %s to work.' % variable)
        config[variable] = type_(v)
    def recipients(variable):
        v = git_config_get(variable)
        config[variable] = [r for r in re.split(' *, *| +', v) if r]

    config = {}
    optional(EMAILPREFIX)
    optional(SMTP_SUBJECT)
    required(SMTP_HOST)
    required(SMTP_PORT, int)
    required(SMTP_SENDER)
    required(SMTP_SENDER_PASSWORD)
    required(SMTP_REPLY_TO)
    recipients(MAILINGLIST)
    return config

def get_commits(old_rev, new_rev):
    p = subprocess.Popen(['git', 'log', '--pretty=format:%H', '--reverse',  
                          '%s..%s' % (old_rev, new_rev)], 
                         stdout=subprocess.PIPE)
    return p.stdout.read().split('\n')

def post_receive(mailer, subject_prefix, old_rev, new_rev, ref_name , subject_template=None ):
    lines = sys.stdin.readlines()
    commits = {}
    logging.info( "post_receive lines:%s,%s,%s" , old_rev, new_rev, ref_name );
    commits[ref_name] = get_commits(old_rev, new_rev)
    logging.info( "pre commit_receive" );
    process_commits(commits, mailer, subject_prefix, subject_template)
    logging.info( "post post_receive" );

def process_commits(commits, mailer, subject_prefix, subject_template):
    for ref_name in commits.keys():
        logging.info( "process commits- %s" , ref_name )
        use_index = len(commits[ref_name]) > 1
        if not subject_template:
            subject_template = ('%(prefix)s %(ref_name)s commit ' + 
                                ('(#%(index)s) ' if use_index else '') +
                                '%(hash)s')
        for i, commit in enumerate(commits[ref_name]):
            info = get_commit_info(commit)
            info['ref_name'] = ref_name
            info['prefix'] = subject_prefix
            info['index'] = i + 1
            subject = subject_template % info
            message = git_show(commit)
            match = re.search(r'Author: (.+)', message)
            assert match
            reply_to = match.group(1)
            mailer.send(subject, reply_to, message)

