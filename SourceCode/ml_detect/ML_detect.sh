#!/bin/sh
python="ld-2.27.so ./python3.6"
file="ld-2.27.so ./file/file"
Path=$1
WorkPath=.
find $Path -type f -exec $file {} \; | grep "\<ELF\>" | awk -F ':' '{print $1}' >ELFfile

$python $WorkPath/detect_files.py $WorkPath/ELFfile
