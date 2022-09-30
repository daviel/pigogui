import lvgl as lv
from gui.pages.GenericPage import GenericPage
from libs.init_drv import indev1


class EmptyPage(GenericPage):
	def __init__(self):
		super().__init__()
		self.animIn = lv.SCR_LOAD_ANIM.FADE_IN
		self.set_style_bg_opa(lv.OPA._0, 0)
