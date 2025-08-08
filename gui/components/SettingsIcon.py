import lvgl as lv

from libs.Helper import loadImage, SDL_KEYS
from gui.components.GameIcon import GameIcon



class SettingsIcon(GameIcon):
	parent = None

	def __init__(self, container):
		self.parent = container
		config = self.parent.parent.singletons["DATA_MANAGER"].get("configuration")

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

	def start(self, e):
		print("show settingspage")
		self.parent.parent.singletons["PAGE_MANAGER"].setCurrentPage("settingspage", True)
