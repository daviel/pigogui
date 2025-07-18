import lvgl as lv

from libs.Helper import loadImage, SDL_KEYS
from gui.components.GameIcon import GameIcon



class SettingsIcon(GameIcon):
	def __init__(self, container):
		config = DATA_MANAGER.get("configuration")

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
		PAGE_MANAGER.setCurrentPage("settingspage", True)
