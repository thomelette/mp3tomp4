# FileHelper.py 
#
# helper class for file/folder manipulation

import os
import sys
import shutil
import random
import logging
log = logging.getLogger(__name__)

class FileHelper:
    
    tmp_dir = ""
    default_seed = 8534701049500966276

    # constructor
    #
    # a new FileHelper object will construct tmp_dir
    # if it doesn't already exist (used for storing ffmpeg
    # input files, logs, etc.)
    #
    # tmp_dir [input] - place to copy your files to
    # seed    [input] - optional seed for file shuffling
    def __init__(self, tmp_dir, seed = default_seed):

        if not os.path.exists(tmp_dir): 
            os.mkdir(tmp_dir)

        self.tmp_dir = tmp_dir
        
        
        # TODO pass verbose logging (by caller) to print seed msgs

        # TODO refactor logging to separate .py file
        

        if seed != self.default_seed:
            seed = random.randrange(sys.maxsize)
        random.seed(seed)

        print("(not debug statement) seed = " + str(seed))
        log.info("hi there:) seed is {0}".format(seed))


    # # copy directory to "here" (FileHelper init'd location aka temp_dir)
    # #
    # def Copy(self, dir_name):
    #     source = dir_name
    #     target = "tmp/."
    #     # TODO move would be faster :/
    #     subprocess.call(['cp', '-r', dir_name, "tmp/."])

    # # get list of folders (one level deep) inside directory
    # # 
    # # d [input] - starting point
    # def GetFolderList(self, d):
    #     folders = []
    #     print("get folder list")
    #     return folders

    # 
    def GetSortedFiles(self, d, extension, shuffle=False):
        files = filter(
            lambda x: os.path.isfile(os.path.join(d, x)),
            os.listdir(d)
        )  

        files = filter(lambda x: x.endswith("." + extension), files)

        # shuffle list
        def sort():
            if shuffle:
                return random.random()
            else:
                return 0

        files = sorted(files, key=lambda x: sort())

        files = ([(d + "/" + f)
            for f in files])

        return files

    def WriteSimpleFile(self, filename, data, dirname=""):
        file_loc = (self.temp_dir + "/"
            + ((dirname + "/") if (dirname) else "" ) 
            + filename
        )

        file = open(file_loc, "w")
        file.write(data)
        file.close

    def WriteEvenSimplerFile(self, filename, data):
        file = open(
            self.tmp_dir + "/" + filename,
            "w"
        )
        file.write(data)
        file.close

    def CopyFileToHere(self, filename):
        # TODO pass timestamp to ffmpeg name
        n = './tmp_run.ffmpeg'
        shutil.copyfile(filename, n)

        return n



    # TODO: check for diff in playlist
    # (compare to existing copy in tmp?)
    # if not exist, start from scratch
    # if does, diff new + existing M3U
    # somehow return file list to higher class

    # get list of files by filter





    