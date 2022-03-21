#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# main entry point of mp3tomp4;  convert a bunch of mp3s to mp4
# (i.e. go one directory up and run 'python3 mp3tomp4')
#
# batch album example operation,
# python3 mp3tomp4 -s "./input" -a
#
# single long playlist example operation,
# python3 mp3tomp4 -d "./playlist-mp3s" --shuffle -m 60 -p "videoname-prefix"
#
# single long updated playlist example operation,
# python3 mp3tomp4 -d "./playlist-mp3s" --shuffle -m 60 -p "videoname-prefix" --update

import os 
import sys

import argparse
import logging
import datetime

from src.config import StartTime

from src.helpers.FileHelper import FileHelper
fh = FileHelper("./tmp", seed=8534701049500966276)

from src.Convert import Convert

# define input arguments
p = argparse.ArgumentParser()
p.add_argument("-v", "--verbose", action="store_true",
    help="verbose")
p.add_argument("-d", "--inputdir",
    help="single directory of input audio files")
p.add_argument("-s", "--inputdirs",
    help="(root directory of) directories of input audio files"
    + ", processed independently")
p.add_argument("--shuffle", action="store_true",
    help="shuffle input files (or directories, independently)")
p.add_argument("-m", "--maxvideotime", type=int,
    help="max amount of time, in minutes, a video length can be "
    + "before splitting into a new video. defaults to 0 (unlimited)")
p.add_argument("-p", "--playlistname",
    help="name of \"playlist\"; setting this parameter assumes " 
    + "a playlist is being processed. this will be the resulting "
    + "video name (or names)")
p.add_argument("-a", "--albummode", action="store_true",
    help="setting this parameter assumes an album(s) is being "
    + "processed. the resulting video name will be identified "
    + "from MP3 tags, and video description will be simplified.")
p.add_argument("-o", "--outputdir",
    help="output location, defaults to . or tmp (not sure)")

# TODO add --update for playlist changes
# TODO add argument for temp directory (use tmp for now)
# TODO is there even a need for "album mode" parameter?

args = p.parse_args()

# define logger
if args.verbose:
    logging.basicConfig(format="%(levelname)s: %(message)s",
                        handlers=[
                            logging.FileHandler(
                                fh.tmp_dir + "/" + str(StartTime) + "-run.log"),
                            logging.StreamHandler()
                        ],
                        level=logging.DEBUG)
    logging.info("******** (verbose mode) **********")
    logging.debug("seed used for FileHelper random(): {0}".format(fh.seed))
else: 
    logging.basicConfig(format="%(levelname)s: %(message)s", 
                        stream=sys.stdout, 
                        level=logging.INFO)

# sanitize parameters
logging.debug("Checking input parameters ... ")

if ((not args.inputdir) and (not args.inputdirs)):
    logging.error("no input specified")
    sys.exit(2)
elif((args.inputdir) and (args.inputdirs)):
    logging.error("too many input arguments")
    sys.exit(2)
else:
    if ((args.inputdir) and (not os.path.isdir(args.inputdir))):
        logging.error("failed to read input dir: " + args.inputdir)
        sys.exit(2)

    if ((args.inputdirs) and (not os.path.isdir(args.inputdirs))):
        logging.error("failed to read input dir: " + args.inputdirs)
        sys.exit(2)

if (not args.maxvideotime):
    args.maxvideotime = 0

# and run! 
StartTime = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
logging.debug("Start time is {0}".format(StartTime))
Convert.Convert(fh, args)
