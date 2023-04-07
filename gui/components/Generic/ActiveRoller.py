import lvgl as lv
from libs.init_drv import indev1
from libs.Helper import SDL_KEYS

class ActiveRoller(lv.roller):
	label = ""
	slider = ""
	data = ""
	pressCallback = False
	lastGroup = ""
	group = ""

	def __init__(self, container):
		super().__init__(container)
		self.add_event_cb(self.addPressEvent, lv.EVENT.PRESSED, None)
		self.add_event_cb(self.cancelEvent, lv.EVENT.CANCEL, None)

		self.group = lv.group_create()
		self.group.add_obj(self)
		self.clear_state(lv.STATE.ANY)

	def addPressEvent(self, e):
		if indev1.group != self.group:
			self.lastGroup = indev1.group
			indev1.set_group(self.group)
		else:
			indev1.set_group(self.lastGroup)

	def cancelEvent(self, e):
		indev1.set_group(self.lastGroup)
