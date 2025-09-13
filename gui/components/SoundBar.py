import lvgl as lv

from gui.anims.GenericAnim import GenericAnim
from libs.libsdl import addGlobalKeyCallback
from libs.threading import runShellCommand_bg


class SoundBar(lv.obj):
	currentValue = 25
	bar = None
	soundSymbol = None
	isVisible = False

	message = ""
	timer = None
	animTime = 250
	duration = 3000
	doneCB = None

	def __init__(self, singletons):
		super().__init__(lv.layer_top())
		self.singletons = singletons

		self.set_size(32, 160)
		self.fade_out(0, 0)
		self.align(lv.ALIGN.LEFT_MID, 8, 0)
		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.remove_flag(self.FLAG.SCROLLABLE)
		self.set_style_opa(lv.OPA._90, 0)

		self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		self.set_style_pad_column(0, 0)
		self.set_style_pad_row(8, 0)
		#self.set_style_bg_color(lv.theme_get_color_secondary(0), 0)

		self.set_style_border_width(1, 0)
		self.set_style_border_color(lv.theme_get_color_primary(0), 0)

		bar1 = lv.bar(self)
		bar1.set_size(16, 116)
		bar1.set_value(25, False)
		bar1.set_range(0, 100)
		self.bar = bar1

		soundSymbol = lv.label(self)
		soundSymbol.set_text(lv.SYMBOL.VOLUME_MID)
		soundSymbol.set_size(32, 32)
		soundSymbol.set_pos(8, 0)
		self.soundSymbol = soundSymbol

		self.scroll_to(6, 0, False)
		addGlobalKeyCallback(self.inc_vol, "louder")
		addGlobalKeyCallback(self.dec_vol, "quieter")

		self.animShow = GenericAnim()
		self.animShow.set_values(-40, 8)
		self.animShow.set_duration(self.animTime)
		self.animShow.set_path_cb(lv.anim_t.path_ease_in)
		self.animShow.target = self
		self.animShow.anim_cb = self.anim_func
		self.animShow.anim_done_cb = self.hide

		self.animHide = GenericAnim()
		self.animHide.set_values(8, -40)
		self.animHide.set_duration(self.animTime)
		self.animHide.set_path_cb(lv.anim_t.path_ease_in)
		self.animHide.target = self
		self.animHide.set_delay(self.duration)
		self.animHide.anim_cb = self.anim_func
		self.animHide.anim_done_cb = self.done
		
		config = self.singletons["DATA_MANAGER"].get("configuration")
		self.currentValue = int(config["user"]["sound"]["volume"])
		self.inc_volume(0)

	def show(self):
		if self.isVisible == False:
			self.isVisible = True
			self.fade_in(self.animTime, 0)
			self.showanim = self.animShow.start()
	
	def hide(self, obj, anim):
		self.animHide.start()
		self.fade_out(self.animTime - 100, self.duration)

	def done(self, obj, anim):
		self.isVisible = False

	def anim_func(self, obj, anim, val):
		obj.target.set_pos(val, 0)

	def inc_volume(self, inc):
		self.show()
		self.currentValue += inc
		if self.currentValue < 0:
			self.currentValue = 0
			self.soundSymbol.set_text(lv.SYMBOL.MUTE)
		elif self.currentValue > 100:
			self.currentValue = 100
			self.soundSymbol.set_text(lv.SYMBOL.VOLUME_MAX)
		else:
			self.soundSymbol.set_text(lv.SYMBOL.VOLUME_MID)
		self.bar.set_value(self.currentValue, True)
		
		config = self.singletons["DATA_MANAGER"].get("configuration")
		if config["debug"] == False:
			handle = runShellCommand_bg("amixer set PCM " + self.currentValue + "%")
		config["user"]["sound"]["volume"] = self.currentValue
		self.singletons["DATA_MANAGER"].saveAll()

	def get_volume(self):
		return self.currentValue

	def inc_vol(self):
		self.inc_volume(10)
	
	def dec_vol(self):
		self.inc_volume(-10)