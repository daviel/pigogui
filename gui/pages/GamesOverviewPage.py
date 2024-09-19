import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.TopBar import TopBar
from gui.components.BottomBar import BottomBar
from gui.components.GamesCarousel import GamesCarousel


class GamesOverviewPage(GenericPage):
	container = ""
	animOut = lv.SCR_LOAD_ANIM.MOVE_BOTTOM
	animIn = lv.SCR_LOAD_ANIM.MOVE_TOP
	animDuration = 500

	def __init__(self):
		super().__init__()

		self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		self.set_size(320, 240)
		self.set_style_pad_column(0, 0)
		self.set_style_pad_row(0, 0)
		self.set_style_border_width(0, 0)
		self.set_style_bg_opa(100, 0)

		self.tobpar1 = TopBar(self)
		self.games1 = GamesCarousel(self)
		self.bottombar1 = BottomBar(self)

		self.group = self.games1.group

	def pageOpened(self):
		self.games1.load()

	def pageClosed(self):
		self.games1.unload()