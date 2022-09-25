import lvgl as lv
from gui.components.GameIcon import GameIcon
from gui.components.SettingsIcon import SettingsIcon
from libs.init_drv import indev1
from libs.Helper import SDL_KEYS


def anim_game_sizes(game, v):
	game.set_size(v, v)

class Games(lv.obj):
	isZoomedIn = True
	games = []
	animZoomIn = ""
	animZoomOut = ""
	group = ""

	gameData = [
		{
			'title': "Game 1",
			'description': "This is an example game",
			'titleScreenSrc': "./imgs/covers/cover5.png",
			'genre': "Strategy",
			'size': "104",
			'screenshots': ["./imgs/covers/cover4.png", "./imgs/covers/cover5.png"]
		},
		{
			'title': "Game 2",
			'description': "This is an example game with much text",
			'titleScreenSrc': "./imgs/covers/cover5.png",
			'genre': "Strategy",
			'size': "1334",
			'screenshots': ["./imgs/covers/cover3.png", "./imgs/covers/cover4.png"]
		},
		{
			'title': "Game 3",
			'description': "This is an example game with even more text in the description",
			'titleScreenSrc': "./imgs/covers/cover5.png",
			'genre': "Strategy",
			'size': "12",
			'screenshots': [
				"./imgs/covers/cover1.png", 
				"./imgs/covers/cover2.png",
				"./imgs/covers/cover3.png",
				"./imgs/covers/cover4.png",
				"./imgs/covers/cover5.png",
			]
		},
	]

	def click_handle(self, event):
		code = event.get_code()

		if code == lv.EVENT.KEY:
			key = event.get_key()
			if key == SDL_KEYS["SDLK_x"]:
				self.zoomToggle()
		if code == lv.EVENT.CLICKED:
			print("clicked")

	def __init__(self, container):
		super().__init__(container)

		self.set_size(320, 184)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.set_style_border_width(0, 0)
		self.set_style_pad_column(12, 0)
		self.set_style_pad_row(0, 0)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.ROLLOVER)

		for data in self.gameData:
			game = GameIcon(self, data)
			game.add_event_cb(self.click_handle, lv.EVENT.ALL, None)
			self.games.append(game)
		SettingsIcon(self)

		self.scroll_to(0, 8, lv.ANIM.OFF)

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
		self.group = group

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