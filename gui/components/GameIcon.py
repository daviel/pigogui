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

		if data['main_image'] == None:
			self.label = lv.label(self)
			self.label.set_text(data['title'])
		else:
			config = SINGLETONS.DATA_MANAGER.get("configuration")
			gameImage = loadImageAndConvert(
				data["main_image"]
			)
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
		self.add_event(self.showDetails, lv.EVENT.KEY, None)
		self.add_event(self.start, lv.EVENT.PRESSED, None)

	def start(self, e):
		code = e.get_code()
		if code == lv.EVENT.PRESSED:
			print("Game started: ", self.data["title"])
			config = SINGLETONS.DATA_MANAGER.get("configuration")
			SINGLETONS.APPLICATION_MANAGER.startApp(
				config["gamesdir"] + self.data["dirname"] + "/" + self.data["executable"],
				self.data["keymap"]
			)
		
		if(self.pressCallback):
			self.pressCallback(self, e)

	def showDetails(self, e):
		code = e.get_code()

		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == SDL_KEYS["SDLK_y"]:
				print("loading detailspage")
				SINGLETONS.PAGE_MANAGER.setCurrentPage("gamedetailspage", True, self.data)
			elif key == SDL_KEYS["SDLK_DELETE"]:
				SINGLETONS.APPLICATION_MANAGER.resumeMainApp()
				SINGLETONS.PAGE_MANAGER.hideCurrentPage()
		