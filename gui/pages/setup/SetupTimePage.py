import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.Generic.Button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS, COUNTRY_LIST, add_or_replace_in_file, TIMEZONE_LIST
from gui.styles.CustomTheme import CustomTheme

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller

from gui.styles.PageStyle import SETUP_PAGE_STYLE

from libs.ffishell import runShellCommand


class SetupTimePage(GenericPage):
	errLabel = ""
	nametextarea = ""
	nextbutton = ""
	keyboard = False
	group = ""
	language_list = COUNTRY_LIST
	language_list_parsed = []

	def __init__(self, container):
		super().__init__(container)

		self.add_style(SETUP_PAGE_STYLE, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.set_style_pad_column(4, 0)
		self.set_style_pad_row(4, 0)

		# content
		label = lv.label(self)
		label.set_text("Timezone")
		label.set_width(100)

		self.timezoneRoller = ActiveRoller(self)
		self.timezoneRoller.set_options("\n".join(TIMEZONE_LIST), lv.roller.MODE.INFINITE)
		self.timezoneRoller.set_visible_row_count(2)
		self.timezoneRoller.set_width(180)
		self.timezoneRoller.add_event_cb(self.changeTimezone, lv.EVENT.ALL, None)

		self.nextbutton = Button(self, lv.SYMBOL.RIGHT)
		self.nextbutton.set_size(50, 30)
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

	def pageNext(self, e):
		self.singletons["PAGE_MANAGER"].setCurrentPage("setuppage", True)
	
	