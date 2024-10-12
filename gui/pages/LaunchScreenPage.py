import lvgl as lv

from gui.pages.GenericPage import GenericPage
from libs.init_drv import indev1
from libs.Helper import loadImage, font_baloo_chettan_24, font_baloo_chettan_14
import libs.Singletons as SINGLETONS



class LaunchScreenPage(GenericPage):
	keyPressed = False
	labelVisible = True
	label = ""
	pigoLabel = ""
	animDuration = 1000

	def __init__(self):
		super().__init__()

		self.animIn = lv.SCR_LOAD_ANIM.NONE

		container = lv.obj(self)
		container.set_size(320, 240)

		pigoLabel = lv.label(container)
		pigoLabel.align(lv.ALIGN.CENTER, 0, 0)
		pigoLabel.set_text("PiGO")
		pigoLabel.set_style_text_font(font_baloo_chettan_24, 0)
		
		pigoLabel.fade_in(3000, 0)
		self.pigoLabel = pigoLabel

		versionLabel = lv.label(container)
		versionLabel.align(lv.ALIGN.BOTTOM_RIGHT, 0, 0)
		versionLabel.set_text("v1.0")
		versionLabel.set_style_text_font(font_baloo_chettan_14, 0)
		versionLabel.fade_in(1000, 3000)

		self.add_event_cb(self.page_done, lv.EVENT.ALL, None)
		#self.timer = lv.timer_create(self.update_time, 1500, self)

	def pageOpened(self):
		config = SINGLETONS.DATA_MANAGER.get("configuration")
		self.primaryColor = config["user"]["theme"]["primaryColor"]

		colors = []
		for color in lv.PALETTE.__dict__:
			colors.append(color)
		self.pigoLabel.set_style_text_color(lv.palette_main(colors.index(self.primaryColor)), 0)

	def page_done(self, event):
		code = event.get_code()
		if code == lv.EVENT.KEY:
			if(self.keyPressed == False):
				self.keyPressed = True
				#self.timer.delete()
				config = SINGLETONS.DATA_MANAGER.get("configuration")
				username = config["user"]["profile"]["username"]
				if username == "":
					SINGLETONS.PAGE_MANAGER.setCurrentPage("setuppage", True, self)
				else:
					SINGLETONS.PAGE_MANAGER.setCurrentPage("gamesoverviewpage", True)


	def update_time(self, timer):
		if self.labelVisible:
			self.labelVisible = False
			self.label.add_flag(self.FLAG.HIDDEN)
		else:
			self.labelVisible = True
			self.label.remove_flag(self.FLAG.HIDDEN)