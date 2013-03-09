#!/bin/sh
set -v

mkdir -p $HOME/.local/share/gedit/plugins/gedit_autopep8
cp -r gedit_autopep8 $HOME/.local/share/gedit/plugins/.
cp gedit_autopep8.plugin $HOME/.local/share/gedit/plugins/.
