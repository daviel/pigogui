import lvgl as lv
import time

from gui.components.button import Button


class TopBar(lv.obj):
	label_time = ""
	timer = ""


	def __init__(self, container):
		super().__init__(container)

		self.set_size(320, 24)
		self.align(lv.ALIGN.CENTER, 0, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.clear_flag(self.FLAG.SCROLLABLE)

		self.label_time = lv.label(self)
		#self.label_time.center()
		self.label_time.set_text('10:15')

		spacer = lv.obj(self)
		spacer.set_flex_grow(1)

		self.label1 = lv.label(self)
		self.label1.set_text('W')

		self.label1 = lv.label(self)
		self.label1.set_text('B')

		self.timer = lv.timer_create(self.update_time, 1000, self)

	def update_time(obj, timer):
		current_time = time.localtime()
		hour = str(current_time[3])
		minute = str(current_time[4])

		if(len(hour) == 1):
			hour = '0' + hour
		if(len(minute) == 1):
			minute = '0' + minute
		obj.label_time.set_text(hour + ':' + minute)