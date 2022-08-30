import lvgl as lv

from gui.pages.GenericPage import GenericPage
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS

from gui.styles.PageStyle import SETUP_PAGE_STYLE


class SetupPage(GenericPage):
	errLabel = ""


	def __init__(self):
		super().__init__()

		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.ON)
		self.add_flag(self.FLAG.SCROLLABLE)
		self.add_style(SETUP_PAGE_STYLE, 0)
		
		consolename = lv.textarea(self)
		consolename.set_one_line(True)
		consolename.set_max_length(16)
		consolename.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
                  	  	  lv.GRID_ALIGN.STRETCH, 1, 1)
		consolename.add_state(lv.STATE.FOCUSED)

		label = lv.label(self)
		label.set_text("Your nickname:")
		label.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
                  	  	  lv.GRID_ALIGN.STRETCH, 0, 1)

		self.errLabel = lv.label(self)
		self.errLabel.set_text("#ff0000 Should at least have 3 characters #")
		self.errLabel.set_recolor(True)
		self.errLabel.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
                  	  	  			lv.GRID_ALIGN.STRETCH, 2, 1)

		kb = KEYBOARD_LETTERS_ONLY()

		self.group = lv.group_create()
		self.group.add_obj(kb)
		indev1.set_group(self.group)

		kb.set_textarea(consolename)
