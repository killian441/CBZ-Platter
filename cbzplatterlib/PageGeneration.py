# -*- coding: utf-8 -*-

import os
import zipfile #for zipfile manipulation
import tempfile #For temp file operations
from string import Template #template for HTML generation
from urllib.parse import quote as urlquote

import cbzplatterlib.utils as utils

#Global vars here:
supportedFileType = utils.supportedFileType
blankGIF = "data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
loadingSVG = (''
    '<svg width="42px" height="12px" viewBox="0 0 42 12">'
     '<circle id="cir1" fill="#3A3A3A" cx="6"  cy="6" r="4" >'
      '<animate href="#cir1" attributeName="r" values="4;6;4;4" dur="1.8s" begin="0s" repeatCount="indefinite" />'
      '<animate href="#cir1" attributeName="fill" values="#3A3A3A;#4fb95c;#3A3A3A;#3A3A3A" dur="1.8s" begin="0s" repeatCount="indefinite" />'
     '</circle>'
     '<circle id="cir2" fill="#3A3A3A" cx="21" cy="6" r="4" >'
      '<animate href="#cir2" attributeName="r" values="4;6;4;4" dur="1.8s" begin="0s" repeatCount="indefinite" />'
      '<animate href="#cir2" attributeName="fill" values="#3A3A3A;#4fb95c;#3A3A3A;#3A3A3A" dur="1.8s" begin="0s" repeatCount="indefinite" />'
     '</circle>'
     '<circle id="cir3" fill="#3A3A3A" cx="36" cy="6" r="4" >'
      '<animate href="#cir3" attributeName="r" values="4;6;4;4" dur="1.8s" begin="0s" repeatCount="indefinite" />'
      '<animate href="#cir3" attributeName="fill" values="#3A3A3A;#4fb95c;#3A3A3A;#3A3A3A" dur="1.8s" begin="0s" repeatCount="indefinite" />'
     '</circle>'
    '</svg>')
blazyScript =  ("\n  /*!\n"
    "  hey, [be]Lazy.js - v1.8.2 - 2016.10.25 \n"
    "  A fast, small and dependency free lazy load script (https://github.com/dinbror/blazy)\n"
    "  (c) Bjoern Klinggaard - @bklinggaard - http://dinbror.dk/blazy\n"
    "  */\n"
    '   (function(q,m){"function"===typeof define&&define.amd?define(m):"object"===typeof exports?module.exports=m():q.Blazy=m()})(this,function(){function q(b){var c=b._util;c.elements=E(b.options);c.count=c.elements.length;c.destroyed&&(c.destroyed=!1,b.options.container&&l(b.options.container,function(a){n(a,"scroll",c.validateT)}),n(window,"resize",c.saveViewportOffsetT),n(window,"resize",c.validateT),n(window,"scroll",c.validateT));m(b)}function m(b){for(var c=b._util,a=0;a<c.count;a++){var d=c.elements[a],e;a:{var g=d;e=b.options;var p=g.getBoundingClientRect();if(e.container&&y&&(g=g.closest(e.containerClass))){g=g.getBoundingClientRect();e=r(g,f)?r(p,{top:g.top-e.offset,right:g.right+e.offset,bottom:g.bottom+e.offset,left:g.left-e.offset}):!1;break a}e=r(p,f)}if(e||t(d,b.options.successClass))b.load(d),c.elements.splice(a,1),c.count--,a--}0===c.count&&b.destroy()}function r(b,c){return b.right>=c.left&&b.bottom>=c.top&&b.left<=c.right&&b.top<=c.bottom}function z(b,c,a){if(!t(b,a.successClass)&&(c||a.loadInvisible||0<b.offsetWidth&&0<b.offsetHeight))if(c=b.getAttribute(u)||b.getAttribute(a.src)){c=c.split(a.separator);var d=c[A&&1<c.length?1:0],e=b.getAttribute(a.srcset),g="img"===b.nodeName.toLowerCase(),p=(c=b.parentNode)&&"picture"===c.nodeName.toLowerCase();if(g||void 0===b.src){var h=new Image,w=function(){a.error&&a.error(b,"invalid");v(b,a.errorClass);k(h,"error",w);k(h,"load",f)},f=function(){g?p||B(b,d,e):b.style.backgroundImage=\'url("\'+d+\'")\';x(b,a);k(h,"load",f);k(h,"error",w)};p&&(h=b,l(c.getElementsByTagName("source"),function(b){var c=a.srcset,e=b.getAttribute(c);e&&(b.setAttribute("srcset",e),b.removeAttribute(c))}));n(h,"error",w);n(h,"load",f);B(h,d,e)}else b.src=d,x(b,a)}else"video"===b.nodeName.toLowerCase()?(l(b.getElementsByTagName("source"),function(b){var c=a.src,e=b.getAttribute(c);e&&(b.setAttribute("src",e),b.removeAttribute(c))}),b.load(),x(b,a)):(a.error&&a.error(b,"missing"),v(b,a.errorClass))}function x(b,c){v(b,c.successClass);c.success&&c.success(b);b.removeAttribute(c.src);b.removeAttribute(c.srcset);l(c.breakpoints,function(a){b.removeAttribute(a.src)})}function B(b,c,a){a&&b.setAttribute("srcset",a);b.src=c}function t(b,c){return-1!==(" "+b.className+" ").indexOf(" "+c+" ")}function v(b,c){t(b,c)||(b.className+=" "+c)}function E(b){var c=[];b=b.root.querySelectorAll(b.selector);for(var a=b.length;a--;c.unshift(b[a]));return c}function C(b){f.bottom=(window.innerHeight||document.documentElement.clientHeight)+b;f.right=(window.innerWidth||document.documentElement.clientWidth)+b}function n(b,c,a){b.attachEvent?b.attachEvent&&b.attachEvent("on"+c,a):b.addEventListener(c,a,{capture:!1,passive:!0})}function k(b,c,a){b.detachEvent?b.detachEvent&&b.detachEvent("on"+c,a):b.removeEventListener(c,a,{capture:!1,passive:!0})}function l(b,c){if(b&&c)for(var a=b.length,d=0;d<a&&!1!==c(b[d],d);d++);}function D(b,c,a){var d=0;return function(){var e=+new Date;e-d<c||(d=e,b.apply(a,arguments))}}var u,f,A,y;return function(b){if(!document.querySelectorAll){var c=document.createStyleSheet();document.querySelectorAll=function(a,b,d,h,f){f=document.all;b=[];a=a.replace(/\[for\\b/gi,"[htmlFor").split(",");for(d=a.length;d--;){c.addRule(a[d],"k:v");for(h=f.length;h--;)f[h].currentStyle.k&&b.push(f[h]);c.removeRule(0)}return b}}var a=this,d=a._util={};d.elements=[];d.destroyed=!0;a.options=b||{};a.options.error=a.options.error||!1;a.options.offset=a.options.offset||100;a.options.root=a.options.root||document;a.options.success=a.options.success||!1;a.options.selector=a.options.selector||".b-lazy";a.options.separator=a.options.separator||"|";a.options.containerClass=a.options.container;a.options.container=a.options.containerClass?document.querySelectorAll(a.options.containerClass):!1;a.options.errorClass=a.options.errorClass||"b-error";a.options.breakpoints=a.options.breakpoints||!1;a.options.loadInvisible=a.options.loadInvisible||!1;a.options.successClass=a.options.successClass||"b-loaded";a.options.validateDelay=a.options.validateDelay||25;a.options.saveViewportOffsetDelay=a.options.saveViewportOffsetDelay||50;a.options.srcset=a.options.srcset||"data-srcset";a.options.src=u=a.options.src||"data-src";y=Element.prototype.closest;A=1<window.devicePixelRatio;f={};f.top=0-a.options.offset;f.left=0-a.options.offset;a.revalidate=function(){q(a)};a.load=function(a,b){var c=this.options;void 0===a.length?z(a,b,c):l(a,function(a){z(a,b,c)})};a.destroy=function(){var a=this._util;this.options.container&&l(this.options.container,function(b){k(b,"scroll",a.validateT)});k(window,"scroll",a.validateT);k(window,"resize",a.validateT);k(window,"resize",a.saveViewportOffsetT);a.count=0;a.elements.length=0;a.destroyed=!0};d.validateT=D(function(){m(a)},a.options.validateDelay,a);d.saveViewportOffsetT=D(function(){C(a.options.offset)},a.options.saveViewportOffsetDelay,a);C(a.options.offset);l(a.options.breakpoints,function(a){if(a.width>=window.screen.width)return u=a.src,!1});setTimeout(function(){q(a)})}});'
    "\n")

#End Globals

def _HTMLTemplate ( title="", head="", style="", script="", body="" ):
    generatedHTML = Template(""
    "<!DOCTYPE html>\n"
    "<html>\n"
    " <head>\n"
    "  <title> ${_title}  </title>\n"
    "  ${_head} \n"
    "  <style> ${_style}  </style>\n"
    "  <script> ${_script}  </script>\n"
    " </head>\n"
    " <body>\n"
    "  ${_body} </body>\n"
    "</html>"
    "")
    utils.verboseOutput(3,"Title: "+title+"\nHead: "+head+"\nStyle: "+style+"\nScript: "+script+"\nBody: "+body+"\n")
    return generatedHTML.substitute(_title=title,_style=style,_head=head,_script=script,_body=body)


def generateIndexHTML ( fileList ): #Generate index.html, input is listofZipFiles class
    #Ideally I'd like this function to take a list of zip files (names only, not full paths) and generate
    #an index.html and stylesheet.css as well as thumbnails for all zip files.
    currentDir=os.getcwd()

    tempDir = tempfile.mkdtemp(dir=currentDir) #create tmp dir for thumbnails, etc.
    utils.filesToRemove.addDir(tempDir)
    indexFile = open("index.html",'w') #open or create index.html
    utils.filesToRemove.addFile(indexFile)
    
    titleText = "Index"
    headText = "<link rel=\"stylesheet\" href=\"stylesheet.css\"/>"
    bodyText = ""
    
    bodyText += "<div class=\"wrap\">\n  <div id=\"mainTable\">\n"
    for val, eachimageArchive in enumerate(fileList.files):
        if eachimageArchive.imagesExist:
            try:
                a = zipfile.ZipFile(eachimageArchive.fullpathFileName,mode='r') #open zip for reading
                tf = tempfile.mkstemp(suffix=os.path.basename(a.namelist()[eachimageArchive.imagesIndex[0]]),prefix='',dir=tempDir) #temp files for thumbnails
                utils.filesToRemove.addFile(tf[1]) #Index 1 is the name of the temporary file
                os.write(tf[0],a.read(a.namelist()[eachimageArchive.imagesIndex[0]]))
                os.close(tf[0]) #Close the file to write whats what into the file
                bodyText += "   <div class=\"preview\"><a href=\"" + os.path.relpath(eachimageArchive.fullpathFileName) + ".html\"><img class=\"b-lazy loading\" src=" + blankGIF + " data-src=\"" + os.path.join(os.path.basename(tempDir),os.path.basename(tf[1])) + "\" /><br/>" + os.path.basename(eachimageArchive.fullpathFileName) + "</a><br/> " + str(int(os.path.getsize(eachimageArchive.fullpathFileName)/1024)) + " kB </div>\n"
            except zipfile.BadZipFile:
                utils.verboseOutput(1, str(eachimageArchive.fullpathFileName + " reported as BadZipFile"))
    
    bodyText += "  </div>\n  </div>\n <script>\n var bLazy = new Blazy({\n   selector: 'img'\n  });\n </script>"

    scriptText = blazyScript

    indexFile.write(_HTMLTemplate(title=titleText,head=headText,body=bodyText,script=scriptText))
    indexFile.close()

    #begin generate CSS
    cssFile = open("stylesheet.css",'w') #open or create stylesheet.css
    utils.filesToRemove.addFile(cssFile)
    cssText  = ("body{\n    font-family: arial, helvetica, sans-serif;\n    background-color: #CCCCCC;\n}\n"
        ".loading {\n    background: #1E1E1E url(\"data:image/svg+xml," + urlquote(loadingSVG,"/ \"=") + "\") "
        "center center no-repeat;\n}\n"
        "img {\n border-style: solid;\n    border-width: 1px;\n    border-color: black;\n    height: 165px;\n    width: 120px;\n}\n"
        ".preview {\n    text-align: center;\n   font-size:0.85em;\n color: white;\n width: 300px;   \n  padding: 10px;\n    background-color: #666666;\n    border-radius: 14px;\n  margin:20px;\n}\n"
        ".wrap {\n   content: '';\n    position: relative;\n    top: 0;\n    bottom: 0;\n}\n"
        "#mainTable{\n   padding:0 5%;\n display:flex;\n flex-wrap:wrap;\n   justify-content:center;\n}\n"
        "#mainTable:before {\n   content: '';\n    position: absolute;\n    top: 0;\n    bottom: 0;\n    z-index: -1;\n    left: 5%;\n   width:90%;\n    background: #336699;\n  border-radius: 14px;\n}\n"
        "")
    cssFile.write(cssText)
    cssFile.close()

    return

def generateWebPage( pagePath ):
    currentDir=os.getcwd()
    tempDir = tempfile.mkdtemp(dir=os.path.join(currentDir,os.path.dirname(pagePath))) #create new tmp dir for images, new folder for each html file
    utils.filesToRemove.addDir(tempDir) #Add to list of dirs to delete
    htmlFile = open((pagePath + ".html"),'w')
    utils.filesToRemove.addFile(htmlFile)
    utils.verboseOutput(3,"Generating HTML for " + str(pagePath) + "\nCurrent Path: " + str(currentDir) + "\nTemp Dir: " + str(tempDir))

    titleText  = os.path.basename(pagePath).partition('.')[0]
    scriptText = ""
    styleText  = ""
    bodyText   = ""
    
    bodyText += "<div id=\"mainTable\">\n   <div id=\"bottom\"><a href=\"/index.html\"><span>Home</span></a></div>\n"
    a = zipfile.ZipFile(pagePath,mode='r')
    #The following line checks that each file in the zip is an image (ie in our supportFiles) and returns a list of the files names that are images
    #TODO: This returns files in the order specified in supportedFileType not alphabetical of the zip
    imagesinArchive = [v for r in supportedFileType for v in a.namelist() if r.lower() in v.lower()] 
    numberofimagesinArchive = len(imagesinArchive)
    for val, x in enumerate(imagesinArchive, start=1): 
        tf = os.path.join(tempDir,(str(val) + '.' + x.rpartition('.')[2])) #Create list of temp files, numbered from 1 to end of zip, this way we can keep track of pages easily without having specfic names for different books
        fd = os.open(tf,os.O_WRONLY|os.O_CREAT|os.O_BINARY) #O_BINARY is windows only, haven't tested on linux
        utils.filesToRemove.addFile(tf) #Add temporary image files to list to clean up at end
        try: #This is here to allow archives with errors to be included. Upon failure the archive file is skipped but the disk file still exists.
            os.write(fd,a.read(x)) #Write image to open file, needs to be in binary to work
        except zipfile.BadZipFile as inst:
            utils.verboseOutput(1,"File " + str(pagePath) + " reported " + str(inst))
        os.close(fd) #Close the file to write whats what into the file
        if val == numberofimagesinArchive: #Links for last file in zip go back to index
            bodyText += "   <div class=\"preview\" id=\"page" + str(val) + "\"><div class=\"left\"><a href=\"#page" + str(val-1) + "\"><span><</span></a></div><a href=\"/index.html\"><img class=\"b-lazy loading\" src=" + blankGIF + " data-src=\"" + os.path.relpath(tf,os.path.join(currentDir,os.path.dirname(pagePath))) + "\" /></a><div class=\"right\"><a href=\"index.html\"><span>></span></a></div></div>\n"
        else:
            bodyText += "   <div class=\"preview\" id=\"page" + str(val) + "\"><div class=\"left\"><a href=\"#page" + str(val-1) + "\"><span><</span></a></div><a href=\"#page" + str(val +1) + "\"><img class=\"b-lazy loading\" src=" + blankGIF + " data-src=\"" + os.path.relpath(tf,os.path.join(currentDir,os.path.dirname(pagePath))) + "\" /></a><div class=\"right\"><a href=\"#page" + str(val +1) + "\"><span>></span></a></div></div>\n"

    bodyText += "  </div>\n <script>\n  var bLazy = new Blazy({\n   selector: 'img'\n  });\n </script>"
  
    #begin generate CSS    
    styleText = ("body{\n    font-family: molengo, comic sans ms, sans-serif;\n    background-color: #CCCCCC;\n	margin:0px;\n	overflow:hidden;\n}\nimg {\n    max-height: 100%;\n    max-width: 100%;\n}\n"
        ".preview {\n	text-align: center;\n	position: relative;\n	width: 100vw;   \n	height: 100vh;\n}\n"
        "span {\n	font-size:3em;\n	color:rgba(0, 0, 0, 0.2);\n	text-align: center;\n}\n"
        ".left a{\n	text-decoration: none;\n	line-height: 100vh; \n	display:block;\n    position: absolute;\n	width: 10%; \n    top: 0;\n	left:0;\n    bottom: 0;\n	z-index:1;	\n	transition:background-color, 1s;\n}\n"
        ".left a:hover {\n	border-radius:10px;\n	opacity:0.6;\n	background-color:gray;\n}\n"
        ".right a{\n	text-decoration: none;\n	line-height: 100vh; \n	display:block;\n    position: absolute;\n	width: 10%; \n    top: 0;\n	right:0;\n    bottom: 0;\n	z-index:1;\n	transition:background-color, 1s;\n}\n"
        ".right a:hover {\n	border-radius:10px;\n	opacity:0.6;\n	background-color:gray;\n}\n"
        "#bottom a{\n	text-decoration: none;\n	text-align: center;\n	display:block;\n    position: fixed;\n	height: 8%; \n	width: 30%;\n	right:35vw;\n    bottom: 0;\n	z-index:1;\n	transition:background-color, 1s;\n}\n"
        "#bottom a:hover {\n	border-radius:10px;\n	opacity:0.6; \n	background-color:gray;\n}\n")
    
    #bLazy javascript here
    scriptText = blazyScript

    htmlFile.write(_HTMLTemplate(title=titleText,style=styleText,script=scriptText,body=bodyText))

    htmlFile.close()
    return