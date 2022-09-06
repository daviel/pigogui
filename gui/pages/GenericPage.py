import lvgl as lv

from libs.init_drv import indev1
from gui.styles.PageStyle import GENERIC_PAGE_STYLE
from gui.anims.PageAnim import ANIM_PAGE_SLIDE_OUT_LEFT, ANIM_PAGE_SLIDE_IN_RIGHT



class GenericPage(lv.obj):
	animOut = ""
	animIn = ""
	group = ""

	returnable = False

	def __init__(self):
		super().__init__(lv.scr_act())
		self.group = lv.group_create()
		self.group.add_obj(self)

		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.clear_flag(self.FLAG.SCROLLABLE)
		self.add_style(GENERIC_PAGE_STYLE, 0)
		#self.set_pos(320, 0)
		#self.add_flag(self.FLAG.HIDDEN)

		self.animOut = ANIM_PAGE_SLIDE_OUT_LEFT()
		self.animIn = ANIM_PAGE_SLIDE_IN_RIGHT()

		self.animOut.target = self
		self.animIn.target = self

	def focusPage(self):
		indev1.set_group(self.group)

	def moveIn(self):
		if(self.animIn.is_running() == False):
			self.animIn.start()

	def moveOut(self):
		if(self.animOut.is_running() == False):
			self.animOut.start()

	def pageNextCb(self, page):
		print("Next Page Callback not implemented ", page)

	def pagePrevCb(self, page):
		print("Prev Page Callback not implemented ", page)
