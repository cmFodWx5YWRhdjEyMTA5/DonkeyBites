import  os

def dump_online_to_file():
    print "Content-Type: text/plain\n\n"
    for key in os.environ.keys():
        print "%30s %s \n" % (key,os.environ[key])


if __name__ == '__main__':

    dump_online_to_file()
