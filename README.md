# RJZ Server

**by Chris McCormick <chris@mccormick.cx>**
**updated for Reality Jockey Ltd. by Christian Haudum <christian.h@rjdj.me>**

GPLv3 licensed. See the file COPYING for details.

This is not a very secure server, so don't run it on public facing networks. Intended for internal LAN use only.

## Dependencies:

  - Python 2.7
  - wxPython >= 2.9.1.1
  - py2app
  - setuptools

## Bootstrap:

    $ python2.7 bootstrap.py
    $ bin/buildout

## Run server and GUI (separately):

    $ bin/server
    $ bin/gui

## Build:

    $ python2.7 setup.py py2app
