####################################################################################
#
#	RjzServer
#	By Chris McCormick
# 	GPLv3
#
#	See the files README and COPYING for details.
#
#       Modified by Christian Haudum for Reality Jockey Ltd.
#       2012
#
#
#       -*- coding: utf-8 -*-
#       vim: set fileencodings=utf-8
#
####################################################################################

import os
from setuptools import setup, find_packages

APP_VERSION = "1.1"

plist = dict(
    LSPrefersPPC = True,
    CFBundleShortVersionString = APP_VERSION,
)

requirements = ['py2app',
                'mako',
                'wxPython',
                ]

OPTIONS = dict(plist=plist,
               iconfile=os.path.join("src","resources","RjzServer.icns"),
               argv_emulation=1,
               includes=['mako.cache',],
               resources=[os.path.join("src","resources","templates"),
                          os.path.join("src","resources","media"),
                          ],
    )

setup(name = "RJZServer",
      app = [os.path.join("src","application.py"),],
      data_files = [],
      options = dict(py2app=OPTIONS),
      version = APP_VERSION,
      author = 'Reality Jockey Limited',
      author_email = 'info@rjdj.me',
      description = 'RJZ Server',
      url = 'http://rjdj.me',
      packages = find_packages('src'),
      package_dir = {'':'src'},
      setup_requires = requirements,
      install_requires = requirements + ['distribute',],
      entry_points = {
          'console_scripts':[
	      'server=application:run',
              'gui=application:gui',
	  ],
          },
      include_package_data = True,
      zip_safe = False,
)
