#!/bin/bash
# read.sh /path/to/pipe
# 
# this script will read from a pipe and print anything read.

pipe=$1

while true
do
    if read line <$pipe; then
        echo $line
    fi
done
