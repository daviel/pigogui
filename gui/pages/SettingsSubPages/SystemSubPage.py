import lvgl as lv

from gui.components.Generic.SubPage import SubPage

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller
from gui.components.Generic.Switch import Switch
from gui.components.Generic.Button import Button

from libs.ffishell import runShellCommand

from libs.Helper import add_or_replace_in_file


class SystemSubPage(SubPage):
	label = ""
	data = ""
	pressCallback = False
	switch = ""

	labelUsername = ""
	labelHostname = ""
	labelIP = ""

	def __init__(self, container, singletons):
		super().__init__(container, singletons)
		# Create sub pages
		self.set_width(240)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_style_pad_hor(8, 0)
		self.set_style_pad_ver(8, 0)
		# content
		label = lv.label(self)
		label.set_text("Enable SSH")
		label.set_width(120)

		self.switch = Switch(self)
		self.switch.add_event_cb(self.enableSwitch, lv.EVENT.ALL, None)

		config = self.singletons["DATA_MANAGER"].get("configuration")

		self.labelUsername = lv.label(self)
		self.labelUsername.set_text("Username: " + config["user"]["profile"]["username"])
		self.labelUsername.set_width(160)

		self.labelHostname = lv.label(self)
		self.labelHostname.set_text("Hostname: pigo-" + config["user"]["profile"]["username"])
		self.labelHostname.set_width(160)

		self.labelIP = lv.label(self)
		self.labelIP.set_text("IP: " + self.singletons["WIFI_MANAGER"].IPAddress)
		self.labelIP.set_width(160)

		label = lv.label(self)
		label.set_text("Default password: pigo")
		label.set_width(160)

		button = Button(self, "Set new password")
	
	def loadSubPage(self, event):
		config = self.singletons["DATA_MANAGER"].get("configuration")

		self.labelIP.set_text("IP: " + self.singletons["WIFI_MANAGER"].IPAddress)
		self.labelHostname.set_text("Hostname: pigo-" + config["user"]["profile"]["username"])
		self.labelUsername.set_text("Username: " + config["user"]["profile"]["username"])

		if config["user"]["system"]["ssh"] == True:
			self.switch.add_state(lv.STATE.CHECKED)
		else:
			self.switch.remove_state(lv.STATE.CHECKED)
		pass

	def enableSwitch(self, e):
		code = e.get_code()
		if code == lv.EVENT.VALUE_CHANGED:
			enabled = self.switch.has_state(lv.STATE.CHECKED) == True
			config = self.singletons["DATA_MANAGER"].get("configuration")
			if config["debug"] == False:
				if enabled:
					add_or_replace_in_file("/etc/ssh/ssh_config", "PasswordAuthentication Yes", identifier="PasswordAuthentication", replace_line=True)
					
					ret = runShellCommand('rm /etc/ssh/ssh_host_*')
					ret = runShellCommand('dpkg-reconfigure openssh-server')
					ret = runShellCommand('ssh-keygen -A')
					
					ret = runShellCommand('systemctl enable ssh &')
					ret = runShellCommand('systemctl start ssh &')
					config["user"]["system"]["ssh"] = True
				else:
					ret = runShellCommand('systemctl disable ssh &')
					ret = runShellCommand('systemctl stop ssh &')
					config["user"]["system"]["ssh"] = False
				self.singletons["DATA_MANAGER"].saveAll()
