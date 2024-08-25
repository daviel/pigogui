import lvgl as lv


class Button(lv.button):
	label = ""
	data = ""
	pressCallback = False

	def __init__(self, container, text):
		super().__init__(container)
		self.label = lv.label(self)
		self.label.set_text(text)
		self.label.center()
		self.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)

	def addPressEvent(self, e):
		if(self.pressCallback):
			self.pressCallback(self, e)
