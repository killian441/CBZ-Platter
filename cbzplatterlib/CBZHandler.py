# -*- coding: utf-8 -*-

# This module handles Zip files

import sys
import os #This is for file operations
import zipfile #for zipfile manipulation

#Global vars here:
supportedFileType = ('.jpg','.jpeg','.gif','.png','.bmp')
blankGIF = "data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
verboseLevel = 3 #Levels 0 = suppress error reporting, 1 = print errors but not much else, 2 = print most stuff, 3 = debug
#End Globals

def zipListIndex( zipList): #This removes any zipfiles from the list, that don't have images in them
    zipListIndex = []
    for x in zipList[:]: #the slice notation makes copy of list, so I can modify actual list inside loop
        try:
            a = zipfile.ZipFile(x)
            if a.testzip():
                if (verboseLevel >= 2): { print("Removing " + x + " - failed testzip()") }
                zipList.remove(x)
            else:
                temp = [val for x in supportedFileType for val, y in enumerate(a.namelist()) if x.lower() in y.lower()]
                if not temp:
                    zipList.remove(x)
                else:
                    zipListIndex.append(temp[0])
        except BadZipFile:
            if (verboseLevel >= 1): { print(x + " reported as BadZipFile") }
            zipList.remove(x)
        
    if len(zipList) != len(zipListIndex):
        if (verboseLevel >= 1): { print("There was an error with the zipFileIndex doing things") }
    
    return zipListIndex
