import threading, webbrowser, cgi, BaseHTTPServer, SimpleHTTPServer, os, sys, json
from subprocess import *

class Mp3CommandHandler():

    serverStarted = False

    def __init__( self, locator ):
        self.locator = locator

    def processExec(self, command):
        result = []

        # Get the information from the mocp process
        com = Popen(command, stdout=PIPE, stderr=PIPE).communicate()

        # Check to see if the server is in an error state; if so restart
        # the mocp server
        if( "FATAL_ERROR" in com[1]):
            self.startSoundServer()
        else:
            result = com[0].split("\n")[0:-1]

        return result


	# Mp3 player commands
    def startSoundServer(self):
        print( "Starting server" )
        self.processExec( [ "mocp", "-x" ] )
        self.processExec( [ "mocp", "-S" ] )

    def play(self):
      self.stop()
      print( "playing from: %s" % self.locator.current() );
      #processExec( "mocp", "-p -a '%s'" % self.locator.current() )
      self.processExec( ["mocp", "-p", "-a", self.locator.current() ] )

    def pause(self):
      print "pause"
      self.processExec( [ "mocp", "--toggle-pause" ] )

    def stop(self):
      print "stop"
      self.processExec( [ "mocp", "-c", "-s" ] )

    def next(self):
      print "next track"
      self.processExec( [ "mocp", "--next" ] )

    def prev(self):
      print "prev track"
      self.processExec( [ "mocp", "--prev" ] )

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

        try: raw = self.processExec(["mocp", "-i"])
        except Exception as e: 
          print "Could not get MOCP information: %s" % e

        for entry in map( lambda x: x.split(": "), raw ):
            if len(entry) == 2:
                result[entry[0].lower()] = entry[1]


        result["lists"] = self._processLists( self.locator.listDirs() )
        result["currentList"] = self._processListName( self.locator.current() )

        return result

    def refresh_data(self):
        self.stop()
        self.locator.updateRoot()
        print "Dirs loaded...", self.locator.listDirs()
        return self.locator.listDirs()

    def shuffle(self):
        print "toggle shuffle"
        self.processExec( [ "mocp", "--toggle", "shuffle" ] )

    def handle(self, action, response, data):

        # Handle the action if it is defined on this object
        if hasattr(self, action):
            response["output"] = getattr(self, action)()
            response["message"] = "Command '%s' executed" % action
        else:
            response["message"] = "Command '%s' not found" % action
