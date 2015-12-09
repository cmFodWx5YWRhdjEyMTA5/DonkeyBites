import sys
import os
import logging
import urllib2
import SOAPpy
import ConfigParser
import getpass


#-----------------------------------------------------------------------------
# Jira helper functions
#


# Given a Jira server URL (which is stored in git config)
# Starts an authenticated jira session using SOAP api
# Returns a list of the SOAP object and the authentication token
def jira_start_session(jira_url):
    jira_url = jira_url.rstrip("/")
    try:
        jira_client_url = jira_url + "/rpc/soap/jirasoapservice-v2?wsdl"
        soap_client = SOAPpy.WSDL.Proxy(jira_client_url)
        soap_client.soapproxy.config.dumpFaultInfo=False
        # print "self.soap_client set", self.soap_client

    except KeyboardInterrupt:
        logging.info("... interrupted")

    except Exception, e:
        save_jira_cached_auth(jira_url, "")
        logging.error("Invalid Jira URL: '%s'", jira_url)
        logging.debug(e)
        return -1

    auth = jira_login(jira_url, soap_client)
    if auth == None:
        return (None, None)

    return (soap_client, auth)

# Try to use the cached authentication object to log in
# to Jira first. ("implicit")
# if that fails, then prompt the user ("explicit")
# for username/password
def jira_login(jira_url, soap_client):

    auth = get_jira_cached_auth(jira_url)
    if auth != None and auth != "": 
        auth = jira_implicit_login(soap_client, auth) 
    else:
        auth = None

    if auth == None:
        save_jira_cached_auth(jira_url, "")
        auth = jira_explicit_login(soap_client)


    if auth != None:
        save_jira_cached_auth(jira_url, auth)

    return auth

def jira_implicit_login(soap_client, auth):

    # test jira to see if auth is valid
    try:
        jira_types = soap_client.getIssueTypes(auth)
        return auth
    except KeyboardInterrupt:
        logging.info("... interrupted")

    except Exception, e:
        print >> sys.stderr, "Previous Jira login is invalid or has expired"
        # logging.debug(e)
        

    return None

def jira_explicit_login(soap_client):
    max_retry_count = 3
    retry_count = 0

    while retry_count < max_retry_count:
        if retry_count > 0:
            logging.info("Invalid Jira password/username combination, try again")

        # We now need to read the Jira username/password from
        # the console.
        # However, there is a problem. When git hooks are invoked
        # stdin is pointed to /dev/null, see here:
        # http://kerneltrap.org/index.php?q=mailarchive/git/2008/3/4/1062624/thread
        # The work-around is to re-assign stdin back to /dev/tty , as per
        # http://mail.python.org/pipermail/patches/2002-February/007193.html
        sys.stdin = open('/dev/tty', 'r')
        sys.stdout = open('/dev/tty', 'w')

        username = raw_input('Jira username: ')
        password = getpass.getpass('Jira password: ')

        # print "abc"
        # print "self.soap_client login...%s " % username + password
        try:
            auth = soap_client.login(username, password) 

            try:
                jira_types = soap_client.getIssueTypes(auth)
                return auth

            except KeyboardInterrupt:
                logging.info("... interrupted")

            except Exception,e:
                logging.error("User '%s' does not have access to Jira issues")
                return None

        except KeyboardInterrupt:
            logging.info("... interrupted")

        except Exception,e:
            logging.debug("Login failed")

        auth=None
        retry_count = retry_count + 1


    if auth == None:
        logging.error("Invalid Jira password/username combination")

    return auth



def jira_find_issue(issuekey, jira_soap_client, jira_auth, jira_text):
    try:
        issue = jira_soap_client.getIssue(jira_auth, issuekey)
        logging.debug("Found issue '%s' in Jira: (%s)",  
                    issuekey, issue["summary"])
        return issue

    except KeyboardInterrupt:
        logging.info("... interrupted")

    except Exception, e:
        logging.error("No such issue '%s' in Jira", issuekey)
        #logging.debug(e)
        return None

def jira_add_comment_to_issue(issuekey, jira_soap_client, jira_auth, jira_text):
    try:
        jira_soap_client.addComment(jira_auth, issuekey, {"body":jira_text})
        logging.debug("Added to issue '%s' in Jira:\n%s", issuekey, jira_text)

    except Exception, e:
        logging.error("Error adding comment to issue '%s' in Jira", issuekey)
        logging.debug(e)
        return -1


# TODO: Not fully implemented yet!
def jira_add_comment_to_and_fix_issue(issuekey, jira_soap_client, jira_text):
    return jira_add_comment_to_issue(issuekey, jira_soap_client, jira_text)




#-----------------------------------------------------------------------------
# Miscellaneous Jira related utility functions
#
def get_jira_url( git_config_get ):
    jira_url = git_config_get("jira.url")
    if jira_url == None or jira_url == "":
        logging.error("Jira URL is not set. Please use 'git config jira.url <actual-jira-url> to set it'")
        return None

    return jira_url

def get_jira_cached_auth(jira_url):
    return get_cfg_value(os.environ['HOME'] + "/.jirarc", jira_url, "auth")

def save_jira_cached_auth(jira_url, auth):
    return save_cfg_value(os.environ['HOME'] + "/.jirarc", jira_url, "auth", auth)
    
#---------------------------------------------------------------------
# Misc. helper functions
#
def get_gitweb_url():
    return git_config_get("gitweb.url")

def get_cfg_value(cfg_file_name, section, key):
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read(cfg_file_name)
        value = cfg.get(section, key)
    except:
        return None
    return value
    

def save_cfg_value(cfg_file_name, section, key, value):
    try:
        cfg = ConfigParser.SafeConfigParser()
    except Exception, e:
        logging.warning("Failed to instantiate a ConfigParser object")
        logging.debug(e)
        return

    try:
        cfg.read(cfg_file_name)
    except Exception, e:
        logging.warning("Failed to read .jirarc")
        logging.debug(e)
        return

    try:
        cfg.add_section(section)
    except ConfigParser.DuplicateSectionError,e:
        logging.debug("Section '%s' already exists in '%s'", section, cfg_file_name)

    try:
        cfg.set(section, key, value)
    except Exception,e:
        logging.warning("Failed to add '%s' to '%s'", key, cfg_file_name)
        logging.debug(e)

    try:
        cfg.write(open(cfg_file_name, 'wb'))
    except Exception, e:
        logging.warning("Failed to write '%s'='%s' to file %s", key, value, cfg_file_name)
        logging.debug(e)
        return

# given a string, executes it as an executable, and returns the STDOUT
# as a string
def get_shell_cmd_output(cmd):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        return proc.stdout.read().rstrip('\n')
    except KeyboardInterrupt:
        logging.info("... interrupted")

    except Exception, e:
        logging.error("Failed trying to execute '%s'", cmd)
