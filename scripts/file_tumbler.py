#!/usr/bin/python3
#
# "tumbles" a bunch of mp3s
# shuffles their order then assembles them into subfolders (called "chunks")

import os, sys
import datetime, getopt, glob, random
from mutagen.mp3 import MP3

# how many minutes of music do you want in a chunk?
length_per_chunk = datetime.timedelta(minutes=60)

def main(argv):
    input_dir = ""

    try:
        opts, args = getopt.getopt(argv, "hd:")
    except getopt.GetoptError:
        print("bad args ... dying ... ")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("TODO: the rest of help message")
            print("just use -d /path/to/input/dir")
            sys.exit(1)
        elif opt == '-d':
            input_dir = arg

    if (not os.path.isdir(input_dir)):
        print("input directory is not really a directory ... dying ... ")
        sys.exit(2)
    
    print("### tumbling your files ... ###")
    print("starting in input directory = " + input_dir)

    # get list of ALL files in directory
    files = filter(
        lambda x: os.path.isfile(os.path.join(input_dir, x)),
        os.listdir(input_dir)
        )

    # filter by mp3
    mp3s = filter(lambda x: x.endswith(".mp3"), files)

    # shuffle list
    mp3s = sorted(mp3s, key=lambda x: random.random())

    # get ready to build chunks
    current_chunk_length = datetime.timedelta(seconds=0)
    current_chunk_no = 0
    current_file_no = 1
    start_time = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

    chunk_dir = os.path.join(input_dir,
                             start_time
                             + "chunk"
                             + str(current_chunk_no))
    os.mkdir(chunk_dir)

    # start moving files to chunks...
    for filename in mp3s:
        if (current_chunk_length >= length_per_chunk):
            current_chunk_no += 1

            print("making new chunk" + str(current_chunk_no))
            chunk_dir = os.path.join(input_dir,
                                     start_time
                                     + "chunk"
                                     + str(current_chunk_no))
            os.mkdir(chunk_dir)
            current_chunk_length = datetime.timedelta(seconds=0)

        # grab length before moving
        mp3_length_s = MP3(input_dir + "/" + filename).info.length

        # move and rename
        os.rename(
            os.path.join(input_dir,filename),
            os.path.join(chunk_dir,
                         str(current_file_no).zfill(4) + "-" + filename
                         )
            )

        # increment
        current_file_no += 1
        current_chunk_length += datetime.timedelta(seconds=mp3_length_s)


if __name__ == "__main__":
    main(sys.argv[1:])
