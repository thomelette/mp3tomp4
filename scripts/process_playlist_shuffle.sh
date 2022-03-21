#!/bin/bash

# runs through ONE directory that has a lot of music
# processes it into multiple ~1hr video chunks

# [ ] add support for when a playlist gets updated on spotify, not locally
# save savify generated .m3u (can you have savify just get the .m3u?)
# if not, run savify, diff the two .m3u files (hopefully you saved the old one)
# use .m3u files to create new subdirectory

./scripts/file_tumbler.py -d $1

# need to get a better workflow for which directory to start in
cd $1
../scripts/process_all_directories.sh
