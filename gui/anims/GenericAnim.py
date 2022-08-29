import lvgl as lv


class GenericAnim(lv.anim_t):
	target = ""
	anim_cb = ""

	def __init__(self):
		super().__init__()

	def anim_func(self, anim, val):
		self.anim_cb(self, anim, val)