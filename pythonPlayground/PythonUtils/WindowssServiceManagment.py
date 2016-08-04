#!/usr/bin/python

# needs win32all, or ActiveState's ActivePython distribution
import win32serviceutil
import os
import sys

def service_running(service, machine):
    return win32serviceutil.QueryServiceStatus(service, machine)[1] == 4

def service_info(action, machine, service):
    running = service_running(service, machine)
    servname = 'service (%s) on machine(%s)'%(service, machine)
    action = action.lower(  )
    if action == 'stop':
        if not running:
            print "Can't stop, %s not running"%servname
            return 0
        win32serviceutil.StopService(service, machine)
        running = service_running(service, machine)
        if running:
            print "Can't stop %s (???)"%servname
            return 0
        print '%s stopped successfully' % servname
    elif action == 'start':
        if running:
            print "Can't start, %s already running"%servname
            return 0
        win32serviceutil.StartService(service, machine)
        running = service_running(service, machine)
        if not running:
            print "Can't start %s (???)"%servname
            return 0
        print '%s started successfully' % servnam
    elif action == 'restart':
        if not running:
            print "Can't restart, %s not running"%servname
            return 0
        win32serviceutil.RestartService(service, machine)
        running = service_running(service, machine)
        if not running:
            print "Can't restart %s (???)"%servname
            return 0
        print '%s restarted successfully' % servname
    elif action == 'status':
        if running:
            print "%s is running" % servname
        else:
            print "%s is not running" % servname
    else:
        print "Unknown action (%s) requested on %s"%(action, servname)

if __name__ == '__main__':

    machine=os.environ['COMPUTERNAME']

    # Read command line args

    action=sys.argv[1]

    with open('serviceList.txt', 'rU') as file:
        services = [line.rstrip('\n') for line in file]

    for service in services:
        service_info(action, machine, service)
