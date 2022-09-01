import lvgl as lv

from gui.pages.GenericPage import GenericPage
from libs.init_drv import indev1
from libs.Helper import loadImage


class LaunchScreenPage(GenericPage):
	def __init__(self):
		super().__init__()

		png_data = loadImage('./imgs/launchscreens/10.png')
		
		img_launchscreen_argb = lv.img_dsc_t({
			'data_size': len(png_data),
			'data': png_data
		})

		img1 = lv.img(self)
		img1.set_src(img_launchscreen_argb)
		img1.set_size(320, 240)

		label = lv.label(img1)
		label.set_text("< Press Start >")
		label.align(lv.ALIGN.BOTTOM_MID, 0, -4)

		self.add_event_cb(self.click_handle, lv.EVENT.ALL, None)

	def click_handle(self, event):
		code = event.get_code()
		if code == lv.EVENT.KEY:
			key = event.get_key()
			self.moveOut()
