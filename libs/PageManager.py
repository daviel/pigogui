import lvgl as lv

from gui.pages.LaunchScreenPage import LaunchScreenPage
from gui.pages.SetupPage import SetupPage


class PageManager():
	launchScreenPage = ""
	setupPage = ""

	def __init__(self):
		self.launchScreenPage = LaunchScreenPage()
		self.setupPage = SetupPage()
		
		#self.setupPage.focusPage()