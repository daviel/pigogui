import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS
from gui.styles.CustomTheme import CustomTheme

from gui.styles.PageStyle import SETUP_PAGE_STYLE


class SetupWifi(GenericPage):
	errLabel = ""
	nametextarea = ""
	nextbutton = ""
	keyboard = False

	def __init__(self):
		super().__init__()

		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.ON)
		self.add_flag(self.FLAG.SCROLLABLE)
		self.add_style(SETUP_PAGE_STYLE, 0)
		
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.set_style_pad_column(12, 0)
		self.set_style_pad_row(12, 0)
		
		self.nametextarea = lv.textarea(self)
		self.nametextarea.set_one_line(True)
		self.nametextarea.set_max_length(16)
		self.nametextarea.set_height(40)
		self.nametextarea.set_width(260)
		self.nametextarea.set_placeholder_text("Your nickname")
		#self.nametextarea.add_state(lv.STATE.FOCUSED)
		#self.nametextarea.add_state(lv.STATE.PRESSED)
		self.nametextarea.add_event_cb(self.nameinputdone, lv.EVENT.READY, None)

		self.errLabel = lv.label(self)
		self.errLabel.set_text("#ff0000 Should at least have 3 characters #")
		self.errLabel.set_recolor(True)
		self.errLabel.add_flag(self.errLabel.FLAG.HIDDEN)

		self.nextbutton = Button(self, "Proceed")
		self.nextbutton.set_size(260, 40)
		self.nextbutton.label.center()
		
		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)
		#lv.gridnav_set_focused(self, self.nametextarea, lv.ANIM.OFF)

		
	def nameinputdone(self, e):
		obj = e.get_target()

		if self.keyboard == False:
			self.keyboard = KEYBOARD_LETTERS_ONLY()
			self.keyboard.set_textarea(obj)

			group = lv.group_create()
			group.add_obj(self.keyboard)
			indev1.set_group(group)

			self.set_height(120)
			self.scroll_to(0, obj.get_y(), lv.ANIM.ON)
		elif self.keyboard != False:
			if(len(obj.get_text()) < 3):
				print("name too short")
				self.errLabel.clear_flag(self.errLabel.FLAG.HIDDEN)
			else:
				self.errLabel.add_flag(self.errLabel.FLAG.HIDDEN)
				self.keyboard.delete()
				self.keyboard = False
				indev1.set_group(self.group)
				self.set_height(320)
				self.scroll_to(0, 0, lv.ANIM.ON)

