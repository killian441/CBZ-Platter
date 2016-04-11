# -*- coding: utf-8 -*-

import os
import zipfile #for zipfile manipulation
import tempfile #For temp file operations
import http.server #this is python 3.4
#import SimpleHTTPServer #this is python 2.6
import socketserver
from string import Template #template for HTML generation

from cbzplatterlib.utils import filesToRemove
from cbzplatterlib.CBZHandler import zipListIndex

#Global vars here:
supportedFileType = ('.jpg','.jpeg','.gif','.png','.bmp')
blankGIF = "data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
verboseLevel = 3 #Levels 0 = suppress error reporting, 1 = print errors but not much else, 2 = print most stuff, 3 = debug
#End Globals

def generateIndexHTML ( fileList ): #Generate index.html, input is list of zip files
    #Ideally I'd like this function to take a list of zip files (names only, not full paths) and generate
    #an index.html and stylesheet.css as well as thumbnails for all zip files, and return a list of 
    #all temporary files and directories created (both for manipulation and for cleanup reasons).
    currentDir=os.getcwd()
    listofDirs = []
    listofFiles = []
    fileListIndex = zipListIndex(fileList)

    if (verboseLevel >= 3): { print("fileListIndex:" + str(fileListIndex)) }

    listofDirs.append(tempfile.mkdtemp(dir=currentDir)) #create tmp dir for thumbnails, etc.
    indexFile = open("index.html",'w') #open or create index.html
    listofFiles.append(indexFile)
    
    indexStr = Template("<!DOCTYPE html>\n<html>\n <head>\n  <title>${title}</title>\n ${head}\n  <script>${script}  </script>\n </head>\n <body>\n  ${body} </body>\n</html>")
    
    titleText = "Index"
    headText = "<link rel=\"stylesheet\" href=\"stylesheet.css\"/>"
    bodyText = ""
    
    bodyText += "<div class=\"wrap\">\n  <div id=\"mainTable\">\n"
    for val, x in enumerate(fileList):
        try:
            a = zipfile.ZipFile(x)
            tf = tempfile.mkstemp(suffix=os.path.basename(a.namelist()[fileListIndex[val]]),prefix='',dir=listofDirs[0]) #temp files for thumbnails
            listofFiles.append(tf[1]) #Index 1 is the name of the temporary file
            os.write(tf[0],a.read(a.namelist()[fileListIndex[val]]))
            os.close(tf[0]) #Close the file to write whats what into the file
            bodyText += "   <div class=\"preview\"><a href=\"" + os.path.relpath(x) + ".html\"><img class=\"b-lazy\" src=" + blankGIF + " data-src=\"" + os.path.join(os.path.basename(listofDirs[0]),os.path.basename(tf[1])) + "\" /><br/>" + os.path.basename(x) + "</a><br/> " + str(int(os.path.getsize(x)/1024)) + " kB </div>\n"
        except BadZipFile:
            print(x + " reported as BadZipFile")
            
    bodyText += "  </div>\n  </div>\n <script>\n var bLazy = new Blazy({\n });\n </script>"

    scriptText = "/*!\n  hey, [be]Lazy.js - v1.3.1 - 2015.02.01\n  A lazy loading and multi-serving image script\n  (c) Bjoern Klinggaard - @bklinggaard - http://dinbror.dk/blazy\n*/\n  (function(d,h){\"function\"===typeof define&&define.amd?define(h):\"object\"===typeof exports?module.exports=h():d.Blazy=h()})(this,function(){function d(b){if(!document.querySelectorAll){var g=document.createStyleSheet();document.querySelectorAll=function(b,a,e,d,f){f=document.all;a=[];b=b.replace(/\[for\b/gi,\"[htmlFor\").split(\",\");for(e=b.length;e--;){g.addRule(b[e],\"k:v\");for(d=f.length;d--;)f[d].currentStyle.k&&a.push(f[d]);g.removeRule(0)}return a}}m=!0;k=[];e={};a=b||{};a.error=a.error||!1;a.offset=a.offset||100;a.success=a.success||!1;a.selector=a.selector||\".b-lazy\";a.separator=a.separator||\"|\";a.container=a.container?document.querySelectorAll(a.container):!1;a.errorClass=a.errorClass||\"b-error\";a.breakpoints=a.breakpoints||!1;a.successClass=a.successClass||\"b-loaded\";a.src=r=a.src||\"data-src\";u=1<window.devicePixelRatio;e.top=0-a.offset;e.left=0-a.offset;f=v(w,25);t=v(x,50);x();n(a.breakpoints,function(b){if(b.width>=window.screen.width)return r=b.src,!1});h()}function h(){y(a.selector);m&&(m=!1,a.container&&n(a.container,function(b){p(b,\"scroll\",f)}),p(window,\"resize\",t),p(window,\"resize\",f),p(window,\"scroll\",f));w()}function w(){for(var b=0;b<l;b++){var g=k[b],c=g.getBoundingClientRect();if(c.right>=e.left&&c.bottom>=e.top&&c.left<=e.right&&c.top<=e.bottom||-1!==(\" \"+g.className+\" \").indexOf(\" \"+a.successClass+\" \"))d.prototype.load(g),k.splice(b,1),l--,b--}0===l&&d.prototype.destroy()}function z(b,g){if(g||0<b.offsetWidth&&0<b.offsetHeight){var c=b.getAttribute(r)||b.getAttribute(a.src);if(c){var c=c.split(a.separator),d=c[u&&1<c.length?1:0],c=new Image;n(a.breakpoints,function(a){b.removeAttribute(a.src)});b.removeAttribute(a.src);c.onerror=function(){a.error&&a.error(b,\"invalid\");b.className=b.className+\" \"+a.errorClass};c.onload=function(){\"img\"===b.nodeName.toLowerCase()?b.src=d:b.style.backgroundImage='url(\"'+d+'\")';b.className=b.className+\" \"+a.successClass;a.success&&a.success(b)};c.src=d}else a.error&&a.error(b,\"missing\"),b.className=b.className+\" \"+a.errorClass}}function y(b){b=document.querySelectorAll(b);for(var a=l=b.length;a--;k.unshift(b[a]));}function x(){e.bottom=(window.innerHeight||document.documentElement.clientHeight)+a.offset;e.right=(window.innerWidth||document.documentElement.clientWidth)+a.offset}function p(b,a,c){b.attachEvent?b.attachEvent&&b.attachEvent(\"on\"+a,c):b.addEventListener(a,c,!1)}function q(b,a,c){b.detachEvent?b.detachEvent&&b.detachEvent(\"on\"+a,c):b.removeEventListener(a,c,!1)}function n(a,d){if(a&&d)for(var c=a.length,e=0;e<c&&!1!==d(a[e],e);e++);}function v(a,d){var c=0;return function(){var e=+new Date;e-c<d||(c=e,a.apply(k,arguments))}}var r,a,e,k,l,u,m,f,t;d.prototype.revalidate=function(){h()};d.prototype.load=function(b,d){-1===(\" \"+b.className+\" \").indexOf(\" \"+a.successClass+\" \")&&z(b,d)};d.prototype.destroy=function(){a.container&&n(a.container,function(a){q(a,\"scroll\",f)});q(window,\"scroll\",f);q(window,\"resize\",f);q(window,\"resize\",t);l=0;k.length=0;m=!0};return d});"
    
    indexFile.write(indexStr.substitute(title=titleText,head=headText,body=bodyText,script=scriptText))
    indexFile.close()

    #begin generate CSS
    cssFile = open("stylesheet.css",'w') #open or create stylesheet.css
    listofFiles.append(cssFile)
    cssText  = "body{\n    font-family: arial, helvetica, sans-serif;\n    background-color: #CCCCCC;\n}\n"
    cssText += "img {\n border-style: solid;\n    border-width: 1px;\n    border-color: black;\n    height: 165px;\n    width: 120px;\n}\n"
    cssText += ".preview {\n    text-align: center;\n   font-size:0.85em;\n color: white;\n width: 300px;   \n  padding: 10px;\n    background-color: #666666;\n    border-radius: 14px;\n  margin:20px;\n}\n"
    cssText += ".wrap {\n   content: '';\n    position: relative;\n    top: 0;\n    bottom: 0;\n}\n"
    cssText += "#mainTable{\n   padding:0 5%;\n display:flex;\n flex-wrap:wrap;\n   justify-content:center;\n}\n"
    cssText += "#mainTable:before {\n   content: '';\n    position: absolute;\n    top: 0;\n    bottom: 0;\n    z-index: -1;\n    left: 5%;\n   width:90%;\n    background: #336699;\n  border-radius: 14px;\n}\n"
    cssFile.write(cssText)
    cssFile.close()
    
    #This is a copout and I should add this above where applicable
    for x in listofDirs:
        filesToRemove.dirs.append(x)
	
    for y in listofFiles:
        filesToRemove.files.append(y)
	
    return
    #return (listofDirs, listofFiles) #return tuple composed of two lists

def generateWebPage( pagePath ):
    currentDir=os.getcwd()
    tempDir = tempfile.mkdtemp(dir=os.path.join(currentDir,os.path.dirname(pagePath))) #create new tmp dir for images, new folder for each html file
    filesToRemove.addDir(tempDir) #Add to list of dirs to delete
    htmlFile = open((pagePath + ".html"),'w')
    filesToRemove.addFile(htmlFile)
    if (verboseLevel >= 3): { print("Generating HTML for " + str(pagePath) + "\nCurrent Path: " + str(currentDir) + "\nTemp Dir: " + str(tempDir)) }

    indexStr = Template("<!DOCTYPE html>\n<html>\n <head>\n  <title>${title}</title>\n  <style>${style}  </style>\n  <script>${script}  </script>\n </head>\n <body>\n  ${body} </body>\n</html>")
    
    titleText  = os.path.basename(pagePath).partition('.')[0]
    scriptText = ""
    styleText  = ""
    bodyText   = ""
    
    bodyText += "<div id=\"mainTable\">\n   <div id=\"bottom\"><a href=\"/index.html\"><span>Home</span></a></div>\n"
    a = zipfile.ZipFile(pagePath)
    for val, x in enumerate([v for r in supportedFileType for v in a.namelist() if r.lower() in v.lower()], start=1): #This complicated line, checks that each file in the zip is an image (ie in our supportFiles) and returns a list of the files names that are images
        tf = os.path.join(tempDir,(str(val) + '.' + x.rpartition('.')[2])) #Create list of temp files, numbered from 1 to end of zip, this way we can keep track of pages easily without having specfic names for different books
        fd = os.open(tf,os.O_WRONLY|os.O_CREAT|os.O_BINARY) #O_BINARY is windows only, haven't tested on linux
        filesToRemove.addFile(tf) #Add temporary image files to list to clean up at end
        os.write(fd,a.read(x)) #Write image to open file, needs to be in binary to work
        os.close(fd) #Close the file to write whats what into the file
        if val == len(a.namelist()): #Links for last file in zip go back to index
            bodyText += "   <div class=\"preview\" id=\"page" + str(val) + "\"><div class=\"left\"><a href=\"#page" + str(val-1) + "\"><span><</span></a></div><a href=\"/index.html\"><img class=\"b-lazy\" src=" + blankGIF + " data-src=\"" + os.path.relpath(tf,os.path.join(currentDir,os.path.dirname(pagePath))) + "\" /></a><div class=\"right\"><a href=\"index.html\"><span>></span></a></div></div>\n"
        else:
            bodyText += "   <div class=\"preview\" id=\"page" + str(val) + "\"><div class=\"left\"><a href=\"#page" + str(val-1) + "\"><span><</span></a></div><a href=\"#page" + str(val +1) + "\"><img class=\"b-lazy\" src=" + blankGIF + " data-src=\"" + os.path.relpath(tf,os.path.join(currentDir,os.path.dirname(pagePath))) + "\" /></a><div class=\"right\"><a href=\"#page" + str(val +1) + "\"><span>></span></a></div></div>\n"

    bodyText += "  </div>\n <script>\n var bLazy = new Blazy({\n });\n </script>"
  
    #begin generate CSS    
    styleText  = "body{\n    font-family: molengo, comic sans ms, sans-serif;\n    background-color: #CCCCCC;\n	margin:0px;\n	overflow:hidden;\n}\nimg {\n    max-height: 100%;\n    max-width: 100%;\n}\n"
    styleText += ".preview {\n	text-align: center;\n	position: relative;\n	width: 100vw;   \n	height: 100vh;\n}\n"
    styleText += "span {\n	font-size:3em;\n	color:rgba(0, 0, 0, 0.2);\n	text-align: center;\n}\n"
    styleText += ".left a{\n	text-decoration: none;\n	line-height: 100vh; \n	display:block;\n    position: absolute;\n	width: 10%; \n    top: 0;\n	left:0;\n    bottom: 0;\n	z-index:1;	\n	transition:background-color, 1s;\n}\n"
    styleText += ".left a:hover {\n	border-radius:10px;\n	opacity:0.6;\n	background-color:gray;\n}\n"
    styleText += ".right a{\n	text-decoration: none;\n	line-height: 100vh; \n	display:block;\n    position: absolute;\n	width: 10%; \n    top: 0;\n	right:0;\n    bottom: 0;\n	z-index:1;\n	transition:background-color, 1s;\n}\n"
    styleText += ".right a:hover {\n	border-radius:10px;\n	opacity:0.6;\n	background-color:gray;\n}\n"
    styleText += "#bottom a{\n	text-decoration: none;\n	text-align: center;\n	display:block;\n    position: fixed;\n	height: 8%; \n	width: 30%;\n	right:35vw;\n    bottom: 0;\n	z-index:1;\n	transition:background-color, 1s;\n}\n"
    styleText += "#bottom a:hover {\n	border-radius:10px;\n	opacity:0.6; \n	background-color:gray;\n}\n"
    
    #bLazy javascript here
    scriptText = "/*!\n  hey, [be]Lazy.js - v1.3.1 - 2015.02.01\n  A lazy loading and multi-serving image script\n  (c) Bjoern Klinggaard - @bklinggaard - http://dinbror.dk/blazy\n*/\n  (function(d,h){\"function\"===typeof define&&define.amd?define(h):\"object\"===typeof exports?module.exports=h():d.Blazy=h()})(this,function(){function d(b){if(!document.querySelectorAll){var g=document.createStyleSheet();document.querySelectorAll=function(b,a,e,d,f){f=document.all;a=[];b=b.replace(/\[for\b/gi,\"[htmlFor\").split(\",\");for(e=b.length;e--;){g.addRule(b[e],\"k:v\");for(d=f.length;d--;)f[d].currentStyle.k&&a.push(f[d]);g.removeRule(0)}return a}}m=!0;k=[];e={};a=b||{};a.error=a.error||!1;a.offset=a.offset||100;a.success=a.success||!1;a.selector=a.selector||\".b-lazy\";a.separator=a.separator||\"|\";a.container=a.container?document.querySelectorAll(a.container):!1;a.errorClass=a.errorClass||\"b-error\";a.breakpoints=a.breakpoints||!1;a.successClass=a.successClass||\"b-loaded\";a.src=r=a.src||\"data-src\";u=1<window.devicePixelRatio;e.top=0-a.offset;e.left=0-a.offset;f=v(w,25);t=v(x,50);x();n(a.breakpoints,function(b){if(b.width>=window.screen.width)return r=b.src,!1});h()}function h(){y(a.selector);m&&(m=!1,a.container&&n(a.container,function(b){p(b,\"scroll\",f)}),p(window,\"resize\",t),p(window,\"resize\",f),p(window,\"scroll\",f));w()}function w(){for(var b=0;b<l;b++){var g=k[b],c=g.getBoundingClientRect();if(c.right>=e.left&&c.bottom>=e.top&&c.left<=e.right&&c.top<=e.bottom||-1!==(\" \"+g.className+\" \").indexOf(\" \"+a.successClass+\" \"))d.prototype.load(g),k.splice(b,1),l--,b--}0===l&&d.prototype.destroy()}function z(b,g){if(g||0<b.offsetWidth&&0<b.offsetHeight){var c=b.getAttribute(r)||b.getAttribute(a.src);if(c){var c=c.split(a.separator),d=c[u&&1<c.length?1:0],c=new Image;n(a.breakpoints,function(a){b.removeAttribute(a.src)});b.removeAttribute(a.src);c.onerror=function(){a.error&&a.error(b,\"invalid\");b.className=b.className+\" \"+a.errorClass};c.onload=function(){\"img\"===b.nodeName.toLowerCase()?b.src=d:b.style.backgroundImage='url(\"'+d+'\")';b.className=b.className+\" \"+a.successClass;a.success&&a.success(b)};c.src=d}else a.error&&a.error(b,\"missing\"),b.className=b.className+\" \"+a.errorClass}}function y(b){b=document.querySelectorAll(b);for(var a=l=b.length;a--;k.unshift(b[a]));}function x(){e.bottom=(window.innerHeight||document.documentElement.clientHeight)+a.offset;e.right=(window.innerWidth||document.documentElement.clientWidth)+a.offset}function p(b,a,c){b.attachEvent?b.attachEvent&&b.attachEvent(\"on\"+a,c):b.addEventListener(a,c,!1)}function q(b,a,c){b.detachEvent?b.detachEvent&&b.detachEvent(\"on\"+a,c):b.removeEventListener(a,c,!1)}function n(a,d){if(a&&d)for(var c=a.length,e=0;e<c&&!1!==d(a[e],e);e++);}function v(a,d){var c=0;return function(){var e=+new Date;e-c<d||(c=e,a.apply(k,arguments))}}var r,a,e,k,l,u,m,f,t;d.prototype.revalidate=function(){h()};d.prototype.load=function(b,d){-1===(\" \"+b.className+\" \").indexOf(\" \"+a.successClass+\" \")&&z(b,d)};d.prototype.destroy=function(){a.container&&n(a.container,function(a){q(a,\"scroll\",f)});q(window,\"scroll\",f);q(window,\"resize\",f);q(window,\"resize\",t);l=0;k.length=0;m=!0};return d});"
   
    htmlFile.write(indexStr.substitute(title=titleText,style=styleText,script=scriptText,body=bodyText))

    htmlFile.close()
    return

#This will be for python 3.4    
class HTTPHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        #Here is the commands to run when dealing with incoming requests.
        #I guess at the beginning index.html will exist, but clicking on a comic will require that page to be built
        #If I create a temp page (with no content) for the comic in the temp directory then I know that any page request
        # for a page in the temp directory will need to be built...

        #extra thought: need to convert from %20 to spaces...
        if self.path=="/":
            self.path="/index.html"

        try:
            #Check the file extension required and set the right mime type
            sendReply = False
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            elif self.path.endswith(".jpeg"):
                mimetype='image/jpeg'
                sendReply = True
            elif self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            elif self.path.endswith(".png"):
                mimetype='image/png'
                sendReply = True
            elif self.path.endswith(".bmp"):
                mimetype='image/bmp'
                sendReply = True
            elif self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True
            elif self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
                #Here is where I generate the file:
                fileToUse = self.path.lstrip("/").rstrip(".html").replace('%20',' ')
                if os.path.isfile(fileToUse) and not os.path.isfile(self.path.replace('%20',' ').lstrip("/")):
                    #print(self.path.replace('%20',' ').lstrip("/"))
                    generateWebPage(fileToUse)
                                          
            if sendReply == True:
                #Open the static file requested and send it
#                fullPath = os.curdir + os.sep + self.path
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
    PORT_NUMBER = 8000

    try:
        #Create a web server and define the handler to manage the incoming request
        server = http.server.HTTPServer(('', PORT_NUMBER), HTTPHandler)
        print('Starting httpserver on port ' , PORT_NUMBER, ', use <Ctrl-C> to stop')
        #Wait forever for incoming http requests
        server.serve_forever()
    except KeyboardInterrupt:
        print('<Ctrl-C> received, shutting down the web server')
        server.socket.close()
    return
