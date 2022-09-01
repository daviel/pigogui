import lvgl as lv

from gui.pages.LaunchScreenPage import LaunchScreenPage
from gui.pages.SetupPage import SetupPage


class PageManager():
	currentPage = ""

	launchScreenPage = ""
	setupPage = ""

	def __init__(self):
		self.setupPage = SetupPage()
		self.launchScreenPage = LaunchScreenPage()

		self.setupPage.pageDoneCb = self.pageDone

		#self.setupPage.add_flag(self.setupPage.FLAG.HIDDEN)
		self.setCurrentPage(self.launchScreenPage)

	def setCurrentPage(self, page):
		self.currentPage = page
		page.clear_flag(page.FLAG.HIDDEN)
		page.focusPage()

	def pageDone(self, page):
		pass
