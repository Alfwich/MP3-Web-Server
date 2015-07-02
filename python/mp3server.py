import threading, webbrowser, cgi, BaseHTTPServer, SimpleHTTPServer, os, sys, json
from subprocess import *
from mp3locator import *
from mp3handler import *

MOUNT_DIRECTORY = "/media/"
PORT = 8080

if len( sys.argv ) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print "Port is not an int. Defaulting to 8080"
        PORT = 8080

if PORT == 8080:
  print( "Server starting on default port. Some features will be disabled while on the default port." )

if len( sys.argv ) > 2:
    MOUNT_DIRECTORY = sys.argv[2]

def start_server():
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, Mp3Handler)
    server.serve_forever()


class Mp3Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    commandHandler = Mp3CommandHandler( Mp3Locator( MOUNT_DIRECTORY ) )

    # Server methods
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

    def end_headers(self):
      self.defaultHeaders()
      SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def defaultHeaders(self):
      self.send_header( "Access-Control-Allow-Origin", "*" )

    def do_POST(self):
      try:
        response = { "message": "Invalid command", "output":"" }

        # Handle the command from the web client
        post = self.getPostData()
        if "action" in post:
          action = post["action"]
          self.commandHandler.handle( action, response, post )

        responseData = json.dumps( response );

        # Process response and headers
        self.send_response(200)
        self.send_header( "Content-Type", "application/json" )
        self.send_header( "Content-Size", str(len(responseData)) )
        self.end_headers()
        self.wfile.write( responseData )
      except Exception as e:
        print( "Error in post handler for mp3 server:\n %s" % e )
        self.wfile.write( "[]" )


if __name__ == "__main__":
    print( "Started moc server and web server on port: %s, reading music recursively from directory: %s" % ( PORT, MOUNT_DIRECTORY ) )
    start_server()
