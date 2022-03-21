#!/usr/bin/python3
#
# from a folder of mp3s, print out their accumulated length
# in hh:mm:ss (to console)

import os
import datetime, glob
from mutagen.mp3 import MP3

# set to True if you want to print artist + song title (false for just song title)
printArtist = False

# directory to start in 
dirName = "."

# Get list of all files in a given directory sorted by name
dirFiles  = sorted( filter( lambda x: os.path.isfile(os.path.join(dirName, x)),
                        os.listdir(dirName) ) )

# collect and print accumulated timer
curr_time = datetime.timedelta(seconds=0)
for filename in dirFiles:
    if filename.endswith(".mp3"):
        audio = MP3(filename)
        
        title = str(audio["TIT2"])
        artist_blob = ""
        if (printArtist):
            artist_blob = str(audio["TPE1"]) + " - "
            
        length_s = audio.info.length

        # timedelta sucks and can't format itself
        # (i think i was angry when i wrote that earlier)
        curr_seconds = curr_time.seconds
        hours, rem = divmod(curr_seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        
        print(
            "{:02}:{:02}:{:02}".format(
                int(hours),
                int(minutes),
                int(seconds))
            + " - " + artist_blob + title)
        curr_time += datetime.timedelta(seconds=length_s)
        
    else:
        continue



