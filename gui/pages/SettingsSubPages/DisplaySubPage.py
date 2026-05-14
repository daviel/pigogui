import lvgl as lv

from gui.components.Generic.SubPage import SubPage
from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller
from libs.threading import runShellCommand_bg


_TIMEOUT_OPTIONS = ["1 min", "2 min", "3 min", "5 min", "10 min", "15 min", "Never"]
_TIMEOUT_VALUES  = [1, 2, 3, 5, 10, 15, 0]


class DisplaySubPage(SubPage):
	def __init__(self, container, singletons):
		super().__init__(container, singletons)
		self.set_width(230)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)

		label = lv.label(self)
		label.set_text("Brightness")
		label.set_width(80)

		self.brightnessSlider = ActiveSlider(self)
		self.brightnessSlider.set_width(130)
		self.brightnessSlider.set_range(0, 100)
		self.brightnessSlider.add_event_cb(self._onBrightness, lv.EVENT.ALL, None)

		label = lv.label(self)
		label.set_text("Screen off after")
		label.set_width(120)

		self.turnOffRoller = ActiveRoller(self)
		self.turnOffRoller.set_options("\n".join(_TIMEOUT_OPTIONS), lv.roller.MODE.NORMAL)
		self.turnOffRoller.set_visible_row_count(3)
		self.turnOffRoller.set_width(90)
		self.turnOffRoller.add_event_cb(self._onTurnOff, lv.EVENT.ALL, None)

		label = lv.label(self)
		label.set_text("Dim after")
		label.set_width(120)

		self.darkenRoller = ActiveRoller(self)
		self.darkenRoller.set_options("\n".join(_TIMEOUT_OPTIONS), lv.roller.MODE.NORMAL)
		self.darkenRoller.set_visible_row_count(3)
		self.darkenRoller.set_width(90)
		self.darkenRoller.add_event_cb(self._onDarken, lv.EVENT.ALL, None)

	def loadSubPage(self, event):
		config = self.singletons["DATA_MANAGER"].get("configuration")
		d = config["user"]["display"]
		self.brightnessSlider.set_value(d["brightness"], True)
		off_val = d["turnOffTime"]
		dim_val = d["darkenTime"]
		self.turnOffRoller.set_selected(
			_TIMEOUT_VALUES.index(off_val) if off_val in _TIMEOUT_VALUES else 1, True)
		self.darkenRoller.set_selected(
			_TIMEOUT_VALUES.index(dim_val) if dim_val in _TIMEOUT_VALUES else 3, True)

	def _onBrightness(self, e):
		if e.get_code() == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.LEFT or key == lv.KEY.RIGHT:
				value = self.brightnessSlider.get_value()
				config = self.singletons["DATA_MANAGER"].get("configuration")
				config["user"]["display"]["brightness"] = value
				if config["debug"] == False:
					runShellCommand_bg("brightnessctl set {}%".format(value))

	def _onTurnOff(self, e):
		if e.get_code() == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.UP or key == lv.KEY.DOWN:
				idx = self.turnOffRoller.get_selected()
				config = self.singletons["DATA_MANAGER"].get("configuration")
				config["user"]["display"]["turnOffTime"] = _TIMEOUT_VALUES[idx]

	def _onDarken(self, e):
		if e.get_code() == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.UP or key == lv.KEY.DOWN:
				idx = self.darkenRoller.get_selected()
				config = self.singletons["DATA_MANAGER"].get("configuration")
				config["user"]["display"]["darkenTime"] = _TIMEOUT_VALUES[idx]
