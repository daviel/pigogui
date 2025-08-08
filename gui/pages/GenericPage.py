import lvgl as lv

from libs.init_drv import indev1
from gui.styles.PageStyle import GENERIC_PAGE_STYLE


class GenericPage(lv.obj):
	animOut = lv.SCR_LOAD_ANIM.MOVE_RIGHT
	animIn = lv.SCR_LOAD_ANIM.MOVE_LEFT
	animDuration = 1000
	group = None
	data = {}
	singletons = None

	def __init__(self, singletons):
		self.setSingletons(singletons)
		super().__init__()
		self.group = lv.group_create()
		self.group.add_obj(self)

		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.remove_flag(self.FLAG.SCROLLABLE)
		self.add_style(GENERIC_PAGE_STYLE, 0)

	def focusPage(self):
		indev1.set_group(self.group)

	def pageOpened(self):
		print("page has been opened")

	def pageClosed(self):
		print("page has been closed")
    
	def setSingletons(self, singletons):
		self.singletons = singletons