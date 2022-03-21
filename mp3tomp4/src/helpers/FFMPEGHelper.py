# FFMPEGHelper.py
#
# helper class for handling ffmpeg calls

import subprocess
from datetime import datetime

import logging
log = logging.getLogger(__name__)

# from src.config import StartTime

# TODO (very big, potentially unnecessary task) - port to ffmpeg-python binding
# https://github.com/kkroening/ffmpeg-python

class FFMPEGHelper:

    out_dir = ""

    # command line code for concatenating mp3s,
    #
    # {0} = input audio files (.ffmpeg_audio)
    # {1} = output mp3 filename
    concat_mp3_cmd = "ffmpeg -nostdin -f concat -safe 0 -i '{0}' -c copy '{1}.mp3'"
    
    # command line code for rendering mp4,
    #
    # {0} = input mp3 filename
    # {1} = output mp4 filename
    make_mp4_cmd = \
        "ffmpeg -loop 1 -i assets/blank.jpg " + \
        "-i '{0}.mp3' " + \
        "-c:v libx264 -preset veryslow -tune stillimage -crf 20 -vf scale=854:480 " + \
        "-c:a aac -b:a 320k -shortest -strict experimental " + \
        "'{1}.mp4'"

    # constructor
    #
    # output_dir [input] - location for output files
    def __init__(self, output_dir):
        self.out_dir = output_dir

    # static method for sanitizing text, namely against ' and \ characters
    # useful for both ffmpeg and general shell handling of filenames
    #
    # input_text [input] - text to sanitize
    #
    # [return] sanitized text
    @staticmethod
    def sanitize_text(input_text):
        san1 = str(input_text).replace("\\", "\\\\")
        san2 = str(san1).replace("'", "'\\''")

        return san2

    # render mp4 from .ffmpeg_audio file
    #
    # input_file_ffmpeg [input] - list of mp3 files to concatenate + render
    # output_mp4_name  [output] - filename of resulting mp4 file
    # 
    def makeMP4(self, input_file_ffmpeg, output_mp4_name):
        start_time = datetime.now()

        # sanitize filenames
        input_sanitized = self.sanitize_text(input_file_ffmpeg)
        output_sanitized = self.sanitize_text(output_mp4_name)
        
        log.debug("... Concatenating mp3s defined in {0}".format(input_sanitized))
        
        mp3_filename = self.out_dir + "/" + \
                start_time.strftime("%y%m%d-%H%M%S") + "_tmp_vid"
        log.debug("... Creating .mp3 file {0}".format(mp3_filename))
        
        mp3_cmd = self.concat_mp3_cmd.format(
            input_sanitized, mp3_filename
        )
        log.debug("... Running this command in terminal:")
        log.debug("... " + mp3_cmd)

        process = subprocess.Popen(
            mp3_cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )

        # (stderr because that's how ffmpeg does it >_< )
        for line in process.stderr:
            log.debug(line)
        process.wait()

        log.debug("... done with concatenating mp3s! ")
        
        mp4_filename = self.out_dir + "/" + output_sanitized
        log.debug("... Creating .mp4 file {0}".format(mp4_filename))

        mp4_cmd = self.make_mp4_cmd.format(
            mp3_filename, mp4_filename
        )
        log.debug("... Running this command in terminal:")
        log.debug("... " + mp4_cmd)

        process = subprocess.Popen(
            mp4_cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )

        # TODO this doesn't report real-time status :/ 
        for line in process.stderr:
            log.debug(line)
            # TODO if line contains (timestamp identifier)
            #     report to std out or something
        process.wait()

        time_delta = datetime.now() - start_time
        log.info("... Video finished! Rendered in {0} minutes"
            .format(time_delta.total_seconds() / 60.0))
        

