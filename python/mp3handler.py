import threading, webbrowser, cgi, BaseHTTPServer, SimpleHTTPServer, os, sys, json
from subprocess import *

def exeC( cmd, prams="" ):
  try:
    os.system( "%s %s" % ( cmd, prams ) )
  except:
    print "Could not execute command: %s, with prams: %s" % ( cmd, prams )

class Mp3CommandHandler():

    serverStarted = False

    def __init__( self, locator ):
        self.locator = locator

    def processExec(self, command):
        result = []

        # Get the information from the mocp process
        com = Popen(command, stdout=PIPE, stderr=PIPE).communicate()

        # Check to make sure the stderr field is not populated; if it is then
        # the most likely case is the sound server is not running so attempt to
        # start the sound server. We do not attempt to run the command because
        # the server will be in a fresh state
        if( com[1] != "" ):
            self.startSoundServer()
        else:
            result = raw.split("\n")[0:-1]

        return result


	# Mp3 player commands
    def startSoundServer(self):
        print( "Starting server" )
        exeC( "mocp", "-x" )
        exeC( "mocp", "-S" )
        self.serverStarted = True

    def play(self):
      self.stop()
      print( "playing from: %s" % self.locator.current() );
      #exeC( "mocp", "-p -a '%s'" % self.locator.current() )
      self.processExec( ["mocp", "-p", "-a %s" % self.locator.current() ] )

    def pause(self):
      print "pause"
      exeC( "mocp", "--toggle-pause" )

    def stop(self):
      print "stop"
      exeC( "mocp", "-c -s" )

    def next(self):
      print "next track"
      exeC( "mocp", "--next" )

    def prev(self):
      print "prev track"
      exeC( "mocp", "--prev" )

    def next_album(self):
      print "next album"
      self.stop()
      return self.locator.next()

    def prev_album(self):
      print "next album"
      self.stop()
      return self.locator.prev()

    def _processListName( self, name ):
        result = name

        if not name is None:
            name = name.replace("\\", "/" )
            comps = name.split("/")
            if len(comps) > 1:
                result = " ".join( comps[-2:] )

        return result

    def _processLists( self, listNames ):
      result = []

      for name in listNames:
        result.append( self._processListName( name ) )

      return result


    def info(self):
        result = {}
        raw = []

        try: raw = self.getCommandOutput( ["mocp", "-i"])
        except: print "Could not get MOCP information!"

        for entry in map( lambda x: x.split(": "), raw ):
            if len(entry) == 2:
                result[entry[0].lower()] = entry[1]


        result["lists"] = self._processLists( self.locator.listDirs() )
        result["currentList"] = self._processListName( self.locator.current() )

        return result

    def refresh_data(self):
        self.stop()
        self.locator.updateRoot( MOUNT_DIRECTORY )
        print "Dirs loaded...", self.locator.listDirs()
        return self.locator.listDirs()

    def shuffle(self):
        print "toggle shuffle"
        exeC( "mocp", "--toggle shuffle" )

    def handle(self, action, response, data):
        # Start the sound server if it has not already been attempted to be started
        if not self.serverStarted:
            self.startSoundServer()

        # Handle the action if it is defined on this object
        if hasattr(self, action):
            response["output"] = getattr(self, action)()
            response["message"] = "Command '%s' executed" % action
        else:
            response["message"] = "Command '%s' not found" % action
