# -*- coding: utf-8 -*-

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
