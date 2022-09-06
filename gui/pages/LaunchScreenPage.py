import lvgl as lv

from gui.pages.GenericPage import GenericPage
from libs.init_drv import indev1
from libs.Helper import loadImage


class LaunchScreenPage(GenericPage):
	keyPressed = False
	labelVisible = True
	label = ""

	def __init__(self):
		super().__init__()

		self.animIn = lv.SCR_LOAD_ANIM.FADE_IN

		#self.set_pos(0, 0)

		container = lv.obj(self)
		container.set_size(320, 240)

		labelVersion = lv.label(container)
		labelVersion.align(lv.ALIGN.CENTER, 0, 0)
		labelVersion.set_text("\uf960 GO v1.0")
		#labelVersion.set_recolor(True)
		labelVersion.set_style_text_font(lv.font_montserrat_16, 0)
		#labelVersion.fade_in(3000, 500)

		#label = lv.label(container)
		#label.set_text("< Press any button >")
		#label.align(lv.ALIGN.BOTTOM_MID, 0, -4)
		#self.label = label

		self.add_event_cb(self.page_done, lv.EVENT.ALL, None)
		#self.timer = lv.timer_create(self.update_time, 1500, self)

	def page_done(self, event):
		code = event.get_code()
		if code == lv.EVENT.KEY:
			if(self.keyPressed == False):
				self.keyPressed = True
				#self.timer._del()
				self.pageNextCb(self)

	def update_time(self, timer):
		if self.labelVisible:
			self.labelVisible = False
			self.label.add_flag(self.FLAG.HIDDEN)
		else:
			self.labelVisible = True
			self.label.clear_flag(self.FLAG.HIDDEN)