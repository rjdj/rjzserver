import threading
import ctypes
from time import sleep
from sys import exit

from server import RjzServer
from gui import RjzGUI

# set up the GUI
gui = RjzGUI()

# rjzserver's output should go via an event into the GUI
def Output(txt):
	gui.PostMessage(txt + "\n")

# set up the server
server = RjzServer(outputfn=Output)

# start the background server thread
threadSrv = threading.Thread(target=server.Launch)
threadSrv.start()

# run the app loop in this thread
gui.MainLoop()
exit(0)

