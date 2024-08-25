import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.Generic.Button import Button
from gui.components.Generic.IconButton import IconButton
from gui.styles.PageStyle import SETUP_PAGE_STYLE
from gui.components.Generic.Loader import Loader

from libs.init_drv import indev1
from libs.Helper import loadImageAndConvert, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS
import libs.Singletons as SINGLETONS


class GameDetailsPage(GenericPage):
	animIn = lv.SCR_LOAD_ANIM.FADE_IN
	animOut = lv.SCR_LOAD_ANIM.FADE_OUT

	nextbutton = ""
	wifiContainer = ""
	loadAnim = ""

	def __init__(self):
		super().__init__()

		self.animIn = lv.SCR_LOAD_ANIM.FADE_IN
		self.animOut = lv.SCR_LOAD_ANIM.FADE_OUT

		self.add_style(SETUP_PAGE_STYLE, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.set_style_pad_column(0, 0)
		self.set_style_pad_row(4, 0)

		self.leftContainer = lv.obj(self)
		self.leftContainer.set_size(100, 236)
		self.leftContainer.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.leftContainer.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.leftContainer.set_style_pad_column(0, 0)
		self.leftContainer.set_style_pad_row(6, 0)
		self.leftContainer.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

		imageButton = lv.image(self.leftContainer)
		gameIconImage = loadImageAndConvert("./imgs/cover1.png")
		imageButton.set_size(72, 72)
		imageButton.set_src(gameIconImage)
		imageButton.align(lv.ALIGN.CENTER, 0, 0)
		imageButton.set_style_radius(4, 0)
		imageButton.set_style_clip_corner(4, 0)
		self.imageButton = imageButton

		groupButton = IconButton(self.leftContainer, lv.SYMBOL.DIRECTORY, "Group")
		groupButton.set_size(90, 24)
		updateButton = IconButton(self.leftContainer, lv.SYMBOL.REFRESH, "Update")
		updateButton.set_size(90, 24)
		deleteButton = IconButton(self.leftContainer, lv.SYMBOL.TRASH, "Delete")
		deleteButton.set_size(90, 24)
		backButton = IconButton(self.leftContainer, lv.SYMBOL.LEFT, "Back")
		backButton.set_size(90, 24)
		backButton.add_event_cb(self.pageBack, lv.EVENT.PRESSED, None)

		self.rightContainer = lv.obj(self)
		self.rightContainer.set_size(210, 236)
		self.rightContainer.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.rightContainer.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.rightContainer.set_style_pad_column(4, 0)
		self.rightContainer.set_style_pad_row(4, 0)
		self.rightContainer.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

		gameTitle = lv.label(self.rightContainer)
		gameTitle.set_text("Title 1")
		gameTitle.set_width(200)
		gameTitle.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
		self.gameTitle = gameTitle

		description = lv.label(self.rightContainer)
		description.set_text("Here is a very long description of a game. It is about testing this textbox.")
		description.set_size(200, 16)
		description.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
		self.description = description

		self.imageContainer = lv.obj(self.rightContainer)
		self.imageContainer.set_size(200, 140)
		self.imageContainer.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.imageContainer.set_style_pad_column(4, 0)
		self.imageContainer.set_style_pad_row(0, 0)
		self.imageContainer.set_style_border_width(0, 0)
		self.imageContainer.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)

		sizeLabel = lv.label(self.rightContainer)
		self.sizeLabel = sizeLabel

		genre = lv.label(self.rightContainer)
		self.genre = genre
		
		self.group = lv.group_create()
		self.group.add_obj(self.leftContainer)
		self.group.add_obj(self.imageContainer)
		indev1.set_group(self.group)

		lv.gridnav_add(self.leftContainer, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(self.imageContainer, lv.GRIDNAV_CTRL.NONE)

	def pageBack(self, e):
		SINGLETONS.PAGE_MANAGER.pagePrev()

	def pageOpened(self):
		self.gameTitle.set_text(self.data['title'])
		self.description.set_text(self.data['description'])
		self.genre.set_text(' '.join(self.data['tags']))
		self.sizeLabel.set_text(lv.SYMBOL.SD_CARD + " " + self.data['size'] + "MB")

		for imageSrc in self.data['screenshots']:
			self.createScreenshot(imageSrc)

	def pageClosed(self):
		for i in range(self.imageContainer.get_child_count()):
			self.imageContainer.get_child(i).delete_delayed(1000)

	def createScreenshot(self, src):
		imgSize = 112
		screenshotButton = lv.button(self.imageContainer)
		screenshotButton.set_size(imgSize, imgSize)
		gameImage = loadImageAndConvert(src)
		screenshotImg = lv.image(screenshotButton)
		screenshotImg.set_size(imgSize - 8, imgSize - 8)
		screenshotImg.set_src(gameImage)
		screenshotImg.set_style_radius(4, 0)
		screenshotImg.set_style_clip_corner(4, 0)
		screenshotImg.align(lv.ALIGN.CENTER, 0, 0)
		return screenshotButton
