import lvgl as lv

from gui.pages.LaunchScreenPage import LaunchScreenPage
from gui.pages.SetupPage import SetupPage
from gui.pages.SetupWifi import SetupWifi
from gui.pages.GamesOverviewPage import GamesOverviewPage
from gui.pages.SettingsPage import SettingsPage
from gui.pages.GameDetailsPage import GameDetailsPage

class PageManager():
	currentPage = None
	currentPageName = None

	history = []
	pageAnimTime = 1000
	timer = ""

	index = {
		'launchscreenpage': {
			'page': LaunchScreenPage(),
			'nextpage': "setuppage",
			'prevpage': None,
			'returnable': False,
		},
		'setuppage': {
			'page': SetupPage(),
			'nextpage': "setupwifi",
			'prevpage': None,
			'returnable': True,
		},
		'setupwifi': {
			'page': SetupWifi(),
			'nextpage': "gamesoverviewpage",
			'prevpage': None,
			'returnable': True,
		},
		'gamesoverviewpage': {
			'page': GamesOverviewPage(),
			'nextpage': None,
			'prevpage': None,
			'returnable': True,
		},
		'settingspage': {
			'page': SettingsPage(),
			'nextpage': None,
			'prevpage': None,
			'returnable': True,
		},
		'gamedetailspage': {
			'page': GameDetailsPage(),
			'nextpage': None,
			'prevpage': None,
			'returnable': True,
		},
	}

	def __init__(self):
		self.timer = lv.timer_create(self.animDone, self.pageAnimTime, None)
		#self.setCurrentPage("launchscreenpage", True)
		self.setCurrentPage("gamedetailspage", True)

	def setCurrentPage(self, pageName, movingIn, pageData=None):
		if self.currentPage != None:
			self.currentPage.pageClosed()

		self.currentPageName = pageName
		self.currentPage = self.getPageByName(pageName)
		page = self.currentPage
		page.data = pageData

		if movingIn:
			lv.scr_load_anim(page, page.animIn, self.pageAnimTime, 0, False)
		else:
			lv.scr_load_anim(page, page.animOut, self.pageAnimTime, 0, not page.returnable)
		
		self.timer.reset()
		self.timer.resume()

		page.pageNextCb = self.pageNext
		page.pagePrevCb = self.pagePrev
		page.pageOpened()
		page.focusPage()

	def loadPageByName(self, pageName, data=None):
		self.setCurrentPage(pageName, True, data)

	def pageNext(self):
		print("NextPage")
		nextPageName = self.lookupNextPage()

		if(self.isCurrentPageReturnable()):
			self.history.append(self.currentPage)

		self.setCurrentPage(nextPageName, True)

	def pagePrev(self, page):
		print("PrevPage")
		self.history.pop()
		prevPageName = self.lookupPrevPage()
		self.setCurrentPage(prevPageName, False)

	def lookupNextPage(self):
		return self.getCurrentPageInIndex()["nextpage"]

	def lookupPrevPage(self):
		return self.getCurrentPageInIndex()["prevpage"]

	def isCurrentPageReturnable(self):
		return self.getCurrentPageInIndex()["returnable"]

	def getPageByName(self, pageName):
		return self.index[pageName]["page"]

	def getCurrentPageInIndex(self):
		return self.index[self.currentPageName]

	def animDone(self, timer):
		print("Anim done")
		timer.pause()
