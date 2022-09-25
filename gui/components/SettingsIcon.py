import lvgl as lv

from libs.Helper import loadImage, SDL_KEYS
from gui.components.GameIcon import GameIcon
import libs.Singletons as SINGLETONS


class SettingsIcon(GameIcon):
	def __init__(self, container):
		super().__init__(container, {
			'title': "Settings",
			'description': "Settings",
			'titleScreenSrc': "./imgs/icons/wrench.png",
			'genre': "",
			'size': "",
			'screenshots': []
		})

	def start(self, e):
		print("show settingspage")
		SINGLETONS.PAGE_MANAGER.setCurrentPage("settingspage", True)
