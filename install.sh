#!/bin/sh

if [ ! -d ~/bin ]; then
  mkdir ~/bin
fi
if [ ! -d ~/bin/autoHeader ]; then
  mkdir ~/bin/autoHeader
fi
if [ ! -d ~/bin/autoHeader/includes ]; then
  mkdir ~/bin/autoHeader/includes
fi
echo "Copying the files"
cp autoHeader/includes/* ~/bin/autoHeader/includes/
cp autoHeader/general.conf ~/bin/autoHeader/
cp auto_header.py ~/bin/
echo "Done, restart the bash"
