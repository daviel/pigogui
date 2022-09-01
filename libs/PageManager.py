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

		#self.add_event_cb(self.click_handle, lv.EVENT.ALL, None)
		
		#self.setupPage.add_flag(self.setupPage.FLAG.HIDDEN)
		self.setCurrentPage(self.launchScreenPage)

	def setCurrentPage(self, page):
		self.currentPage = page
		page.clear_flag(page.FLAG.HIDDEN)
		page.focusPage()
