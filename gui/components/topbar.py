import lvgl as lv
import time

from gui.components.Generic.Button import Button


class TopBar(lv.obj):
	label_time = ""
	timer = ""


	def __init__(self, container):
		super().__init__(container)

		self.set_size(320, 16)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.clear_flag(self.FLAG.SCROLLABLE)
		self.set_style_border_width(0, 0)
		self.set_style_pad_all(1, 0)
		self.set_style_radius(0, 0)
		#self.set_style_opa(lv.OPA._80, 0)
		self.set_style_bg_color(lv.theme_get_color_primary(0), 0)

		self.label_time = lv.label(self)
		self.label_time.set_text('10:15')

		spacer = lv.obj(self)
		spacer.set_flex_grow(1)

		spacer.set_style_bg_color(lv.theme_get_color_primary(0), 0)
		spacer.set_style_border_width(0, 0)

		self.label1 = lv.label(self)
		self.label1.set_text(lv.SYMBOL.WIFI)

		self.label1 = lv.label(self)
		self.label1.set_text(lv.SYMBOL.BATTERY_FULL)

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