#!/bin/sh

if [ ! -d ~/bin ]; then
  mkdir ~/bin
fi
if [ ! -d ~/bin/settings ]; then
  mkdir ~/bin/settings
fi
echo "Copying the files"
cp settings/* ~/bin/settings/
cp auto_header.py ~/bin/
echo "Done, restart the bash"
