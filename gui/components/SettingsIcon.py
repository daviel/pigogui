import lvgl as lv

from libs.Helper import loadImage, SDL_KEYS
from gui.components.GameIcon import GameIcon



class SettingsIcon(GameIcon):
	singletons = None

	def __init__(self, container):
		self.singletons = container.singletons
		config = self.singletons["DATA_MANAGER"].get("configuration")

		super().__init__(container, {
			'title': "Settings",
			'description': "Settings",
			'main_image': config["imgdir"] + "/wrench.png",
			'dirname': "settings",
			'tags': [],
			'size': "",
			'deletable': False,
			'screenshots': []
		})
		self.add_event_cb(self.handleKey, lv.EVENT.KEY, None)


	def handleKey(self, e):
		code = e.get_code()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == SDL_KEYS["SDLK_a"]:
				self.start(e)

	def start(self, e):
		print("show settingspage")
		self.singletons["PAGE_MANAGER"].setCurrentPage("settingspage", True)
