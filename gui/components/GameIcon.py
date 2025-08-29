import lvgl as lv

from libs.Helper import SDL_KEYS, loadImageAndConvert



class GameIcon(lv.button):
	label = ""
	titleScreen = ""
	data = {}

	pressCallback = None

	def __init__(self, container, data):
		super().__init__(container)
		self.singletons = container.singletons
		self.data = data

		if data['main_image'] == None:
			self.label = lv.label(self)
			self.label.set_text(data['title'])
		else:
			config = self.singletons["DATA_MANAGER"].get("configuration")
			gameImage = loadImageAndConvert(
				data["main_image"]
			)
			titleScreen = lv.image(self)
			titleScreen.set_size(92, 164)
			titleScreen.set_src(gameImage)
			#titleScreen.set_style_radius(16, 0)
			#titleScreen.set_style_clip_corner(16, 0)
			titleScreen.align(lv.ALIGN.CENTER, 0, 0)
			self.titleScreen = titleScreen
			
		self.set_size(100, 172)
		#self.set_style_radius(16, 0)
		#self.set_style_clip_corner(16, 0)
		self.add_event_cb(self.handleKey, lv.EVENT.KEY, None)


	def handleKey(self, e):
		code = e.get_code()

		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == SDL_KEYS["SDLK_y"]:
				print("loading detailspage")
				config = self.singletons["DATA_MANAGER"].get("configuration")
				self.singletons["AUDIO_MANAGER"].play(config["sounddir"] + "/tick_002.ogg")
				self.singletons["PAGE_MANAGER"].setCurrentPage("gamedetailspage", True, self.data)
			elif key == SDL_KEYS["SDLK_DELETE"]:
				self.singletons["APPLICATION_MANAGER"].resumeMainApp()
				self.singletons["PAGE_MANAGER"].hideCurrentPage()
			elif key == SDL_KEYS["SDLK_a"]:
				print("Game started: ", self.data["title"])
				config = self.singletons["DATA_MANAGER"].get("configuration")
				self.singletons["APPLICATION_MANAGER"].startApp(
					config["gamesdir"] + self.data["dirname"] + "/" + self.data["executable"],
					self.data["keymap"]
				)
				
				if(self.pressCallback):
					self.pressCallback(self, e)
		