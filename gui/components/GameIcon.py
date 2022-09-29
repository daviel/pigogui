import lvgl as lv

from libs.Helper import SDL_KEYS, loadImageAndConvert
import libs.Singletons as SINGLETONS


class GameIcon(lv.btn):
	label = ""
	titleScreen = ""
	data = {}

	pressCallback = None

	def __init__(self, container, data):
		super().__init__(container)
		self.data = data

		if data['titleScreenSrc'] == None:
			self.label = lv.label(self)
			self.label.set_text(data['title'])
		else:
			gameImage = loadImageAndConvert(data['titleScreenSrc'])
			titleScreen = lv.img(self)
			titleScreen.set_size(92, 164)
			titleScreen.set_src(gameImage)
			#titleScreen.set_style_radius(16, 0)
			#titleScreen.set_style_clip_corner(16, 0)
			titleScreen.align(lv.ALIGN.CENTER, 0, 0)
			self.titleScreen = titleScreen
			
		self.set_size(100, 172)
		#self.set_style_radius(16, 0)
		#self.set_style_clip_corner(16, 0)
		self.add_event_cb(self.showDetails, lv.EVENT.ALL, None)
		self.add_event_cb(self.start, lv.EVENT.PRESSED, None)

	
	def start(self, e):
		print("Game started: ", self.data["title"])
		code = e.get_code()
		if code == lv.EVENT.PRESSED:

			print("pressed")
			key = e.get_key()
			print(key)
		
		if(self.pressCallback):
			self.pressCallback(self, e)

	def showDetails(self, e):
		code = e.get_code()

		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == SDL_KEYS["SDLK_y"]:
				print("loading detailspage")
				SINGLETONS.PAGE_MANAGER.setCurrentPage("gamedetailspage", True, self.data)
		