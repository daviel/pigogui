import lvgl as lv

from gui.components.Generic.SubPage import SubPage

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller

import libs.Singletons as SINGLETONS


class SoundSubPage(SubPage):
	label = ""
	data = ""
	volume = 10
	menu = 5

	volumeSlider = ""
	menuSlider = ""

	def __init__(self, container):
		super().__init__(container)
		# Create sub pages
		self.set_width(200)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(self)
		label.set_text("Volume")

		self.volumeSlider = ActiveSlider(self)
		self.volumeSlider.center()
		self.volumeSlider.set_width(160)
		self.volumeSlider.set_range(0, 10)
		self.volumeSlider.add_event(self.setVolume, lv.EVENT.ALL, None)

		label = lv.label(self)
		label.set_text("Menu Sounds")

		self.menuSlider = ActiveSlider(self)
		self.menuSlider.center()
		self.menuSlider.set_width(160)
		self.menuSlider.set_range(0, 10)
		self.menuSlider.add_event(self.setMenuVolume, lv.EVENT.ALL, None)

	def loadSubPage(self, event):
		config = SINGLETONS.DATA_MANAGER.get("configuration")
		self.volume = config["user"]["sound"]["volume"]
		self.menu = config["user"]["sound"]["menu"]

		self.volumeSlider.set_value(self.volume, True)
		self.menuSlider.set_value(self.menu, True)
		pass

	def setVolume(self, e):
		code = e.get_code()
		obj = e.get_target_obj()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.LEFT or key == lv.KEY.RIGHT:
				config = SINGLETONS.DATA_MANAGER.get("configuration")
				print("volume changed", self.volumeSlider.get_value())
				config["user"]["sound"]["volume"] = self.volumeSlider.get_value()
		pass

	def setMenuVolume(self, e):
		code = e.get_code()
		obj = e.get_target_obj()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.LEFT or key == lv.KEY.RIGHT:
				config = SINGLETONS.DATA_MANAGER.get("configuration")
				print("volume changed", self.menuSlider.get_value())
				config["user"]["sound"]["menu"] = self.menuSlider.get_value()
		pass