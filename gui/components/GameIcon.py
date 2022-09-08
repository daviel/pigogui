import lvgl as lv

from libs.Helper import loadImage


class GameIcon(lv.btn):
	label = ""
	titleScreen = ""

	title = ""
	description = ""
	titleScreenSrc = ""
	screenshots = []

	pressCallback = None

	def __init__(self, container, title, description, titleScreenSrc=None, screenshots=[]):
		super().__init__(container)

		if titleScreenSrc == None:
			self.label = lv.label(self)
			self.label.set_text(title)
		else:
			gameImage = loadImage(titleScreenSrc)
		
			gameImage = lv.img_dsc_t({
				'data_size': len(gameImage),
				'data': gameImage
			})

			titleScreen = lv.img(self)
			titleScreen.set_size(92, 172)
			titleScreen.set_src(gameImage)
			titleScreen.set_style_radius(16, 0)
			titleScreen.set_style_clip_corner(16, 0)
			titleScreen.align(lv.ALIGN.CENTER, 0, 0)
			self.titleScreen = titleScreen
			
		self.set_size(100, 180)
		self.set_style_radius(16, 0)
		self.set_style_clip_corner(16, 0)
		self.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)

	def addPressEvent(self, e):
		if(self.pressCallback):
			self.pressCallback(self, e)
