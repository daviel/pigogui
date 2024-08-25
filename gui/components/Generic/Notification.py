import lvgl as lv

from gui.anims.GenericAnim import GenericAnim


class Notification(lv.obj):
	message = ""
	timer = None
	animTime = 1000
	doneCB = None

	def __init__(self, symbol, text, duration, doneCB=None):
		super().__init__(lv.layer_top())
		self.duration = duration
		self.doneCB = doneCB

		self.set_size(0, 40)
		self.align(lv.ALIGN.TOP_MID, 0, 8)
		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.remove_flag(self.FLAG.SCROLLABLE)
		self.set_style_opa(lv.OPA._80, 0)

		self.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.set_style_pad_column(0, 0)
		self.set_style_pad_row(0, 0)
		#self.set_style_bg_color(lv.theme_get_color_secondary(0), 0)

		self.set_style_border_width(1, 0)
		self.set_style_border_color(lv.theme_get_color_primary(0), 0)
		
		messageSymbol = lv.label(self)
		messageSymbol.set_text(symbol)
		messageSymbol.set_size(24, 24)
		
		message = lv.label(self)
		message.set_text(text)
		message.set_size(148, 24)
		message.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
		self.message = message

		self.scroll_to(0, 2, lv.ANIM.OFF)

		self.animShow = GenericAnim()
		self.animShow.set_values(0, 200)
		self.animShow.set_time(self.animTime)
		self.animShow.set_path_cb(lv.anim_t.path_ease_in)
		self.animShow.target = self
		self.animShow.anim_cb = self.anim_func
		self.animShow.anim_done_cb = self.hide

		self.animHide = GenericAnim()
		self.animHide.set_values(200, 0)
		self.animHide.set_time(self.animTime)
		self.animHide.set_path_cb(lv.anim_t.path_ease_in)
		self.animHide.target = self
		self.animHide.set_delay(self.duration)
		self.animHide.anim_cb = self.anim_func
		self.animHide.anim_done_cb = self.done

	def hide(self, obj, anim):
		#print("hide notification", self.message.get_text())
		self.animHide.start()
		self.fade_out(self.animTime - 100, self.duration)


	def show(self):
		#print("show notification", self.message.get_text())
		self.animShow.start()
		self.fade_in(self.animTime, 0)

	def done(self, obj, anim):
		#print("done notification")
		if self.doneCB:
			self.doneCB(self)

	def anim_func(self, obj, anim, val):
		obj.target.set_width(val)
