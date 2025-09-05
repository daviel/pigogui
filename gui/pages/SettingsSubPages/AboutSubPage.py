import lvgl as lv

from gui.components.Generic.SubPage import SubPage

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller

from libs.ffishell import runShellCommand
from libs.Helper import update_available
import time


class AboutSubPage(SubPage):
	label = ""
	data = ""
	pressCallback = False
	updateCheckBtn = ""
	updateBtn = ""

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
		label.set_width(180)

		label = lv.label(self)
		label.set_text("Last time checked:")
		label.set_width(180)

		label = lv.label(self)
		label.set_text(config["user"]["system"]["updateCheckDate"])
		label.set_width(180)
		self.checkDate = label

		btn = lv.button(self)
		btn.add_event_cb(self.checkUpdate, lv.EVENT.PRESSED, None)
		btn.set_width(180)
		label = lv.label(btn)
		label.set_text("Check for Updates")
		self.updateCheckBtn = btn

		btn = lv.button(self)
		btn.add_event_cb(self.installUpdate, lv.EVENT.PRESSED, None)
		btn.set_width(180)
		label = lv.label(btn)
		label.set_text("Install Update")
		btn.add_flag(self.FLAG.HIDDEN)
		self.updateBtn = btn

		label = lv.label(self)
		label.set_text(
"""
Made and developed by David Krawiec \n
Thank you for using PiGo. :)
""")
		label.set_long_mode(lv.label.LONG_MODE.WRAP)
		label.set_width(180)
		
	def checkUpdate(self, event):
		t = time.localtime()
		year, month, day, hour, minute, second, _, _, _ = t
		date = f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
		self.checkDate.set_text(date)
	
		config = self.singletons["DATA_MANAGER"].get("configuration")
		config["user"]["system"]["updateCheckDate"] = date
		self.singletons["DATA_MANAGER"].saveAll()

		if update_available():
			print("update available")
			self.updateCheckBtn.add_state(self.FLAG.HIDDEN)
			self.updateBtn.remove_flag(self.FLAG.HIDDEN)
			#self.group.add_obj(self.updateBtn)
			lv.gridnav_set_focused(self, self.updateBtn, False)
		else:
			print("no update available")
			self.updateCheckBtn.remove_flag(self.FLAG.HIDDEN)
			self.updateBtn.add_state(self.FLAG.HIDDEN)
			#self.group.add_obj(self.updateCheckBtn)
			lv.gridnav_set_focused(self, self.updateCheckBtn, False)

	def installUpdate(self, event):
		ret = runShellCommand('git pull')
		ret = runShellCommand('systemctl restart pigogui')
		pass
