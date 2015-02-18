# 
# Example file for parsing and processing HTML
# (For Python 3.x, be sure to use the ExampleSnippets3.txt file)

import os
import sys
import subprocess

def printdir(dir):
    filenames = os.listdir(dir)
    for filename in filenames:
        print (filename)  ## foo.txt
        print (os.path.join(dir, filename)) ## dir/foo.txt (relative to current dir)
        print (os.path.abspath(os.path.join(dir, filename))) ## /home/nick/dir/foo.txt
    
## Given a dir path, run an external 'ls -l' on it --
## shows how to call an external program
def listdir(dir):
    cmd = 'dir ' + dir
    print ("Command to run:", cmd)   ## good to debug cmd before actually running it
    (status, output) = subprocess.getstatusoutput(cmd)
    if status:    ## Error case, print the command's output to stderr and exit
        sys.stderr.write(output)
        sys.exit(1)
    print (output)  ## Otherwise do something with the command's output

def main():
    print ("aaaaa")
    # Echo the contents of a file
    f = open('foo.txt', 'rU')
    for line in f:  ## iterates over the lines of the file
        print (line,) ## trailing , so print does not add an end-of-line char
                    ## since 'line' already includes the end-of line.
    f.close()
    
    printdir("c:\\Users")
    listdir("c:\\Users")
    
    
    
    
        
if __name__ == "__main__":
  main();  