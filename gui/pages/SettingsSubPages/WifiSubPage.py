import lvgl as lv

from gui.components.Generic.SubPage import SubPage
from gui.components.Generic.Button import Button
from gui.components.Generic.Loader import Loader
from libs.init_drv import indev1
from libs.Helper import KEYBOARD_ALL_SYMBOLS


class WifiSubPage(SubPage):
	def __init__(self, container, singletons):
		super().__init__(container, singletons)
		self.set_width(240)
		self.set_style_pad_column(4, 0)
		self.set_style_pad_row(6, 0)
		self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		self.set_style_pad_hor(4, 0)
		self.set_style_pad_ver(4, 0)

		self._keyboard = False
		self._currentSSID = ""
		self._passwordTextarea = None
		self._passwordDialog = None
		self._errLabel = None
		self._savedGroup = None

		self.statusLabel = lv.label(self)
		self.statusLabel.set_text("Not connected")
		self.statusLabel.set_width(220)
		self.statusLabel.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)

		scanRow = lv.obj(self)
		scanRow.set_size(220, 32)
		scanRow.set_flex_flow(lv.FLEX_FLOW.ROW)
		scanRow.set_style_border_width(0, 0)
		scanRow.set_style_bg_opa(lv.OPA.TRANSP, 0)
		scanRow.set_style_pad_column(8, 0)
		scanRow.remove_flag(lv.obj.FLAG.SCROLLABLE)

		scanBtn = Button(scanRow, lv.SYMBOL.REFRESH + " Scan")
		scanBtn.set_size(100, 28)
		scanBtn.label.center()
		scanBtn.add_event_cb(self._onScan, lv.EVENT.PRESSED, None)

		self._loader = Loader(scanRow)
		self._loader.set_size(24, 24)
		self._loader.add_flag(self._loader.FLAG.HIDDEN)

		self.wifiContainer = lv.obj(self)
		self.wifiContainer.set_size(220, 168)
		self.wifiContainer.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		self.wifiContainer.set_style_pad_row(2, 0)
		self.wifiContainer.set_style_pad_hor(0, 0)
		self.wifiContainer.set_style_border_width(1, 0)

		self._scanTimer = lv.timer_create(self._onScanDone, 5000, None)
		self._scanTimer.pause()

	def loadSubPage(self, event):
		self._updateStatus()
		self._refreshNetworkList()

	def _updateStatus(self):
		wm = self.singletons["WIFI_MANAGER"]
		if wm.connected:
			self.statusLabel.set_text(wm.connectedAP + "  " + wm.IPAddress)
		else:
			self.statusLabel.set_text("Not connected")

	def _refreshNetworkList(self):
		self.wifiContainer.clean()
		networks = self.singletons["WIFI_MANAGER"].getNetworks()
		for network in networks:
			if not isinstance(network, dict):
				continue
			ssid     = network.get("ssid", "")
			bars     = network.get("bars", "")
			security = network.get("security", "")
			in_use   = network.get("in-use", False)
			secured  = "WPA" in security or "WEP" in security

			prefix = lv.SYMBOL.OK + " " if in_use else "  "
			btn = Button(self.wifiContainer, prefix + ssid)
			btn.set_width(210)
			btn.set_height(24)
			btn.set_style_pad_hor(4, 0)
			btn.set_style_pad_ver(2, 0)
			btn.label.align(lv.ALIGN.LEFT_MID, 4, 0)
			btn.label.set_width(145)
			btn.label.set_long_mode(lv.label.LONG_MODE.CLIP)

			infoLabel = lv.label(btn)
			infoLabel.set_text(bars + (" " + lv.SYMBOL.LOCK if secured else ""))
			infoLabel.align(lv.ALIGN.RIGHT_MID, -4, 0)

			def make_cb(s, sec):
				def cb(obj, e):
					if sec:
						self._showPasswordDialog(s)
					else:
						self.singletons["WIFI_MANAGER"].connect(s, "")
				return cb
			btn.pressCallback = make_cb(ssid, secured)

	def _onScan(self, e):
		self._loader.remove_flag(self._loader.FLAG.HIDDEN)
		self.singletons["WIFI_MANAGER"].scan()
		self._scanTimer.reset()
		self._scanTimer.resume()

	def _onScanDone(self, timer):
		timer.pause()
		self._loader.add_flag(self._loader.FLAG.HIDDEN)
		self._updateStatus()
		self._refreshNetworkList()

	def _showPasswordDialog(self, ssid):
		self._currentSSID = ssid
		self._savedGroup = indev1.get_group()

		dialog = lv.msgbox(lv.screen_active())
		dialog.align(lv.ALIGN.CENTER, 0, 0)
		dialog.add_text(ssid)
		self._passwordDialog = dialog

		content = dialog.get_content()

		errLabel = lv.label(content)
		errLabel.set_text("")
		errLabel.set_width(220)
		errLabel.add_flag(errLabel.FLAG.HIDDEN)
		self._errLabel = errLabel

		ta = lv.textarea(content)
		ta.set_one_line(True)
		ta.set_password_mode(True)
		ta.set_placeholder_text("Password")
		ta.set_height(36)
		ta.set_width(220)
		ta.add_event_cb(self._onPasswordReady, lv.EVENT.READY, None)
		ta.add_event_cb(self._onPasswordCancel, lv.EVENT.CANCEL, None)
		self._passwordTextarea = ta

		lv.gridnav_set_focused(content, ta, False)
		self._onPasswordReady(None)

	def _onPasswordReady(self, e):
		if self._keyboard == False:
			self._keyboard = KEYBOARD_ALL_SYMBOLS()
			self._keyboard.set_textarea(self._passwordTextarea)
			group = lv.group_create()
			group.add_obj(self._keyboard)
			indev1.set_group(group)
		else:
			password = self._passwordTextarea.get_text()
			if len(password) < 8:
				self._errLabel.set_text("At least 8 characters required")
				self._errLabel.remove_flag(self._errLabel.FLAG.HIDDEN)
				return
			self._hideKeyboard()
			self.singletons["WIFI_MANAGER"].connect(self._currentSSID, password)

	def _onPasswordCancel(self, e):
		self._hideKeyboard()

	def _hideKeyboard(self):
		if self._keyboard:
			self._keyboard.delete()
			self._keyboard = False
		if self._savedGroup:
			indev1.set_group(self._savedGroup)
			self._savedGroup = None
		if self._passwordDialog:
			self._passwordDialog.close()
			self._passwordDialog = None
