# FileHelper.py 
#
# helper class for file/folder manipulation

import os
import sys
import shutil
import random

import logging
log = logging.getLogger(__name__)

from src.config import StartTime

class FileHelper:
    
    tmp_dir = ""
    seed = 0

    # constructor
    #
    # a new FileHelper object will construct tmp_dir
    # if it doesn't already exist (used for storing ffmpeg
    # input files, logs, etc.)
    #
    # tmp_dir [input] - place to copy your files to
    # seed    [input] - optional seed for file shuffling
    def __init__(self, tmp_dir, seed = 0):

        if not os.path.exists(tmp_dir): 
            os.mkdir(tmp_dir)

        self.tmp_dir = tmp_dir        

        if seed == 0:
            self.seed = random.randrange(sys.maxsize)
        else:
            self.seed = seed
        random.seed(self.seed)

    # return a list of "sorted" files (either alphabetical or random)
    #
    # dir     [input] - input directory
    # ext     [input] - extension to filter on
    # shuffle [input] - set True to randomize (defaults to False)
    #
    # [return] array of file names
    def GetSortedFiles(self, dir, ext, shuffle=False):
        files = filter(
            lambda x: os.path.isfile(os.path.join(dir, x)),
            os.listdir(dir)
        )  

        files = filter(lambda x: x.endswith("." + ext), files)

        # shuffle list
        def sort():
            if shuffle:
                return random.random()
            else:
                return 0

        files = sorted(files, key=lambda x: sort())

        files = ([(dir + "/" + f) for f in files])

        return files

    # write the "video description" file as a .txt
    #
    # filename    [input] - name of .txt file to generate
    # description [input] - video description data
    def WriteDescription(self, filename, description):

        descr_name = "{0}/{1}.txt".format(
            self.tmp_dir, filename)

        with open(descr_name, "w") as file:
            file.write(description)

    # write the ffmpeg input data to a .ffmpeg_audio file
    # (this is just a list of input audio files)
    #
    # filename    [input] - name of .ffmpeg_audio file to generate
    # audio_files [input] - formatted list of audio files
    #
    # [return] the filename of the resulting .ffmpeg_audio file
    def WriteFFMPEGRecipe(self, filename, audio_files):

        ffmpeg_filename = "{0}/{1}-{2}.ffmpeg_audio".format(
            self.tmp_dir, StartTime, filename)

        with open(ffmpeg_filename, "w") as file:
            file.write(audio_files)

        return ffmpeg_filename


    # TODO: check for diff in playlist
    # (compare to existing copy in tmp?)
    # if not exist, start from scratch
    # if does, diff new + existing M3U
    # somehow return file list to higher class

    # get list of files by filter





    