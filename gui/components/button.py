import lvgl as lv


class Button(lv.btn):
	label = ""

	def __init__(self, container, text):
		super().__init__(container)
		self.label = lv.label(self)
		self.label.set_text(text)
