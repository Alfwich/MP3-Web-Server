#!bin/bash/

MUSIC_DIRECTORY="~/Music/*.mp3"

echo "Basic mp3 player."
echo "Arthur Wuterich, 2014"
while true; do
	stty cbreak
	char=`dd if=/dev/tty bs=1 count=1 2>/dev/null`
	stty -cbreak
	if [ $char = "q" ]; then
		echo ":Play Command"
		mocp -p
		eval "mocp -q $MUSIC_DIRECTORY -p"
	elif [ $char = "w" ]; then
		echo ":Stop Command"
		eval "mocp -c -s"
	elif [ $char = "e" ]; then
		echo ":Pause Command"
		eval "mocp --toggle-pause"
	elif [ $char = "r" ]; then
		echo ":Prev Command"
		eval "mocp --previous"
	elif [ $char = "t" ]; then
		echo ":Next Command"
		eval "mocp --next"
	elif [ $char = "y" ]; then
		echo ":Shuffle Command"
		eval "mocp --on shuffle"
	elif [ $char = "u" ]; then
		echo ":Command 7"
	elif [ $char = "i" ]; then
		echo ":Install Moc"
		eval "sudo apt-get install moc"
	elif [ $char = "x" ]; then
		echo ":Exiting"
		eval "mocp -c -s"
		return
	else
		echo ":Unrecognized Command"
	fi
done
