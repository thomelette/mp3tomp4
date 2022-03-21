# MP3Helper.py
#
# helper class for MP3 manipulation

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class MP3Helper:

    # set to True if you want to print artist + song title (false for just song title)
    print_artist_str = False 



    audio = None

    # constructor
    def __init__(self, mp3_filepath):
        self.audio = MP3(mp3_filepath, ID3=EasyID3)

    def GetSeconds(self):
        return self.audio.info.length

    def GetAlbumNameString(self):

        date = str(self.audio["date"][0])

        # condition any mm or dd out of it
        date_a = str.split(date, "-")
        year = date_a[0]

        year_blob = "[" + year + "]"
        album_blob = str(self.audio["album"][0]).lower()

        return album_blob + " " + year_blob

    def GetArtistString(self):
        return str(self.audio["artist"][0]).lower()

    def ToString(self, print_artist_str=False):
        artist_blob = ""
        if (print_artist_str):
            artist_blob = str(self.audio["artist"]) + " - "

        title = str(self.audio["title"][0])
            
        return artist_blob + title

    # TODO write __str__