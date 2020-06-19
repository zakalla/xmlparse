#!/bin/bash

folder="/home/zyb/test/auto/config/"
files=$(ls $folder)
flag=0
for file in $files
do
  xmllint -format $folder$file > temp.xml
  if [[ -s temp.xml ]]; then
    cat temp.xml > $folder$file
  else
    flag=1
    break
  fi
done
rm temp.xml

if [ $flag -eq 0 ]; then
  python3 parse.py
fi
