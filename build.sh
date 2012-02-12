#!/bin/bash
python2.7 setup.py py2app
REV=`git log --pretty=format:'%h' -n 1`
zip -r rjzserver-$REV.zip dist/RJZServer.app/
