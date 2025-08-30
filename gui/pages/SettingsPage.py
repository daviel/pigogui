import lvgl as lv

from gui.pages.GenericPage import GenericPage
from libs.init_drv import indev1
from libs.Helper import SDL_KEYS, loadImage


from gui.pages.SettingsSubPages.DisplaySubPage import DisplaySubPage
from gui.pages.SettingsSubPages.SoundSubPage import SoundSubPage
from gui.pages.SettingsSubPages.WifiSubPage import WifiSubPage
from gui.pages.SettingsSubPages.BluetoothSubPage import BluetoothSubPage
from gui.pages.SettingsSubPages.StorageSubPage import StorageSubPage
from gui.pages.SettingsSubPages.UserSubPage import UserSubPage
from gui.pages.SettingsSubPages.AboutSubPage import AboutSubPage


class SettingsPage(GenericPage):
	menu = None
	hidden = False

	def __init__(self, singletons):
		#self.setSingletons(singletons)
		super().__init__(singletons)

		container = lv.obj(self)
		container.set_size(320, 240)
		container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		container.remove_flag(container.FLAG.SCROLLABLE)

		# Create a menu object
		menu = lv.menu(container)
		self.menu = menu
		menu.align(lv.ALIGN.CENTER, 0, 0)
		menu.set_style_pad_column(0, 0)
		menu.set_style_pad_row(0, 0)
		menu.set_style_border_width(0, 0)
		menu.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		menu.set_size(320, 240)

		# Create a main page
		main_page = lv.obj(container)
		self.main_page = main_page
		main_page.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		main_page.set_flex_align(lv.FLEX_FLOW.ROW, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		main_page.set_height(240)
		main_page.set_width(88)
		main_page.set_style_pad_column(0, 0)
		main_page.set_style_pad_row(6, 0)
		main_page.set_style_border_width(0, 0)
		main_page.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

		pages = [
			{
				"page": DisplaySubPage(menu, singletons),
				"symbol": lv.SYMBOL.IMAGE,
				"name": "Display"
			},
			{
				"page": SoundSubPage(menu, singletons),
				"symbol": lv.SYMBOL.AUDIO,
				"name": "Sound"
			},
			{
				"page": WifiSubPage(menu, singletons),
				"symbol": lv.SYMBOL.WIFI,
				"name": "Wifi"
			},
			{
				"page": BluetoothSubPage(menu, singletons),
				"symbol": lv.SYMBOL.BLUETOOTH,
				"name": "Bluetooth"
			},
			{
				"page": UserSubPage(menu, singletons),
				"symbol": lv.SYMBOL.HOME,
				"name": "User"
			},
			{
				"page": StorageSubPage(menu, singletons),
				"symbol": lv.SYMBOL.SD_CARD,
				"name": "Storage"
			},
			{
				"page": AboutSubPage(menu, singletons),
				"symbol": lv.SYMBOL.LIST,
				"name": "About"
			}
		]
		self.group = lv.group_create()
		self.group.add_obj(main_page)
		for page in pages:
			self.addMenuPage(page["symbol"], page["name"], page["page"])
			menu.set_page(page["page"])
			self.group.add_obj(page["page"])
			lv.gridnav_add(page["page"], lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(main_page, lv.GRIDNAV_CTRL.NONE)
		menu.set_sidebar_page(main_page)
		menu.set_page(pages[0]["page"])

	def pageOpened(self):
		self.hidden = False

	def pageClosed(self):
		self.singletons["DATA_MANAGER"].saveAll()

	def globalExitPage(self, indev, drv, data):
		#print(indev.get_key())
		if indev.get_key() == 27 and self.hidden == False and indev.group == self.group:
			self.hidden = True
			self.singletons["PAGE_MANAGER"].setCurrentPage("gamesoverviewpage", False)

	def addMenuPage(self, symbol, title, page):
		btn = lv.button(self.main_page)
		btn.set_size(72, 24)
		btn.set_style_pad_hor(4, 0)
		btn.set_style_pad_ver(4, 0)
		btn.set_flex_flow(lv.FLEX_FLOW.ROW)
		#btn.add_flag(btn.FLAG.EVENT_BUBBLE)
		btn.add_event_cb(page.loadSubPage, lv.EVENT.PRESSED, None)
		btn.add_event_cb(self.handleReturn, lv.EVENT.KEY, None)
		
		symbolLabel = lv.label(btn)
		symbolLabel.set_text(symbol)
		symbolLabel.set_width(18)
		symbolLabel.center()

		label = lv.label(btn)
		label.set_text(title)
		label.set_width(42)
		label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
		
		self.menu.set_load_page_event(btn, page)
		page.set_width(240)
		return btn
	
	def handleReturn(self, e):
		code = e.get_code()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == SDL_KEYS["SDLK_ESCAPE"] and self.hidden == False and indev1.get_group() == self.group:
				self.hidden = True
				self.singletons["PAGE_MANAGER"].setCurrentPage("gamesoverviewpage", False)