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
	nextbutton = ""
	keyboard = False

	def __init__(self):
		super().__init__()

		self.radioSecondaryColors = lv.PALETTE.__dict__

		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.ON)
		self.add_flag(self.FLAG.SCROLLABLE)
		self.add_style(SETUP_PAGE_STYLE, 0)
		
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)

		avatarlabel = lv.label(self)
		avatarlabel.set_text("Your avatar: ")
		avatarlabel.set_width(290)

		imgbtn_mid_data = loadImage('./imgs/covers/cover1.png')

		imgbtn_mid_dsc = lv.img_dsc_t({
		  'data_size': len(imgbtn_mid_data),
		  'data': imgbtn_mid_data
		})

		imgAvatar = lv.imgbtn(self)
		imgAvatar.set_src(lv.imgbtn.STATE.RELEASED, imgbtn_mid_dsc, imgbtn_mid_dsc, imgbtn_mid_dsc)
		imgAvatar.set_style_radius(lv.RADIUS_CIRCLE, 0)
		imgAvatar.set_size(96, 96)
		imgAvatar.set_style_clip_corner(lv.RADIUS_CIRCLE, 0)

		imgAvatar.set_style_border_color(lv.palette_main(lv.PALETTE.GREEN), 0)
		imgAvatar.set_style_border_width(15, 0)
		imgAvatar.set_style_border_opa(lv.OPA._50, 0)
		imgAvatar.set_style_border_side(lv.BORDER_SIDE.BOTTOM | lv.BORDER_SIDE.RIGHT, 0)

		label = lv.label(imgAvatar)
		label.set_text("test")


		nicknamelabel = lv.label(self)
		nicknamelabel.set_text("Your nickname: ")
		nicknamelabel.set_width(290)
		
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

		self.nextbutton = Button(self, "Proceed")
		self.nextbutton.set_size(264, 40)
		self.nextbutton.label.center()
		self.nextbutton.set_style_pad_row(32, 0)
		
		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)

		
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
