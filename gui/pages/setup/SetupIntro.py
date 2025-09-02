import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.Generic.Button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS, COUNTRY_LIST
from gui.styles.CustomTheme import CustomTheme

from gui.styles.PageStyle import SETUP_PAGE_STYLE

from libs.ffishell import runShellCommand


class SetupIntro(GenericPage):
	errLabel = ""
	nextbutton = ""
	group = ""

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
		label.set_text("""\n\n
			Welcome to PiGo!

			We will get you started now - This will be done in no time.
		""")
		label.set_size(240, 180)
		label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

		self.nextbutton = Button(self, lv.SYMBOL.RIGHT)
		self.nextbutton.set_size(260, 30)
		self.nextbutton.label.center()
		self.nextbutton.add_event_cb(self.pageNext, lv.EVENT.PRESSED, None)

		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_set_focused(self, self.nextbutton, False)

	def pageNext(self, e):
		self.singletons["PAGE_MANAGER"].setCurrentPage("setuplanguagepage", True)
	
	