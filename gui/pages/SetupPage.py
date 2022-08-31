import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS

from gui.styles.PageStyle import SETUP_PAGE_STYLE


class SetupPage(GenericPage):
	errLabel = ""
	nametextarea = ""
	keyboard = False

	def __init__(self):
		super().__init__()

		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.ON)
		self.add_flag(self.FLAG.SCROLLABLE)
		self.add_style(SETUP_PAGE_STYLE, 0)
		
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		
		label = lv.label(self)
		label.set_text("Your nickname: ")
		
		self.nametextarea = lv.textarea(self)
		self.nametextarea.set_one_line(True)
		self.nametextarea.set_max_length(16)
		self.nametextarea.set_height(40)
		self.nametextarea.set_placeholder_text("JANE")
		self.nametextarea.add_state(lv.STATE.FOCUSED)
		
		self.nametextarea.add_state(lv.STATE.PRESSED)
		
		self.nametextarea.add_event_cb(self.nameinput, lv.EVENT.VALUE_CHANGED, None)
		self.nametextarea.add_event_cb(self.nameinputdone, lv.EVENT.READY, None)
		self.nametextarea.add_event_cb(self.nameinputfocused, lv.EVENT.FOCUSED, None)

		self.errLabel = lv.label(self)
		self.errLabel.set_text("#ff0000 Should at least have 3 characters #")
		self.errLabel.set_recolor(True)
		self.errLabel.add_flag(self.errLabel.FLAG.HIDDEN)
		
		primcolorlabel = lv.label(self)
		primcolorlabel.set_text("Primary color: ")
		primcolorlabel.set_width(128)

		seccolorlabel = lv.label(self)
		seccolorlabel.set_text("Secondary color: ")
		seccolorlabel.set_width(128)
		
		primarycolordd = lv.dropdown(self)
		primarycolordd.set_options("\n".join(["White", "Black"]))
		primarycolordd.set_size(128, 40)
		primarycolordd.add_event_cb(self.dropdown, lv.EVENT.ALL, None)
		
		secondarycolordd = lv.dropdown(self)
		secondarycolordd.set_options("\n".join([lv.SYMBOL.FILE + " Blue", "Green", "Red", "Yellow", "Pink", "Purple"]))
		secondarycolordd.set_size(128, 40)
		secondarycolordd.add_event_cb(self.dropdown, lv.EVENT.ALL, None)
		
		self.nextbutton = Button(self, "Proceed")
		self.nextbutton.set_size(264, 40)
		self.nextbutton.label.center()
		self.nextbutton.set_style_pad_row(32, 0)
		
		self.group = lv.group_create()
		#self.group.add_obj(self.nametextarea)
		#self.group.add_obj(primarycolordd)
		#self.group.add_obj(secondarycolordd)
		#self.group.add_obj(nextbutton)
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)

	def dropdown(self, e):
		code = e.get_code()
		obj = e.get_target()
		if code == lv.EVENT.VALUE_CHANGED:
			option = " "*10 # should be large enough to store the option
			obj.get_selected_str(option, len(option))
			# .strip() removes trailing spaces
			print("Option: \"%s\"" % option.strip())

			indev1.set_group(self.group)
			lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)
			self.nextbutton.set_style_bg_color(lv.palette_main(lv.PALETTE.GREEN), 0)
		elif code == lv.EVENT.READY:
			print("dropdown focused")
			lv.gridnav_remove(self)
			group = lv.group_create()
			group.add_obj(obj)
			indev1.set_group(group)
			

	def nameinput(self, e):
		print(e)
		
	def nameinputdone(self, e):
		print(e)
		if self.keyboard == False:
			self.keyboard = KEYBOARD_LETTERS_ONLY()
			self.keyboard.set_textarea(e.get_target())
			e.get_target().scroll_to(0, 0, lv.ANIM.ON)

			group = lv.group_create()
			group.add_obj(self.keyboard)
			indev1.set_group(group)
		elif self.keyboard != False:
			if(len(e.get_target().get_text()) < 3):
				print("name too short")
				self.errLabel.clear_flag(self.errLabel.FLAG.HIDDEN)
			else:
				self.errLabel.add_flag(self.errLabel.FLAG.HIDDEN)
				self.keyboard.delete()
				self.keyboard = False
				indev1.set_group(self.group)

	def nameinputfocused(self, e):
		print(e)
		print("focused")
		