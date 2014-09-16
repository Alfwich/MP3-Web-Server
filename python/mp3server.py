import threading
import webbrowser
import cgi
import BaseHTTPServer
import SimpleHTTPServer
import os

MUSIC_DIRECTORY = "music/*"
PORT = 8080

def exeC( cmd ):
  os.system( cmd )

# Mp3 player commands
def startSServer():
  print( "Starting server" )
  exeC( "mocp -S" )

def play():
  print( "play" );
  exeC( "mocp -q %s -p" % MUSIC_DIRECTORY )

def pause():
  print "pause"
  exeC( "mocp --toggle-pause" )

def stop():
  print "stop"
  exeC( "mocp -c -s" )
  play.isPlaying = False

def next():
  print "next track"
  exeC( "mocp --next" )

def prev():
  print "prev track"
  exeC( "mocp --prev" )

class Mp3Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    serverStarted = False
    def getPostData(self):
      result = {}
      form = cgi.FieldStorage(
          fp=self.rfile,
          headers=self.headers,
          environ={'REQUEST_METHOD':'POST',
                   'CONTENT_TYPE':self.headers['Content-Type'],
      })

      for item in form.list:
        result[item.name] = item.value
      return result

    def do_POST(self):
      """Handle a post request by returning the square of the number."""
      response = "Invalid command"

      # Start the sound server if it has not already been attempted to be started
      if not Mp3Handler.serverStarted:
        startSServer()
        Mp3Handler.serverStarted = True

      # Handle the command from the web client
      post = self.getPostData()
      if "action" in post:
        action = post["action"]
        if action == "play":
          play()
        elif action == "stop":
          stop()
        elif action == "pause":
          pause()
        elif action == "next":
          next()
        elif action == "prev":
          prev()

        response = "Command '%s' executed" % action
        
      self.wfile.write(response)

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, Mp3Handler)
    server.serve_forever()

if __name__ == "__main__":
    print( "Started moc server and web server on port: %s." % PORT )
    start_server()
