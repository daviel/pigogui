import lvgl as lv

from gui.pages.LaunchScreenPage import LaunchScreenPage
from gui.pages.SetupPage import SetupPage


class PageManager():
	currentPage = ""

	launchScreenPage = ""
	setupPage = ""

	def __init__(self):
		self.launchScreenPage = LaunchScreenPage()
		self.setupPage = SetupPage()
		
		self.setCurrentPage(self.setupPage)

	def setCurrentPage(self, page):
		self.currentPage = page
		page.focusPage()