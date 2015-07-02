import os, sys, glob

class Mp3Locator:
  dirs = []

  def __init__( self, root ):
    self.updateRoot( root )

  def listSubDirs( self, root ):
    result = []
    try:
      result = os.listdir( root )
      result.sort()
    except OSError:
      print( "Could not find the directory for media: %s" % root )
    return result

  def updateRoot( self, newRoot ):

    if not newRoot is None and len(newRoot):

      self.dirs = []

      # Find all of the sub-directories within the root and add the child folders to the dir list
      # We do this because we are expecting the root folder to be the mount directory for media devices
      # and want to support play-lists through folder structure
      for file in map( lambda x: "%s/%s"%(newRoot,x), self.listSubDirs( newRoot )):

        # Find the folders in the media device and index each play-list
        if os.path.isdir(file):
          for innerFile in map( lambda x: "%s/%s"%(file,x), self.listSubDirs(file)):
            if os.path.isdir( innerFile ):
              self.dirs.append( innerFile )

    return self.current()

  def next( self ):
    if len(self.dirs):
      self.dirs.append(self.dirs.pop(0))
    return self.current()

  def prev( self ):
    if len(self.dirs):
      self.dirs.insert(0,self.dirs.pop())
    return self.current()

  def current( self ):
    if len(self.dirs) > 0:
      return self.dirs[0]

  def listDirs(self):
    return sorted(self.dirs)
