# Convert.py
#
# main entrance for mp3 to mp4 "convert" logic and operations

import os

import logging
log = logging.getLogger(__name__)

from src.config import StartTime

from src.helpers.Timer import Timer
from src.helpers.MP3Helper import MP3Helper
from src.helpers.FFMPEGHelper import FFMPEGHelper

class Convert:

    def Convert(fileHelper, args):
        
        log.info("**********************************")
        log.info("* time to convert mp3(s) to mp4  *")
        log.info("**********************************")
        log.info("")
        log.debug("Starting time string is: {0}".format(StartTime))

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
        timer = Timer()

        for dir in dirs:
            log.debug("... processing dir: " + dir)
            log.debug("... current chunk: " + str(current_chunk_number))

            # sort files (either shuffle or don't)
            files = fileHelper.GetSortedFiles(dir, "mp3", args.shuffle)

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
                video_description += "{0} - {1}\n".format(timer, mp3.ToString(False))
                ffmpeg_filelist += "file '{0}'\n".format(ffmpeg_filename)

                make_new_video = False
                chunk_suffix = ""

                timer.Increment(mp3.GetSeconds())
                # TODO add separate time handler for cumulative audio time
                # if video is too long,
                if ((args.maxvideotime > 0) and (timer.GetMinutes() > args.maxvideotime)):

                    log.debug("... ... length ({:.2f} mins) exceeds parameter time"
                        .format(timer.GetMinutes()))

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
                    video_name = "{0}-NAME_UNKNOWN".format(StartTime)
                    if (args.albummode):
                        video_name = mp3.GetAlbumNameString() + chunk_suffix
                        video_description = (
                            mp3.GetArtistString() + "\n\n" 
                            + video_description)
                    elif (args.playlistname):
                        # TODO clean this up
                        video_name = args.playlistname + chunk_suffix
                        video_description = (
                            video_name + "\n\n" 
                            + video_description)
                    else:
                        log.warning("Unsure of video name! Check --playlistname or ID3 data!")

                    log.debug("... writing out data for video render '" + video_name + "'")      
                    
                    fileHelper.WriteDescription(video_name, video_description)
                    ffmpeg_recipe_name = fileHelper.WriteFFMPEGRecipe(video_name, ffmpeg_filelist)

                    # build list of .ffmpeg_audio files
                    ffmpeg_input_files.append(ffmpeg_recipe_name)

                    # cleanup
                    timer.Reset()
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
            # fh.SetTime(th.StartTime)
            print(vid)
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