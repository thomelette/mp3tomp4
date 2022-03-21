#!/bin/bash

# runs mp3tomp4 on a directory (used in higher scripts)
# assume directory is arg. $1

# get current directory...
pwd=$(pwd)

# ... then go to $1...
cd "$1"
echo "executing mp3tomp4 on directory..."
echo "$1"

# break directory name by spaces for simplicity
splitname=(${1})
videofilename=${splitname[0]}_${splitname[1]}
# TODO this will break if folder has no spaces

# render video
../mp3tomp4.sh $videofilename
echo "...done with mp3tomp4!"

# copy back up one folder
echo "copying .mp4 to (this) directory..."
cp $videofilename.mp4 $pwd/.
cd $pwd

