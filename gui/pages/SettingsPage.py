import lvgl as lv

from gui.pages.GenericPage import GenericPage
from libs.init_drv import indev1
from libs.Helper import loadImage


class SettingsPage(GenericPage):
	menu = None
	darkTheme = False
	primaryColor = lv.PALETTE.GREEN

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
		#main_page.set_width(60)
		main_page.set_style_pad_column(0, 0)
		main_page.set_style_pad_row(6, 0)
		main_page.set_style_border_width(0, 0)
		main_page.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

		QuickSettingsPage = self.addQuickSettingsPage()
		DisplayPage = self.addDisplayPage()
		SoundPage = self.addSoundPage()
		WifiPage = self.addWifiPage()
		BluetoothPage = self.addBluetoothPage()
		BatteryPage = self.addBatteryPage()
		ThemePage = self.addThemePage()
		HomescreenPage = self.addHomescreenPage()
		StoragePage = self.addStoragePage()
		VersionPage = self.addVersionPage()
		AboutPage = self.addAboutPage()
		PowerPage = self.addPowerPage()

		hardwareLabel = lv.label(main_page)
		hardwareLabel.set_text("Hardware")
		self.addMenuPage(lv.SYMBOL.SETTINGS, "Quicksettings", QuickSettingsPage)
		self.addMenuPage(lv.SYMBOL.IMAGE, "Display", DisplayPage)
		self.addMenuPage(lv.SYMBOL.AUDIO, "Sound", SoundPage)
		self.addMenuPage(lv.SYMBOL.WIFI, "WiFi", WifiPage)
		self.addMenuPage(lv.SYMBOL.BLUETOOTH, "Bluetooth", BluetoothPage)
		self.addMenuPage(lv.SYMBOL.BATTERY_FULL, "Battery", BatteryPage)
		customizationLabel = lv.label(main_page)
		customizationLabel.set_text("Customization")
		self.addMenuPage(lv.SYMBOL.TINT, "Theme", ThemePage)
		self.addMenuPage(lv.SYMBOL.HOME, "Homescreen", HomescreenPage)
		miscLabel = lv.label(main_page)
		miscLabel.set_text("Misc")
		self.addMenuPage(lv.SYMBOL.SD_CARD, "Storage", StoragePage)
		self.addMenuPage(lv.SYMBOL.REFRESH, "Version", VersionPage)
		self.addMenuPage(lv.SYMBOL.LIST, "About", AboutPage)
		self.addMenuPage(lv.SYMBOL.POWER, "Power", PowerPage)

		menu.set_page(QuickSettingsPage)
		menu.set_page(DisplayPage)
		menu.set_page(SoundPage)
		menu.set_page(WifiPage)
		menu.set_page(BluetoothPage)
		menu.set_page(BatteryPage)
		menu.set_page(ThemePage)
		menu.set_page(HomescreenPage)
		menu.set_page(StoragePage)
		menu.set_page(VersionPage)
		menu.set_page(AboutPage)
		menu.set_page(PowerPage)
		menu.set_page(ThemePage)
		menu.set_sidebar_page(main_page)

		self.group = lv.group_create()
		self.group.add_obj(main_page)
		self.group.add_obj(QuickSettingsPage)
		self.group.add_obj(DisplayPage)
		self.group.add_obj(SoundPage)
		self.group.add_obj(WifiPage)
		self.group.add_obj(BluetoothPage)
		self.group.add_obj(BatteryPage)
		self.group.add_obj(ThemePage)
		self.group.add_obj(HomescreenPage)
		self.group.add_obj(StoragePage)
		self.group.add_obj(VersionPage)
		self.group.add_obj(AboutPage)
		self.group.add_obj(PowerPage)

		lv.gridnav_add(main_page, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(QuickSettingsPage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(DisplayPage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(SoundPage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(WifiPage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(BluetoothPage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(BatteryPage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(ThemePage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(HomescreenPage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(StoragePage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(VersionPage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(AboutPage, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(PowerPage, lv.GRIDNAV_CTRL.NONE)

	def addPressEvent(self, event):
		print(event)

	def changeThemeHandler(self, e):
		code = e.get_code()
		obj = e.get_target()
		if code == lv.EVENT.VALUE_CHANGED:
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

	def addQuickSettingsPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		label = lv.label(btn)
		label.set_text("Hello, I am hiding here")

		return subPage

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

		slider = lv.slider(subPage)
		slider.center()
		slider.set_width(160)

		label = lv.label(subPage)
		label.set_text("Minutes to wait to turn off display")
		label.set_width(80)

		roller1 = lv.roller(subPage)
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

		roller1 = lv.roller(subPage)
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

		slider = lv.slider(subPage)
		slider.center()
		slider.set_width(160)

		return subPage

	def addWifiPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		label = lv.label(btn)
		label.set_text("Hello, I am hiding here")

		return subPage

	def addBluetoothPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		label = lv.label(btn)
		label.set_text("Hello, I am hiding here")

		return subPage

	def addBatteryPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		label = lv.label(btn)
		label.set_text("Hello, I am hiding here")

		return subPage

	def addThemePage(self):
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

		roller1 = lv.roller(subPage)
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

		roller1 = lv.roller(subPage)
		roller1.set_options("\n".join(colors), lv.roller.MODE.INFINITE)
		roller1.set_visible_row_count(3)
		roller1.set_width(120)
		roller1.add_event_cb(self.changeThemeHandler, lv.EVENT.ALL, None)

		return subPage

	def addHomescreenPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		label = lv.label(btn)
		label.set_text("Hello, I am hiding here")

		return subPage

	def addStoragePage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		label = lv.label(btn)
		label.set_text("Hello, I am hiding here")

		return subPage

	def addVersionPage(self):
		# Create sub pages
		subPage = lv.obj(self.menu)
		subPage.set_width(240)
		subPage.set_style_pad_column(8, 0)
		subPage.set_style_pad_row(8, 0)
		subPage.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		label = lv.label(btn)
		label.set_text("Hello, I am hiding here")

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
		label.set_text(
"""PiGO V1.0\n\n
Made and developed by David Krawiec \n\n
Thank you for using PiGO. :)
""")
		label.set_long_mode(lv.label.LONG.WRAP)
		label.set_width(200)

		return subPage

	def addPowerPage(self):
		# Create sub pages
		subPage = lv.menu_page(self.menu, lv.SYMBOL.POWER + " Power")
		# content
		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		btn.set_width(128)
		label = lv.label(btn)
		label.set_text("Reboot")

		btn = lv.btn(subPage)
		btn.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		btn.set_width(128)
		label = lv.label(btn)
		label.set_text("Shutdown")

		return subPage