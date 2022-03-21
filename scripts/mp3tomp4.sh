#!/bin/bash

# batch convert mp3s to mp4, then stitch them together

# cleanup any temp files
rm -rf templist.txt
rm -rf tempaudio.mp3

# make list of mp3s
for filename in *.mp3; do
    # filename=$(printf '%q' "$filename")

    # break single quote ' marks
    # because of masochism
    filename=${filename//\'/\'\\\'\'}
    echo "file '$filename'" >> templist.txt
done

echo "** files to process... ** "
cat templist.txt

echo "** concatenating mp3s... **"
ffmpeg -f concat -safe 0 -i templist.txt -c copy tempaudio.mp3

echo "** streaming to video... **"
rm -f $1.mp4
ffmpeg -loop 1 -i ../blank.jpg -i tempaudio.mp3 -c:v libx264 -preset veryslow -tune stillimage -crf 20 -vf scale=854:480 -c:a aac -b:a 320k -shortest -strict experimental $1.mp4

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


# the settings below (29 nov 2021) add a wee bit of compression on top of mp3s...
# will need some more tuning... but it's an okay start!!


# 2022 jan 20
# c:v libx264 -preset veryslow -tune stillimage -crf 20 -codec: copy -shortest -strict experimental $1.mp4
# EXTREMELY fast but has problems uploading to vimeo

# replace -b:a with -vbr (scale 1-5) for VBR audio. speed is about 6.6x
# vimeo recommends 320kbs CBR though (runs closer to 7.0x, but filesize increases)

# TODO may improve speed by using pre-rendered "black" 1s video and looping that

echo "** DONE! rendered $1.mp4**"

echo "***********************************"
echo "Copy to vimeo" 
echo "***********************************"
rm -rf tempaudio.mp3
rm -rf output_descr.txt
python3 ../parse_mp3.py | tee -a output_descr.txt

echo "***********************************"
