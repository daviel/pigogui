import lvgl as lv

from libs.Helper import SDL_KEYS, loadImageAndConvert
from libs.threading import runShellCommand_bg
import uasyncio as asyncio


class DownloadIcon(lv.button):
    label = ""
    titleScreen = ""
    data = {}
    installProgressLabel = ""

    pressCallback = None
    handle = ""

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
            downloadImg.set_size(24, 24)
            downloadImg.set_src(downloadImage)
            downloadImg.set_pos(2, 2)

            installProgressLabel = lv.label(titleScreen)
            installProgressLabel.set_size(92, 24)
            installProgressLabel.set_pos(0, 82)
            installProgressLabel.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
            installProgressLabel.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
            installProgressLabel.set_text("")
            self.installProgressLabel = installProgressLabel

            gameName = lv.label(titleScreen)
            gameName.set_size(92, 24)
            gameName.set_pos(0, 164-24)
            gameName.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
            gameName.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
            gameName.set_text(data['title'])
            self.gameName = gameName

            self.titleScreen = titleScreen
            
        self.set_size(100, 172)
        self.add_event_cb(self.handleKey, lv.EVENT.KEY, None)
        self.add_event_cb(self.installGame, lv.EVENT.PRESSED, None)

    def handleKey(self, e):
        code = e.get_code()
        if code == lv.EVENT.KEY:
            key = e.get_key()
            if key == SDL_KEYS["SDLK_y"]:
                print("loading detailspage")
                self.singletons["PAGE_MANAGER"].setCurrentPage("gamedetailspage", True, self.data)

    def installGame(self, e):
        code = e.get_code()
        if code == lv.EVENT.PRESSED:
            key = e.get_key()
            # install dialog
            config = self.singletons["DATA_MANAGER"].get("configuration")
            self.handle = runShellCommand_bg(config["pigoguidir"] + "/installGame.sh", on_line=self.progress)
            
            if(self.pressCallback):
                self.pressCallback(self, e)

    def progress(self, s: str):
        self.installProgressLabel.set_text(s)
        print(">>> ", s)