import lvgl as lv

from gui.components.topbar import TopBar
from gui.components.bottombar import BottomBar
from gui.components.games import Games


class GamesOverviewPage():

	def click_handle(ev, element):
		print(ev)

	def __init__(self, indev1):
		#super().__init__(container)

		col_dsc = [320, lv.GRID_TEMPLATE_LAST]
		row_dsc = [32, 160, 48, lv.GRID_TEMPLATE_LAST]

		container = lv.obj(lv.scr_act())
		container.set_style_grid_column_dsc_array(col_dsc, 0)
		container.set_style_grid_row_dsc_array(row_dsc, 0)
		container.set_size(320, 240)
		container.set_layout(lv.LAYOUT_GRID.value)
		container.set_style_pad_all(0, 0)
		container.set_style_pad_row(0, 0)
		container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		container.clear_flag(container.FLAG.SCROLLABLE)


		tobpar1 = TopBar(container)
		tobpar1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
		                     lv.GRID_ALIGN.STRETCH, 0, 1)

		games1 = Games(container, indev1)
		games1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
		                     lv.GRID_ALIGN.STRETCH, 1, 1)


		bottombar1 = BottomBar(container)
		bottombar1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
		                     lv.GRID_ALIGN.STRETCH, 2, 1)