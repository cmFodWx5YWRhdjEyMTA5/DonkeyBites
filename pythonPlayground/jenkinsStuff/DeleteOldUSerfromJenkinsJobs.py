#!/usr/bin/python
__author__ = 'Doron Shai'

from genericpath import isdir
from glob import glob
import os, sys

def inplace_change(filename, old_string, new_string):
    s=open(filename).read()
    if old_string in s:
        print 'Changing "{old_string}" to "{new_string}"'.format(**locals())
        s=s.replace(old_string, new_string)
        f=open(filename, 'w')
        f.write(s)
        f.flush()
        f.close()
    else:
        print 'No occurances of "{old_string}" found.'.format(**locals())

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

mypath = '/opt/jenkins/jobs'


result = [y for x in walklevel(mypath) for y in glob(os.path.join(x[0], 'config.xml'))]
#print (result)
for s in result:
   #inplace_change(s, 'name@company.com', '');
   print (s)
