import lvgl as lv

from libs.Helper import loadImage, SDL_KEYS
from gui.components.GameIcon import GameIcon
import libs.Singletons as SINGLETONS


class SettingsIcon(GameIcon):
	def __init__(self, container):
		config = SINGLETONS.DATA_MANAGER.get("configuration")

		super().__init__(container, {
			'title': "Settings",
			'description': "Settings",
			'main_image': config["imgdir"] + "/icons/wrench.png",
			'dirname': "settings",
			'tags': [],
			'size': "",
			'deletable': False,
			'screenshots': []
		})

	def start(self, e):
		print("show settingspage")
		SINGLETONS.PAGE_MANAGER.setCurrentPage("settingspage", True)
