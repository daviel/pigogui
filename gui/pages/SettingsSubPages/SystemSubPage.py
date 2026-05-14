import io
import lvgl as lv

from gui.components.Generic.SubPage import SubPage
from gui.components.Generic.Switch import Switch
from gui.components.Generic.Button import Button

from libs.threading import runShellCommand_bg
from libs.init_drv import indev1
from libs.Helper import add_or_replace_in_file, KEYBOARD_ALL_SYMBOLS


class SystemSubPage(SubPage):
	def __init__(self, container, singletons):
		super().__init__(container, singletons)
		self.set_width(240)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_style_pad_hor(8, 0)
		self.set_style_pad_ver(8, 0)

		self._keyboard = False
		self._passwordDialog = None
		self._passwordTextarea = None
		self._errLabel = None
		self._savedGroup = None

		label = lv.label(self)
		label.set_text("Enable SSH")
		label.set_width(120)

		self.switch = Switch(self)
		self.switch.add_event_cb(self.enableSwitch, lv.EVENT.ALL, None)

		config = self.singletons["DATA_MANAGER"].get("configuration")

		self.labelHostname = lv.label(self)
		self.labelHostname.set_text("Hostname: pigo-" + config["user"]["profile"]["username"])
		self.labelHostname.set_width(160)

		self.labelIP = lv.label(self)
		self.labelIP.set_text("IP: " + self.singletons["WIFI_MANAGER"].IPAddress)
		self.labelIP.set_width(160)

		self.labelUsername = lv.label(self)
		self.labelUsername.set_text("Username: pigo")
		self.labelUsername.set_width(160)

		pwBtn = Button(self, "Set new password")
		pwBtn.set_width(160)
		pwBtn.set_height(28)
		pwBtn.label.center()
		pwBtn.add_event_cb(self._onPwBtn, lv.EVENT.PRESSED, None)

	def loadSubPage(self, event):
		config = self.singletons["DATA_MANAGER"].get("configuration")
		self.labelIP.set_text("IP: " + self.singletons["WIFI_MANAGER"].IPAddress)
		self.labelHostname.set_text("Hostname: pigo-" + config["user"]["profile"]["username"])
		if config["user"]["system"]["ssh"] == True:
			self.switch.add_state(lv.STATE.CHECKED)
		else:
			self.switch.remove_state(lv.STATE.CHECKED)

	def enableSwitch(self, e):
		code = e.get_code()
		if code == lv.EVENT.VALUE_CHANGED:
			enabled = self.switch.has_state(lv.STATE.CHECKED) == True
			config = self.singletons["DATA_MANAGER"].get("configuration")
			if config["debug"] == False:
				if enabled:
					add_or_replace_in_file("/etc/ssh/ssh_config", "PasswordAuthentication Yes", identifier="PasswordAuthentication", replace_line=True)
					runShellCommand_bg("systemctl enable ssh")
					runShellCommand_bg("systemctl start ssh")
					config["user"]["system"]["ssh"] = True
				else:
					runShellCommand_bg("systemctl disable ssh")
					runShellCommand_bg("systemctl stop ssh")
					config["user"]["system"]["ssh"] = False
				self.singletons["DATA_MANAGER"].saveAll()

	def _onPwBtn(self, e):
		self._showPasswordDialog()

	def _showPasswordDialog(self):
		self._savedGroup = indev1.get_group()

		dialog = lv.msgbox(lv.screen_active())
		dialog.align(lv.ALIGN.CENTER, 0, 0)
		dialog.add_text("Set new password")
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
		ta.set_placeholder_text("New password (min 8 chars)")
		ta.set_height(36)
		ta.set_width(220)
		ta.add_event_cb(self._onPwReady, lv.EVENT.READY, None)
		ta.add_event_cb(self._onPwCancel, lv.EVENT.CANCEL, None)
		self._passwordTextarea = ta

		lv.gridnav_set_focused(content, ta, False)
		self._onPwReady(None)

	def _onPwReady(self, e):
		if self._keyboard == False:
			self._keyboard = KEYBOARD_ALL_SYMBOLS()
			self._keyboard.set_textarea(self._passwordTextarea)
			group = lv.group_create()
			group.add_obj(self._keyboard)
			indev1.set_group(group)
		else:
			pw = self._passwordTextarea.get_text()
			if len(pw) < 8:
				self._errLabel.set_text("At least 8 characters required")
				self._errLabel.remove_flag(self._errLabel.FLAG.HIDDEN)
				return
			self._hideKeyboard()
			f = io.open("/tmp/.pigo_pw", "w")
			f.write("pigo:" + pw + "\n")
			f.close()
			runShellCommand_bg("chpasswd < /tmp/.pigo_pw; rm -f /tmp/.pigo_pw")

	def _onPwCancel(self, e):
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
