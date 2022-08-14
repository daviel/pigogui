import lvgl as lv
from gui.components.button import Button
from imagetools import get_png_info, open_png


class Games(lv.obj):
	clock = ""

	def __init__(self, container):
		col_dsc = [70, 70, 70, 70, lv.GRID_TEMPLATE_LAST]
		row_dsc = [70, 70, lv.GRID_TEMPLATE_LAST]

		super().__init__(container)

		self.set_style_grid_column_dsc_array(col_dsc, 0)
		self.set_style_grid_row_dsc_array(row_dsc, 0)
		self.set_size(320, 240)
		self.set_layout(lv.LAYOUT_GRID.value)

		button1 = Button(self, "10:11")
		button1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
							lv.GRID_ALIGN.STRETCH, 0, 1)

		button2 = Button(self, "11:11")
		button2.set_grid_cell(lv.GRID_ALIGN.STRETCH, 1, 1,
							  lv.GRID_ALIGN.STRETCH, 0, 1)

		button3 = Button(self, "11:12")
		button3.set_grid_cell(lv.GRID_ALIGN.STRETCH, 2, 1,
							  lv.GRID_ALIGN.STRETCH, 0, 1)
		
		button4 = Button(self, "11:12")
		button4.set_grid_cell(lv.GRID_ALIGN.STRETCH, 1, 1,
							  lv.GRID_ALIGN.STRETCH, 1, 1)

		button5 = Button(self, "11:12")
		button5.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
							  lv.GRID_ALIGN.STRETCH, 1, 1)

		# Register PNG image decoder
		decoder = lv.img.decoder_create()
		decoder.info_cb = get_png_info
		decoder.open_cb = open_png

		# Create an image from the png file
		f = open('./imgs/covers/picowar.png','rb')
		imgbtn_left_data = f.read()

		imgbtn_left_dsc = lv.img_dsc_t({
		'data_size': len(imgbtn_left_data),
		'data': imgbtn_left_data
		})

		button6 = lv.imgbtn(self)
		button6.set_grid_cell(lv.GRID_ALIGN.STRETCH, 2, 1,
							  lv.GRID_ALIGN.STRETCH, 1, 1)

		button6.set_src(lv.imgbtn.STATE.RELEASED, imgbtn_left_dsc, imgbtn_left_dsc, imgbtn_left_dsc)

		#button1.add_event_cb(click_handle, lv.EVENT.CLICKED, None)

		group = lv.group_create()
		group.add_obj(self)
		#indev.set_group(group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.ROLLOVER)