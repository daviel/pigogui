import lvgl as lv
from gui.components.GameIcon import GameIcon
from gui.components.SettingsIcon import SettingsIcon
from gui.components.StoreIcon import StoreIcon
from libs.init_drv import indev1
from libs.Helper import SDL_KEYS



def anim_game_sizes(game, v):
	game.set_size(v, v)

class GamesCarousel(lv.obj):
	isZoomedIn = True
	games = []
	animZoomIn = ""
	animZoomOut = ""
	group = ""

	gameData = []
	singletons = None

	def __init__(self, container):
		super().__init__(container)
		self.singletons = container.singletons

		self.set_size(320, 200)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.set_style_border_width(0, 0)
		self.set_style_pad_column(12, 0)
		self.set_style_pad_row(0, 0)
		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
		bg_color = lv.color_hex(0x555555)
		#bg_color.alpha = 200
		self.set_style_bg_color(bg_color, 0)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.ROLLOVER)

		#self.scroll_to(0, 16, False)

		self.animZoomOut = lv.anim_t()
		self.animZoomOut.init()
		self.animZoomOut.set_values(144, 64)
		self.animZoomOut.set_duration(1000)
		self.animZoomOut.set_path_cb(lv.anim_t.path_ease_in)
		self.animZoomOut.set_custom_exec_cb(self.anim_func)

		self.animZoomIn = lv.anim_t()
		self.animZoomIn.init()
		self.animZoomIn.set_values(64, 144)
		self.animZoomIn.set_duration(1000)
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

	def load(self):
		self.gameData = self.singletons["DATA_MANAGER"].get("games")
		for data in self.gameData:
			game = GameIcon(self, data)
			game.add_event_cb(self.key_pressed, lv.EVENT.KEY, None)
			self.games.append(game)
		SettingsIcon(self)
		StoreIcon(self)

	def key_pressed(self, event):
		code = event.get_code()

		if code == lv.EVENT.KEY:
			key = event.get_key()
			if key == SDL_KEYS["SDLK_x"]:
				self.zoomToggle()

	def unload(self):
		for i in range(self.get_child_count()):
			self.get_child(i).delete_delayed(1000)