import lvgl as lv
from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller


class WifiSubPage(lv.obj):
	label = ""
	data = ""
	pressCallback = False

	def __init__(self, container):
		super().__init__(container)
		# Create sub pages
		self.set_width(240)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(self)
		label.set_text("Not implemented yet")
		label.set_width(160)
