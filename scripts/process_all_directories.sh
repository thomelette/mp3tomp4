#!/bin/bash

# runs through all directories here,
# and stitches up an mp4 for each directory (set of music files)

find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c './process_dir.sh "$0"' {} \;

# TODO handle directory better 
