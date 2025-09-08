import lvgl as lv

from libs.Helper import SDL_KEYS, loadImageAndConvert


class DownloadIcon(lv.button):
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
                config["pigoguidir"] + data["main_image"]
            )
            titleScreen = lv.image(self)
            titleScreen.set_size(92, 164)
            titleScreen.set_src(gameImage)
            titleScreen.align(lv.ALIGN.CENTER, 0, 0)

            downloadImage = loadImageAndConvert(
                config["imgdir"] + "/icons/import.png"
            )
            downloadImg = lv.image(titleScreen)
            downloadImg.set_size(32, 32)
            downloadImg.set_src(downloadImage)
            downloadImg.set_pos(4, 4)

            downloadIcon = lv.label(titleScreen)
            downloadIcon.set_size(92, 24)
            downloadIcon.set_pos(0, 164-24)
            downloadIcon.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
            downloadIcon.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
            downloadIcon.set_text(data['title'])

            gameName = lv.label(titleScreen)
            gameName.set_size(92, 24)
            gameName.set_pos(0, 164-24)
            gameName.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
            gameName.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
            gameName.set_text(data['title'])

            self.titleScreen = titleScreen
            
        self.set_size(100, 172)
        #self.set_style_radius(16, 0)
        #self.set_style_clip_corner(16, 0)
        self.add_event_cb(self.handleKey, lv.EVENT.KEY, None)
        self.add_event_cb(self.installGame, lv.EVENT.PRESSED, None)


    def handleKey(self, e):
        code = e.get_code()
        print(code)
        if code == lv.EVENT.KEY:
            key = e.get_key()
            print(key)
            if key == SDL_KEYS["SDLK_y"]:
                print("loading detailspage")
                self.singletons["PAGE_MANAGER"].setCurrentPage("gamedetailspage", True, self.data)

    def installGame(self, e):
        code = e.get_code()
        if code == lv.EVENT.PRESSED:
            key = e.get_key()
            # install dialog
            
            if(self.pressCallback):
                self.pressCallback(self, e)