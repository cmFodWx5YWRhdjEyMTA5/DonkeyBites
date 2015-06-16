import urllib
import requests
import json
import sys
import urllib
import zipfile

def printResults(data):
  theJSON = json.loads(data)
  print (theJSON["version"])

  
def buildURL(id):
    myURL='https://clients2.google.com/service/update2/crx?response=redirect&os=win&arch=x86&nacl_arch=x86-64&prod=chromecrx&prodchannel=stable&prodversion=40.0.2214.93&lang=en-US&x=id%3D' + str(id) + '%26v%3D0.0.0.0%26uc'
    return myURL

def downloadFile(url):
    urllib.urlretrieve(url,'test.crx')

def extractFile(file):
    with zipfile.ZipFile(file, "r") as z:
        z.extractall("archive")

def main():

    #First argument can be pbjikboenpfhbbejgkoklgkhjpfogcam
    currentUrl = buildURL(sys.argv[1])
    downloadFile(currentUrl)
    extractFile('test.crx')

    file = open('archive\manifest.json', 'r')

    jsonData = file.read()
    printResults(jsonData)

if __name__ == "__main__":
  main()