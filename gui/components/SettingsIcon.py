import lvgl as lv

from libs.Helper import loadImage
from gui.components.GameIcon import GameIcon
import libs.Singletons as SINGLETONS


class SettingsIcon(GameIcon):
	def __init__(self, container):
		super().__init__(container, "Settings", "Settings", "./imgs/icons/wrench.png", [])

	def addPressEvent(self, e):
		print("pressed settings")
		SINGLETONS.PAGE_MANAGER.loadPageByName("settingspage")
