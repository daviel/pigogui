import lvgl as lv
from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller


class SoundSubPage(lv.obj):
	label = ""
	data = ""
	pressCallback = False

	def __init__(self, container):
		super().__init__(container)
		# Create sub pages
		self.set_width(200)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(self)
		label.set_text("Volume")

		slider = ActiveSlider(self)
		slider.center()
		slider.set_width(160)
		slider.set_range(0, 10)

		label = lv.label(self)
		label.set_text("Menu Sounds")

		slider = ActiveSlider(self)
		slider.center()
		slider.set_width(160)
		slider.set_range(0, 10)
