import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS
from gui.styles.CustomTheme import CustomTheme
from gui.styles.PageStyle import SETUP_PAGE_STYLE
from libs.WifiShellParser import WifiShellParser


class SetupWifi(GenericPage):
	nextbutton = ""
	wifiShellParser = WifiShellParser()
	table = ""
	loadAnim = ""

	def __init__(self):
		super().__init__()
		self.wifiShellParser.scanCallback = self.scanResults
		self.wifiShellParser.scan()

		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.ON)
		self.add_flag(self.FLAG.SCROLLABLE)
		self.add_style(SETUP_PAGE_STYLE, 0)
		
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.set_style_pad_column(12, 0)
		self.set_style_pad_row(12, 0)
		
		table = lv.table(self)
		table.set_cell_value(0, 0, "SSID")
		table.set_cell_value(0, 1, "Signal")
		self.table = table

		self.nextbutton = Button(self, "Proceed")
		self.nextbutton.set_size(260, 40)
		self.nextbutton.label.center()
		
		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)

	def scanResults(self, results):
		table = self.table

		i = 1
		for wifiEntry in results:
			table.set_cell_value(i, 0, wifiEntry["ssid"])
			table.set_cell_value(i, 1, wifiEntry["signal"])
			i += 1

		table.set_height(120)
		table.set_width(300)
		table.center()
