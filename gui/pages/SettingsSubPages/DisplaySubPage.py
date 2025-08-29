import lvgl as lv

from gui.components.Generic.SubPage import SubPage

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller


class DisplaySubPage(SubPage):
	label = ""
	data = ""
	pressCallback = False

	def __init__(self, container, singletons):
		super().__init__(container, singletons)
		# Create sub pages
		self.set_width(230)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)

		# content
		label = lv.label(self)
		label.set_text("Brightness")

		slider = ActiveSlider(self)
		slider.center()
		slider.set_width(160)
		slider.set_range(0, 10)

		label = lv.label(self)
		label.set_text("Minutes to wait to turn off display")
		label.set_width(80)

		roller1 = ActiveRoller(self)
		roller1.set_options("\n".join([
			"1",
			"2",
			"3",
			"5",
			"10",
			"15",
			"Never",
			]),lv.roller.MODE.INFINITE)

		roller1.set_visible_row_count(3)
		roller1.set_width(60)

		label = lv.label(self)
		label.set_text("Minutes to wait to turn darken display")
		label.set_width(80)

		roller2 = ActiveRoller(self)
		roller2.set_options("\n".join([
			"1",
			"2",
			"3",
			"5",
			"10",
			"15",
			"Never",
			]),lv.roller.MODE.INFINITE)

		roller2.set_visible_row_count(3)
		roller2.set_width(60)
