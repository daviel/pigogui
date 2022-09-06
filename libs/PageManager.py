import lvgl as lv

from gui.pages.LaunchScreenPage import LaunchScreenPage
from gui.pages.SetupPage import SetupPage
from gui.pages.SetupWifi import SetupWifi


class PageManager():
	currentPage = ""

	pageOrder = []
	history = []
	pageIndex = 0

	pageAnimTime = 1000
	timer = ""


	def __init__(self):
		self.pageOrder.append(LaunchScreenPage())
		self.pageOrder.append(SetupPage())
		self.pageOrder.append(SetupWifi())

		self.timer = lv.timer_create(self.animDone, self.pageAnimTime, None)
		self.setCurrentPage(self.pageOrder[self.pageIndex], True)

	def setCurrentPage(self, page, movingIn):
		self.currentPage = page
		
		if movingIn:
			lv.scr_load_anim(page, page.animIn, self.pageAnimTime, 0, False)
		else:
			lv.scr_load_anim(page, page.animOut, self.pageAnimTime, 0, False)
		self.timer.reset()
		self.timer.resume()

		page.pageNextCb = self.pageNext
		page.pagePrevCb = self.pagePrev
		page.focusPage()

	def pageNext(self, page):
		print("NextPage")
		if(self.currentPage.returnable == True):
			self.history.append(self.currentPage)

		self.pageIndex += 1
		self.setCurrentPage(self.pageOrder[self.pageIndex], True)

	def pagePrev(self, page):
		print("PrevPage")
		self.history.pop()
		self.pageIndex -= 1
		self.setCurrentPage(self.pageOrder[self.pageIndex], False)

	def animDone(self, timer):
		print("Anim done")
		timer.pause()
		pass
