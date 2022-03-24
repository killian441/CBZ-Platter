# -*- coding: utf-8 -*-

import configparser #python 3.4

#Global vars here:
config = configparser.ConfigParser()
config.read('config.ini')
verboseLevel = config['DEFAULT'].getint('verboseLevel', 1) #Levels 0 = suppress error reporting, 1 = print errors but not much else, 2 = print most stuff, 3 = debug
serverport = config['DEFAULT'].getint('serverPort',8000)
supportedFileType = ('.jpg','.jpeg','.jpe','.gif','.png','.bmp','.webp')
#End Globals

class filesToClean:
	def __init__(self):
		self.dirs  = []
		self.files = []
		
	def addFile(self, file):
		self.files.append(file)
		
	def addDir(self, dir):
		self.dirs.append(dir)
		
	def showFiles(self):
		return self.files
		
	def showDirs(self):
		return self.dirs
	
	def latestDir(self):
		if not self.dirs:
			return None
		return self.dirs[-1]
			
	def removeFile(self, fileName): #Remove a specific file
		#add this in later
		pass
	
	def removeDir(self, dirName): #Remove a specific dir
		#add this in later
		pass
		
	def popFile(self): #Remove last file in list
		return self.files.pop()
		
	def popDir(self):
		return self.dirs.pop()
		
filesToRemove = filesToClean()

def verboseOutput ( verboseThreshold, message ): #output message if verboseLevel is equal to or above verboseThreshold
    if (verboseLevel >= verboseThreshold): { print(message) }
    return
