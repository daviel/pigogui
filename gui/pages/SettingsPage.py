import lvgl as lv

from gui.pages.GenericPage import GenericPage
from libs.init_drv import indev1, addGlobalKeyCallback, removeGlobalKeyCallback
from libs.Helper import loadImage
import libs.Singletons as SINGLETONS
from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller


class SettingsPage(GenericPage):
	menu = None
	darkTheme = False
	primaryColor = lv.PALETTE.GREEN
	hidden = False

	def __init__(self):
		super().__init__()

		container = lv.obj(self)
		container.set_size(320, 240)
		container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		container.clear_flag(container.FLAG.SCROLLABLE)

		# Create a menu object
		menu = lv.menu(container)
		self.menu = menu
		menu.align(lv.ALIGN.TOP_LEFT, -24, -16)
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
				"page": self.addDisplayPage(),
				"symbol": lv.SYMBOL.IMAGE,
				"name": "Display"
			},
			{
				"page": self.addSoundPage(),
				"symbol": lv.SYMBOL.AUDIO,
				"name": "Sound"
			},
			{
				"page": self.addWifiPage(),
				"symbol": lv.SYMBOL.WIFI,
				"name": "Wifi"
			},
			{
				"page": self.addBluetoothPage(),
				"symbol": lv.SYMBOL.BLUETOOTH,
				"name": "Bluetooth"
			},
			{
				"page": self.addUserPage(),
				"symbol": lv.SYMBOL.HOME,
				"name": "User"
			},
			{
				"page": self.addStoragePage(),
				"symbol": lv.SYMBOL.SD_CARD,
				"name": "Storage"
			},
			{
				"page": self.addAboutPage(),
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
		menu.set_page(pages[0]["page"])

	def pageOpened(self):
		addGlobalKeyCallback(self.globalExitPage)
		self.hidden = False

	def pageClosed(self):
		removeGlobalKeyCallback(self.globalExitPage)

	def globalExitPage(self, indev, drv, data):
		#print(indev.get_key())
		if indev.get_key() == 27 and self.hidden == False and indev.group == self.group:
			self.hidden = True
			SINGLETONS.PAGE_MANAGER.setCurrentPage("gamesoverviewpage", False)

	def addPressEvent(self, event):
		print(event)

	def changeThemeHandler(self, e):
		code = e.get_code()
		obj = e.get_target()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.UP or key == lv.KEY.DOWN:
				option = " " * 20
				obj.get_selected_str(option, len(option))
				selection = option.strip()[:-1]

				if selection == "Light":
					self.darkTheme = False
				elif selection == "Dark":
					self.darkTheme = True
				else:
					colors = lv.PALETTE.__dict__
					primary_color = colors[selection]
					self.primaryColor = primary_color

				lv.theme_default_init(lv.disp_get_default(), 
						lv.palette_main(self.primaryColor), 
						lv.palette_main(lv.PALETTE.GREY), 
						self.darkTheme, 
						lv.font_montserrat_16)


	def addMenuPage(self, symbol, title, page):
		btn = lv.btn(self.main_page)
		btn.set_size(72, 24)
		btn.set_style_pad_hor(4, 0)
		btn.set_style_pad_ver(4, 0)
		btn.set_flex_flow(lv.FLEX_FLOW.ROW)

		symbolLabel = lv.label(btn)
		symbolLabel.set_text(symbol)
		symbolLabel.set_width(18)
		symbolLabel.center()

		label = lv.label(btn)
		label.set_text(title)
		label.set_width(42)
		label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
		
		self.menu.set_load_page_event(btn, page)
		return btn

	def addDisplayPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(230)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)

		# content
		label = lv.label(subPage)
		label.set_text("Brightness")

		slider = ActiveSlider(subPage)
		slider.center()
		slider.set_width(160)
		slider.set_range(0, 10)

		label = lv.label(subPage)
		label.set_text("Minutes to wait to turn off display")
		label.set_width(80)

		roller1 = ActiveRoller(subPage)
		roller1.set_options("\n".join([
			"1",
			"2",
			"3",
			"5",
			"10",
			"15",
			"Never",
			]),lv.roller.MODE.INFINITE)

		roller1.set_visible_row_count(3)
		roller1.set_width(60)

		label = lv.label(subPage)
		label.set_text("Minutes to wait to turn darken display")
		label.set_width(80)

		roller2 = ActiveRoller(subPage)
		roller2.set_options("\n".join([
			"1",
			"2",
			"3",
			"5",
			"10",
			"15",
			"Never",
			]),lv.roller.MODE.INFINITE)

		roller2.set_visible_row_count(3)
		roller2.set_width(60)

		return subPage

	def addSoundPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(subPage)
		label.set_text("Volume")

		slider = ActiveSlider(subPage)
		slider.center()
		slider.set_width(160)
		slider.set_range(0, 10)

		label = lv.label(subPage)
		label.set_text("Menu Sounds")

		slider = ActiveSlider(subPage)
		slider.center()
		slider.set_width(160)
		slider.set_range(0, 10)

		return subPage

	def addWifiPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(subPage)
		label.set_text("Not implemented yet")
		label.set_width(160)

		return subPage

	def addBluetoothPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(subPage)
		label.set_text("Not implemented yet")
		label.set_width(160)

		return subPage

	def addUserPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(subPage)
		label.set_text("Theme mode")
		label.set_width(80)

		roller1 = ActiveRoller(subPage)
		roller1.set_options("\n".join([
			"Light",
			"Dark",
			]),lv.roller.MODE.NORMAL)
		roller1.set_visible_row_count(2)
		roller1.set_width(120)
		roller1.add_event_cb(self.changeThemeHandler, lv.EVENT.ALL, None)

		label = lv.label(subPage)
		label.set_text("Theme color")
		label.set_width(80)

		colors = []
		for color in lv.PALETTE.__dict__:
			colors.append(color)

		roller1 = ActiveRoller(subPage)
		roller1.set_options("\n".join(colors), lv.roller.MODE.INFINITE)
		roller1.set_visible_row_count(3)
		roller1.set_width(120)
		roller1.add_event_cb(self.changeThemeHandler, lv.EVENT.ALL, None)

		return subPage

	def addStoragePage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(subPage)
		label.set_text("Not implemented yet")
		label.set_width(160)

		return subPage

	def addAboutPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		subPage.set_style_pad_hor(8, 0)
		subPage.set_style_pad_ver(8, 0)
		# content
		label = lv.label(subPage)
		label.set_text("PiGO V1.0")
		label.set_width(160)

		label = lv.label(subPage)
		label.set_text("Last time checked:")
		label.set_width(160)

		label = lv.label(subPage)
		label.set_text("About an hour ago")
		label.set_width(160)

		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		btn.set_width(160)
		label = lv.label(btn)
		label.set_text("Check for Updates")

		label = lv.label(subPage)
		label.set_text(
"""
Made and developed by David Krawiec \n\n
Thank you for using PiGO. :)
""")
		label.set_long_mode(lv.label.LONG.WRAP)
		label.set_width(160)

		return subPage
