import lvgl as lv

from libs.Helper import SDL_KEYS, loadImageAndConvert
from libs.threading import runShellCommand_bg
import uasyncio as asyncio


class DownloadIcon(lv.button):
    label = ""
    titleScreen = ""
    data = {}
    installProgressLabel = ""
    statusLabel = ""

    pressCallback = None
    handle = ""

    def __init__(self, container, data):
        super().__init__(container)
        self.singletons = container.singletons
        self.data = data

        config = self.singletons["DATA_MANAGER"].get("configuration")
        gameImage = None
        if data['main_image'] is not None:
            gameImage = loadImageAndConvert(config["pigoguidir"] + data["main_image"])

        if gameImage is None:
            self.label = lv.label(self)
            self.label.set_text(data['title'])
        else:
            titleScreen = lv.image(self)
            titleScreen.set_size(92, 164)
            titleScreen.set_src(gameImage)
            titleScreen.align(lv.ALIGN.CENTER, 0, 0)

            statusLabel = lv.label(titleScreen)
            statusLabel.set_pos(4, 4)
            self.statusLabel = statusLabel

            installProgressLabel = lv.label(titleScreen)
            installProgressLabel.set_size(92, 32)
            installProgressLabel.set_pos(0, 64)
            installProgressLabel.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
            self.installProgressLabel = installProgressLabel

            gameName = lv.label(titleScreen)
            gameName.set_size(92, 24)
            gameName.set_pos(0, 164-24)
            gameName.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
            gameName.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
            gameName.set_text(data['title'])
            self.gameName = gameName

            self.titleScreen = titleScreen
            self._refreshStatus()

        self.set_size(100, 172)
        self.add_event_cb(self.handleKey, lv.EVENT.KEY, None)
        self.add_event_cb(self.installGame, lv.EVENT.CLICKED, None)

    def _getInstalledGame(self):
        for game in self.singletons["DATA_MANAGER"].get("games"):
            if game.get("dirname") == self.data["dirname"]:
                return game
        return None

    def _hasUpdate(self, installed):
        return self.data.get("version", "") != installed.get("version", "")

    def _refreshStatus(self):
        if not self.installProgressLabel:
            return
        installed = self._getInstalledGame()
        if installed and not self._hasUpdate(installed):
            self.statusLabel.set_text(lv.SYMBOL.OK)
            self.installProgressLabel.set_text("Installed")
        elif installed and self._hasUpdate(installed):
            self.statusLabel.set_text(lv.SYMBOL.REFRESH)
            self.installProgressLabel.set_text("Update v" + self.data.get("version", ""))
        else:
            self.statusLabel.set_text(lv.SYMBOL.DOWNLOAD)
            self.installProgressLabel.set_text("")

    def handleKey(self, e):
        code = e.get_code()
        if code == lv.EVENT.KEY:
            key = e.get_key()
            if key == SDL_KEYS["SDLK_y"]:
                print("loading detailspage")
                self.singletons["PAGE_MANAGER"].setCurrentPage("gamedetailspage", True, self.data)

    def installGame(self, e):
        installed = self._getInstalledGame()
        if installed and not self._hasUpdate(installed):
            return

        if "installing" not in self.data:
            config = self.singletons["DATA_MANAGER"].get("configuration")
            downloadPath = config["user"]["store"]["downloadpath"]
            self.handle = runShellCommand_bg(
                "wget --progress=dot " + self.data["file_url"] + " -P " + downloadPath,
                on_line=self.downloadProgress,
                on_done=self.downloadDone
            )
            self.data["installing"] = True

        if self.pressCallback:
            self.pressCallback(self, e)

    def downloadProgress(self, s: str):
        if not self.installProgressLabel:
            return
        for val in s.split(" "):
            if val.find("%") != -1:
                self.installProgressLabel.set_text("DL: " + val)
                break

    def downloadDone(self, rc):
        print("extracting...")
        config = self.singletons["DATA_MANAGER"].get("configuration")
        downloadPath = config["user"]["store"]["downloadpath"]
        gamePath = config["gamesdir"]
        self.handle = runShellCommand_bg(
            "7z -y x " + downloadPath + self.data["filename"] + " -o" + gamePath,
            on_line=self.extractingProgress,
            on_done=self.extractionDone
        )

    def extractingProgress(self, s: str):
        if self.installProgressLabel:
            self.installProgressLabel.set_text("Extracting...")

    def extractionDone(self, rc):
        self.data.pop("installing", None)
        self.singletons["DATA_MANAGER"].findGames(
            self.singletons["DATA_MANAGER"].get("configuration")["gamesdir"]
        )
        self._refreshStatus()
