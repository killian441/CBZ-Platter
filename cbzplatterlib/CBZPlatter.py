# -*- coding: utf-8 -*-

#Currently supports Python 3.4

#Eventually I really should put the zipList into a class to keep track of all the stuff I do with it
#Also could put the supportedFileType check in generateHTMLPage into its own def and use that with zipListIndex
#Thirdly thumbs.db keeps showing up and preventing folder from being deleted.
#Need to have more robust error handling
#Maybe a verbose command to print out where things are etc.
#subfolders in zip files cause issues
#If enough files, no thumbnails? just file names? Maybe seperate by folders?
#Add swipe gestures for mobile devices

#Down the road I want minimize thumbnails, some sort of config file external to easily change options,
# and to add support for EPUB, PDF and RAR, even though that will require external modules.

import sys
import io #some io operations need this
import os #This is for file operations
import zipfile #for zipfile manipulation
import configparser #python 3.4

import cbzplatterlib.utils as utils
import cbzplatterlib.WebServer as WebServer
from cbzplatterlib.CBZHandler import listofZipFiles

#Global vars here:

#End Globals

def cleanUp( ):
    #Got to put this all in a try try again loop in case Windows is indexing images or something when i try to kill it
    while utils.filesToRemove.showFiles():
        x = utils.filesToRemove.popFile()
        if type(x) is io.TextIOWrapper:
            os.remove(x.name)
        else:
            os.remove(x)
    
    while utils.filesToRemove.showDirs():
        x = utils.filesToRemove.popDir()
        os.rmdir(x) #Delete temp directory. directory must be empty
        
    return

def main():
    """Main entry point for the script."""
    
    utils.verboseOutput(0,"Initializing...")
    
    startDirectory = utils.config['DEFAULT'].get('startdirectory',os.getcwd())
    os.chdir(startDirectory)
    utils.verboseOutput(2,"Starting in " + startDirectory)

    utils.verboseOutput(1,"Reading list of archived files...")
    zipList = listofZipFiles(startDirectory)

    utils.verboseOutput(1,"Generating Web template...")      
    WebServer.generateIndexHTML(zipList)
    WebServer.runHTTPServer ( )

    cleanUp()

if __name__ == '__main__':
    sys.exit(main())
