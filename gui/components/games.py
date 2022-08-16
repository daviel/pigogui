import lvgl as lv
from gui.components.button import Button
from imagetools import get_png_info, open_png


def anim_game_sizes(game, v):
	game.set_size(v, v)

class Games(lv.obj):
	isZoomedIn = True
	games = []
	animZoomIn = ""
	animZoomOut = ""

	def click_handle(self, event):
		code = event.get_code()

		if code == lv.EVENT.KEY:
			key = event.get_key()
			if key == 120:
				self.zoomToggle()
		if code == lv.EVENT.CLICKED:
			print("clicked")

	def __init__(self, container, indev):
		super().__init__(container)

		self.set_size(320, 240)
		self.align(lv.ALIGN.CENTER, 0, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.set_style_border_width(0, 0)

		for i in range(8):
			game = Button(self, "Title " + str(i))
			game.set_size(144, 144)
			game.label.center()
			game.add_event_cb(self.click_handle, lv.EVENT.ALL, None)
			self.games.append(game)

		self.animZoomOut = lv.anim_t()
		self.animZoomOut.init()
		self.animZoomOut.set_values(144, 64)
		self.animZoomOut.set_time(1000)
		self.animZoomOut.set_path_cb(lv.anim_t.path_ease_in)
		self.animZoomOut.set_custom_exec_cb(self.anim_func)

		self.animZoomIn = lv.anim_t()
		self.animZoomIn.init()
		self.animZoomIn.set_values(64, 144)
		self.animZoomIn.set_time(1000)
		self.animZoomIn.set_path_cb(lv.anim_t.path_ease_in)
		self.animZoomIn.set_custom_exec_cb(self.anim_func)
			
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

	def zoomToggle(self):
		if self.isZoomedIn:
			self.zoomOut()
			self.isZoomedIn = False
		else:
			self.zoomIn()
			self.isZoomedIn = True

	def zoomIn(self):
		print("zoomin")
		lv.anim_t.start(self.animZoomIn)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)

	def zoomOut(self):
		print("zoomout")
		lv.anim_t.start(self.animZoomOut)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)

	def anim_func(self, anim, val):
		for game in self.games:
			game.set_size(val, val)