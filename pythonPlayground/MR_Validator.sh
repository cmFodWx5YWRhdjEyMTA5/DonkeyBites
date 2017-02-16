#!/usr/bin/env python

import sys
import re
import string

# This code-review Validator will let us find merge commits that were not reviewed by a different developer than the commit author.
# a valid commit will contain an up-vote at least from one developer which is not the author and is not the Jenkins voter (called xxx-build)
# in case it will find Merge commits that are no valid, the output will list these commits and the owner of it.
# This code will be used by Jenkins jobs when Jenkins will identify new merge commits in master.
# Expected Usage:
#       git log <OLDER_COMMIT>..<NEWER_COMMIT> --merges --format="COMMIT||||%h||||%an||||%ae||||%B" | ./codereview_validator.py | tee messages.txt
#       --merges:                   In order to filter out all the non merge commits
#       --format="COMMIT||||...":   This syntax is critical for the validator to work.
#                                   The "COMMIT" prefix shouldn't be replaced
#                                   The "||||" separator shouldn't be replaced


# array to store dict of commit data
commits = []
def check_approved_well(commit, message_lines):
    if len(message_lines) == 0:
        return
    for line in message_lines:
        approved_by = re.match('\s*\+1: (.*)', str(line), re.IGNORECASE)
        if approved_by:
            m = approved_by.group(1)
            commit['approved_by'] = m.split(",")
            for name in (commit['author'], 'build-xxx'):
                if name in commit['approved_by']:
                    commit['approved_by'].remove(name)

def parse_commit_log(message_lines):
    # dict to store commit data
    commit = {'approved_by': []}

    # iterate lines and save
    for next_line in message_lines:
        if not next_line.strip():
            # ignore empty lines
            pass
        elif bool(re.match('^COMMIT', next_line)):
            # commit xxxx
            # check_approved_well(commit, message_lines)
            if len(commit) != 0:            ## new commit, so re-initialize
                    commit = {'approved_by': [], 'message': []}
            s = next_line.split("||||")
            commit['hash'] = s[1]
            commits.append(commit)
            commit['author'] = s[2]
            commit['email'] = s[3]
            commit['message'].append(str(s[4]))
            message_lines =  [s[4].split('\n')]
            if bool(re.match('Merge remote-tracking', str(s[4]), re.IGNORECASE)):
                commits.remove(commit)
        else:
            message_lines.append(next_line)
            commit['message'].append(next_line)
            check_approved_well(commit, message_lines)

if __name__ == '__main__':
    parse_commit_log(sys.stdin.readlines())
    list_to_notify = []

    #print commits
    print 'Author'.ljust(15) + '  ' + 'Email'.ljust(30) +'  ' + 'Hash'.ljust(16) + '  ' + 'Message'.ljust(60    ) + '  ' + 'Approved by'.ljust(20)
    print "================================================================================================================================================="
    for commit in [commit for commit in commits if len(commit['approved_by']) == 0]:
        print commit['author'].ljust(15) + '  ' + commit['email'][:30].ljust(30) + '  ' +  commit['hash'][:16].ljust(16) + '  ' + str(commit['message'])[:60].ljust(60) + '  ' + str(commit['approved_by'])
        list_to_notify.append(commit['email'])

    if len(list_to_notify) > 0:
        with open('list_to_notify.txt', 'w') as list_to_notify_file:
            list_to_notify_file.write("EMAIL_LIST=")
            list_to_notify_file.write(",".join(set(list_to_notify)))
