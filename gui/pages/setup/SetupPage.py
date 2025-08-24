import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.Generic.Button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS
from gui.styles.CustomTheme import CustomTheme

from gui.styles.PageStyle import SETUP_PAGE_STYLE

from libs.ffishell import runShellCommand


class SetupPage(GenericPage):
	errLabel = ""
	nametextarea = ""
	nextbutton = ""
	keyboard = False

	noneAvatar = ""
	avatarPath = "./imgs/avatars/"
	avatars = [
		'bear.png', 'buffalo.png', 'chick.png', 'chicken.png', 'cow.png', 
		'crocodile.png', 'dog.png', 'duck.png', 'elephant.png', 'frog.png', 
		'giraffe.png', 'goat.png', 'gorilla.png', 'hippo.png', 'horse.png', 
		'monkey.png', 'moose.png', 'narwhal.png', 'owl.png', 'panda.png', 
		'parrot.png', 'penguin.png', 'pig.png', 'rabbit.png', 'rhino.png', 
		'sloth.png', 'snake.png', 'walrus.png', 'whale.png', 'zebra.png',
	]

	def __init__(self, singletons):
		#self.setSingletons(singletons)
		super().__init__(singletons)

		container = lv.obj(self)
		container.set_size(320, 240)
		self.container = container
		container.add_style(SETUP_PAGE_STYLE, 0)
		
		container.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		container.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		container.set_style_pad_column(12, 0)
		container.set_style_pad_row(12, 0)

		lv.gridnav_add(container, lv.GRIDNAV_CTRL.NONE)

		noneAvatar = loadImage('./imgs/avatars/none.png')
		
		imageNoneAvatar = lv.image_dsc_t({
			'data_size': len(noneAvatar),
			'data': noneAvatar
		})

		imgAvatar = lv.image(container)
		imgAvatar.set_size(108, 108)
		imgAvatar.set_src(imageNoneAvatar)
		self.imgAvatar = imgAvatar

		nametextarea = lv.textarea(container)
		nametextarea.set_one_line(True)
		nametextarea.set_max_length(16)
		nametextarea.set_height(40)
		nametextarea.set_width(260)
		nametextarea.set_placeholder_text("Your nickname")
		nametextarea.add_event_cb(self.nameInput, lv.EVENT.READY, None)
		nametextarea.add_event_cb(self.cancelInput, lv.EVENT.CANCEL, None)
		self.nametextarea = nametextarea

		errLabel = lv.label(container)
		errLabel.set_text("#ff0000 Should at least have 3 characters #")
		#errLabel.set_recolor(True)
		errLabel.add_flag(errLabel.FLAG.HIDDEN)
		self.errLabel = errLabel

		nextbutton = Button(container, lv.SYMBOL.RIGHT)
		nextbutton.set_size(260, 30)
		nextbutton.label.center()
		nextbutton.add_state(lv.STATE.DISABLED)
		nextbutton.add_event_cb(self.page_done, lv.EVENT.PRESSED, None)
		self.nextbutton = nextbutton
		
		self.group = lv.group_create()
		self.group.add_obj(container)
		indev1.set_group(self.group)
		
		lv.gridnav_set_focused(self, self.nametextarea, False)

	def page_done(self, e):
		code = e.get_code()
		if(self.validateInput()):
			config = self.singletons["DATA_MANAGER"].get("configuration")
			config["user"]["profile"]["username"] = self.nametextarea.get_text()
			runShellCommand('hostnamectl set-hostname "pigo-' +config["user"]["profile"]["username"] + '" 2> /dev/null')
			self.singletons["DATA_MANAGER"].saveAll()
			self.singletons["PAGE_MANAGER"].setCurrentPage("setupwifipage", True, self)
	
	def validateInput(self):
		if(len(self.nametextarea.get_text()) < 3):
			self.errLabel.remove_flag(self.errLabel.FLAG.HIDDEN)
			self.nextbutton.add_state(lv.STATE.DISABLED)
			return False
		else:
			self.errLabel.add_flag(self.errLabel.FLAG.HIDDEN)
			self.nextbutton.remove_state(lv.STATE.DISABLED)
			return True

	def cancelInput(self, e):
		self.hideKeyboard()

	def nameInput(self, e):
		obj = self.nametextarea

		if self.keyboard == False:
			self.keyboard = KEYBOARD_LETTERS_ONLY()
			self.keyboard.set_textarea(obj)

			group = lv.group_create()
			group.add_obj(self.keyboard)
			indev1.set_group(group)

			self.container.set_height(120)
			self.container.scroll_to(0, obj.get_y() + obj.get_height(), True)
		elif self.keyboard != False:
			if(self.validateInput()):
				self.hideKeyboard()
				self.randomizeAvatar(obj.get_text())

	def hideKeyboard(self):
		self.keyboard.delete()
		self.keyboard = False
		indev1.set_group(self.group)
		self.container.set_height(320)
		self.container.scroll_to(0, 0, True)

	def randomizeAvatar(self, name):
		sum = 0
		for char in name:
			sum += ord(char)
		val = sum % 30
		imgSrc = self.avatarPath + self.avatars[val]
		imgdata = loadImage(imgSrc)

		imageAvatar = lv.image_dsc_t({
		  'data_size': len(imgdata),
		  'data': imgdata
		})

		self.imgAvatar.set_src(imageAvatar)
