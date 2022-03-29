# -*- coding: utf-8 -*-

# This module handles Zip files

import sys
import os #This is for file operations
import zipfile #for zipfile manipulation

import cbzplatterlib.utils as utils

#Global vars here:
supportedFileType = utils.supportedFileType
#End Globals

class imageArchive:
	def __init__(self, name, fullpath):
		self.fullpathFileName = fullpath
		self.name = name
		self.imagesExist = False
		self.imagesIndex = []
		self.archiveType = 'Zip' #Place holder for now, can add logic to determine type later
		self.archiveError = False
		
		if self.archiveType == 'Zip':
			self.__zipListIndex()
		
	def __zipListIndex( self ): #This marks any zip with images as such and fills imagesIndex
		try:
			a = zipfile.ZipFile(self.fullpathFileName,mode='r')
			if a.testzip():
				utils.verboseOutput(1,"Warning " + self.fullpathFileName + " - failed testzip()")
				self.archiveError = True
            #Without the else here, we allow zipfile that fail checks, but if we want to keep allow them, 
            #  we need more robust error handling when we attempt to unpack them (in Webserver.py)
#			else: 
			#This list comprehension does the bulk of the work here: 
			#  For each supportedFileType it checks if it exists in each file name in the archive
			#  and if it does it appends that file's numerical position within the archive
			self.imagesIndex = [index for eachFileType in supportedFileType for index, eachArchiveFile in enumerate(a.namelist()) if eachFileType.lower() in eachArchiveFile.lower()]
			if not self.imagesIndex:
				self.imagesExist = False
			else:
				self.imagesExist = True
		except zipfile.BadZipFile:
			utils.verboseOutput(1,str(self.fullpathFileName + " reported as BadZipFile"))
			self.archiveError = True
		
		return		
	
class listofZipFiles:
# This will have the list of all Zip archives in the given directory and subdirectories
# It will have an imagesExist variable that will say whether it has images or not, 
# alternatively it will remove zipFiles that don't contain images
# It will have an Index to each image file in the archive
# This should also have a method to update everything once its been created.

	def __init__(self, directory):
		self.baseDirectory = directory #Directory to look for zip files
		self.files = self.__searchForZip(self.__recursDir(self.baseDirectory)) #List of full path archives
		self.__pruneList()

	def __recursDir ( self, currentDir ):
		dirContents = os.listdir(currentDir) #list of contents
		returnList = [currentDir] #list to return
		
		for y in dirContents: #for each item in this list check if it is a folder
			if os.path.isdir(os.path.join(currentDir,y)):
				returnList=returnList+(self.__recursDir(os.path.join(currentDir,y) ))

		return returnList #Returns a list of fullpath subdirectories

	def __searchForZip ( self, directoryList ): #input list of directories to search
		returnList = [] #list to return
		
		for dir in directoryList: #for each directory in this list check if it contains zipfiles
			dirContents = os.listdir(dir)
			for file in dirContents:
				fullx=os.path.join(dir,file)
				if zipfile.is_zipfile(fullx):
					returnList.append(imageArchive(file,fullx))#Add zipfile imageArchive class to this list
					
		utils.verboseOutput(3, "__searchForZip, returnList length: " + str(len(returnList)))
		return returnList
		
	def __pruneList (self):
		#List comprehension will remove non image archives from our list
		self.files = [archive for archive in self.files[:] if archive.imagesExist]
		utils.verboseOutput(3, "__pruneList, files length: " + str(len(self.files)))
		return
	
	def showFileNames(self):
		return [archive.name for archive in self.files]
		
	def showFullPathFileNames(self):
		return [archive.fullpathFileName for archive in self.files]
		
	def showBaseDirectory(self):
		return self.baseDirectory
		
	def totalNumberOfFiles(self):
		return len(self.files)
		

		