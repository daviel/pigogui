import lvgl as lv
from gui.components.Generic.Button import Button


class BottomBar(lv.obj):
	clock = ""
	buttons_desc = [
		{
			'button_text': "A",
			'text': "Start",
			'color': lv.PALETTE.BLUE
		},
		{
			'button_text': "B",
			'text': "Back",
			'color': lv.PALETTE.RED
		},
		{
			'button_text': "X",
			'text': "Zoom",
			'color': lv.PALETTE.YELLOW
		},
		{
			'button_text': "Y",
			'text': "Details",
			'color': lv.PALETTE.GREEN
		}
	]
	buttons = []
	button_style = ""

	def __init__(self, container):
		super().__init__(container)
		self.init_button_style()

		self.set_size(320, 30)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.set_style_border_width(0, 0)
		self.set_style_pad_column(4, 0)
		self.set_style_pad_row(0, 0)

		for button in self.buttons_desc:
			button1 = Button(self, button['button_text'])
			button1.set_size(24, 24)
			button1.label.center()
			button1.add_style(self.button_style, 0)
			button1.set_style_bg_color(lv.palette_main(button['color']), 0)
			self.buttons.append(button1)

			label = lv.label(self)
			label.set_text(button['text'])

		self.scroll_to(0, 14, False)

	def init_button_style(self):
		button_style = lv.style_t()
		button_style.init()
		button_style.set_radius(lv.RADIUS_CIRCLE)
		#button_style.set_bg_opa(lv.OPA.COVER)
		button_style.set_text_color(lv.palette_main(lv.PALETTE.NONE))
		button_style.set_shadow_width(0)
		button_style.set_border_width(1)
		button_style.set_border_color(lv.palette_main(lv.PALETTE.NONE))

		self.button_style = button_style		