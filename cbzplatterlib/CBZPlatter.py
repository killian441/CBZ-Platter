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

from cbzplatterlib.utils import filesToRemove
import cbzplatterlib.WebServer as WebServer

#Global vars here:
supportedFileType = ('.jpg','.jpeg','.gif','.png','.bmp')
blankGIF = "data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
verboseLevel = 3 #Levels 0 = suppress error reporting, 1 = print errors but not much else, 2 = print most stuff, 3 = debug
#End Globals

def recursDir ( currentDir ):
    dirContents = os.listdir(currentDir) #list of contents
    returnList = [currentDir] #list to return
#    temp = []
    
    for y in dirContents: #for each item in this list check if it is a folder
        if os.path.isdir(os.path.join(currentDir,y)):
            returnList=returnList+(recursDir(os.path.join(currentDir,y) ))

    return returnList #Returns a list of fullpath subdirectories

def recursZip ( directoryList ): #input list of directories to search
    returnList = [] #list to return
    
    for y in directoryList: #for each directory in this list check if it contains zipfiles
        dirContents = os.listdir(y)
        for x in dirContents:
            fullx=os.path.join(y,x)
            if zipfile.is_zipfile(fullx):
                returnList.append(fullx) #Add zipfiles to this list
                
    if (verboseLevel >= 3): { print("recursZip, returnList: " + str(returnList)) }
    return returnList

def archiveList ( currentDir ):
        directoryList = recursDir (currentDir)
        returnList = recursZip(directoryList)
        return returnList

def cleanUp( ):
    #Got to put this all in a try try again loop in case Windows is indexing images or something when i try to kill it
    while filesToRemove.showFiles():
        x = filesToRemove.popFile()
        if type(x) is io.TextIOWrapper:
            os.remove(x.name)
        else:
            os.remove(x)
    
    while filesToRemove.showDirs():
        x = filesToRemove.popDir()
        os.rmdir(x) #Delete temp directory. directory must be empty
        
    return

def main():
        """Main entry point for the script."""

        if (verboseLevel >= 0): { print("Initializing...") }

        ########################################
        #Temp stuff - In future use current dir or argv
        s = "E:\media\comics" #this is hardcoded dir for now
        #s = "F:\\downloads"
        os.chdir(s)
        ########################################

        currentDir = os.getcwd()  #GetCurrentWorkingDirectory, server should be started in directory of interest

        #subDirectory = [] #list of subdirectories
        zipList = [] #Null list of zip files
        subFiles = [] #Null list for subdirectory files

        if (verboseLevel >= 2): { print("Reading list of archived files...") }
                
        #subDirectory = (recursDir(currentDir)) #get all subfolders, including local folder, into list
        #zipList = (recursZip(subDirectory)) #List of all the zip files in the directory and subdirectories
        zipList = archiveList(currentDir) #List of all the archive files in the current directory plus subdirectories

        if (verboseLevel >= 2): { print("Generating Web template...") }
        
        #tempFiles = WebServer.generateIndexHTML(zipList)
        WebServer.generateIndexHTML(zipList)
		
        WebServer.runHTTPServer ( )

        #cleanUp(tempFiles[0],tempFiles[1])
        cleanUp()


if __name__ == '__main__':
    sys.exit(main())
