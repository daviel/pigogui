import lvgl as lv


class GenericAnim(lv.anim_t):
	target = ""
	anim_cb = ""
	anim_done_cb = None

	running = False

	def __init__(self):
		super().__init__()
		self.set_start_cb(self.set_is_running)
		self.set_ready_cb(self.set_is_not_running)
		self.set_custom_exec_cb(self.anim_func)

	def anim_func(self, anim, val):
		self.anim_cb(self, anim, val)

	def set_is_running(self, anim):
		self.running = True

	def set_is_not_running(self, anim):
		if self.anim_done_cb:
			self.anim_done_cb(self, anim)
		self.running = False

	def is_running(self):
		return self.running

	def start(self):
		return super().start()