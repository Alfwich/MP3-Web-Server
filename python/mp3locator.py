import os
import sys
import glob

class Mp3Locator:
	currentDir = 0
	dirs = []
	def listSubDirs( self, root ):
		result = []
		try:
			result = os.listdir( root )
			result.sort()
		except OSError:
			print( "Could not find the directory for media: %s" % root )
		return result

	def updateRoot( self, newRoot ):

		if newRoot == None or len(newRoot) == 0:
			print "Invalid new root"
			return

		# Minor processing if root is not in standard
		if newRoot[-1] != "/":
			newRoot = "%s/" % newRoot

		dirs = []

		# Get root level files
		rootFiles = self.listSubDirs( newRoot )

		# For each file check if they are a dir, if so then add all sub dirs to the result set
		"""
		for file in rootFiles:
			tmpPath = "%s%s" % (newRoot, file)
			if tmpPath[0] != "." and os.path.isdir( tmpPath ):
				innerFiles = self.listSubDirs(tmpPath)
				for innerFile in innerFiles:
					tmpInnerPath = "%s/%s" % (tmpPath, innerFile)
					if tmpInnerPath[0] != "." and os.path.isdir( tmpInnerPath ):
						innerDirs = self.listSubDirs(tmpInnerPath)
						for innerD in innerDirs:
							dirs += [("%s/%s/" % ( tmpInnerPath, innerD ))]
		"""

		# Format results
		dirs = [newRoot]


		if len(dirs) > 0:
			self.dirs = dirs
			self.currentDir = 0

		return self.current()

	def next( self ):
		self.currentDir = (self.currentDir+1)%len(self.dirs)
		return self.current()

	def prev( self ):
		self.currentDir = (self.currentDir-1)%len(self.dirs)
		return self.current()
	
	def current( self ):
		if len(self.dirs) > 0:
			return self.dirs[self.currentDir]
	
	def listDirs(self):
		return self.dirs

