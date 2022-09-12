import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.button import Button
from gui.styles.PageStyle import SETUP_PAGE_STYLE
from gui.components.Loader import Loader

from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS
#from libs.WifiShellParser import WifiShellParser

class SetupWifi(GenericPage):
	nextbutton = ""
	#wifiShellParser = WifiShellParser()
	wifiContainer = ""
	loadAnim = ""

	def __init__(self):
		super().__init__()
		#self.wifiShellParser.scanCallback = self.scanResults
		#self.wifiShellParser.scan()

		self.add_style(SETUP_PAGE_STYLE, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.set_style_pad_column(0, 0)
		self.set_style_pad_row(4, 0)
		
		label = lv.label(self)
		label.set_text("WiFi-Setup")
		label.set_width(300)

		self.loaderContainer = lv.obj(self)
		self.loaderContainer.set_size(310, 170)
		self.loaderContainer.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.loaderContainer.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.loaderContainer.set_style_pad_column(0, 0)
		self.loaderContainer.set_style_pad_row(8, 0)
		self.loader = Loader(self.loaderContainer)

		self.wifiContainer = lv.obj(self)
		self.wifiContainer.set_size(310, 170)
		self.wifiContainer.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.wifiContainer.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.wifiContainer.set_style_pad_column(0, 0)
		self.wifiContainer.set_style_pad_row(8, 0)
		self.wifiContainer.add_flag(self.FLAG.HIDDEN)

		self.backbutton = Button(self, lv.SYMBOL.LEFT)
		self.backbutton.set_size(50, 30)
		self.backbutton.label.center()
		self.backbutton.add_event_cb(self.pageBack, lv.EVENT.PRESSED, None)

		self.refreshbutton = Button(self, lv.SYMBOL.REFRESH)
		self.refreshbutton.set_size(50, 30)
		self.refreshbutton.label.center()
		self.refreshbutton.add_event_cb(self.pageNext, lv.EVENT.PRESSED, None)

		self.nextbutton = Button(self, lv.SYMBOL.RIGHT)
		self.nextbutton.set_size(50, 30)
		self.nextbutton.label.center()
		self.nextbutton.add_event_cb(self.pageNext, lv.EVENT.PRESSED, None)
		
		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)

	def scanResults(self, results):
		self.wifiContainer.clean()

		for wifiEntry in results:
			wifiConnectButton = Button(self.wifiContainer, lv.SYMBOL.WIFI + " " + wifiEntry["ssid"])
			wifiConnectButton.set_width(280)
			wifiConnectButton.data = wifiEntry
			wifiConnectButton.pressCallback = self.connectWifi

		self.loaderContainer.add_flag(self.FLAG.HIDDEN)
		self.wifiContainer.clear_flag(self.FLAG.HIDDEN)
		self.group.add_obj(self.wifiContainer)

		lv.gridnav_remove(self.wifiContainer)
		lv.gridnav_add(self.wifiContainer, lv.GRIDNAV_CTRL.NONE)


	def connectWifi(self, obj, e):
		self.wifiShellParser.connect(obj.data["ssid"], "password")

	def pageBack(self, e):
		self.pagePrevCb()

	def pageNext(self, e):
		self.pageNextCb()
