#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# convert a bunch of mp3s to mp4
#
# batch album example operation,
# ./convert.py -s "./input" -a
#
# single long playlist example operation,
# ./convert.py -d "./playlist-mp3s" --shuffle -m 60 -p "videoname-prefix"
#
# single long updated playlist example operation,
# ./convert.py -d "./playlist-mp3s" --shuffle -m 60 -p "videoname-prefix" --update

import os, sys
import argparse
import logging
log = logging.getLogger(__name__)

from helpers.FileHelper import FileHelper
fh = FileHelper("./tmp")
from helpers.MP3Helper import MP3Helper
from helpers.TimeHelper import TimeHelper
th = TimeHelper()
from helpers.FFMPEGHelper import FFMPEGHelper

# TODO move to time helper
# TODO bake timestamp into file handler or time helper (copied from below)
# really just pass a time object into time helper and file helper
# start_time = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

# https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules


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

def init_logging():
    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s",
                            handlers=[
                                logging.FileHandler(
                                    fh.tmp_dir + "/" + str(th.StartTime) + "-run.log"),
                                logging.StreamHandler()
                            ],
                            level=logging.DEBUG)
        log.info("******** (verbose mode) **********")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s",
                        level=logging.INFO)

def check_input_parameters():
    log.debug("Checking input parameters ... ")

    if ((not args.inputdir) and (not args.inputdirs)):
        log.error("no input specified")
        sys.exit(2)
    elif((args.inputdir) and (args.inputdirs)):
        log.error("too many input arguments")
        sys.exit(2)
    else:
        if ((args.inputdir) and (not os.path.isdir(args.inputdir))):
            log.error("failed to read input dir: " + args.inputdir)
            sys.exit(2)

        if ((args.inputdirs) and (not os.path.isdir(args.inputdirs))):
            log.error("failed to read input dir: " + args.inputdirs)
            sys.exit(2)

    if (not args.maxvideotime):
        args.maxvideotime = 0


def main(argv):

    init_logging()
    check_input_parameters()
    
    log.info("**********************************")
    log.info("* time to convert mp3(s) to mp4  *")
    log.info("**********************************")
    log.info("")
    log.debug("Starting time string is: {0}".format(th.StartTime))

    log.debug("")
    log.debug("Determining input directory(s) ...")

    dirs = []

    if (args.inputdir): # single directory case
        # sanitize and add to dirs... 
        args.inputdir = args.inputdir.strip('/')
        dirs.append(args.inputdir)
        log.debug("... single directory: " + args.inputdir)

    elif (args.inputdirs): # multi directory case
        # sanitize, but post-pend a '/'
        args.inputdirs = args.inputdirs.strip('/') + "/"

        dirs = [(args.inputdirs + d) 
                for d in os.listdir(args.inputdirs)
                    if os.path.isdir(os.path.join(args.inputdirs, d))]

        if args.verbose:
            log.debug("... multiple directories (in): " + args.inputdirs)
            for d in dirs:
                log.debug("... ... found dir: " + d)

    log.debug("")
    log.debug("Scanning input directory(s) for mp3s ...")
    log.debug("(to generate video descriptions, ffmpeg inputs)")

    video_description = ""
    ffmpeg_filelist = ""
    current_chunk_number = 1
    ffmpeg_input_files = []

    for dir in dirs:
        log.debug("... processing dir: " + dir)
        log.debug("... current chunk: " + str(current_chunk_number))

        # sort files (either shuffle or don't)
        files = fh.GetSortedFiles(dir, "mp3", args.shuffle)

        # process files
        log.debug("... ... file list: " 
            + ("(shuffled) " if args.shuffle else ""))

        for k, file in enumerate(files):
            log.debug("... ... ... " + file)

            mp3 = MP3Helper(file)

            # TODO need to sanitize text for ffmpeg

            # '././test-playlist/Elton John - I Guess Thats'
            # ^^^ a bug
            #ffmpeg_filename = file
            #ffmpeg_filename = "./tmp/." + file
            ffmpeg_filename = "." + file
            # ^^ this one works w/o copy
            # because you're invoking ffmpeg from tmp/*.ffmpeg, it "start"s there

            # compile some metadata
            video_description += "{0} - {1}\n".format(th, mp3.ToString(False))
            ffmpeg_filelist += "file '{0}'\n".format(ffmpeg_filename)

            make_new_video = False
            chunk_suffix = ""

            th.IncrementTimer(mp3.GetSeconds())
            # TODO add separate time handler for cumulative audio time
            # if video is too long,
            if ((args.maxvideotime > 0) and (th.GetTimeMinutes() > args.maxvideotime)):

                log.debug("... ... length ({:.2f} mins) exceeds parameter time"
                    .format(th.GetTimeMinutes()))

                chunk_suffix = " - part {}".format(current_chunk_number)

                make_new_video = True

            # ... or if we've reached end of dir,
            elif (k == len(files) - 1): # see TODO below ... and args.albummode) (???)
                log.debug("... ... reached final file")
                # default behavior is to "call it a day" 
                # with existing partial chunk
                # TODO change this later if you have "one playlist" in
                #      multiple folders
                if (current_chunk_number > 1):
                    chunk_suffix = " - part {}".format(current_chunk_number)
                
                make_new_video = True

            # prepare for new video render
            if make_new_video:

                # determine filename (later used as mp4 name)
                video_name = "{0}-NAME_UNKNOWN".format(th.StartTime)
                if (args.albummode):
                    video_name = mp3.GetAlbumNameString() + chunk_suffix
                    video_description = (
                        mp3.GetArtistString() + "\n\n" 
                        + video_description)
                elif (args.playlistname):
                    video_name = args.playlistname + chunk_suffix
                else:
                    log.warning("Unsure of video name! Check --playlistname or ID3 data!")

                # TODO bake timestamp into file handler or time helper
                log.debug("... writing out data for video render '" + video_name + "'")      
                # fh.SetTime(th.StartTime)
                # fh.WriteDescription(video_name, video_description)
                # ffmpeg_filename = fh.WriteFFMPEGRecipe(video_name, ffmpeg_filelist)          
                fh.WriteEvenSimplerFile("{0}-{1}.txt".format(th.StartTime, video_name), video_description)
                fh.WriteEvenSimplerFile("{0}-{1}.ffmpeg".format(th.StartTime, video_name), ffmpeg_filelist)

                # TODO confusing - get tmp/starttime from somewhere else
                # confusing because tmp is handled by file handler 
                ffmpeg_input_files.append("./tmp/{0}-{1}.ffmpeg".format(th.StartTime, video_name))
                # ffmpeg_input_files.append(ffmpeg_filename)

                # cleanup
                th.ResetTimer()
                video_description = ""
                ffmpeg_filelist = ""

                if (k != (len(files) - 1)):
                    current_chunk_number += 1
                    log.debug("... next chunk: " + str(current_chunk_number))

        # (end process files in directory)

    log.debug("")
    log.info("Inputs parsed: ")
    log.info("... Number of directories    : {0}".format(len(dirs)))
    log.info("... Number of files          : {0}".format(len(files)))
    log.info("... Number of videos to make : {0}".format(len(ffmpeg_input_files)))
    log.info("")

    log.debug("Begin batch processing files via ffmpeg ...")
    log.debug("")
    ffh = FFMPEGHelper()

    # ffh = FFMPEGHelper(tmp_dir, timehelper)

    for vid in ffmpeg_input_files:
        ffh.runMP3(vid)

    # TODO need to clean up tmp files 

    # TODO start a timer 

    #out_name = fh.CopyFileToHere(ffmpeg_input_files[0])
    #ffh.runMP3(out_name)

    # ffh.runMP3(ffmpeg_input_files[0])

    # TODO items (maybe addressable in FileHelper)
    #   [-] check for existing posterity m3u
    #   [-] make (new) m3u for (future) posterity 

    # call_mp3tomp4
    # for each $(some_format).txt file,
    #   execute ffmpeg sh script
    #   (parse.mp3.py, but with files in .txt file) -> output to $(video_name).txt
    #   TODO here may need "playlist parameter?" - what do you title the description?
    #   moving on... assume video is named well, assume video.txt is formatted okay
    #
    # if not verbose, cleanup video_input_lists

    # move output files (.mp4 and .txt description) to tmp/$(timestamp)

    # done! 




    log.info("**********************************")
    log.info("**** ~~~~~~~ finished ~~~~~~~ ****")
    log.info("**********************************")

# main entry,
if __name__ == "__main__":
    main(sys.argv[1:])
