import lvgl as lv

from gui.components.Generic.SubPage import SubPage

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller

import libs.Singletons as SINGLETONS


class UserSubPage(SubPage):
	label = ""
	data = ""
	colors = []
	primaryColor = ""
	darkTheme = False

	primaryColorRoller = ""
	darkThemeRoller = ""

	def __init__(self, container):
		super().__init__(container)
		# Create sub pages
		self.set_width(240)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(self)
		label.set_text("Theme mode")
		label.set_width(70)

		self.darkThemeRoller = ActiveRoller(self)
		self.darkThemeRoller.set_options("\n".join([
			"Light",
			"Dark",
			]),lv.roller.MODE.NORMAL)
		self.darkThemeRoller.set_visible_row_count(2)
		self.darkThemeRoller.set_width(120)
		self.darkThemeRoller.add_event(self.changeThemeHandler, lv.EVENT.ALL, None)

		label = lv.label(self)
		label.set_text("Theme color")
		label.set_width(70)

		for color in lv.PALETTE.__dict__:
			self.colors.append(color)

		self.primaryColorRoller = ActiveRoller(self)
		self.primaryColorRoller.set_options("\n".join(self.colors), lv.roller.MODE.INFINITE)
		self.primaryColorRoller.set_visible_row_count(3)
		self.primaryColorRoller.set_width(120)
		self.primaryColorRoller.add_event(self.changeThemeHandler, lv.EVENT.ALL, None)
		
	def loadSubPage(self, event):
		config = SINGLETONS.DATA_MANAGER.get("configuration")
		self.primaryColor = config["user"]["theme"]["primaryColor"]
		self.darkTheme = config["user"]["theme"]["darkTheme"]

		self.primaryColorRoller.set_selected(self.colors.index(self.primaryColor), True)
		if self.darkTheme == True:
			self.darkThemeRoller.set_selected(1, True)
		else:
			self.darkThemeRoller.set_selected(0, True)
		pass

	def changeThemeHandler(self, e):
		code = e.get_code()
		obj = e.get_target_obj()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.UP or key == lv.KEY.DOWN:
				option = " " * 20
				obj.get_selected_str(option, len(option))
				selection = option.strip()[:-1]

				colors = lv.PALETTE.__dict__
				primary_color = colors[self.primaryColor]
				config = SINGLETONS.DATA_MANAGER.get("configuration")

				if selection == "Light":
					self.darkTheme = False
				elif selection == "Dark":
					self.darkTheme = True
				else:
					primary_color = colors[selection]
					self.primaryColor = selection
					config["user"]["theme"]["primaryColor"] = selection

				lv.theme_default_init(lv.disp_get_default(), 
						lv.palette_main(primary_color), 
						lv.palette_main(lv.PALETTE.GREY), 
						self.darkTheme, 
						lv.font_montserrat_16)
				
				config["user"]["theme"]["darkTheme"] = self.darkTheme