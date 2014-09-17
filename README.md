python_web_mp3
========
Python web server MP3(moc) Player for Rpi

install:
	Will install two packages:
		'moc': Music on Console, core package for music
		'usbmount': command line auto usb drive mounting

useage:
	execute the python file mp3server.py in the python folder after installing.
	```
	python mp3server.py {port} {read_directory}
	```

	EX: python mp3server.py 8000 ~/Music/
		This will start the python simple http server listening on port 8000 and reading all the music, recursivly, in the directory ~/Music/

