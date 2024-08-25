import lvgl as lv

from gui.pages.GenericPage import GenericPage
from libs.Helper import SDL_KEYS
import libs.Singletons as SINGLETONS
from libs.init_drv import indev1

class EmptyPage(GenericPage):
	animOut = lv.SCR_LOAD_ANIM.MOVE_BOTTOM
	animIn = lv.SCR_LOAD_ANIM.MOVE_TOP
	animDuration = 500
	
	def __init__(self):
		super().__init__()
		self.set_style_bg_color(lv.color_t(), 0)

		self.group = lv.group_create()
		button = lv.button()
		button.add_event_cb(self.homeButtonPressed, lv.EVENT.KEY, None)
		self.group.add_obj(button)
		indev1.set_group(self.group)

	def homeButtonPressed(self, indev):
		if indev.get_key() == SDL_KEYS["SDLK_DELETE"]:
			print("show quickmenu")
			SINGLETONS.APPLICATION_MANAGER.pauseMainApp()
			SINGLETONS.PAGE_MANAGER.showCurrentPage()