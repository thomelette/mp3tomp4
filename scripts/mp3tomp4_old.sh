#!/bin/bash

# batch convert mp3s to mp4, then stitch them together

# make list of mp3s
rm -rf templist.txt
for filename in *.mp3; do
    echo "file '$filename'" >> templist.txt
done
echo "** files to process... ** "
cat templist.txt

# randomize files...
num_files = $(ls | grep '\.mp3' | wc -l)
# rand_sequence = seq $(num_files) | shuf

# for each mp3
#   grab metadata

echo "** concatenating mp3s... **"
rm -rf tempaudio.mp3
ffmpeg -f concat -safe 0 -i templist.txt -c copy tempaudio.mp3

echo "** streaming to video... **"
rm -f output1.mp4


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

ffmpeg -loop 1 -i blank.jpg -i tempaudio.mp3 -c:v libx264 -preset veryslow -tune stillimage -crf 30 -vf scale=854:480 -c:a aac -b:a 128k -shortest -strict experimental output1.mp4


echo "** DONE! **"

echo "***********************************"
echo "Copy to vimeo" 
echo "***********************************"
python3 ./parse_mp3.py | tee -a vimeo_descr.txt

echo "***********************************"
