import lvgl as lv


class Switch(lv.switch):
	data = ""
	pressCallback = False

	def __init__(self, container):
		super().__init__(container)
		self.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)

	def addPressEvent(self, e):
		if(self.pressCallback):
			self.pressCallback(self, e)
