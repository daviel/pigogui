import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.topbar import TopBar
from gui.components.bottombar import BottomBar
from gui.components.games import Games


class GamesOverviewPage(GenericPage):
	container = ""

	def __init__(self):
		super().__init__()

		self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		self.set_size(320, 240)
		self.set_style_pad_column(0, 0)
		self.set_style_pad_row(0, 0)
		self.set_style_border_width(0, 0)

		tobpar1 = TopBar(self)
		games1 = Games(self)
		bottombar1 = BottomBar(self)
		
		self.group = games1.group