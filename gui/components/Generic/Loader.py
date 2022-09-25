import lvgl as lv


class Loader(lv.arc):
	currentValue = 90

	def __init__(self, container):
		super().__init__(container)

		self.set_bg_angles(0, 360)
		self.set_angles(270, 270)
		self.center()
		#self.set_size(64, 64)
		self.clear_flag(self.FLAG.CLICKABLE)
		self.remove_style(None, lv.PART.KNOB)

		self.timer = lv.timer_create(self.fill, 30, None)

	def fill(self, timer):
		self.currentValue += 15
		if(self.currentValue >= 450):
			self.currentValue = 90
		self.set_angles(self.currentValue - 90, self.currentValue)
