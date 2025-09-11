import lvgl as lv

from gui.components.Generic.SubPage import SubPage

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller
from gui.components.Generic.Loader import Loader

from libs.ffishell import runShellCommand


class InfoSubPage(SubPage):
	label = ""
	data = ""
	pressCallback = False
	updateCheckBtn = ""
	updateBtn = ""

	checkDate = ""

	def __init__(self, container, singletons):
		super().__init__(container, singletons)
		# Create sub pages
		self.set_width(240)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_style_pad_hor(8, 0)
		self.set_style_pad_ver(8, 0)
		# content

		label = lv.label(self)
		label.set_text(
"""
Made and developed by David Krawiec \n
Thank you for using PiGo. :)
""")
		label.set_long_mode(lv.label.LONG_MODE.WRAP)
		label.set_width(180)
