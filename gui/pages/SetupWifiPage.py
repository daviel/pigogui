import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.Generic.Button import Button
from gui.styles.PageStyle import SETUP_PAGE_STYLE
from gui.components.Generic.Loader import Loader

from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS
from libs.WifiShellParser import WifiShellParser
import libs.Singletons as SINGLETONS


class SetupWifiPage(GenericPage):
	nextbutton = ""
	wifiShellParser = WifiShellParser()
	wifiContainer = ""
	loadAnim = ""
	nametextarea = ""
	keyboard = False
	currentWiFiData = ""

	def __init__(self):
		super().__init__()

		self.add_style(SETUP_PAGE_STYLE, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.set_style_pad_column(0, 0)
		self.set_style_pad_row(4, 0)
		
		label = lv.label(self)
		label.set_text("WiFi-Setup")
		label.set_width(300)

		self.loaderContainer = lv.obj(self)
		self.loaderContainer.set_size(310, 170)
		self.loaderContainer.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.loaderContainer.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.loaderContainer.set_style_pad_column(0, 0)
		self.loaderContainer.set_style_pad_row(8, 0)
		self.loader = Loader(self.loaderContainer)

		self.wifiContainer = lv.obj(self)
		self.wifiContainer.set_size(310, 170)
		self.wifiContainer.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.wifiContainer.set_flex_align(lv.FLEX_FLOW.ROW_WRAP, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		self.wifiContainer.set_style_pad_column(0, 0)
		self.wifiContainer.set_style_pad_row(8, 0)
		self.wifiContainer.add_flag(self.FLAG.HIDDEN)

		# get the networks and render them
		self.renderWifiNetworks(self.wifiShellParser.getNetworks())

		self.backbutton = Button(self, lv.SYMBOL.LEFT)
		self.backbutton.set_size(50, 30)
		self.backbutton.label.center()
		self.backbutton.add_event_cb(self.pageBack, lv.EVENT.PRESSED, None)

		self.refreshbutton = Button(self, lv.SYMBOL.REFRESH)
		self.refreshbutton.set_size(50, 30)
		self.refreshbutton.label.center()
		self.refreshbutton.add_event_cb(self.refreshWifiNetworks, lv.EVENT.PRESSED, None)

		self.nextbutton = Button(self, lv.SYMBOL.RIGHT)
		self.nextbutton.set_size(50, 30)
		self.nextbutton.label.center()
		self.nextbutton.add_event_cb(self.pageNext, lv.EVENT.PRESSED, None)
		
		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)

	def renderWifiNetworks(self, networks):
		lv.gridnav_remove(self.wifiContainer)
		self.wifiContainer.clean()

		for wifiEntry in networks:
			if wifiEntry["in-use"] == True:
				wifiConnectButton = Button(self.wifiContainer, wifiEntry["ssid"] + " (Connected)")
			else:
				wifiConnectButton = Button(self.wifiContainer, wifiEntry["ssid"] + " (" + wifiEntry["security"] + ")")
			wifiConnectButton.label.align(lv.ALIGN.LEFT_MID, 8, 0)
			wifiConnectButton.set_width(280)
			wifiConnectButton.set_height(20)
			wifiConnectButton.data = wifiEntry
			#wifiConnectButton.pressCallback = self.connectWifi
			wifiConnectButton.pressCallback = self.showDialog

		self.loaderContainer.add_flag(self.FLAG.HIDDEN)
		self.wifiContainer.remove_flag(self.FLAG.HIDDEN)
		self.group.add_obj(self.wifiContainer)

		lv.gridnav_add(self.wifiContainer, lv.GRIDNAV_CTRL.NONE)

	def showDialog(self, object, event):
		wifiData = object.data
		self.currentWiFiData = wifiData
		passwordDialog = lv.msgbox(self.get_parent())
		passwordDialog.align(lv.ALIGN.TOP_MID, 8, 8)
		passwordDialog.add_text("SSID: " + wifiData["ssid"])
		passwordDialogContent = passwordDialog.get_content()
		self.passwordDialog = passwordDialog
		
		errLabel = lv.label(passwordDialogContent)
		#errLabel.set_recolor(True)
		errLabel.add_flag(errLabel.FLAG.HIDDEN)
		errLabel.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
		self.errLabel = errLabel

		#close_button = passwordDialog.add_footer_button("Abort")
		#close_button.set_height(20)
		#accept_button = passwordDialog.add_footer_button("Connect")
		#accept_button.set_height(20)

		nametextarea = lv.textarea(passwordDialogContent)
		nametextarea.set_one_line(True)
		nametextarea.set_max_length(16)
		nametextarea.set_password_mode(True)
		nametextarea.set_height(40)
		nametextarea.set_width(240)
		nametextarea.set_placeholder_text("WiFi Password")
		nametextarea.add_event_cb(self.connectWifi, lv.EVENT.READY, None)
		self.nametextarea = nametextarea

		lv.gridnav_set_focused(self, self.nametextarea, lv.ANIM.OFF)
		self.connectWifi(event)

	def connectWifi(self, event):
		if self.keyboard == False:
			self.keyboard = KEYBOARD_ALL_SYMBOLS()
			self.keyboard.set_textarea(self.nametextarea)

			group = lv.group_create()
			group.add_obj(self.keyboard)
			indev1.set_group(group)
		elif self.keyboard != False:
			if(self.connectAttempt(event.get_target_obj().get_text())):
				indev1.set_group(self.group)
				self.wifiContainer.scroll_to(0, 0, lv.ANIM.ON)
				
				self.keyboard.delete()
				self.passwordDialog.close()
				self.keyboard = False

	def pageBack(self, e):
		SINGLETONS.PAGE_MANAGER.setCurrentPage("setuppage", False)

	def pageNext(self, e):
		SINGLETONS.PAGE_MANAGER.setCurrentPage("gamesoverviewpage", True)
	
	def refreshWifiNetworks(self, e):
		self.renderWifiNetworks(self.wifiShellParser.getNetworks())

	def connectAttempt(self, password):
		if(len(self.nametextarea.get_text()) < 8):
			self.errLabel.remove_flag(self.errLabel.FLAG.HIDDEN)
			self.errLabel.set_text("#ff0000 Should at least have 8 characters #")
			return False

		self.errLabel.remove_flag(self.errLabel.FLAG.HIDDEN)
		self.errLabel.set_text("Connection... Please wait.")
		
		status = self.wifiShellParser.connect(self.currentWiFiData["ssid"], password)
		if status != True:
			self.errLabel.set_text("Error: Connection failed")
			self.errLabel.remove_flag(self.errLabel.FLAG.HIDDEN)
			return False
		else:
			self.errLabel.add_flag(self.errLabel.FLAG.HIDDEN)
			self.pageNext(None)
			return True