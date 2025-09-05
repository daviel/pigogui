import lvgl as lv

from libs.Helper import loadImage, SDL_KEYS
from gui.components.GameIcon import GameIcon



class StoreIcon(GameIcon):
	singletons = None

	def __init__(self, container):
		self.singletons = container.singletons
		config = self.singletons["DATA_MANAGER"].get("configuration")

		super().__init__(container, {
			'title': "Store",
			'description': "Store",
			'main_image': config["imgdir"] + "/icons/cart.png",
			'dirname': "store",
			'tags': [],
			'size': "",
			'deletable': False,
			'screenshots': [],
			'executable': "",
			'keymap': "",
		})
		self.add_event_cb(self.start, lv.EVENT.PRESSED, None)

	def start(self, e):
		print("show storepage")
		#self.singletons["PAGE_MANAGER"].setCurrentPage("settingspage", True)
