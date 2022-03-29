# -*- coding: utf-8 -*-

import os
import http.server #this is python 3.4+
#import SimpleHTTPServer #this is python 2.6
import socketserver

import cbzplatterlib.utils as utils
from cbzplatterlib.PageGeneration import generateWebPage

#Global vars here:
supportedFileType = utils.supportedFileType

#End Globals

#This is for python 3.4+    
class HTTPHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        #Here is the commands to run when dealing with incoming requests.
        #I guess at the beginning index.html will exist, but clicking on a comic will require that page to be built
        #If I create a temp page (with no content) for the comic in the temp directory then I know that any page request
        # for a page in the temp directory will need to be built...

        #extra thought: need to convert from %20 to spaces... urllib.parse might be useful here
        if self.path=="/":
            self.path="/index.html"

        try:
            sendReply = True
            #Check if the image extension is supported and set the right mime type
            for imageSupported in supportedFileType:
                if self.path.endswith(imageSupported):
                    mimetype="image/"+imageSupported.lstrip(".")
                    utils.verboseOutput(3,"GET command - Path: "+self.path+" ; mimetype: "+mimetype)
                    break
            else:

            #Here we check for any additional supported files, ie .css and .html
                if self.path.endswith(".css"):
                    mimetype='text/css'
                elif self.path.endswith(".html"):
                    mimetype='text/html'
                    #Here is where I generate the file:
                    fileToUse = self.path.lstrip("/").rstrip(".html").replace('%20',' ')
                    utils.verboseOutput(3,"GET command - File: "+fileToUse+" ; replaced: "+(self.path.replace('%20',' ').lstrip("/")))
                    if os.path.isfile(fileToUse) and not os.path.isfile(self.path.replace('%20',' ').lstrip("/")):
                        generateWebPage(fileToUse)
                else:
                    sendReply = False
                                          
            if sendReply == True:
                #Open the static file requested and send it
                f = open(os.curdir + self.path.replace('%20',' '),'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())                     
                f.close()
            return
            
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
			
def runHTTPServer ( ):
    PORT_NUMBER = utils.serverport

    try:
        #Create a web server and define the handler to manage the incoming request
        server = http.server.HTTPServer(('', PORT_NUMBER), HTTPHandler)
        utils.verboseOutput(0,"Starting httpserver on port " + str(PORT_NUMBER) + ", use <Ctrl-C> to stop")
        #Wait forever for incoming http requests
        server.serve_forever()
    except KeyboardInterrupt:
        utils.verboseOutput(0,"<Ctrl-C> received, shutting down the web server")
        server.socket.close()
    return
