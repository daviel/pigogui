import lvgl as lv

from gui.pages.LaunchScreenPage import LaunchScreenPage
from gui.pages.SetupPage import SetupPage
from gui.pages.SetupWifiPage import SetupWifiPage
from gui.pages.GamesOverviewPage import GamesOverviewPage
from gui.pages.SettingsPage import SettingsPage
from gui.pages.GameDetailsPage import GameDetailsPage
from gui.pages.EmptyPage import EmptyPage
from libs.init_drv import indev1


class PageManager():
	currentPage = None
	currentPageName = None
	currentPageGroup = None

	history = []
	pageAnimTime = 1000
	timer = ""

	index = {
		'launchscreenpage': LaunchScreenPage(),
		'setuppage': SetupPage(),
		'setupwifipage': SetupWifiPage(),
		'gamesoverviewpage': GamesOverviewPage(),
		'settingspage': SettingsPage(),
		'gamedetailspage': GameDetailsPage(),
		'emptypage': EmptyPage(),
	}

	def __init__(self):
		self.timer = lv.timer_create(self.animDone, self.pageAnimTime, None)
		#self.setCurrentPage("launchscreenpage", True)
		self.setCurrentPage("gamesoverviewpage", True)

	def setCurrentPage(self, pageName, movingIn, pageData=None):
		if self.currentPage != None:
			self.currentPage.pageClosed()

		self.currentPageName = pageName
		self.currentPage = self.getPageByName(pageName)
		page = self.currentPage
		self.currentPageGroup = page.group
		page.data = pageData
		self.history.append(pageName)

		if movingIn:
			lv.scr_load_anim(page, page.animIn, self.pageAnimTime, 0, False)
		else:
			lv.scr_load_anim(page, page.animOut, self.pageAnimTime, 0, False)
		
		self.timer.reset()
		self.timer.resume()

		page.pageOpened()
		page.focusPage()

	def pagePrev(self):
		print("PrevPage")
		if len(self.history) > 1:
			self.history.pop()
			lastPageName = self.history[len(self.history) - 1]
			self.setCurrentPage(lastPageName, False)

	def getPageByName(self, pageName):
		return self.index[pageName]

	def getCurrentPageInIndex(self):
		return self.index[self.currentPageName]

	def animDone(self, timer):
		print("Anim done")
		timer.pause()

	def hideCurrentPage(self):
		self.currentPage.fade_out(1000, 0)
		group = lv.group_create()
		group.add_obj(lv.btn())
		indev1.set_group(group)

	def showCurrentPage(self):
		self.currentPage.fade_in(1000, 0)
		indev1.set_group(self.currentPageGroup)
