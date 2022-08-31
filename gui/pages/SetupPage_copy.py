import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS
from gui.styles.CustomTheme import CustomTheme

from gui.styles.PageStyle import SETUP_PAGE_STYLE


class SetupPage(GenericPage):
	errLabel = ""
	nametextarea = ""
	keyboard = False
	th_new = ""
	primary_color = ""
	secondary_color = ""
	
	active_color_num = 0

	radioPrimaryColors = {
		"White": lv.PALETTE.NONE,
		"Black": lv.PALETTE.NONE,
	}
	radioPrimaryObjs = []

	radioSecondaryColors = {}
	radioSecondaryObjs = []

	def __init__(self):
		super().__init__()

		self.radioSecondaryColors = lv.PALETTE.__dict__

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
		self.nametextarea.add_event_cb(self.nameinputdone, lv.EVENT.READY, None)

		self.errLabel = lv.label(self)
		self.errLabel.set_text("#ff0000 Should at least have 3 characters #")
		self.errLabel.set_recolor(True)
		self.errLabel.add_flag(self.errLabel.FLAG.HIDDEN)

		primcolorlabel = lv.label(self)
		primcolorlabel.set_text("Primary color: ")
		primcolorlabel.set_width(110)
		
		self.add_event_cb(self.radioevent, lv.EVENT.CLICKED, None)

		for color in self.radioPrimaryColors:
			check = lv.checkbox(self)
			check.set_text(color)
			check.add_state(check.FLAG.EVENT_BUBBLE)

			check.set_style_radius(lv.RADIUS_CIRCLE, lv.PART.INDICATOR)
			check.set_style_bg_color(lv.palette_main(self.radioPrimaryColors[color]), lv.PART.INDICATOR)

			check.set_style_radius(lv.RADIUS_CIRCLE, lv.STATE.CHECKED)
			check.set_style_bg_color(lv.palette_main(self.radioPrimaryColors[color]), lv.STATE.CHECKED | lv.PART.INDICATOR)
			
			self.radioPrimaryObjs.append(check)
		self.radioPrimaryObjs[0].add_state(lv.STATE.CHECKED)

		seccolorlabel = lv.label(self)
		seccolorlabel.set_text("Secondary color: ")
		seccolorlabel.set_width(290)

		for color in self.radioSecondaryColors:
			check = lv.checkbox(self)
			check.set_text(color)
			check.add_state(check.FLAG.EVENT_BUBBLE)

			check.set_style_radius(lv.RADIUS_CIRCLE, lv.PART.INDICATOR)
			check.set_style_bg_color(lv.palette_main(self.radioSecondaryColors[color]), lv.PART.INDICATOR)

			check.set_style_radius(lv.RADIUS_CIRCLE, lv.STATE.CHECKED)
			check.set_style_bg_color(lv.palette_main(self.radioSecondaryColors[color]), lv.STATE.CHECKED | lv.PART.INDICATOR)

			self.radioSecondaryObjs.append(check)

		self.radioSecondaryObjs[0].add_state(lv.STATE.CHECKED)

		self.nextbutton = Button(self, "Proceed")
		self.nextbutton.set_size(264, 40)
		self.nextbutton.label.center()
		self.nextbutton.set_style_pad_row(32, 0)
		
		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)

	def new_theme_apply_cb(self, th, obj):
		print(obj, obj.get_class())
		if obj.get_class() == lv.btn_class:
		    obj.add_style(self.th_new.style_btn, 0)
		elif obj.get_class() == lv.obj_class:
			obj.add_style(self.th_new.style_obj, 0)
		elif obj.get_class() == lv.dropdown_class:
			obj.add_style(self.th_new.style_dd, 0)

	def radioevent(self, e):
		#for i in range(e.get_target().get_parent().get_child_cnt()):

		#self.radioButtons.get_child(self.active_color_num).clear_state(lv.STATE.CHECKED)
		e.get_target().add_state(lv.STATE.CHECKED)
		self.active_color_num = e.get_target().get_index()
		
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
