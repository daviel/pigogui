import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.topbar import TopBar
from gui.components.bottombar import BottomBar
from gui.components.games import Games


class GamesOverviewPage(GenericPage):
	container = ""

	def __init__(self):
		super().__init__()

		col_dsc = [320, lv.GRID_TEMPLATE_LAST]
		row_dsc = [20, 180, 40, lv.GRID_TEMPLATE_LAST]

		self.set_style_grid_column_dsc_array(col_dsc, 0)
		self.set_style_grid_row_dsc_array(row_dsc, 0)
		self.set_size(320, 240)
		self.set_layout(lv.LAYOUT_GRID.value)
		self.set_style_pad_all(0, 0)
		self.set_style_pad_row(0, 0)
		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.clear_flag(self.FLAG.SCROLLABLE)
		self.set_style_border_width(0, 0)

		tobpar1 = TopBar(self)
		tobpar1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
		                     lv.GRID_ALIGN.STRETCH, 0, 1)

		games1 = Games(self)
		games1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
		                     lv.GRID_ALIGN.STRETCH, 1, 1)

		self.group = games1.group

		bottombar1 = BottomBar(self)
		bottombar1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
		                     lv.GRID_ALIGN.STRETCH, 2, 1)
