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

	noneAvatar = ""
	avatars = [
		'./imgs/avatars/bear.png',
		'./imgs/avatars/buffalo.png',
		'./imgs/avatars/chick.png',
		'./imgs/avatars/chicken.png',
		'./imgs/avatars/cow.png',
		'./imgs/avatars/crocodile.png',
		'./imgs/avatars/dog.png',
		'./imgs/avatars/duck.png',
		'./imgs/avatars/elephant.png',
		'./imgs/avatars/frog.png',
		'./imgs/avatars/giraffe.png',
		'./imgs/avatars/goat.png',
		'./imgs/avatars/gorilla.png',
		'./imgs/avatars/hippo.png',
		'./imgs/avatars/horse.png',
		'./imgs/avatars/monkey.png',
		'./imgs/avatars/moose.png',
		'./imgs/avatars/narwhal.png',
		'./imgs/avatars/owl.png',
		'./imgs/avatars/panda.png',
		'./imgs/avatars/parrot.png',
		'./imgs/avatars/penguin.png',
		'./imgs/avatars/pig.png',
		'./imgs/avatars/rabbit.png',
		'./imgs/avatars/rhino.png',
		'./imgs/avatars/sloth.png',
		'./imgs/avatars/snake.png',
		'./imgs/avatars/walrus.png',
		'./imgs/avatars/whale.png',
		'./imgs/avatars/zebra.png',
	]

	def __init__(self):
		super().__init__()
		self.returnable = True

		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.ON)
		self.add_flag(self.FLAG.SCROLLABLE)
		self.add_style(SETUP_PAGE_STYLE, 0)
		
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.set_style_pad_column(12, 0)
		self.set_style_pad_row(12, 0)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)

		noneAvatar = loadImage('./imgs/avatars/none.png')
		
		imageNoneAvatar = lv.img_dsc_t({
			'data_size': len(noneAvatar),
			'data': noneAvatar
		})

		imgAvatar = lv.img(self)
		imgAvatar.set_size(108, 108)
		imgAvatar.set_src(imageNoneAvatar)
		#imgAvatar.set_style_radius(lv.RADIUS_CIRCLE, 0)
		#imgAvatar.set_style_clip_corner(lv.RADIUS_CIRCLE, 0)
		self.imgAvatar = imgAvatar

		nametextarea = lv.textarea(self)
		nametextarea.set_one_line(True)
		nametextarea.set_max_length(16)
		nametextarea.set_height(40)
		nametextarea.set_width(260)
		nametextarea.set_placeholder_text("Your nickname")
		nametextarea.add_event_cb(self.nameinputdone, lv.EVENT.READY, None)
		self.nametextarea = nametextarea

		errLabel = lv.label(self)
		errLabel.set_text("#ff0000 Should at least have 3 characters #")
		errLabel.set_recolor(True)
		errLabel.add_flag(errLabel.FLAG.HIDDEN)
		self.errLabel = errLabel

		nextbutton = Button(self, lv.SYMBOL.RIGHT)
		nextbutton.set_size(50, 30)
		nextbutton.label.center()
		nextbutton.add_state(lv.STATE.DISABLED)
		nextbutton.add_event_cb(self.page_done, lv.EVENT.PRESSED, None)
		self.nextbutton = nextbutton
		
		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)
		
		lv.gridnav_set_focused(self, self.nametextarea, lv.ANIM.OFF)

	def page_done(self, e):
		code = e.get_code()
		if(self.validateInput()):
			self.pageNextCb(self)
				
	def validateInput(self):
		if(len(self.nametextarea.get_text()) < 3):
			self.errLabel.clear_flag(self.errLabel.FLAG.HIDDEN)
			self.nextbutton.add_state(lv.STATE.DISABLED)
			return False
		else:
			self.errLabel.add_flag(self.errLabel.FLAG.HIDDEN)
			self.nextbutton.clear_state(lv.STATE.DISABLED)
			return True

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
			if(self.validateInput()):
				self.keyboard.delete()
				self.keyboard = False
				indev1.set_group(self.group)
				self.set_height(320)
				self.scroll_to(0, 0, lv.ANIM.ON)

				self.randomizeAvatar(obj.get_text())

	def randomizeAvatar(self, name):
		sum = 0
		for char in name:
			sum += ord(char)
		val = sum % 30
		imgSrc = self.avatars[val]
		imgdata = loadImage(imgSrc)

		imageAvatar = lv.img_dsc_t({
		  'data_size': len(imgdata),
		  'data': imgdata
		})

		self.imgAvatar.set_src(imageAvatar)
