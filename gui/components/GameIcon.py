import lvgl as lv

from libs.Helper import loadImage, SDL_KEYS
import libs.Singletons as SINGLETONS


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
		self.title = title
		self.description = description
		self.titleScreenSrc = titleScreenSrc
		self.screenshots = screenshots

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
		self.add_event_cb(self.showDetails, lv.EVENT.ALL, None)
		self.add_event_cb(self.start, lv.EVENT.PRESSED, None)

	
	def start(self, e):
		print("Game started: ", self.title)
		if(self.pressCallback):
			self.pressCallback(self, e)

	def showDetails(self, e):
		code = e.get_code()

		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == SDL_KEYS["SDLK_y"]:
				print("loading detailspage")
				SINGLETONS.PAGE_MANAGER.loadPageByName("gamedetailspage", self)
		