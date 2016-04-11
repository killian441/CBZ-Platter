# -*- coding: utf-8 -*-

# This module handles Zip files

import sys
import os #This is for file operations
import zipfile #for zipfile manipulation

import cbzplatterlib.utils as utils

#Global vars here:
supportedFileType = utils.supportedFileType
#End Globals

def zipListIndex( zipList): #This removes any zipfiles from the list, that don't have images in them
    zipListIndex = []
    for x in zipList[:]: #the slice notation makes copy of list, so I can modify actual list inside loop
        try:
            a = zipfile.ZipFile(x)
            if a.testzip():
                utils.verboseOutput(2,"Removing " + x + " - failed testzip()")
                zipList.remove(x)
            else:
                temp = [val for x in supportedFileType for val, y in enumerate(a.namelist()) if x.lower() in y.lower()]
                if not temp:
                    zipList.remove(x)
                else:
                    zipListIndex.append(temp[0])
        except BadZipFile:
            utils.verboseOutput(1,str(x + " reported as BadZipFile"))
            zipList.remove(x)
        
    if len(zipList) != len(zipListIndex):
        utils.verboseOutput(1,"There was an error with the zipFileIndex doing things")
    
    return zipListIndex
