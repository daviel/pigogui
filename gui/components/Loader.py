import lvgl as lv


class Loader(lv.arc):
	currentValue = 0

	def __init__(self, container):
		super().__init__(container)

		self.set_bg_angles(0, 360)
		self.set_angles(270, 270)
		self.center()

		timer = lv.timer_create(self.fill, 20, None)

	def fill(self, timer):
		self.currentValue += 5
		if(self.currentValue >= 360):
			self.currentValue = 0
		self.set_angles(0, self.currentValue)
		pass