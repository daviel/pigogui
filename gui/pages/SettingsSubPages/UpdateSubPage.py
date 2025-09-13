import lvgl as lv

from gui.components.Generic.SubPage import SubPage

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller
from gui.components.Generic.Loader import Loader

from libs.threading import runShellCommand_bg


class UpdateSubPage(SubPage):
	label = ""
	data = ""
	pressCallback = False
	updateCheckBtn = ""
	updateBtn = ""
	updateBtnLabel = ""

	checkDate = ""

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
		versions = self.singletons["DATA_MANAGER"].get("pigo")
		config = self.singletons["DATA_MANAGER"].get("configuration")

		label = lv.label(self)
		label.set_text("PiGo: V" + versions["versions"]["pigogui"])
		label.set_width(100)

		loader = Loader(self)
		loader.set_size(24, 24)
		loader.add_flag(loader.FLAG.HIDDEN)
		self.loader = loader

		btn = lv.button(self)
		btn.add_event_cb(self.checkUpdate, lv.EVENT.PRESSED, None)
		btn.set_width(180)
		label = lv.label(btn)
		label.set_text("Check for updates")
		self.updateCheckBtn = btn

		btn = lv.button(self)
		btn.add_event_cb(self.installUpdate, lv.EVENT.PRESSED, None)
		btn.set_width(180)
		label = lv.label(btn)
		label.set_text("Install update")
		btn.add_flag(self.FLAG.HIDDEN)
		self.updateBtn = btn
		self.updateBtnLabel = label

		label = lv.label(self)
		label.set_text("Last time checked:")
		label.set_width(180)

		label = lv.label(self)
		label.set_text(config["user"]["system"]["updateCheckDate"])
		label.set_width(180)
		self.checkDate = label

		config = self.singletons["DATA_MANAGER"].updateAvailableCallbacks.append(self.checkUpdateDone)
		
	def checkUpdate(self, event):
		self.loader.remove_flag(self.loader.FLAG.HIDDEN)
		self.singletons["DATA_MANAGER"].checkForUpdate()

	def checkUpdateDone(self, updateAvailable):
		if updateAvailable:
			print("update available")
			self.updateCheckBtn.add_state(self.FLAG.HIDDEN)
			self.updateBtn.remove_flag(self.FLAG.HIDDEN)
			lv.gridnav_set_focused(self, self.updateBtn, False)
		else:
			print("no update available")
			self.updateCheckBtn.remove_flag(self.FLAG.HIDDEN)
			self.updateBtn.add_state(self.FLAG.HIDDEN)
			lv.gridnav_set_focused(self, self.updateCheckBtn, False)
		self.loader.add_flag(self.loader.FLAG.HIDDEN)

	def installUpdate(self, event):
		self.updateBtn.add_state(lv.STATE.DISABLED)
		self.updateBtnLabel.set_text("Installing...")
		ret = runShellCommand_bg('git pull && systemctl restart pigogui')
		pass
