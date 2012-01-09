#
#	This file is copyright Chris McCormick (PodSix Video Games), 2007
#
#	It is licensed under the terms of the LGPL
#	i.e. if you modify it and distribute it you must make your changes available.
#

from ConfigParser import ConfigParser
from sys import platform
from os import path, environ

DEFAULT_SECTION = "rjz"

class Config(ConfigParser):
    def SetFilename(self, basefilename):
        """
        Build this ConfigParser object and load the file asked for.
        """
        if platform == "win32":
            import win32api
            cfgpath = environ['APPDATA']
            self.filename = path.join(cfgpath, basefilename)
            self.username = win32api.GetUserName()
        elif platform in ["linux2", "linux", "darwin"]:
            cfgpath = path.expanduser("~")
            self.filename = path.join(cfgpath, "." + basefilename)
            self.username = environ['LOGNAME']
        else:
            self.filename = basefilename
            self.username = None

        ConfigParser.__init__(self)
        if path.isfile(self.filename):
            self.read(self.filename)

    def GetFilename(self):
        return self.filename

    def GetUsername(self):
        return self.username

    def Set(self, item, value, section=DEFAULT_SECTION):
        """
        Set an item without throwing an error if the section doesn't exist.
        """
        if not self.has_section(section):
            self.add_section(section)

        self.set(section, item, value)

    def Get(self, item, section=DEFAULT_SECTION, default=""):
        """ Get an item from the default section. """
        if self.has_option(section, item):
            return self.get(section, item)
        else:
            return default

    def Save(self):
        """
        Save this configuration file to where we loaded it from.
        """
        savefile = file(self.filename, "w")
        if savefile:
            self.write(savefile)
            savefile.close()

config = Config()

if __name__ == "__main__":
    config.SetFilename("MyTest.cfg")
    print config.GetFilename()
    print config.GetUsername()

    bob = config.Get("bob")
    print "bob:", str(bob)
    config.Set("bob", (bob and int(bob) or 0) + 1)

    t = config.Get("t", "pants")
    print "t[pants]:", t
    config.Set("t", "hello", "pants")

    config.Save()

