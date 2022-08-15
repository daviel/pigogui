import lvgl as lv
from gui.components.button import Button
from imagetools import get_png_info, open_png


class Games(lv.obj):
	clock = ""

	def click_handle(ev, element):
		print(ev)

	def __init__(self, container, indev):
		super().__init__(container)

		self.set_size(320, 240)
		self.align(lv.ALIGN.CENTER, 0, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)

		for i in range(8):
			button1 = Button(self, "Title " + str(i))
			button1.set_size(128, 128)
			button1.label.center()
			button1.add_event_cb(self.click_handle, lv.EVENT.CLICKED, None)
			
		group = lv.group_create()
		group.add_obj(self)
		indev.set_group(group)

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

		#button6 = lv.imgbtn(self)
		#button6.set_grid_cell(lv.GRID_ALIGN.STRETCH, 2, 1,
		#					  lv.GRID_ALIGN.STRETCH, 1, 1)

		#button6.set_src(lv.imgbtn.STATE.RELEASED, imgbtn_left_dsc, imgbtn_left_dsc, imgbtn_left_dsc)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.ROLLOVER)