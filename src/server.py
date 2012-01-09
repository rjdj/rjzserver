####################################################################################
#
#	RjzServer
#	By Chris McCormick
# 	GPLv3
#
#	See the files README and COPYING for details.
#
#       Modified by Christian Haudum for Reality Jockey Ltd.
#       2012
#
#
#       -*- coding: utf-8 -*-
#       vim: set fileencodings=utf-8
#
####################################################################################


__docformat__ = "reStructuredText"

from os import listdir, path, environ, sep
import zipfile
from cStringIO import *
from sys import argv
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket
from time import sleep
from config import config
import webbrowser

from mako.template import Template

if environ.has_key('RESOURCEPATH'):
    BASE_DIR = path.join(path.dirname(environ['RESOURCEPATH']),"Resources")
else:
    BASE_DIR = path.join(path.dirname(__file__),"resources")

MEDIA_DIR = path.join(BASE_DIR, "media")
TEMPLATE_DIR = path.join(BASE_DIR, "templates")

PORT = 8314

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('91.121.94.180', 80)) # doesn't matter if it fails
    addr = s.getsockname()[0]
    s.close()
    return addr

def zipall(d, zip, base=""):
    for f in [dir for dir in listdir(path.join(base, d)) if dir[0] != "."]:
        z = path.join(d, f)
        if path.isdir(path.join(base, z)):
            zipall(z, zip, base)
        else:
            zip.write(path.join(base, z), z)

def zipdir(rjdir, base, fp):
    zip = zipfile.ZipFile(fp, 'w')
    zipall(rjdir, zip, base=base)

class RjzHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        urlpath = self.path
        if urlpath.startswith("http://"):
            urlpath = "/" + "/".join(urlpath.split("/")[3:])
        if urlpath.endswith(".rjz"):
            self.send_response(200)
            self.send_header('Content-type', 'application/zip')

            rjzfile = path.basename(urlpath)
            # if this is a directory then zip it up
            if path.isdir(path.join(config.Get("scenedir", default="."), rjzfile[:-1])):
                tmpfile = StringIO()
                zipdir(rjzfile[:-1], config.Get("scenedir", default="."), tmpfile)
                tmpfile.seek(0)
                rjz = tmpfile.read()
                tmpfile.close()
            else:
                rjz = file(path.join(config.Get("scenedir", default="."), rjzfile)).read()

            self.send_header('Content-length', len(rjz))
            self.end_headers()

            self.wfile.write(rjz)
            return
        elif urlpath.startswith("/media"):
            # really insecure mini media server
            diskfile = MEDIA_DIR + sep.join(urlpath[len("/media"):].split("/"))
            print "diskfile", diskfile
            if path.isfile(diskfile):
                types = {"jpeg": "jpeg", "jpg": "jpeg", "gif": "gif", "png": "png"}
                for t in types:
                    if urlpath[-len(t):].lower() == t:
                        contentType = "image/" + t
                if urlpath[-3:].lower() == "css":
                    contentType = "text/css"
                if contentType:
                    content = file(diskfile).read()
                    self.send_response(200)
                    self.send_header('Content-type', contentType)
                    self.send_header('Content-length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_response(404)
                    self.wfile.write("Don't support files of that type")
            else:
                self.send_response(404)
                self.wfile.write("%s does not exist" % urlpath)
            return
        else:
            config.SetFilename("rjzserver.cfg")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            rjzs = [d + (d[-3:] == ".rj" and "z" or "") for d in listdir(config.Get("scenedir", default=".")) if d[-3:] == ".rj" or d[-4:] == ".rjz"]

            tpl_file = path.join(TEMPLATE_DIR, "index.html")
            print "tpl_file", tpl_file
            tpl = Template(file(tpl_file).read()).render(rjzs=rjzs, headers=self.headers, listen=self.server.listen)
            self.wfile.write(tpl)
            return
        return

    def log_message(self, format, *args):
        self.server.Output("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), format%args))

class RjzServer(HTTPServer):
    def __init__(self, outputfn):
        config.SetFilename("rjzserver.cfg")
        self.Output = outputfn
        listen = (getIP(), PORT)
        self.listen = listen
        HTTPServer.__init__(self, listen, RjzHandler)
        self.Output("RjzServer launched")
        self.Output("Listening on http://%s:%d/" % listen)
        webbrowser.open("http://%s:%d/" % listen)
        self.Output("Using directory %s" % config.Get("scenedir", default="."))
        self.Output("Select Help from the File menu for instructions on how to use RjzServer!")
        self.quit = False

    def Launch(self):
        self.serve_forever()

if __name__ == '__main__':
    def Output(txt):
        print txt
    server = RjzServer(outputfn=Output)
    try:
        server.Launch()
    except KeyboardInterrupt:
        server.Output("Shutting down RjzServer")


