#!/bin/bash
#
# convert a list of mp3 files to an mp4 file
#
# args:
#    $1 - input list of files to process (*.ffmpeg)
#    $2 - output location of files (both temp audio file and .mp4 file)

# https://stackoverflow.com/questions/6488275/terminal-text-becomes-invisible-after-terminating-subprocess/59148094#59148094

# bug with some files
# https://stackoverflow.com/questions/55914754/how-to-fix-non-monotonous-dts-in-output-stream-01-when-using-ffmpeg

# first, 'concatenate' mp3s (based on input list data)
echo "Concatenating mp3s..."
ffmpeg -nostdin -f concat -safe 0 -i $1 -c copy $2/_tmp.mp3 &> $2/ffmpeglog.txt

# then, process as mp4
echo "... converting mp3 chunk to mp4 video file (this will take a second) ..."
ffmpeg -loop 1 -i blank.jpg \
    -i $2/_tmp.mp3 \
    -c:v libx264 -preset veryslow -tune stillimage -crf 20 -vf scale=854:480 \
    -c:a aac -b:a 320k -shortest -strict experimental \
    $2/$1_out.mp4 &> $2/ffmpeglog.txt
echo "... done with chunk! "

# #############################################################
# general notes below...
# #############################################################

# preset = speed vs. compression (slower = smaller)
# tune = stillimage
# crf = constant rate factor = 0 is lossless, 51 is god-forsaken
# pix_fmt = (yuv420p is deprecated? a single + matches input?)
#        -pix_fmt yuv420p
# vf is filtering, scale sets video size
#        -vf scale = 854:480
# c:a aac = convert audio to aac (why???)
# could also try 'copy'
# could also try 'libmp3lame'

# -b:a = video quality (???)

# shortest = finish encoding when the shortest input stream ends
# strict = "strictly" follow standards? idk

# 2021 nov 29
# add a wee bit of compression on top of mp3s...
# will need some more tuning... but it's an okay start!!

# 2022 jan 20
# c:v libx264 -preset veryslow -tune stillimage -crf 20 -codec: copy -shortest -strict experimental $1.mp4
# EXTREMELY fast but has problems uploading to vimeo

# replace -b:a with -vbr (scale 1-5) for VBR audio. speed is about 6.6x
# vimeo recommends 320kbs CBR though (runs closer to 7.0x, but filesize increases)

# TODO may improve speed by using pre-rendered "black" 1s video and looping that
