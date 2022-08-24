import lvgl as lv

from gui.components.topbar import TopBar
from gui.components.bottombar import BottomBar
from gui.components.games import Games


class GamesOverviewPage():
	container = ""

	def click_handle(self, event):
		code = event.get_code()

		if(event.get_indev()):
			indev = event.get_indev()
			print(indev.get_key())

		if code == lv.EVENT.KEY:
			print("clicked")
		if code == lv.EVENT.PRESSED:
			print("clicked")

	def __init__(self):
		col_dsc = [320, lv.GRID_TEMPLATE_LAST]
		row_dsc = [20, 180, 40, lv.GRID_TEMPLATE_LAST]

		container = lv.obj(lv.scr_act())
		container.set_style_grid_column_dsc_array(col_dsc, 0)
		container.set_style_grid_row_dsc_array(row_dsc, 0)
		container.set_size(320, 240)
		container.set_layout(lv.LAYOUT_GRID.value)
		container.set_style_pad_all(0, 0)
		container.set_style_pad_row(0, 0)
		container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		container.clear_flag(container.FLAG.SCROLLABLE)
		container.set_style_border_width(0, 0)
		self.container = container

		self.container.add_event_cb(self.click_handle, lv.EVENT.ALL, None)


		tobpar1 = TopBar(container)
		tobpar1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
		                     lv.GRID_ALIGN.STRETCH, 0, 1)

		games1 = Games(container)
		games1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
		                     lv.GRID_ALIGN.STRETCH, 1, 1)


		bottombar1 = BottomBar(container)
		bottombar1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
		                     lv.GRID_ALIGN.STRETCH, 2, 1)
