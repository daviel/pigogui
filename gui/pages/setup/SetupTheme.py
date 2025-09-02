import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.Generic.Button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS, COUNTRY_LIST
from gui.styles.CustomTheme import CustomTheme

from gui.styles.PageStyle import SETUP_PAGE_STYLE

from libs.ffishell import runShellCommand

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller


class SetupTheme(GenericPage):
	errLabel = ""
	nextbutton = ""
	group = ""

	colors = []
	primaryColor = ""
	darkTheme = False

	primaryColorRoller = ""
	darkThemeRoller = ""

	def __init__(self, container):
		super().__init__(container)

		self.set_size(320, 240)
		self.add_style(SETUP_PAGE_STYLE, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.set_style_pad_column(12, 0)
		self.set_style_pad_row(12, 0)

		# content
		# content
		label = lv.label(self)
		label.set_text("\nTheme mode")
		label.set_size(100, 80)
		label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

		self.darkThemeRoller = ActiveRoller(self)
		self.darkThemeRoller.set_options("\n".join([
			"Light",
			"Dark",
			]),lv.roller.MODE.NORMAL)
		self.darkThemeRoller.set_visible_row_count(2)
		self.darkThemeRoller.set_width(120)
		self.darkThemeRoller.add_event_cb(self.changeThemeHandler, lv.EVENT.ALL, None)

		label = lv.label(self)
		label.set_text("\nTheme color")
		label.set_size(100, 80)
		label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

		for color in lv.PALETTE.__dict__:
			self.colors.append(color)

		self.primaryColorRoller = ActiveRoller(self)
		self.primaryColorRoller.set_options("\n".join(self.colors), lv.roller.MODE.INFINITE)
		self.primaryColorRoller.set_visible_row_count(2)
		self.primaryColorRoller.set_width(120)
		self.primaryColorRoller.add_event_cb(self.changeThemeHandler, lv.EVENT.ALL, None)

		self.prevButton = Button(self, lv.SYMBOL.LEFT)
		self.prevButton.set_size(100, 30)
		self.prevButton.label.center()
		self.prevButton.add_event_cb(self.pageBack, lv.EVENT.PRESSED, None)

		self.nextbutton = Button(self, lv.SYMBOL.RIGHT)
		self.nextbutton.set_size(100, 30)
		self.nextbutton.label.center()
		self.nextbutton.add_event_cb(self.pageNext, lv.EVENT.PRESSED, None)

		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_set_focused(self, self.nextbutton, False)

	def pageBack(self, e):
		self.singletons["PAGE_MANAGER"].setCurrentPage("setuppage", False)

	def pageOpened(self):
		config = self.singletons["DATA_MANAGER"].get("configuration")
		self.primaryColor = config["user"]["theme"]["primaryColor"]
		self.darkTheme = config["user"]["theme"]["darkTheme"]

		self.primaryColorRoller.set_selected(self.colors.index(self.primaryColor), True)
		if self.darkTheme == True:
			self.darkThemeRoller.set_selected(1, True)
		else:
			self.darkThemeRoller.set_selected(0, True)
		pass

	def changeThemeHandler(self, e):
		code = e.get_code()
		obj = e.get_target_obj()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.UP or key == lv.KEY.DOWN:
				option = " " * 20
				obj.get_selected_str(option, len(option))
				selection = option.strip()[:-1]

				colors = lv.PALETTE.__dict__
				primary_color = colors[self.primaryColor]
				config = self.singletons["DATA_MANAGER"].get("configuration")

				if selection == "Light":
					self.darkTheme = False
				elif selection == "Dark":
					self.darkTheme = True
				else:
					primary_color = colors[selection]
					self.primaryColor = selection
					config["user"]["theme"]["primaryColor"] = selection

				lv.theme_default_init(lv.display_get_default(), 
						lv.palette_main(primary_color), 
						lv.palette_main(lv.PALETTE.GREY), 
						self.darkTheme, 
						lv.font_montserrat_16)
				
				config["user"]["theme"]["darkTheme"] = self.darkTheme

	def pageNext(self, e):
		self.singletons["PAGE_MANAGER"].setCurrentPage("setupwifipage", True)
	
	