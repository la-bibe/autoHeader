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
if ! grep "(load \"~/bin/autoHeader/autoheader-mode.el\")" ~/.emacs > /dev/null; then
    echo "(load \"~/bin/autoHeader/autoheader-mode.el\")" >> ~/.emacs
fi
if ! grep "(add-to-list 'auto-mode-alist '(\"\\\\\\\\.conf\\\\\\\\'\" . autoheader-mode))" ~/.emacs > /dev/null; then
    echo "(add-to-list 'auto-mode-alist '(\"\\\\.conf\\\\'\" . autoheader-mode))" >> ~/.emacs
fi
cp autoheader-mode.el ~/bin/autoHeader/
cp autoHeader/includes/* ~/bin/autoHeader/includes/
cp autoHeader/general.conf ~/bin/autoHeader/
cp autoHeader/makefileHeader ~/bin/autoHeader/
cp autoHeader/headerHeader ~/bin/autoHeader/
cp auto_header.py ~/bin/
echo "Done, restart the bash"
