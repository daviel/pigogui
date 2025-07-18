import lvgl as lv


class IconButton(lv.button):
	label = ""
	data = ""
	pressCallback = False

	def __init__(self, container, symbol, text):
		super().__init__(container)
		self.set_height(24)
		self.set_style_pad_hor(4, 0)
		self.set_style_pad_ver(4, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)

		symbolLabel = lv.label(self)
		symbolLabel.set_text(symbol)
		symbolLabel.set_width(18)
		symbolLabel.center()

		label = lv.label(self)
		label.set_text(text)
		#label.set_width(42)
		label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)


	def addPressEvent(self, e):
		if(self.pressCallback):
			self.pressCallback(self, e)
