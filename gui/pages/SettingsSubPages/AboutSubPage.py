import lvgl as lv

from gui.components.Generic.SubPage import SubPage

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller


class AboutSubPage(SubPage):
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
		self.set_style_pad_hor(8, 0)
		self.set_style_pad_ver(8, 0)
		# content
		label = lv.label(self)
		label.set_text("PiGO V1.0")
		label.set_width(160)

		label = lv.label(self)
		label.set_text("Last time checked:")
		label.set_width(160)

		label = lv.label(self)
		label.set_text("About an hour ago")
		label.set_width(160)

		btn = lv.btn(self)
		btn.add_event(self.addPressEvent, lv.EVENT.PRESSED, None)
		btn.set_width(160)
		label = lv.label(btn)
		label.set_text("Check for Updates")

		label = lv.label(self)
		label.set_text(
"""
Made and developed by David Krawiec \n\n
Thank you for using PiGO. :)
""")
		label.set_long_mode(lv.label.LONG.WRAP)
		label.set_width(160)
		
	def addPressEvent(self, event):
		print(event)
