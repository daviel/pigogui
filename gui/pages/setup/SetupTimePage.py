import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.Generic.Button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS, COUNTRY_LIST, TIMEZONE_LIST
from gui.styles.CustomTheme import CustomTheme

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller

from gui.styles.PageStyle import SETUP_PAGE_STYLE

from libs.ffishell import runShellCommand


class SetupTimePage(GenericPage):
	errLabel = ""
	nametextarea = ""
	nextbutton = ""
	prevButton = ""
	keyboard = False
	group = ""
	tz_list = TIMEZONE_LIST

	def __init__(self, container):
		super().__init__(container)

		self.set_size(320, 240)
		self.add_style(SETUP_PAGE_STYLE, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.set_style_pad_column(12, 0)
		self.set_style_pad_row(12, 0)

		# content
		label = lv.label(self)
		label.set_text("\nTimezone")
		label.set_size(100, 80)
		label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

		self.timezoneRoller = ActiveRoller(self)
		self.timezoneRoller.set_options("\n".join(self.tz_list), lv.roller.MODE.INFINITE)
		self.timezoneRoller.set_visible_row_count(2)
		self.timezoneRoller.set_width(170)
		self.timezoneRoller.add_event_cb(self.changeTimezone, lv.EVENT.ALL, None)

		self.prevButton = Button(self, lv.SYMBOL.LEFT)
		self.prevButton.set_size(120, 30)
		self.prevButton.label.center()
		self.prevButton.add_event_cb(self.pageBack, lv.EVENT.PRESSED, None)

		self.nextbutton = Button(self, lv.SYMBOL.RIGHT)
		self.nextbutton.set_size(120, 30)
		self.nextbutton.label.center()
		self.nextbutton.add_event_cb(self.pageNext, lv.EVENT.PRESSED, None)

		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_set_focused(self, self.timezoneRoller, False)


	def changeTimezone(self, e):
		code = e.get_code()
		obj = e.get_target_obj()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.UP or key == lv.KEY.DOWN:
				option = " " * 20
				obj.get_selected_str(option, len(option))
				selection = option.strip()[:-1]

				config = self.singletons["DATA_MANAGER"].get("configuration")
				if config["debug"] == False:
					ret = runShellCommand('timedatectl set-timezone ' + selection)
				print('timedatectl set-timezone ' + selection)

				config = self.singletons["DATA_MANAGER"].get("configuration")
				config["user"]["system"]["timezone"] = selection
				self.singletons["DATA_MANAGER"].saveAll()

	def pageBack(self, e):
		self.singletons["PAGE_MANAGER"].setCurrentPage("setuplanguagepage", False)

	def pageNext(self, e):
		self.singletons["PAGE_MANAGER"].setCurrentPage("setuppage", True)
	
	