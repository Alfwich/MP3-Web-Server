import threading
import webbrowser
import cgi
import BaseHTTPServer
import SimpleHTTPServer
import os

FILE = 'index.html'
PORT = 8080

def startSServer():
  os.system( "mocp -S" )

def play():
  print "will play"
  os.system( "mocp -q music/*.mp3 -p" )
  return "Will Play"

def pause():
  print "will pause"
  os.system( "mocp --toggle-pause" )
  return "Will pause"

def stop():
  print "will stop"
  os.system( "mocp -c -s" )
  return "Will Stop"

def next():
  print "next track"
  os.system( "mocp --next" )
  return "Next Track"

def prev():
  print "prev track"
  os.system( "mocp --prev" )
  return "Prev track"

class Mp3Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

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
      post = self.getPostData()
      if "action" in post:
        action = post["action"]
        if action == "play":
          response = play()
        elif action == "stop":
          response = stop()
        elif action == "pause":
          response = pause()
        elif action == "next":
          response = next()
        elif action == "prev":
          response = prev()
        
      self.wfile.write(response)

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, Mp3Handler)
    server.serve_forever()

if __name__ == "__main__":
    startSServer()
    start_server()
