#!/bin/bash

# assume directory is $1

pwd = $(pwd)

cd $1
echo "executing"
../mp3tomp4.sh
echo "done"
cd $pwd
