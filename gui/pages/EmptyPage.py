import lvgl as lv

from gui.pages.GenericPage import GenericPage
from libs.Helper import SDL_KEYS

from libs.init_drv import indev1

class EmptyPage(GenericPage):
	animOut = lv.SCR_LOAD_ANIM.MOVE_BOTTOM
	animIn = lv.SCR_LOAD_ANIM.MOVE_TOP
	animDuration = 500
	
	def __init__(self, singletons):
		super().__init__(singletons)
		self.set_style_bg_opa(lv.OPA.TRANSP, 0)

		self.group = lv.group_create()
		button = lv.button()
		button.add_event_cb(self.homeButtonPressed, lv.EVENT.KEY, None)
		self.group.add_obj(button)
		indev1.set_group(self.group)

	def homeButtonPressed(self, indev):
		if indev.get_key() == SDL_KEYS["SDLK_DELETE"]:
			print("show quickmenu")
			APPLICATION_MANAGER.pauseMainApp()
			self.singletons["PAGE_MANAGER"].showCurrentPage()