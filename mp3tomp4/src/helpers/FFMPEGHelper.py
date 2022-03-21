# FFMPEGHelper.py
#
# helper class for handling ffmpeg calls

import subprocess
import datetime

import logging
log = logging.getLogger(__name__)

# TODO (very big) - port to ffmpeg-python binding
# https://github.com/kkroening/ffmpeg-python

class FFMPEGHelper:

    concat_mp3_cmd = \
        "ffmpeg -nostdin -f concat -safe 0 -i {0} " + \
            "-c copy tmp/_tmp.mp3 "

    def Now(self):
        return datetime.datetime.now().strftime("%y%m%d-%H%M%S")


    def runMP3(self, input_file_ffmpeg):

        # the approach should be something like
        # raw .sh file to > log to tmp/somewhere
        # poll on std err *periodically* (i think it's time consuming but not sure)


        print(self.concat_mp3_cmd.format(input_file_ffmpeg))



        print("that's the command ^^^")


        print("running 1")

        process = subprocess.Popen(
            [self.concat_mp3_cmd.format(input_file_ffmpeg)],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )


        #with open('tmp/ffmpeg2.log', 'wb') as f:
        for line in process.stderr:
            log.debug(line)

        process.wait()

        # TODO finish ffmpeg calls (remove mp3tomp4.sh dependency)





        
        #print(self.mp3_concat_cmd.format(input_file_ffmpeg))

        # print(input_file_ffmpeg)

        # process = subprocess.Popen(
        #     #['echo', input_file_ffmpeg],
        #     #self.mp3_concat_cmd.format(input_file_ffmpeg),
        #     #['ffmpeg -f concat -safe 0 -i', input_file_ffmpeg, '-c copy tempaudio.mp3'],

        #     # TODO pass timestamp too
        #     ['./helpers/mp3tomp4.sh', input_file_ffmpeg, 'tmp'],
        #     stdout = subprocess.PIPE,
        #     stderr = subprocess.PIPE
        # )

        #while process.poll() is None:
        #    time.sleep(1)

        #for c in iter(lambda: process.stderr.read(1), b''):
        #    sys.stderr.buffer.write(c)
        #     f.write(c)

        print('done')

        # this works(?) for "real time" output
        # but i may need to monitor stderr (see line below)
        #
        # while True:
        #     output = process.stdout.readline()
        #     if len(output) == 0 and process.poll() is not None:
        #         break
        #     if output:
        #         print(output.strip())
        #     rc = process.poll()


        # # i think there's a bug here where it hangs since
        # # std err is empty

        # while True:
        #     out_std = process.stdout.readline()
        #     out_err = process.stderr.readline()

        #     if len(out_std) == 0 and process.poll() is not None:
        #         break

        #     if out_std: 
        #         print("STD: ")
        #         print(out_std.strip())

        #     if out_err:
        #         print("ERR: ")
        #         print(out_err.strip())
            
        #     rc = process.poll()


        

        # old fashioned way
        # stdout, stderr = process.communicate()

        # TODO okay so stderr has ffmpeg output... 
        # #            move that to my generated .log file
        #print(stderr)

        # return rc

        # copy .ffmpeg file to ./ 

        # render tmp audio file

        # render mp4 file

        # remove tmp audio file
        # remove .ffmpeg file from ./




#     import subprocess
# process = subprocess.Popen(['echo', 'More output'],
#                      stdout=subprocess.PIPE, 
#                      stderr=subprocess.PIPE)
# stdout, stderr = process.communicate()
# stdout, stderr

