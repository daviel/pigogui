import lvgl as lv


class Button(lv.btn):

	def __init__(self, container, text):
		super().__init__(container)
		label = lv.label(self)
		label.set_text(text)
