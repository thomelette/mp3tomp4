
import datetime
import glob
import os

from mutagen.mp3 import MP3

dirName = "."

# Get list of all files in a given directory sorted by name
dirFiles  = sorted( filter( lambda x: os.path.isfile(os.path.join(dirName, x)),
                        os.listdir(dirName) ) )

# collect and print accumulated timer
curr_time = datetime.timedelta(seconds=0)
for filename in dirFiles:
    if filename.endswith(".mp3"):
        audio = MP3(filename)
        
        title = audio["TIT2"]
        artist = audio["TPE1"]
        length_s = audio.info.length

        # timedelta sucks and can't format itself
        curr_seconds = curr_time.seconds
        hours, rem = divmod(curr_seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        
        print("{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)) + " - " + str(title))
        curr_time += datetime.timedelta(seconds=length_s)
        
    else:
        continue



