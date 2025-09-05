import lvgl as lv

from gui.pages.LaunchScreenPage import LaunchScreenPage

from gui.pages.setup.SetupIntro import SetupIntro
from gui.pages.setup.SetupTheme import SetupTheme
from gui.pages.setup.SetupPage import SetupPage
from gui.pages.setup.SetupWifiPage import SetupWifiPage
from gui.pages.setup.SetupLanguage import SetupLanguage
from gui.pages.setup.SetupTimePage import SetupTimePage

from gui.pages.GamesOverviewPage import GamesOverviewPage
from gui.pages.StorePage import StorePage
from gui.pages.SettingsPage import SettingsPage
from gui.pages.GameDetailsPage import GameDetailsPage
from gui.pages.EmptyPage import EmptyPage

from libs.init_drv import indev1

from libs.Helper import SDL_KEYS, update_available
from libs.GenericManager import GenericManager


class PageManager(GenericManager):
	currentPage = None
	currentPageName = None
	currentPageGroup = None

	history = []
	timer = ""

	index = {
		'launchscreenpage': LaunchScreenPage,

		'setupintropage': SetupIntro,
		'setuppage': SetupPage,
		'setupthemepage': SetupTheme,
		'setupwifipage': SetupWifiPage,
		'setuplanguagepage': SetupLanguage,
		'setuptimepage': SetupTimePage,

		'storepage': StorePage,
		'gamesoverviewpage': GamesOverviewPage,
		'settingspage': SettingsPage,
		'gamedetailspage': GameDetailsPage,
		'emptypage': EmptyPage,
	}

	def __init__(self, singletons):
		self.setSingletons(singletons)
		self.timer = lv.timer_create(self.animDone, 500, None)
		self.setCurrentPage("launchscreenpage", True)

		if update_available():
			self.singletons["NOTIFICATION_MANAGER"].add(lv.SYMBOL.UPLOAD, "New update available.")
		#self.setCurrentPage("gamesoverviewpage", True)

	def setCurrentPage(self, pageName, movingIn, pageData=None):
		if self.currentPage != None:
			self.currentPage.pageClosed()

		self.currentPage = self.getPageByName(pageName)(self.singletons)
		page = self.currentPage
		self.currentPageName = pageName
		self.currentPageGroup = page.group
		page.data = pageData
		self.history.append(pageName)

		if movingIn:
			lv.screen_load_anim(page, page.animIn, page.animDuration, 0, False)
		else:
			lv.screen_load_anim(page, page.animOut, page.animDuration, 0, False)
		
		self.timer.set_period(page.animDuration)
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
		self.setCurrentPage("emptypage", True, self)

	def showCurrentPage(self):
		self.pagePrev()
