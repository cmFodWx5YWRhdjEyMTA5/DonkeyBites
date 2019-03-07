from CGIHTTPServer import CGIHTTPRequestHandler
import BaseHTTPServer, SimpleHTTPServer


from http.server import HTTPServer, CGIHTTPRequestHandler
#import CGIHTTPServer

import random
import sys
import cgi

class MyRequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):
    global super_important_list
    super_important_list = range(10)
    random.shuffle(super_important_list)

    def do_POST(s):    
        """Respond to a POST request."""
        form = cgi.FieldStorage(fp=s.rfile,headers=s.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':s.headers['Content-Type'],})
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("<p>Also, super_important_list is:</p>")
        s.wfile.write(str(super_important_list))
        s.wfile.write("<p>Furthermore, you POSTed the following info: ")
        for item in form.keys():
            s.wfile.write("<p>Item: " + item)
            s.wfile.write("<p>Value: " + form[item].value)
        s.wfile.write("</body></html>")

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = CGIHTTPServer.BaseHTTPServer.HTTPServer(server_address, MyRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit()

