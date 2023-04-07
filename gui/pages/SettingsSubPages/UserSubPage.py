import lvgl as lv
from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller


class UserSubPage(lv.obj):
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
		label.set_text("Theme mode")
		label.set_width(80)

		roller1 = ActiveRoller(self)
		roller1.set_options("\n".join([
			"Light",
			"Dark",
			]),lv.roller.MODE.NORMAL)
		roller1.set_visible_row_count(2)
		roller1.set_width(120)
		roller1.add_event_cb(self.changeThemeHandler, lv.EVENT.ALL, None)

		label = lv.label(self)
		label.set_text("Theme color")
		label.set_width(80)

		colors = []
		for color in lv.PALETTE.__dict__:
			colors.append(color)

		roller1 = ActiveRoller(self)
		roller1.set_options("\n".join(colors), lv.roller.MODE.INFINITE)
		roller1.set_visible_row_count(3)
		roller1.set_width(120)
		roller1.add_event_cb(self.changeThemeHandler, lv.EVENT.ALL, None)
		
	def changeThemeHandler(self, e):
		code = e.get_code()
		obj = e.get_target()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.UP or key == lv.KEY.DOWN:
				option = " " * 20
				obj.get_selected_str(option, len(option))
				selection = option.strip()[:-1]

				if selection == "Light":
					self.darkTheme = False
				elif selection == "Dark":
					self.darkTheme = True
				else:
					colors = lv.PALETTE.__dict__
					primary_color = colors[selection]
					self.primaryColor = primary_color

				lv.theme_default_init(lv.disp_get_default(), 
						lv.palette_main(self.primaryColor), 
						lv.palette_main(lv.PALETTE.GREY), 
						self.darkTheme, 
						lv.font_montserrat_16)