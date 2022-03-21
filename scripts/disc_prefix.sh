#!/bin/bash

# takes $1 and appends it to each file in the directory
for f in * ; do mv -- "$f" "$1_$f" ; done
