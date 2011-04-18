from distutils.core import setup
from sys import argv
import shutil
import py2exe
from os import path, getcwd, system

# get the name of this directory
name = path.basename(getcwd())

# seed the install command line with what we want
argv += ["py2exe"]
setup(
    windows = [
        {
            "script": name + ".py",
            "icon_resources": [(1, "media/RjzServer.ico")]
        }
    ],
    options = {"py2exe": {
        "packages": ["mako.cache"],
    }},
)

