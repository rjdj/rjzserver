#!/bin/sh

VER=`bzr revno`
OS_VER=`sw_vers | grep ProductVersion | cut -f2`
DEST=/home/rjdj/www/dev_rjdj_me/builds/rjzserver/
fullname=rjzserver-$VER-OSX_$OS_VER

svn -r447 co http://svn.makotemplates.org/mako/trunk/lib/mako
/System/Library/Frameworks/Python.framework/Versions/2.5/Extras/bin/py2applet --iconfile="`pwd`/media/RjzServer.icns" -i mako.cache rjzserver.py media/
mv rjzserver.app $fullname.app
zip -r $fullname.app.zip $fullname.app
echo
echo "Now do this:"
echo scp $fullname.app.zip osc.rjdj.me:${DEST}versions/
echo ssh osc.rjdj.me "\"cd $DEST; rm rjzserver-*-OSX_$OS_VER.app.zip; ln -s versions/$fullname.app.zip\""
