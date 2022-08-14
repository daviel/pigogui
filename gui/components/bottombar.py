import lvgl as lv
from gui.components.button import Button


class BottomBar(lv.obj):
	clock = ""


	def __init__(self, container):
		col_dsc = [70, 180, 70, lv.GRID_TEMPLATE_LAST]
		row_dsc = [32, lv.GRID_TEMPLATE_LAST]

		super().__init__(container)

		self.set_style_grid_column_dsc_array(col_dsc, 0)
		self.set_style_grid_row_dsc_array(row_dsc, 0)
		self.set_size(320, 32)
		self.set_layout(lv.LAYOUT_GRID.value)
		self.set_style_pad_all(0, 0)
		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.set_style_shadow_width(0, 0)

		label = lv.label(self)
		label.set_text("10:30")
		label.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
							lv.GRID_ALIGN.STRETCH, 0, 1)
		label.set_style_pad_all(0, 0)

		label1 = lv.label(self)
		label1.set_text("87%")
		label1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 2, 1,
							lv.GRID_ALIGN.STRETCH, 0, 1)
		label1.set_style_pad_all(0, 0)
