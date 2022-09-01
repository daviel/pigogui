import lvgl as lv

from gui.pages.LaunchScreenPage import LaunchScreenPage
from gui.pages.SetupPage import SetupPage
from gui.pages.SetupWifi import SetupWifi


class PageManager():
	currentPage = ""

	pageOrder = []
	history = []
	pageIndex = 0


	def __init__(self):
		self.pageOrder.append(LaunchScreenPage())
		self.pageOrder.append(SetupPage())
		self.pageOrder.append(SetupWifi())
		
		self.setCurrentPage(self.pageOrder[self.pageIndex])

	def setCurrentPage(self, page):
		self.currentPage = page

		page.pageNextCb = self.pageNext
		page.pagePrevCb = self.pagePrev

		page.animOut.anim_done_cb = self.animOutDone
		page.animIn.anim_done_cb = self.animInDone
		page.clear_flag(page.FLAG.HIDDEN)
		#page.move_foreground()
		page.focusPage()
		page.moveIn()

	def pageNext(self, page):
		print("NextPage")
		self.currentPage.moveOut()
		
		if(self.currentPage.returnable == True):
			self.history.append(self.currentPage)

		self.pageIndex += 1
		self.setCurrentPage(self.pageOrder[self.pageIndex])


	def pagePrev(self, page):
		print("PrevPage")
		self.currentPage.moveOut()

	def animOutDone(self, obj, anim):
		print("Anim Out done")
		obj.target.add_flag(obj.target.FLAG.HIDDEN)
		#obj.target.delete()

	def animInDone(self, obj, anim):
		print("Anim In done")