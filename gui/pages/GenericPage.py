import lvgl as lv

from libs.init_drv import indev1
from gui.styles.PageStyle import GENERIC_PAGE_STYLE


class GenericPage(lv.obj):
	animOut = ""
	animIn = ""
	group = ""

	def __init__(self):
		super().__init__()
		self.group = lv.group_create()
		self.group.add_obj(self)

		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.clear_flag(self.FLAG.SCROLLABLE)
		self.add_style(GENERIC_PAGE_STYLE, 0)

		self.animOut = lv.SCR_LOAD_ANIM.MOVE_RIGHT
		self.animIn = lv.SCR_LOAD_ANIM.MOVE_LEFT

	def focusPage(self):
		indev1.set_group(self.group)

	def pageNextCb(self):
		print("Next Page Callback not implemented ", self)

	def pagePrevCb(self):
		print("Prev Page Callback not implemented ", self)

	def pageOpened(self):
		print("page has been opened")

	def pageClosed(self):
		print("page has been closed")
