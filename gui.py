import os
import wx
import webbrowser
from config import config

config.SetFilename("RjzServer.cfg")

ID_ABOUT = 101
ID_HELP = 102
ID_DIR = 103
ID_EXIT = 110
# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
	"""Define ExtMsgEvent Event."""
	win.Connect(-1, -1, EVT_RESULT_ID, func)

class ExtMsgEvent(wx.PyEvent):
	"""Simple event to carry arbitrary result data."""
	def __init__(self, data):
		"""Init ExtMsg Event."""
		wx.PyEvent.__init__(self)
		self.SetEventType(EVT_RESULT_ID)
		self.data = data

class MainWindow(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(600, 300), pos=(100, 100))
		
		self.txt = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
		self.txt.SetEditable(False)
		self.txt.AppendText("Waiting for the RjzServer thread to start...\n\n")
		self.firstpost = True
		
		self.CreateStatusBar() # A StatusBar in the bottom of the window
		
		# Setting up the menu.
		filemenu= wx.Menu()
		filemenu.Append(ID_DIR, "&Set scene directory", " Set the scene directory where your scenes are stored")
		filemenu.Append(ID_HELP, "&Help"," How to use RjzServer")
		filemenu.Append(ID_ABOUT, "&About"," Information about this program")
		filemenu.AppendSeparator()
		filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")
		
		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
		
		# attach events to each menu item
		wx.EVT_MENU(self, ID_DIR, self.OnSetDir)
		wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)
		wx.EVT_MENU(self, ID_HELP, self.OnHelp)
		wx.EVT_MENU(self, ID_EXIT, self.OnExit)
		# message events from outside the app
		EVT_RESULT(self, self.OnExtMsg)
		
		self.Show(True)
	
	def OnSetDir(self, e):
		from config import config
		config.SetFilename("rjzserver.cfg")
		# lauch a directory browser
		dialog = wx.DirDialog(None, "Choose the directory where your scenes live", defaultPath=config.Get("scenedir", default="."), style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_OK:
			config.Set("scenedir", dialog.GetPath())
			self.txt.AppendText("Set .rj scenes directory to %s\n" % dialog.GetPath())
			config.Save()
			dialog.Destroy()
	
	def OnAbout(self, e):
		# Create a message dialog box
		d= wx.MessageDialog( self, 	" By Chris McCormick \n"
						" chrism@rjdj.me\n"
						" \n"
						" http://rjdj.me/","RjDj RjzServer", wx.OK)
		d.ShowModal() # Show modally
		d.Destroy() # destroy it when finished.
	
	def OnHelp(self, e):
		webbrowser.open("http://more.rjdj.me/RjzServer/")
	
	def OnExit(self, e):
		self.Close(True)  # Close the frame.
	
	def OnExtMsg(self, event):
		if self.firstpost:
			self.firstpost = False
			self.txt.SetValue("")
		self.txt.AppendText(event.data)

class RjzGUI(wx.PySimpleApp):
	def OnInit(self):
		self.frame = MainWindow(None, -1, "RjDj RjzServer")
		return True
	
	def PostMessage(self, txt):
		wx.PostEvent(self.frame, ExtMsgEvent(txt))

if __name__ == "__main__":
	gui = RjzGUI()
	gui.MainLoop()

